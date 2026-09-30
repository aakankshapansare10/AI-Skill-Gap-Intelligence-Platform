import re


def clean_text(text):
    """
    Clean job description or resume text.
    """

    if not isinstance(text, str):
        return ""

    # Normalize line breaks
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text