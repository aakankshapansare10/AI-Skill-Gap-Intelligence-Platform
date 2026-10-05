import os
import re
import pandas as pd
import ahocorasick


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


# ============================================================
# V13 SKILL DICTIONARY
# ============================================================

DICTIONARY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "skills_dictionary_clean_v13.csv"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(value):

    if value is None:
        return ""

    text = str(value).lower()

    # Fix common encoding characters
    text = text.replace("â€“", "-")
    text = text.replace("â€”", "-")

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# NLP SERVICE
# ============================================================

class NLPService:

    def __init__(self):

        # ----------------------------------------------------
        # CHECK DICTIONARY FILE
        # ----------------------------------------------------

        if not os.path.exists(
            DICTIONARY_FILE
        ):

            raise FileNotFoundError(
                f"V13 dictionary not found: "
                f"{DICTIONARY_FILE}"
            )


        # ----------------------------------------------------
        # LOAD SKILL DICTIONARY
        # ----------------------------------------------------

        skills_df = pd.read_csv(
            DICTIONARY_FILE,
            dtype=str
        )


        # ----------------------------------------------------
        # REQUIRED COLUMNS
        # ----------------------------------------------------

        required_columns = [
            "skill_id",
            "skill_name",
            "canonical_skill_name"
        ]


        for column in required_columns:

            if column not in skills_df.columns:

                raise ValueError(
                    f"Missing column: {column}"
                )


        # ----------------------------------------------------
        # CREATE SKILL LOOKUP
        # ----------------------------------------------------

        self.skill_lookup = {}


        # ----------------------------------------------------
        # GENERIC TERMS TO EXCLUDE
        # ----------------------------------------------------

        excluded_skills = {

            "student",
            "students",

            "candidate",
            "candidates",

            "experience",

            "work",

            "job",
            "jobs",

            "bi",
            "machine",
            "learning"
        }


        # ----------------------------------------------------
        # BUILD LOOKUP FROM CSV
        # ----------------------------------------------------

        for _, row in skills_df.iterrows():

            try:

                skill_id = int(
                    row["skill_id"]
                )

            except Exception:

                continue


            skill_name = str(
                row["skill_name"]
            ).strip()


            canonical_name = str(
                row["canonical_skill_name"]
            ).strip()


            normalized = normalize_text(
                skill_name
            )


            # Ignore empty skills

            if not normalized:

                continue


            # Ignore generic terms

            if normalized in excluded_skills:

                continue


            # Ignore duplicates

            if normalized in self.skill_lookup:

                continue


            self.skill_lookup[
                normalized
            ] = {

                "skill_id":
                    skill_id,

                "skill_name":
                    skill_name,

                "canonical_skill_name":
                    canonical_name
            }


        # ----------------------------------------------------
        # CREATE AHO-CORASICK AUTOMATON
        # ----------------------------------------------------

        self.automaton = (
            ahocorasick.Automaton()
        )


        for pattern, info in (
            self.skill_lookup.items()
        ):

            self.automaton.add_word(
                pattern,
                (
                    pattern,
                    info
                )
            )


        # Build the automaton

        self.automaton.make_automaton()


    # ========================================================
    # VALIDATE WORD BOUNDARIES
    # ========================================================

    @staticmethod
    def valid_boundary(
        text,
        start,
        end
    ):

        # ----------------------------------------------------
        # LEFT BOUNDARY
        # ----------------------------------------------------

        if start > 0:

            left = text[
                start - 1
            ]

            if (
                left.isalnum()
                or left == "_"
            ):

                return False


        # ----------------------------------------------------
        # RIGHT BOUNDARY
        # ----------------------------------------------------

        if end < len(text):

            right = text[end]

            if (
                right.isalnum()
                or right == "_"
            ):

                return False


        return True


    # ========================================================
    # EXTRACT SKILLS
    # ========================================================

    def extract_skills(
        self,
        text
    ):

        # ----------------------------------------------------
        # NORMALIZE INPUT TEXT
        # ----------------------------------------------------

        normalized_text = normalize_text(
            text
        )


        # ----------------------------------------------------
        # EMPTY TEXT
        # ----------------------------------------------------

        if not normalized_text:

            return []


        # ----------------------------------------------------
        # STORE FOUND SKILLS
        # ----------------------------------------------------

        found = {}


        # ----------------------------------------------------
        # SEARCH USING AHO-CORASICK
        # ----------------------------------------------------

        for end_index, value in (
            self.automaton.iter(
                normalized_text
            )
        ):

            pattern, info = value


            # Calculate start position

            start_index = (
                end_index
                - len(pattern)
                + 1
            )


            # Calculate exclusive end

            end_exclusive = (
                end_index + 1
            )


            # ------------------------------------------------
            # CHECK WORD BOUNDARIES
            # ------------------------------------------------

            if not self.valid_boundary(
                normalized_text,
                start_index,
                end_exclusive
            ):

                continue


            # ------------------------------------------------
            # GET SKILL ID
            # ------------------------------------------------

            skill_id = info[
                "skill_id"
            ]


            # ------------------------------------------------
            # SAVE ONLY ONCE
            # ------------------------------------------------

            if skill_id not in found:

                found[skill_id] = {

                    "skill_id":
                        skill_id,

                    "skill_name":
                        info[
                            "skill_name"
                        ],

                    "canonical_skill_name":
                        info[
                            "canonical_skill_name"
                        ]
                }


        # ====================================================
        # REMOVE GENERIC / INVALID SKILLS
        # ====================================================

        excluded_skills = {

            "student",
            "students",

            "candidate",
            "candidates",

            "experience",

            "work",

            "job",
            "jobs",

            "bi",
            "machine",
            "learning"
        }


        results = []


        for skill in found.values():

            canonical = normalize_text(
                skill[
                    "canonical_skill_name"
                ]
            )


            skill_name = normalize_text(
                skill[
                    "skill_name"
                ]
            )


            # ------------------------------------------------
            # EXCLUDE GENERIC CANONICAL NAME
            # ------------------------------------------------

            if canonical in excluded_skills:

                continue


            # ------------------------------------------------
            # EXCLUDE GENERIC SKILL NAME
            # ------------------------------------------------

            if skill_name in excluded_skills:

                continue


            results.append(
                skill
            )


        # ====================================================
        # REMOVE SHORTER SKILLS
        # WHEN A LONGER SKILL CONTAINS THEM
        # ====================================================

        final_results = []


        for skill in results:

            current_skill = normalize_text(
                skill[
                    "canonical_skill_name"
                ]
            )


            shorter_match = False


            for other in results:

                # Don't compare with itself

                if skill is other:

                    continue


                other_skill = normalize_text(
                    other[
                        "canonical_skill_name"
                    ]
                )


                # ------------------------------------------------
                # EXAMPLES:
                #
                # Machine
                #      ↓
                # Machine Learning
                #
                # Learning
                #      ↓
                # Machine Learning
                #
                # BI
                #      ↓
                # Power BI
                # ------------------------------------------------

                if (
                    current_skill
                    and other_skill
                    and current_skill != other_skill
                    and current_skill in other_skill
                ):

                    shorter_match = True

                    break


            # Keep only the longer skill

            if not shorter_match:

                final_results.append(
                    skill
                )


        # ====================================================
        # REMOVE DUPLICATES
        # ====================================================

        unique_results = []


        seen = set()


        for skill in final_results:

            canonical = normalize_text(
                skill[
                    "canonical_skill_name"
                ]
            )


            if canonical not in seen:

                seen.add(
                    canonical
                )

                unique_results.append(
                    skill
                )


        # ====================================================
        # RETURN FINAL SKILLS
        # ====================================================

        return unique_results


# ============================================================
# CREATE NLP SERVICE INSTANCE
# ============================================================

nlp_service = NLPService()