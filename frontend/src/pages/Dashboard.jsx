import { useMemo } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  ArrowUpRight,
  CheckCircle2,
  CircleAlert,
  Target,
  TrendingUp,
  Brain,
  BriefcaseBusiness,
  BookOpen,
  GraduationCap,
  Sparkles,
} from "lucide-react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";

function normalizeSkill(skill) {
  return String(skill || "")
    .trim()
    .toLowerCase();
}

function formatSkill(skill) {
  const text = String(skill || "").trim();

  if (!text) return "";

  const special = {
    sql: "SQL",
    aws: "AWS",
    api: "API",
    ai: "AI",
    nlp: "NLP",
    python: "Python",
    postgresql: "PostgreSQL",
    "power bi": "Power BI",
    "big data analytics": "Big Data Analytics",
    "c++": "C++",
    "c#": "C#",
    "machine learning": "Machine Learning",
  };

  const lower = text.toLowerCase();

  if (special[lower]) {
    return special[lower];
  }

  return text
    .split(" ")
    .map(
      (word) =>
        word.charAt(0).toUpperCase() + word.slice(1)
    )
    .join(" ");
}

function uniqueSkills(skills) {
  const seen = new Set();

  return skills.filter((skill) => {
    const normalized = normalizeSkill(skill);

    if (!normalized || seen.has(normalized)) {
      return false;
    }

    seen.add(normalized);
    return true;
  });
}

function Dashboard() {
  const location = useLocation();

  const analysis = location.state?.analysis || null;

  const targetRole =
    location.state?.targetRole ||
    analysis?.target_role_analysis?.target_role ||
    "Target Role";

  /*
    -------------------------------------------------------
    BACKEND DATA
    -------------------------------------------------------
  */

  const studentProfile = analysis?.student_profile || {};
  const overallAnalysis = analysis?.overall_analysis || {};
  const targetRoleAnalysis =
    analysis?.target_role_analysis || {};

  const studentSkills = useMemo(() => {
    return uniqueSkills(
      Array.isArray(studentProfile.skills)
        ? studentProfile.skills
        : []
    );
  }, [studentProfile.skills]);

  /*
    -------------------------------------------------------
    SKILL GAPS
    -------------------------------------------------------
  */

  const missingSkills = useMemo(() => {
    const skills = Array.isArray(
      targetRoleAnalysis.missing_skills
    )
      ? targetRoleAnalysis.missing_skills
      : [];

    return skills.map((item) => ({
      name: formatSkill(item.skill_name),
      jobsRequired:
        Number(item.jobs_requiring_skill) || 0,
      demandPercentage:
        Number(item.demand_percentage) || 0,
      priority: String(item.priority || "LOW").toUpperCase(),
    }));
  }, [targetRoleAnalysis.missing_skills]);

  /*
    -------------------------------------------------------
    MATCHING SKILLS
    -------------------------------------------------------
  */

  const missingSkillNames = useMemo(() => {
    return new Set(
      missingSkills.map((skill) =>
        normalizeSkill(skill.name)
      )
    );
  }, [missingSkills]);

  const matchingSkills = useMemo(() => {
    return studentSkills.filter(
      (skill) =>
        !missingSkillNames.has(
          normalizeSkill(skill)
        )
    );
  }, [studentSkills, missingSkillNames]);

  /*
    -------------------------------------------------------
    MATCH SCORE
    -------------------------------------------------------
  */

  const matchScore =
    Number(
      overallAnalysis.best_job_match_percentage
    ) || 0;

  const totalSkills =
    Number(studentProfile.total_skills) ||
    studentSkills.length;

  /*
    -------------------------------------------------------
    CAREER RECOMMENDATIONS
    -------------------------------------------------------
  */

  const recommendations = useMemo(() => {
    const jobs = Array.isArray(
      overallAnalysis.top_job_recommendations
    )
      ? overallAnalysis.top_job_recommendations
      : [];

    return jobs.slice(0, 5).map((job) => {
      const matching = String(
        job.matching_skills || ""
      )
        .split("|")
        .map((skill) => skill.trim())
        .filter(Boolean);

      const missing = String(
        job.missing_skills || ""
      )
        .split("|")
        .map((skill) => skill.trim())
        .filter(Boolean);

      return {
        rank: job.rank,
        title:
          job.job_title || "Recommended Role",
        jobMatch:
          Number(job.job_match_percentage) || 0,
        skillGap:
          Number(job.skill_gap_percentage) || 0,
        matchingSkills: matching,
        missingSkills: missing,
      };
    });
  }, [overallAnalysis.top_job_recommendations]);

  /*
    -------------------------------------------------------
    LEARNING ROADMAP
    -------------------------------------------------------

    Backend doesn't provide a separate learning roadmap.

    So we intelligently build one from the actual
    missing_skills returned by the backend.

    Priority:
    HIGH → MEDIUM → LOW

    Within the same priority:
    Higher job demand → earlier in roadmap
  */

  const learningRoadmap = useMemo(() => {
    const priorityOrder = {
      HIGH: 1,
      MEDIUM: 2,
      LOW: 3,
    };

    return [...missingSkills]
      .sort((a, b) => {
        const priorityDifference =
          (priorityOrder[a.priority] || 4) -
          (priorityOrder[b.priority] || 4);

        if (priorityDifference !== 0) {
          return priorityDifference;
        }

        return (
          b.demandPercentage -
          a.demandPercentage
        );
      })
      .slice(0, 6)
      .map((skill, index) => {
        let phase = "Build Core Skills";

        if (index < 2) {
          phase = "Priority Skills";
        } else if (index < 4) {
          phase = "Core Technical Skills";
        } else {
          phase = "Supporting Skills";
        }

        let reason =
          "This skill appears in the job-market requirements for your target role.";

        if (skill.priority === "HIGH") {
          reason =
            "High-priority skill with strong relevance to your target career path.";
        } else if (
          skill.demandPercentage >= 15
        ) {
          reason =
            "Frequently requested by jobs in the analyzed job-market data.";
        } else if (
          skill.demandPercentage >= 5
        ) {
          reason =
            "A useful supporting skill that can strengthen your career alignment.";
        }

        return {
          ...skill,
          step: index + 1,
          phase,
          reason,
        };
      });
  }, [missingSkills]);

  /*
    -------------------------------------------------------
    CAREER DNA
    -------------------------------------------------------
  */

  const radarData = useMemo(() => {
    const importantSkills = [
      "Python",
      "SQL",
      "Data Science",
      "Machine Learning",
      "Statistics",
      "Data Analysis",
    ];

    return importantSkills.map((skill) => {
      const exists = studentSkills.some(
        (studentSkill) =>
          normalizeSkill(studentSkill) ===
          normalizeSkill(skill)
      );

      return {
        skill,
        value: exists ? 100 : 0,
      };
    });
  }, [studentSkills]);

  /*
    -------------------------------------------------------
    GROWTH STATUS
    -------------------------------------------------------
  */

  const growthPotential = useMemo(() => {
    if (matchScore >= 80) return "Excellent";
    if (matchScore >= 60) return "Strong";
    if (matchScore >= 40) return "Developing";
    return "Needs Improvement";
  }, [matchScore]);

  const matchMessage = useMemo(() => {
    if (matchScore >= 80) {
      return "Your profile is strongly aligned with the target career path.";
    }

    if (matchScore >= 60) {
      return "You already have a solid foundation for this career path.";
    }

    if (matchScore >= 40) {
      return "There is a good foundation, with several skills still worth developing.";
    }

    return "Focus on the recommended skills to improve your career alignment.";
  }, [matchScore]);

  /*
    -------------------------------------------------------
    NO ANALYSIS STATE
    -------------------------------------------------------
  */

  if (!analysis) {
    return (
      <main className="min-h-screen bg-[#F7F8FC] px-6 py-16">
        <div className="mx-auto max-w-4xl">
          <div className="rounded-3xl border border-gray-100 bg-white p-10 text-center shadow-sm">
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
              <Brain size={30} />
            </div>

            <h1 className="text-3xl font-bold text-gray-900">
              No Analysis Available
            </h1>

            <p className="mx-auto mt-3 max-w-xl text-gray-500">
              Analyze your resume first to generate your
              Career Intelligence dashboard.
            </p>

            <Link
              to="/analyze"
              className="mt-7 inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white transition hover:bg-indigo-700"
            >
              Analyze My Resume
              <ArrowUpRight size={18} />
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#F7F8FC] px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">

        {/* HEADER */}

        <section className="mb-8 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-indigo-600">
              <Brain size={18} />
              Career Intelligence
            </div>

            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
              Your Career Dashboard
            </h1>

            <p className="mt-3 text-base text-gray-500">
              Here's how your current skills compare with
              your target role.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-100 bg-white px-6 py-4 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">
              Target Role
            </p>

            <p className="mt-1 text-lg font-bold text-gray-900">
              {targetRole}
            </p>
          </div>
        </section>

        {/* STAT CARDS */}

        <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">

          {/* Career Match */}

          <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                <Target size={22} />
              </div>

              <TrendingUp
                size={19}
                className="text-emerald-500"
              />
            </div>

            <p className="mt-7 text-sm text-gray-500">
              Career Match
            </p>

            <p className="mt-1 text-3xl font-bold text-gray-900">
              {matchScore.toFixed(2)}%
            </p>

            <p className="mt-1 text-xs text-gray-400">
              Best job match from your analysis
            </p>
          </div>

          {/* Matching Skills */}

          <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                <CheckCircle2 size={22} />
              </div>

              <TrendingUp
                size={19}
                className="text-emerald-500"
              />
            </div>

            <p className="mt-7 text-sm text-gray-500">
              Matching Skills
            </p>

            <p className="mt-1 text-3xl font-bold text-gray-900">
              {matchingSkills.length}
            </p>

            <p className="mt-1 text-xs text-gray-400">
              Skills already present in your profile
            </p>
          </div>

          {/* Skill Gaps */}

          <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-orange-50 text-orange-500">
                <CircleAlert size={22} />
              </div>

              <span className="text-orange-500">!</span>
            </div>

            <p className="mt-7 text-sm text-gray-500">
              Skill Gaps
            </p>

            <p className="mt-1 text-3xl font-bold text-gray-900">
              {missingSkills.length}
            </p>

            <p className="mt-1 text-xs text-gray-400">
              Skills recommended for development
            </p>
          </div>

          {/* Growth */}

          <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                <TrendingUp size={22} />
              </div>

              <TrendingUp
                size={19}
                className="text-emerald-500"
              />
            </div>

            <p className="mt-7 text-sm text-gray-500">
              Growth Potential
            </p>

            <p className="mt-1 text-2xl font-bold text-gray-900">
              {growthPotential}
            </p>

            <p className="mt-1 text-xs text-gray-400">
              Career development potential
            </p>
          </div>
        </section>

        {/* CAREER MATCH + CAREER DNA */}

        <section className="mt-6 grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
          {/* Match Score */}

          <div className="rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-500">
                  Career Match
                </p>

                <h2 className="mt-1 text-2xl font-bold text-gray-900">
                  {targetRole}
                </h2>
              </div>

              <span className="rounded-full bg-emerald-50 px-4 py-2 text-xs font-semibold text-emerald-600">
                {growthPotential}
              </span>
            </div>

            <div className="mt-8 flex justify-center">
              <div className="relative flex h-48 w-48 items-center justify-center rounded-full border-[16px] border-indigo-100">
                <div className="text-center">
                  <p className="text-4xl font-bold text-gray-900">
                    {matchScore.toFixed(2)}%
                  </p>

                  <p className="mt-1 text-sm text-gray-400">
                    Match Score
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-8 rounded-2xl bg-indigo-50 p-5">
              <h3 className="font-bold text-indigo-700">
                {matchScore >= 60
                  ? "Strong foundation"
                  : "There is room to grow"}
              </h3>

              <p className="mt-2 text-sm leading-6 text-indigo-600">
                {matchMessage}
              </p>
            </div>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-gray-50 p-4">
                <p className="text-xs text-gray-400">
                  Your Skills
                </p>

                <p className="mt-1 text-xl font-bold text-gray-900">
                  {totalSkills}
                </p>
              </div>

              <div className="rounded-xl bg-gray-50 p-4">
                <p className="text-xs text-gray-400">
                  Skill Gaps
                </p>

                <p className="mt-1 text-xl font-bold text-gray-900">
                  {missingSkills.length}
                </p>
              </div>
            </div>
          </div>

          {/* Career DNA */}

          <div className="rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-500">
                  Career DNA
                </p>

                <h2 className="mt-1 text-2xl font-bold text-gray-900">
                  Your Skill Profile
                </h2>
              </div>

              <span className="rounded-full bg-indigo-50 px-4 py-2 text-xs font-semibold text-indigo-600">
                {totalSkills} Skill Areas
              </span>
            </div>

            <div className="mt-5 h-[310px] w-full">
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <RadarChart data={radarData}>
                  <PolarGrid />

                  <PolarAngleAxis
                    dataKey="skill"
                    tick={{
                      fill: "#6B7280",
                      fontSize: 11,
                    }}
                  />

                  <PolarRadiusAxis
                    angle={30}
                    domain={[0, 100]}
                    tick={false}
                    axisLine={false}
                  />

                  <Radar
                    name="Skill Presence"
                    dataKey="value"
                    stroke="#4F46E5"
                    fill="#6366F1"
                    fillOpacity={0.25}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <p className="text-center text-xs text-gray-400">
              Skill presence is based on skills extracted from
              your resume.
            </p>
          </div>
        </section>

        {/* ------------------------------------------------
    HOW WE ANALYZED YOUR RESUME
------------------------------------------------ */}

<section className="mt-6 rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">

  <div className="text-center">

    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
      <Sparkles size={22} />
    </div>

    <p className="mt-4 text-sm font-semibold text-indigo-600">
      AI Analysis Journey
    </p>

    <h2 className="mt-1 text-2xl font-bold text-gray-900">
      How We Analyzed Your Resume
    </h2>

    <p className="mx-auto mt-2 max-w-2xl text-sm leading-6 text-gray-500">
      Your resume was transformed into a career intelligence
      profile by comparing your skills with real job-market
      requirements.
    </p>

  </div>

  <div className="mt-8 grid gap-4 md:grid-cols-4">

    {/* STEP 1 */}

    <div className="relative rounded-2xl border border-gray-100 bg-gray-50/70 p-5">

      <div className="flex items-center justify-between">

        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600">
          <BookOpen size={20} />
        </div>

        <span className="text-xs font-bold text-indigo-400">
          STEP 01
        </span>

      </div>

      <h3 className="mt-5 font-bold text-gray-900">
        Resume Analysis
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-500">
        Your resume content was processed to identify
        relevant career and technical information.
      </p>

    </div>

    {/* STEP 2 */}

    <div className="relative rounded-2xl border border-gray-100 bg-gray-50/70 p-5">

      <div className="flex items-center justify-between">

        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
          <CheckCircle2 size={20} />
        </div>

        <span className="text-xs font-bold text-emerald-400">
          STEP 02
        </span>

      </div>

      <h3 className="mt-5 font-bold text-gray-900">
        Skills Extracted
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-500">
        We identified{" "}
        <strong className="text-gray-700">
          {totalSkills} skills
        </strong>{" "}
        from your resume and created your current skill
        profile.
      </p>

    </div>

    {/* STEP 3 */}

    <div className="relative rounded-2xl border border-gray-100 bg-gray-50/70 p-5">

      <div className="flex items-center justify-between">

        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-purple-50 text-purple-600">
          <Target size={20} />
        </div>

        <span className="text-xs font-bold text-purple-400">
          STEP 03
        </span>

      </div>

      <h3 className="mt-5 font-bold text-gray-900">
        Job Market Comparison
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-500">
        Your skills were compared with job requirements
        related to{" "}
        <strong className="text-gray-700">
          {targetRole}
        </strong>.
      </p>

    </div>

    {/* STEP 4 */}

    <div className="relative rounded-2xl border border-gray-100 bg-gray-50/70 p-5">

      <div className="flex items-center justify-between">

        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
          <TrendingUp size={20} />
        </div>

        <span className="text-xs font-bold text-orange-400">
          STEP 04
        </span>

      </div>

      <h3 className="mt-5 font-bold text-gray-900">
        Career Roadmap
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-500">
        We identified{" "}
        <strong className="text-gray-700">
          {missingSkills.length} skill gaps
        </strong>{" "}
        and prioritized what you should learn next.
      </p>

    </div>

  </div>

  {/* RESULT SUMMARY */}

  <div className="mt-6 rounded-2xl bg-indigo-50 p-5">

    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

      <div>

        <p className="text-sm font-semibold text-indigo-700">
          Analysis Complete
        </p>

        <p className="mt-1 text-sm text-indigo-600">
          Your Career Genome is ready for the{" "}
          {targetRole} career path.
        </p>

      </div>

      <div className="flex flex-wrap gap-2">

        <span className="rounded-full bg-white px-3 py-2 text-xs font-semibold text-indigo-600">
          {totalSkills} Skills
        </span>

        <span className="rounded-full bg-white px-3 py-2 text-xs font-semibold text-orange-600">
          {missingSkills.length} Gaps
        </span>

        <span className="rounded-full bg-white px-3 py-2 text-xs font-semibold text-emerald-600">
          {matchScore.toFixed(2)}% Match
        </span>

      </div>

    </div>

  </div>

</section>

        {/* MATCHING + MISSING */}

        <section className="mt-6 grid gap-6 lg:grid-cols-2">

          {/* Matching Skills */}

          <div className="rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-500">
                  Skills You Have
                </p>

                <h2 className="mt-1 text-2xl font-bold text-gray-900">
                  Matching Skills
                </h2>
              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-50 text-emerald-500">
                <CheckCircle2 size={20} />
              </div>
            </div>

            {matchingSkills.length > 0 ? (
              <div className="mt-6 flex flex-wrap gap-2">
                {matchingSkills.map((skill, index) => (
                  <span
                    key={`${skill}-${index}`}
                    className="rounded-full bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700"
                  >
                    {formatSkill(skill)}
                  </span>
                ))}
              </div>
            ) : (
              <div className="mt-6 rounded-2xl bg-gray-50 p-6 text-center text-sm text-gray-500">
                No matching skills found for this target role.
              </div>
            )}
          </div>

          {/* Missing Skills */}

          <div className="rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-500">
                  Skills to Develop
                </p>

                <h2 className="mt-1 text-2xl font-bold text-gray-900">
                  Your Skill Gaps
                </h2>
              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-50 text-orange-500">
                <CircleAlert size={20} />
              </div>
            </div>

            {missingSkills.length > 0 ? (
              <div className="mt-6 space-y-3">
                {missingSkills.map((skill, index) => (
                  <div
                    key={`${skill.name}-${index}`}
                    className="rounded-2xl border border-gray-100 p-4"
                  >
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <p className="font-semibold text-gray-900">
                          {skill.name}
                        </p>

                        <p className="mt-1 text-xs text-gray-400">
                          Required by {skill.jobsRequired} jobs
                        </p>
                      </div>

                      <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${
                          skill.priority === "HIGH"
                            ? "bg-red-50 text-red-600"
                            : skill.priority === "MEDIUM"
                            ? "bg-orange-50 text-orange-600"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {skill.priority}
                      </span>
                    </div>

                    <div className="mt-3 h-2 overflow-hidden rounded-full bg-gray-100">
                      <div
                        className="h-full rounded-full bg-orange-400"
                        style={{
                          width: `${Math.min(
                            skill.demandPercentage,
                            100
                          )}%`,
                        }}
                      />
                    </div>

                    <p className="mt-2 text-xs text-gray-400">
                      {skill.demandPercentage.toFixed(2)}%
                      {" "}job demand
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="mt-6 rounded-2xl bg-gray-50 p-6 text-center text-sm text-gray-500">
                No skill gaps detected for this target role.
              </div>
            )}
          </div>
        </section>

        {/* ------------------------------------------------
            RECOMMENDED LEARNING ROADMAP
        ------------------------------------------------ */}

        <section className="mt-6 rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">

          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-indigo-600">
                <GraduationCap size={18} />
                Recommended Roadmap
              </div>

              <h2 className="mt-1 text-2xl font-bold text-gray-900">
                What You Should Learn Next
              </h2>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-500">
                Your learning path is prioritized using the
                skills missing from your profile and their
                demand in the analyzed job market.
              </p>
            </div>

            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-600 transition hover:text-indigo-700"
            >
              Analyze Again
              <ArrowUpRight size={17} />
            </Link>

          </div>

          {learningRoadmap.length > 0 ? (

            <div className="relative mt-8">

              {/* Timeline line */}

              <div className="absolute bottom-8 left-[21px] top-8 hidden w-px bg-indigo-100 md:block" />

              <div className="space-y-5">

                {learningRoadmap.map((skill) => (

                  <div
                    key={`${skill.name}-${skill.step}`}
                    className="relative flex flex-col gap-4 md:flex-row"
                  >

                    {/* Step */}

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-sm font-bold text-white shadow-sm">
                      {skill.step}
                    </div>

                    {/* Card */}

                    <div className="flex-1 rounded-2xl border border-gray-100 bg-gray-50/70 p-5 transition hover:border-indigo-100 hover:bg-white hover:shadow-sm">

                      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">

                        <div className="min-w-0">

                          <div className="flex flex-wrap items-center gap-2">

                            <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-600">
                              {skill.phase}
                            </span>

                            <span
                              className={`rounded-full px-3 py-1 text-xs font-semibold ${
                                skill.priority === "HIGH"
                                  ? "bg-red-50 text-red-600"
                                  : skill.priority === "MEDIUM"
                                  ? "bg-orange-50 text-orange-600"
                                  : "bg-gray-100 text-gray-600"
                              }`}
                            >
                              {skill.priority} PRIORITY
                            </span>

                          </div>

                          <h3 className="mt-3 text-xl font-bold text-gray-900">
                            {skill.name}
                          </h3>

                          <p className="mt-2 text-sm leading-6 text-gray-500">
                            {skill.reason}
                          </p>

                        </div>

                        <div className="shrink-0 rounded-xl bg-white px-4 py-3 shadow-sm">

                          <p className="text-xs text-gray-400">
                            Job Demand
                          </p>

                          <p className="mt-1 text-lg font-bold text-gray-900">
                            {skill.demandPercentage.toFixed(2)}%
                          </p>

                          <p className="mt-1 text-xs text-gray-400">
                            {skill.jobsRequired} jobs
                          </p>

                        </div>

                      </div>

                      {/* Demand bar */}

                      <div className="mt-5">

                        <div className="mb-2 flex items-center justify-between text-xs">
                          <span className="font-medium text-gray-500">
                            Market relevance
                          </span>

                          <span className="font-semibold text-indigo-600">
                            {skill.demandPercentage.toFixed(2)}%
                          </span>
                        </div>

                        <div className="h-2 overflow-hidden rounded-full bg-gray-200">

                          <div
                            className="h-full rounded-full bg-indigo-500 transition-all"
                            style={{
                              width: `${Math.min(
                                skill.demandPercentage,
                                100
                              )}%`,
                            }}
                          />

                        </div>

                      </div>

                    </div>

                  </div>

                ))}

              </div>
            </div>

          ) : (

            <div className="mt-7 rounded-2xl border border-dashed border-gray-200 bg-gray-50 p-10 text-center">

              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
                <Sparkles size={24} />
              </div>

              <h3 className="mt-4 font-semibold text-gray-900">
                Your profile is already well aligned
              </h3>

              <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-gray-500">
                No major skill gaps were identified for this
                target role. Keep strengthening the skills
                already present in your profile.
              </p>

            </div>

          )}

        </section>

        {/* ------------------------------------------------
            CAREER OPPORTUNITIES
        ------------------------------------------------ */}

        <section className="mt-6 rounded-3xl border border-gray-100 bg-white p-7 shadow-sm">

          <div className="flex items-start justify-between gap-4">

            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-indigo-600">
                <BriefcaseBusiness size={18} />
                Career Opportunities
              </div>

              <h2 className="mt-1 text-2xl font-bold text-gray-900">
                Roles You Could Target
              </h2>

              <p className="mt-2 text-sm text-gray-500">
                These roles are recommended based on your
                current skill profile and job-market matching.
              </p>
            </div>

          </div>

          {recommendations.length > 0 ? (

            <div className="mt-7 grid gap-4 md:grid-cols-2">

              {recommendations.map((job, index) => (

                <div
                  key={`${job.title}-${index}`}
                  className="rounded-2xl border border-gray-100 p-5 transition hover:-translate-y-0.5 hover:shadow-sm"
                >

                  <div className="flex items-start gap-4">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                      <BriefcaseBusiness size={20} />
                    </div>

                    <div className="min-w-0 flex-1">

                      <div className="flex flex-wrap items-center gap-2">

                        <span className="text-xs font-semibold text-indigo-500">
                          #{job.rank || index + 1}
                        </span>

                        <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-600">
                          {job.jobMatch.toFixed(2)}% match
                        </span>

                      </div>

                      <h3 className="mt-2 font-bold text-gray-900">
                        {job.title}
                      </h3>

                      <p className="mt-1 text-sm text-gray-500">
                        Skill gap: {job.skillGap.toFixed(2)}%
                      </p>

                    </div>
                  </div>

                  {job.matchingSkills.length > 0 && (
                    <div className="mt-4">

                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-400">
                        Matching Skills
                      </p>

                      <div className="flex flex-wrap gap-2">

                        {job.matchingSkills
                          .slice(0, 6)
                          .map((skill, skillIndex) => (

                            <span
                              key={`${skill}-${skillIndex}`}
                              className="rounded-full bg-gray-50 px-2.5 py-1 text-xs text-gray-600"
                            >
                              {formatSkill(skill)}
                            </span>

                          ))}

                      </div>
                    </div>
                  )}

                  {job.missingSkills.length > 0 && (
                    <div className="mt-4">

                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-400">
                        Skills to Develop
                      </p>

                      <div className="flex flex-wrap gap-2">

                        {job.missingSkills
                          .slice(0, 5)
                          .map((skill, skillIndex) => (

                            <span
                              key={`${skill}-${skillIndex}`}
                              className="rounded-full bg-orange-50 px-2.5 py-1 text-xs text-orange-600"
                            >
                              {formatSkill(skill)}
                            </span>

                          ))}

                      </div>
                    </div>
                  )}

                </div>

              ))}

            </div>

          ) : (

            <div className="mt-6 rounded-2xl bg-gray-50 p-8 text-center text-sm text-gray-500">
              No career recommendations were returned for this analysis.
            </div>

          )}

        </section>

        {/* FINAL CTA */}

        <section className="mt-6 overflow-hidden rounded-3xl bg-indigo-600 p-8 text-white shadow-sm sm:p-10">

          <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">

            <div className="max-w-3xl">

              <div className="flex items-center gap-2 text-indigo-100">

                <BriefcaseBusiness size={19} />

                <span className="text-sm font-semibold">
                  Keep Building
                </span>

              </div>

              <h2 className="mt-5 text-3xl font-bold sm:text-4xl">
                You're closer than you think.
              </h2>

              <p className="mt-4 text-base leading-7 text-indigo-100">
                Based on your current skill profile, you can
                continue building toward opportunities related
                to the{" "}
                <strong className="text-white">
                  {targetRole}
                </strong>{" "}
                career path.
              </p>

            </div>

            <Link
              to="/analyze"
              className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-white px-6 py-3 font-semibold text-indigo-600 transition hover:bg-indigo-50"
            >
              Analyze Again
              <ArrowUpRight size={18} />
            </Link>

          </div>

        </section>

        {/* FOOTER INFO */}

        <div className="mt-8 flex flex-col items-center justify-center gap-2 pb-8 text-center text-xs text-gray-400 sm:flex-row">

          <BookOpen size={14} />

          <span>
            Career insights generated from your resume and
            job-market skill data.
          </span>

        </div>

      </div>
    </main>
  );
}

export default Dashboard;