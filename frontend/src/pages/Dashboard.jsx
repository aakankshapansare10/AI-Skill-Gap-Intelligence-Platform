import { useEffect, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  ArrowRight,
  Brain,
  BriefcaseBusiness,
  CheckCircle2,
  ChevronRight,
  CircleAlert,
  Code2,
  Database,
  FileSearch,
  GitBranch,
  GraduationCap,
  Lightbulb,
  Rocket,
  Sparkles,
  Target,
  TrendingUp,
  Upload,
  XCircle,
} from "lucide-react";
import {
  AnimatePresence,
  motion,
  useMotionValue,
  useSpring,
} from "framer-motion";
import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

/* =========================================================
   HELPERS
========================================================= */

function normalizeSkill(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

function formatSkill(value) {
  if (!value) return "";

  const specialCases = {
    sql: "SQL",
    python: "Python",
    aws: "AWS",
    azure: "Azure",
    nlp: "NLP",
    ai: "AI",
    api: "API",
    css: "CSS",
    html: "HTML",
    javascript: "JavaScript",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "data analysis": "Data Analysis",
    "power bi": "Power BI",
    "git hub": "GitHub",
    github: "GitHub",
    mysql: "MySQL",
    mongodb: "MongoDB",
    numpy: "NumPy",
    pandas: "Pandas",
  };

  const normalized = normalizeSkill(value);

  if (specialCases[normalized]) {
    return specialCases[normalized];
  }

  return String(value)
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function uniqueSkills(skills) {
  const seen = new Set();

  return (skills || []).filter((skill) => {
    const normalized = normalizeSkill(skill);

    if (!normalized || seen.has(normalized)) {
      return false;
    }

    seen.add(normalized);
    return true;
  });
}

/* =========================================================
   ANIMATED NUMBER
========================================================= */

function AnimatedNumber({ value, decimals = 0, suffix = "" }) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    const numericValue = Number(value) || 0;
    const duration = 1100;
    const startTime = performance.now();

    let frame;

    const animate = (currentTime) => {
      const progress = Math.min(
        (currentTime - startTime) / duration,
        1
      );

      const eased =
        1 - Math.pow(1 - progress, 3);

      setDisplayValue(numericValue * eased);

      if (progress < 1) {
        frame = requestAnimationFrame(animate);
      }
    };

    frame = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(frame);
  }, [value]);

  return (
    <>
      {displayValue.toFixed(decimals)}
      {suffix}
    </>
  );
}

/* =========================================================
   MATCH RING
========================================================= */

function MatchRing({ score }) {
  const radius = 86;
  const circumference = 2 * Math.PI * radius;

  const safeScore = Math.min(
    Math.max(Number(score) || 0, 0),
    100
  );

  const offset =
    circumference -
    (safeScore / 100) * circumference;

  return (
    <div className="relative flex h-64 w-64 items-center justify-center">
      {/* Glow */}
      <motion.div
        className="absolute inset-8 rounded-full bg-indigo-500/20 blur-3xl"
        animate={{
          scale: [0.9, 1.08, 0.9],
          opacity: [0.35, 0.6, 0.35],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <svg
        viewBox="0 0 220 220"
        className="relative h-full w-full -rotate-90"
      >
        <circle
          cx="110"
          cy="110"
          r={radius}
          fill="none"
          stroke="#EEF2FF"
          strokeWidth="16"
        />

        <motion.circle
          cx="110"
          cy="110"
          r={radius}
          fill="none"
          stroke="url(#matchGradient)"
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{
            strokeDashoffset: circumference,
          }}
          animate={{
            strokeDashoffset: offset,
          }}
          transition={{
            duration: 1.8,
            ease: "easeOut",
          }}
        />

        <defs>
          <linearGradient
            id="matchGradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor="#4338CA" />
            <stop offset="55%" stopColor="#7C3AED" />
            <stop offset="100%" stopColor="#06B6D4" />
          </linearGradient>
        </defs>
      </svg>

      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-black tracking-tight text-gray-950">
          <AnimatedNumber
            value={safeScore}
            decimals={2}
            suffix="%"
          />
        </span>

        <span className="mt-1 text-sm font-medium text-gray-500">
          Career Match
        </span>
      </div>
    </div>
  );
}

/* =========================================================
   FLOATING SKILL NODE
========================================================= */

function SkillNode({
  name,
  icon: Icon = Sparkles,
  x,
  y,
  delay,
  color = "indigo",
}) {
  const colorClasses = {
    indigo:
      "border-indigo-200 bg-indigo-50 text-indigo-700",
    cyan:
      "border-cyan-200 bg-cyan-50 text-cyan-700",
    violet:
      "border-violet-200 bg-violet-50 text-violet-700",
    emerald:
      "border-emerald-200 bg-emerald-50 text-emerald-700",
    orange:
      "border-orange-200 bg-orange-50 text-orange-700",
  };

  return (
    <motion.div
      className="absolute hidden sm:block"
      style={{
        left: x,
        top: y,
      }}
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{
        opacity: 1,
        scale: 1,
        y: [0, -10, 0],
      }}
      transition={{
        opacity: {
          duration: 0.5,
          delay,
        },
        scale: {
          duration: 0.5,
          delay,
        },
        y: {
          duration: 4 + delay,
          repeat: Infinity,
          ease: "easeInOut",
        },
      }}
    >
      <motion.div
        whileHover={{
          scale: 1.08,
          rotate: 2,
        }}
        className={`flex items-center gap-2 rounded-2xl border px-3 py-2 text-xs font-semibold shadow-lg shadow-indigo-100/30 backdrop-blur-md ${colorClasses[color]}`}
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-xl bg-white shadow-sm">
          <Icon size={14} />
        </span>

        {formatSkill(name)}
      </motion.div>
    </motion.div>
  );
}

/* =========================================================
   CAREER GENOME VISUAL
========================================================= */

function CareerGenome({ skills }) {
  const genomeIcons = [
    { icon: Code2, color: "indigo" },
    { icon: Database, color: "cyan" },
    { icon: Brain, color: "violet" },
    { icon: TrendingUp, color: "emerald" },
    { icon: Target, color: "orange" },
    { icon: Sparkles, color: "indigo" },
  ];

  const genomeSkills = uniqueSkills(skills)
    .slice(0, 6)
    .map((name, index) => ({
      name,
      ...genomeIcons[index % genomeIcons.length],
    }));

  return (
    <div className="relative h-[420px] overflow-hidden rounded-[2rem] border border-indigo-100 bg-gradient-to-br from-white via-indigo-50/60 to-violet-100/50 p-5 shadow-inner">
      {/* Background glow */}
      <motion.div
        className="absolute left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full bg-indigo-400/20 blur-3xl"
        animate={{
          scale: [0.9, 1.15, 0.9],
          opacity: [0.3, 0.55, 0.3],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Orbit lines */}
      <motion.div
        className="absolute left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full border border-indigo-200/70"
        animate={{ rotate: 360 }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "linear",
        }}
      />

      <motion.div
        className="absolute left-1/2 top-1/2 h-52 w-52 -translate-x-1/2 -translate-y-1/2 rounded-full border border-violet-200/80"
        animate={{ rotate: -360 }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "linear",
        }}
      />

      <motion.div
        className="absolute left-1/2 top-1/2 h-32 w-32 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-200/70"
        animate={{ rotate: 360 }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: "linear",
        }}
      />

      {/* Floating nodes: skills extracted from the uploaded resume */}
      {genomeSkills.map((skill, index) => {
        const positions = [
          { x: "9%", y: "18%" },
          { x: "71%", y: "17%" },
          { x: "72%", y: "70%" },
          { x: "8%", y: "70%" },
          { x: "41%", y: "5%" },
          { x: "39%", y: "84%" },
        ];

        return (
          <SkillNode
            key={`${normalizeSkill(skill.name)}-${index}`}
            {...skill}
            {...positions[index]}
            delay={0.1 + index * 0.15}
          />
        );
      })}

      {/* Center */}
      <div className="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 items-center justify-center">
        <motion.div
          animate={{
            rotate: [0, 2, -2, 0],
            scale: [1, 1.03, 1],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="relative flex h-40 w-40 items-center justify-center rounded-full border border-white/80 bg-gradient-to-br from-indigo-600 via-violet-600 to-cyan-500 shadow-2xl shadow-indigo-500/30"
        >
          <div className="absolute inset-3 rounded-full border border-white/20" />

          <div className="absolute inset-7 rounded-full border border-white/20" />

          <div className="flex flex-col items-center text-white">
            <Sparkles size={28} />

            <span className="mt-2 text-sm font-semibold">
              Career
            </span>

            <span className="text-lg font-black">
              Genome
            </span>
          </div>
        </motion.div>
      </div>

      {/* Status */}
      <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between rounded-2xl border border-white/80 bg-white/70 px-4 py-3 backdrop-blur-xl">
        <div>
          <p className="text-xs font-medium text-gray-500">
            Skill profile
          </p>

          <p className="text-sm font-bold text-gray-900">
            {skills.length} skill areas detected
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          AI analyzed
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   STAT CARD
========================================================= */

function StatCard({
  icon: Icon,
  label,
  value,
  suffix = "",
  tone = "indigo",
}) {
  const tones = {
    indigo:
      "from-indigo-50 to-violet-50 text-indigo-600",
    emerald:
      "from-emerald-50 to-teal-50 text-emerald-600",
    orange:
      "from-orange-50 to-amber-50 text-orange-600",
    cyan:
      "from-cyan-50 to-sky-50 text-cyan-600",
  };

  return (
    <motion.div
      whileHover={{
        y: -5,
        rotateX: 2,
        rotateY: -2,
      }}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 20,
      }}
      style={{
        transformStyle: "preserve-3d",
      }}
      className="group rounded-3xl border border-gray-100 bg-white p-5 shadow-sm transition-shadow hover:shadow-xl hover:shadow-indigo-100/40"
    >
      <div className="flex items-center justify-between">
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br ${tones[tone]}`}
        >
          <Icon size={20} />
        </div>

        <Sparkles
          size={15}
          className="text-gray-200 transition group-hover:text-indigo-300"
        />
      </div>

      <div className="mt-5">
        <p className="text-sm text-gray-500">
          {label}
        </p>

        <p className="mt-1 text-3xl font-black tracking-tight text-gray-950">
          <AnimatedNumber
            value={value}
            suffix={suffix}
          />
        </p>
      </div>
    </motion.div>
  );
}

/* =========================================================
   SECTION TITLE
========================================================= */

function SectionTitle({
  eyebrow,
  title,
  description,
  icon: Icon = Sparkles,
}) {
  return (
    <div>
      <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-indigo-600">
        <span className="flex h-7 w-7 items-center justify-center rounded-xl bg-indigo-50">
          <Icon size={14} />
        </span>

        {eyebrow}
      </div>

      <h2 className="text-2xl font-black tracking-tight text-gray-950 sm:text-3xl">
        {title}
      </h2>

      {description && (
        <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-500">
          {description}
        </p>
      )}
    </div>
  );
}

/* =========================================================
   ANALYSIS PIPELINE
========================================================= */

function AnalysisPipeline() {
  const steps = [
    {
      icon: Upload,
      title: "Resume analyzed",
      text: "Resume content processed",
    },
    {
      icon: Brain,
      title: "Skills extracted",
      text: "Relevant skills identified",
    },
    {
      icon: BriefcaseBusiness,
      title: "Job comparison",
      text: "Market requirements compared",
    },
    {
      icon: CircleAlert,
      title: "Gaps detected",
      text: "Missing skills identified",
    },
    {
      icon: Rocket,
      title: "Roadmap built",
      text: "Next steps generated",
    },
  ];

  return (
    <div className="mt-8 overflow-x-auto pb-3">
      <div className="flex min-w-[850px] items-center justify-between gap-3">
        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <div
              key={step.title}
              className="flex flex-1 items-center gap-3"
            >
              <motion.div
                initial={{
                  opacity: 0,
                  scale: 0.7,
                }}
                whileInView={{
                  opacity: 1,
                  scale: 1,
                }}
                viewport={{
                  once: true,
                }}
                transition={{
                  delay: index * 0.12,
                }}
                whileHover={{
                  y: -5,
                }}
                className="flex min-w-0 flex-1 flex-col items-center text-center"
              >
                <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl border border-indigo-100 bg-gradient-to-br from-indigo-50 to-violet-50 text-indigo-600 shadow-sm">
                  <Icon size={22} />

                  <span className="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-[10px] font-bold text-white">
                    {index + 1}
                  </span>
                </div>

                <p className="mt-3 text-xs font-bold text-gray-900">
                  {step.title}
                </p>

                <p className="mt-1 text-[11px] text-gray-400">
                  {step.text}
                </p>
              </motion.div>

              {index !== steps.length - 1 && (
                <ChevronRight
                  size={18}
                  className="shrink-0 text-indigo-200"
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* =========================================================
   SKILL PILL
========================================================= */

function SkillPill({ skill, tone = "green" }) {
  const classes =
    tone === "green"
      ? "border-emerald-100 bg-emerald-50 text-emerald-700"
      : "border-orange-100 bg-orange-50 text-orange-700";

  return (
    <motion.span
      whileHover={{
        y: -2,
        scale: 1.03,
      }}
      className={`inline-flex items-center rounded-full border px-3 py-1.5 text-xs font-semibold ${classes}`}
    >
      {formatSkill(skill)}
    </motion.span>
  );
}

/* =========================================================
   SKILL GAP CARD
========================================================= */

function SkillGapCard({ skill }) {
  const demand = Number(skill.demand_percentage) || 0;
  const priority = String(
    skill.priority || "LOW"
  ).toUpperCase();

  const priorityClass =
    priority === "HIGH"
      ? "bg-red-50 text-red-600 border-red-100"
      : priority === "MEDIUM"
        ? "bg-orange-50 text-orange-600 border-orange-100"
        : "bg-gray-50 text-gray-500 border-gray-100";

  return (
    <motion.div
      whileHover={{
        y: -4,
        scale: 1.01,
      }}
      transition={{
        type: "spring",
        stiffness: 280,
        damping: 22,
      }}
      className="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-bold text-gray-900">
            {formatSkill(skill.skill_name)}
          </h3>

          <p className="mt-1 text-xs text-gray-400">
            Required by {skill.jobs_requiring_skill || 0} jobs
          </p>
        </div>

        <span
          className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${priorityClass}`}
        >
          {priority}
        </span>
      </div>

      <div className="mt-4">
        <div className="h-2 overflow-hidden rounded-full bg-gray-100">
          <motion.div
            initial={{
              width: 0,
            }}
            whileInView={{
              width: `${Math.min(demand, 100)}%`,
            }}
            viewport={{
              once: true,
            }}
            transition={{
              duration: 1,
              ease: "easeOut",
            }}
            className="h-full rounded-full bg-gradient-to-r from-orange-400 to-amber-500"
          />
        </div>

        <p className="mt-2 text-xs text-gray-400">
          {demand.toFixed(2)}% job demand
        </p>
      </div>
    </motion.div>
  );
}

/* =========================================================
   SKILL GAP FLOW MAP
========================================================= */

function SkillGapFlow({ matchingSkills, missingSkills, targetRole }) {
  const topGaps = [...missingSkills]
    .sort((a, b) => {
      const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
      const pa =
        priorityOrder[String(a.priority || "LOW").toUpperCase()] ?? 3;
      const pb =
        priorityOrder[String(b.priority || "LOW").toUpperCase()] ?? 3;

      if (pa !== pb) return pa - pb;

      return (
        Number(b.demand_percentage || 0) -
        Number(a.demand_percentage || 0)
      );
    })
    .slice(0, 6);

  const priorityStyles = {
    HIGH: "border-red-200 bg-red-50 text-red-700",
    MEDIUM: "border-orange-200 bg-orange-50 text-orange-700",
    LOW: "border-gray-200 bg-gray-50 text-gray-600",
  };

  return (
    <div className="mt-6 overflow-hidden rounded-[2rem] border border-indigo-100 bg-gradient-to-br from-white via-indigo-50/40 to-violet-50/60 p-5 sm:p-7">
      <div className="relative">
        {/* Desktop connectors */}
        <div className="pointer-events-none absolute left-[23%] right-[23%] top-[72px] hidden h-px bg-gradient-to-r from-emerald-200 via-indigo-300 to-orange-200 lg:block" />
        <div className="pointer-events-none absolute left-[50%] top-[72px] hidden h-[calc(100%-145px)] w-px bg-gradient-to-b from-indigo-200 via-orange-200 to-transparent lg:block" />

        <div className="grid gap-5 lg:grid-cols-[1fr_1.15fr_1fr] lg:items-start">
          {/* Current profile */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="relative z-10 rounded-3xl border border-emerald-100 bg-white/90 p-5 shadow-sm backdrop-blur"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
                <CheckCircle2 size={20} />
              </div>
              <div>
                <p className="text-xs font-semibold text-emerald-600">
                  CURRENT PROFILE
                </p>
                <h3 className="font-black text-gray-950">
                  Skills You Have
                </h3>
              </div>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {matchingSkills.slice(0, 8).map((skill) => (
                <span
                  key={normalizeSkill(skill)}
                  className="rounded-full border border-emerald-100 bg-emerald-50 px-2.5 py-1 text-[10px] font-bold text-emerald-700"
                >
                  {formatSkill(skill)}
                </span>
              ))}
            </div>

            <p className="mt-4 text-xs text-gray-400">
              {matchingSkills.length} aligned skills detected
            </p>
          </motion.div>

          {/* Target role */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative z-20 flex flex-col items-center"
          >
            <motion.div
              animate={{
                scale: [1, 1.04, 1],
                boxShadow: [
                  "0 10px 30px rgba(99,102,241,.15)",
                  "0 15px 45px rgba(99,102,241,.28)",
                  "0 10px 30px rgba(99,102,241,.15)",
                ],
              }}
              transition={{
                duration: 3.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="flex h-28 w-28 items-center justify-center rounded-full border-8 border-white bg-gradient-to-br from-indigo-600 via-violet-600 to-cyan-500 text-white"
            >
              <Target size={34} />
            </motion.div>

            <div className="mt-4 rounded-2xl border border-indigo-100 bg-white px-5 py-3 text-center shadow-sm">
              <p className="text-[10px] font-bold uppercase tracking-wider text-indigo-500">
                Target Role
              </p>
              <p className="mt-1 max-w-[190px] text-sm font-black text-gray-950">
                {targetRole}
              </p>
            </div>

            <div className="mt-3 hidden items-center gap-2 lg:flex">
              <span className="h-2 w-2 rounded-full bg-indigo-500" />
              <span className="text-[10px] font-bold text-gray-400">
                GAP ANALYSIS
              </span>
              <span className="h-2 w-2 rounded-full bg-orange-400" />
            </div>
          </motion.div>

          {/* Missing skills */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="relative z-10 rounded-3xl border border-orange-100 bg-white/90 p-5 shadow-sm backdrop-blur"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-orange-50 text-orange-600">
                <CircleAlert size={20} />
              </div>
              <div>
                <p className="text-xs font-semibold text-orange-600">
                  DETECTED GAPS
                </p>
                <h3 className="font-black text-gray-950">
                  Skills To Develop
                </h3>
              </div>
            </div>

            <div className="mt-4 space-y-2">
              {topGaps.length > 0 ? (
                topGaps.map((skill, index) => {
                  const priority = String(
                    skill.priority || "LOW"
                  ).toUpperCase();

                  return (
                    <motion.div
                      key={`${skill.skill_name}-${index}`}
                      initial={{ opacity: 0, x: 12 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: index * 0.07 }}
                      whileHover={{ x: 4 }}
                      className="flex items-center justify-between gap-2 rounded-2xl border border-gray-100 bg-gray-50/80 px-3 py-2.5"
                    >
                      <div className="min-w-0">
                        <p className="truncate text-xs font-bold text-gray-800">
                          {formatSkill(skill.skill_name)}
                        </p>
                        <p className="mt-0.5 text-[10px] text-gray-400">
                          {Number(skill.demand_percentage || 0).toFixed(2)}%
                          demand
                        </p>
                      </div>

                      <span
                        className={`shrink-0 rounded-full border px-2 py-1 text-[9px] font-black ${
                          priorityStyles[priority] ||
                          priorityStyles.LOW
                        }`}
                      >
                        {priority}
                      </span>
                    </motion.div>
                  );
                })
              ) : (
                <p className="rounded-2xl bg-emerald-50 p-4 text-xs font-semibold text-emerald-700">
                  No major skill gaps detected.
                </p>
              )}
            </div>

            {missingSkills.length > 6 && (
              <p className="mt-3 text-center text-[10px] font-semibold text-gray-400">
                + {missingSkills.length - 6} more gaps in the detailed list
              </p>
            )}
          </motion.div>
        </div>

        {/* Flow direction */}
        <div className="mt-6 flex flex-col items-center justify-center gap-2 lg:flex-row">
          <div className="flex items-center gap-2 rounded-full border border-indigo-100 bg-white px-4 py-2 shadow-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
            <span className="text-[10px] font-bold text-gray-500">
              YOUR SKILLS
            </span>
          </div>

          <ArrowRight className="rotate-90 text-indigo-300 lg:rotate-0" size={16} />

          <div className="flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 shadow-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-indigo-600" />
            <span className="text-[10px] font-bold text-indigo-700">
              TARGET ROLE
            </span>
          </div>

          <ArrowRight className="rotate-90 text-indigo-300 lg:rotate-0" size={16} />

          <div className="flex items-center gap-2 rounded-full border border-orange-100 bg-orange-50 px-4 py-2 shadow-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-orange-500" />
            <span className="text-[10px] font-bold text-orange-700">
              SKILL GAPS
            </span>
          </div>

          <ArrowRight className="rotate-90 text-indigo-300 lg:rotate-0" size={16} />

          <div className="flex items-center gap-2 rounded-full border border-violet-100 bg-violet-50 px-4 py-2 shadow-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-violet-600" />
            <span className="text-[10px] font-bold text-violet-700">
              LEARNING ROADMAP
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

/* =========================================================
   ROADMAP
========================================================= */

function RoadmapCard({ item, index }) {
  return (
    <motion.div
      initial={{
        opacity: 0,
        x: -20,
      }}
      whileInView={{
        opacity: 1,
        x: 0,
      }}
      viewport={{
        once: true,
      }}
      transition={{
        delay: index * 0.08,
      }}
      whileHover={{
        x: 5,
      }}
      className="relative flex gap-4"
    >
      <div className="relative flex flex-col items-center">
        <div className="z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-600 text-sm font-black text-white shadow-lg shadow-indigo-200">
          {String(index + 1).padStart(2, "0")}
        </div>

        {index !== 5 && (
          <div className="absolute top-10 h-full w-px bg-gradient-to-b from-indigo-200 to-transparent" />
        )}
      </div>

      <div className="mb-6 flex-1 rounded-2xl border border-gray-100 bg-white p-4 shadow-sm">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm font-bold text-gray-900">
              {formatSkill(item.skill_name)}
            </p>

            <p className="mt-1 text-xs text-gray-400">
              Priority:{" "}
              {String(item.priority || "LOW").toUpperCase()}
            </p>
          </div>

          <span className="rounded-full bg-indigo-50 px-2.5 py-1 text-[10px] font-bold text-indigo-600">
            {Number(item.demand_percentage || 0).toFixed(2)}%
          </span>
        </div>

        <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
          <Lightbulb
            size={14}
            className="text-indigo-500"
          />

          Build this skill to improve your alignment with the target role.
        </div>
      </div>
    </motion.div>
  );
}

/* =========================================================
   JOB RECOMMENDATION
========================================================= */

function JobCard({ job, index }) {
  const match = Number(
    job.job_match_percentage
  ) || 0;

  return (
    <motion.div
      whileHover={{
        y: -7,
        rotateX: 2,
        rotateY: -2,
      }}
      transition={{
        type: "spring",
        stiffness: 260,
        damping: 20,
      }}
      style={{
        transformStyle: "preserve-3d",
      }}
      className="group rounded-3xl border border-gray-100 bg-white p-5 shadow-sm hover:shadow-xl hover:shadow-indigo-100/40"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-indigo-50 font-black text-indigo-600">
            #{index + 1}
          </div>

          <div>
            <h3 className="font-bold text-gray-900">
              {job.job_title || "Recommended Role"}
            </h3>

            <p className="mt-1 text-xs text-gray-400">
              Career opportunity
            </p>
          </div>
        </div>

        <ArrowRight
          size={18}
          className="text-gray-300 transition group-hover:translate-x-1 group-hover:text-indigo-600"
        />
      </div>

      <div className="mt-5">
        <div className="flex items-end justify-between">
          <div>
            <p className="text-xs text-gray-400">
              Job match
            </p>

            <p className="mt-1 text-2xl font-black text-indigo-600">
              {match.toFixed(2)}%
            </p>
          </div>

          <div className="h-16 w-16">
            <svg
              viewBox="0 0 40 40"
              className="h-full w-full -rotate-90"
            >
              <circle
                cx="20"
                cy="20"
                r="15"
                fill="none"
                stroke="#EEF2FF"
                strokeWidth="4"
              />

              <motion.circle
                cx="20"
                cy="20"
                r="15"
                fill="none"
                stroke="#6366F1"
                strokeWidth="4"
                strokeLinecap="round"
                strokeDasharray="94"
                initial={{
                  strokeDashoffset: 94,
                }}
                whileInView={{
                  strokeDashoffset:
                    94 - (Math.min(match, 100) / 100) * 94,
                }}
                viewport={{
                  once: true,
                }}
                transition={{
                  duration: 1,
                }}
              />
            </svg>
          </div>
        </div>
      </div>

      <div className="mt-5 border-t border-gray-100 pt-4">
        <p className="text-xs font-semibold text-gray-500">
          Matching skills
        </p>

        <div className="mt-2 flex flex-wrap gap-2">
          {String(job.matching_skills || "")
            .split("|")
            .map((skill) => skill.trim())
            .filter(Boolean)
            .slice(0, 5)
            .map((skill) => (
              <span
                key={skill}
                className="rounded-full bg-emerald-50 px-2.5 py-1 text-[10px] font-semibold text-emerald-700"
              >
                {formatSkill(skill)}
              </span>
            ))}
        </div>
      </div>
    </motion.div>
  );
}

/* =========================================================
   MAIN DASHBOARD
========================================================= */

function Dashboard() {
  const location = useLocation();

  // Keep the latest analysis available after refresh or when the user
  // returns to the dashboard from another page.
  const [savedResult, setSavedResult] = useState(() => {
    try {
      const stored = localStorage.getItem("careergenome_last_analysis");
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const stateAnalysis = location.state?.analysis || null;

  useEffect(() => {
    if (!stateAnalysis) return;

    const resultToSave = {
      analysis: stateAnalysis,
      targetRole:
        location.state?.targetRole ||
        stateAnalysis?.target_role_analysis?.target_role ||
        "Target Role",
      filename: location.state?.filename || "",
      savedAt: new Date().toISOString(),
    };

    try {
      localStorage.setItem(
        "careergenome_last_analysis",
        JSON.stringify(resultToSave)
      );
      setSavedResult(resultToSave);
    } catch (error) {
      console.warn("Could not save the latest analysis locally.", error);
    }
  }, [
    stateAnalysis,
    location.state?.targetRole,
    location.state?.filename,
  ]);

  const analysis = stateAnalysis || savedResult?.analysis || null;

  const targetRole =
    location.state?.targetRole ||
    savedResult?.targetRole ||
    analysis?.target_role_analysis?.target_role ||
    "Target Role";

  const studentProfile =
    analysis?.student_profile || {};

  const overallAnalysis =
    analysis?.overall_analysis || {};

  const targetRoleAnalysis =
    analysis?.target_role_analysis || {};

  const studentSkills = useMemo(
    () =>
      uniqueSkills(
        studentProfile.skills || []
      ),
    [studentProfile.skills]
  );

  const missingSkills = useMemo(
    () =>
      Array.isArray(
        targetRoleAnalysis.missing_skills
      )
        ? targetRoleAnalysis.missing_skills
        : [],
    [targetRoleAnalysis.missing_skills]
  );

  // Trust the backend's target-role matched list rather than guessing by
  // subtracting missing skills from every skill found in the resume.
  const matchingSkills = useMemo(() => {
    const roleMatchedSkills = targetRoleAnalysis?.matched_skills;

    if (!Array.isArray(roleMatchedSkills)) return [];

    return uniqueSkills(
      roleMatchedSkills.map((skill) =>
        typeof skill === "string" ? skill : skill?.skill_name
      )
    );
  }, [targetRoleAnalysis]);

  // Career Match must represent the selected target role, not the best job
  // match across the whole dataset.
  const matchScore = useMemo(() => {
    const roleScore = Number(targetRoleAnalysis?.match_percentage);
    if (!Number.isFinite(roleScore)) return 0;
    return Math.min(100, Math.max(0, roleScore));
  }, [targetRoleAnalysis]);

  const recommendations = useMemo(() => {
    const primary = overallAnalysis?.top_job_recommendations;
    const fallback = analysis?.top_job_recommendations;

    const jobs = Array.isArray(primary)
      ? primary
      : Array.isArray(fallback)
        ? fallback
        : [];

    return jobs.filter(Boolean);
  }, [
    overallAnalysis?.top_job_recommendations,
    analysis?.top_job_recommendations,
  ]);

  const roadmap = useMemo(() => {
    return [...missingSkills]
      .sort((a, b) => {
        const priorityOrder = {
          HIGH: 0,
          MEDIUM: 1,
          LOW: 2,
        };

        const priorityA =
          priorityOrder[
            String(a.priority || "LOW").toUpperCase()
          ] ?? 3;

        const priorityB =
          priorityOrder[
            String(b.priority || "LOW").toUpperCase()
          ] ?? 3;

        if (priorityA !== priorityB) {
          return priorityA - priorityB;
        }

        return (
          Number(b.demand_percentage || 0) -
          Number(a.demand_percentage || 0)
        );
      })
      .slice(0, 6);
  }, [missingSkills]);

  /* =========================================================
     RADAR
  ========================================================= */

  const radarSkills = [
    "Python",
    "SQL",
    "Data Science",
    "Machine Learning",
    "Statistics",
    "Data Analysis",
  ];

  const radarData = radarSkills.map((skill) => ({
    skill,
    value: matchingSkills.some(
      (matchedSkill) => normalizeSkill(matchedSkill) === normalizeSkill(skill)
    )
      ? 100
      : 0,
  }));

  /* =========================================================
     NO DATA
  ========================================================= */

  if (!analysis) {
    return (
      <main className="min-h-[75vh] bg-[#F7F8FC] px-6 py-20">
        <div className="mx-auto max-w-3xl">
          <motion.div
            initial={{
              opacity: 0,
              y: 30,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            className="rounded-[2rem] border border-gray-100 bg-white p-10 text-center shadow-xl shadow-indigo-100/30"
          >
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-indigo-50 text-indigo-600">
              <FileSearch size={34} />
            </div>

            <h1 className="mt-6 text-3xl font-black text-gray-950">
              Your Career Genome is waiting.
            </h1>

            <p className="mx-auto mt-3 max-w-xl text-gray-500">
              Upload your resume and let CareerGenome
              analyze your skills, career alignment and
              skill gaps.
            </p>

            <Link
              to="/analyze"
              className="mt-8 inline-flex items-center gap-2 rounded-2xl bg-indigo-600 px-6 py-3.5 font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700"
            >
              Analyze My Resume
              <ArrowRight size={18} />
            </Link>
          </motion.div>
        </div>
      </main>
    );
  }

  return (
    <main className="relative overflow-hidden bg-[#F7F8FC] px-4 py-8 sm:px-6 lg:px-8">
      {/* =====================================================
          AMBIENT BACKGROUND
      ===================================================== */}

      <motion.div
        className="pointer-events-none absolute -left-40 top-20 h-96 w-96 rounded-full bg-indigo-300/20 blur-3xl"
        animate={{
          x: [0, 40, 0],
          y: [0, -30, 0],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <motion.div
        className="pointer-events-none absolute -right-40 top-[35%] h-96 w-96 rounded-full bg-violet-300/20 blur-3xl"
        animate={{
          x: [0, -30, 0],
          y: [0, 40, 0],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <div className="relative mx-auto max-w-7xl">
        {/* =================================================
            HERO
        ================================================= */}

        <motion.section
          initial={{
            opacity: 0,
            y: 25,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.6,
          }}
          className="relative overflow-hidden rounded-[2rem] border border-indigo-100 bg-white p-6 shadow-xl shadow-indigo-100/30 sm:p-8 lg:p-10"
        >
          <div className="grid items-center gap-8 lg:grid-cols-[0.95fr_1.05fr]">
            {/* Left */}
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1.5 text-xs font-bold text-indigo-600">
                <Sparkles size={13} />
                Your Career Intelligence
              </div>

              <h1 className="mt-5 max-w-xl text-4xl font-black tracking-tight text-gray-950 sm:text-5xl">
                Your career is a{" "}
                <span className="bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-500 bg-clip-text text-transparent">
                  genome.
                </span>
              </h1>

              <p className="mt-4 max-w-xl text-base leading-7 text-gray-500">
                We analyzed your resume, extracted your
                skills and compared them with real job
                requirements to build your personalized
                career intelligence.
              </p>

              <div className="mt-6 flex flex-wrap items-center gap-3">
                <div className="rounded-2xl border border-gray-100 bg-gray-50 px-4 py-3">
                  <p className="text-xs text-gray-400">
                    Target role
                  </p>

                  <p className="mt-1 font-bold text-gray-900">
                    {targetRole}
                  </p>
                </div>

                <Link
                  to="/analyze"
                  className="group inline-flex items-center gap-2 rounded-2xl bg-indigo-600 px-5 py-3 font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700"
                >
                  Analyze Again
                  <ArrowRight
                    size={17}
                    className="transition group-hover:translate-x-1"
                  />
                </Link>
              </div>
            </div>

            {/* Genome Visual */}
            <div className="relative">
              <CareerGenome
                skills={studentSkills}
              />
            </div>
          </div>
        </motion.section>

        {/* =================================================
            STATS
        ================================================= */}

        <section className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            icon={Brain}
            label="Skills Identified"
            value={studentSkills.length}
            tone="indigo"
          />

          <StatCard
            icon={CheckCircle2}
            label="Matching Skills"
            value={matchingSkills.length}
            tone="emerald"
          />

          <StatCard
            icon={CircleAlert}
            label="Skill Gaps"
            value={
              targetRoleAnalysis?.missing_skill_count ??
              missingSkills.length
            }
            tone="orange"
          />

          <StatCard
            icon={Target}
            label="Career Match"
            value={matchScore}
            suffix="%"
            tone="cyan"
          />
        </section>

        {/* =================================================
            MATCH + DNA
        ================================================= */}

        <section className="mt-6 grid gap-6 lg:grid-cols-[0.85fr_1.15fr]">
          {/* Match */}
          <motion.div
            initial={{
              opacity: 0,
              x: -20,
            }}
            whileInView={{
              opacity: 1,
              x: 0,
            }}
            viewport={{
              once: true,
            }}
            className="rounded-[2rem] border border-gray-100 bg-white p-6 shadow-sm sm:p-8"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-400">
                  Career Match
                </p>

                <h2 className="mt-1 text-2xl font-black text-gray-950">
                  {targetRole}
                </h2>
              </div>

              <span className="rounded-full bg-orange-50 px-3 py-1.5 text-xs font-bold text-orange-600">
                {matchScore >= 70
                  ? "Strong Match"
                  : matchScore >= 50
                    ? "Good Progress"
                    : "Needs Improvement"}
              </span>
            </div>

            <div className="mt-4 flex justify-center">
              <MatchRing score={matchScore} />
            </div>

            <div className="rounded-2xl bg-gradient-to-r from-indigo-50 to-violet-50 p-5">
              <div className="flex gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm">
                  <Lightbulb size={19} />
                </div>

                <div>
                  <p className="font-bold text-indigo-900">
                    {matchScore >= 70
                      ? "You are strongly aligned."
                      : "There is room to grow."}
                  </p>

                  <p className="mt-1 text-sm leading-6 text-indigo-600/80">
                    Focus on your highest-priority skill
                    gaps to improve your career alignment.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Radar */}
          <motion.div
            initial={{
              opacity: 0,
              x: 20,
            }}
            whileInView={{
              opacity: 1,
              x: 0,
            }}
            viewport={{
              once: true,
            }}
            className="rounded-[2rem] border border-gray-100 bg-white p-6 shadow-sm sm:p-8"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-400">
                  Career DNA
                </p>

                <h2 className="mt-1 text-2xl font-black text-gray-950">
                  Your Skill Profile
                </h2>
              </div>

              <span className="rounded-full bg-indigo-50 px-3 py-1.5 text-xs font-bold text-indigo-600">
                {studentSkills.length} Skill Areas
              </span>
            </div>

            <div className="mt-4 h-[320px]">
              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <RadarChart
                  data={radarData}
                  cx="50%"
                  cy="50%"
                  outerRadius="72%"
                >
                  <PolarGrid
                    stroke="#E0E7FF"
                  />

                  <PolarAngleAxis
                    dataKey="skill"
                    tick={{
                      fill: "#64748B",
                      fontSize: 11,
                    }}
                  />

                  <Radar
                    name="Your Skills"
                    dataKey="value"
                    stroke="#6366F1"
                    fill="#818CF8"
                    fillOpacity={0.25}
                    strokeWidth={2}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <p className="text-center text-xs text-gray-400">
              Skill presence is based on skills extracted
              from your resume.
            </p>
          </motion.div>
        </section>

        {/* =================================================
            HOW AI ANALYZED
        ================================================= */}

        <section className="mt-6 rounded-[2rem] border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
          <SectionTitle
            eyebrow="AI Analysis Journey"
            title="How We Analyzed Your Resume"
            description="Your resume moves through a structured intelligence pipeline before the career recommendations are generated."
            icon={Sparkles}
          />

          <AnalysisPipeline />
        </section>

        {/* =================================================
            MATCHING + GAPS
        ================================================= */}

        <section className="mt-6">
          <SectionTitle
            eyebrow="Skill Gap Intelligence"
            title="See exactly what is missing"
            description="The flow below connects your current skills to the target role and shows the highest-impact skills you should develop next."
            icon={GitBranch}
          />

          <SkillGapFlow
            matchingSkills={matchingSkills}
            missingSkills={missingSkills}
            targetRole={targetRole}
          />

          {/* Detailed skill gaps */}
          <div className="mt-5 rounded-[2rem] border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
            <div className="flex items-start justify-between">
              <SectionTitle
                eyebrow="Detailed Gap Breakdown"
                title="Skill-by-skill analysis"
                description="Job-demand signals and priority are shown for every detected gap."
                icon={CircleAlert}
              />

              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-orange-50 text-orange-600">
                <CircleAlert size={20} />
              </div>
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {missingSkills.length > 0 ? (
                missingSkills.map((skill, index) => (
                  <SkillGapCard
                    key={`${skill.skill_name}-${index}`}
                    skill={skill}
                  />
                ))
              ) : (
                <div className="rounded-2xl bg-emerald-50 p-5 text-sm font-medium text-emerald-700 sm:col-span-2 lg:col-span-3">
                  Great! No major skill gaps were returned for this target role.
                </div>
              )}
            </div>
          </div>
        </section>

        {/* =================================================
            ROADMAP
        ================================================= */}

        <section className="mt-6 rounded-[2rem] border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
          <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
            <SectionTitle
              eyebrow="Recommended Roadmap"
              title="What You Should Learn Next"
              description="A prioritized learning sequence generated from your current skill gaps and job-demand signals."
              icon={GraduationCap}
            />

            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 text-sm font-bold text-indigo-600 transition hover:text-indigo-700"
            >
              Analyze Again
              <ArrowRight size={16} />
            </Link>
          </div>

          <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_0.8fr]">
            {/* Timeline */}
            <div>
              {roadmap.length > 0 ? (
                roadmap.map((item, index) => (
                  <RoadmapCard
                    key={`${item.skill_name}-${index}`}
                    item={item}
                    index={index}
                  />
                ))
              ) : (
                <div className="rounded-2xl bg-gray-50 p-8 text-center text-sm text-gray-500">
                  No learning recommendations were
                  returned for this analysis.
                </div>
              )}
            </div>

            {/* Roadmap Visual */}
            <div className="hidden lg:block">
              <div className="sticky top-28 overflow-hidden rounded-[2rem] border border-indigo-100 bg-gradient-to-br from-indigo-50 via-white to-violet-100/60 p-7">
                <motion.div
                  className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-violet-300/30 blur-3xl"
                  animate={{
                    scale: [0.8, 1.15, 0.8],
                  }}
                  transition={{
                    duration: 5,
                    repeat: Infinity,
                  }}
                />

                <div className="relative">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-lg shadow-indigo-200">
                    <GitBranch size={25} />
                  </div>

                  <h3 className="mt-6 text-2xl font-black text-gray-950">
                    Build your next version.
                  </h3>

                  <p className="mt-3 text-sm leading-6 text-gray-500">
                    Your roadmap turns the skill-gap analysis
                    into a practical sequence of areas to
                    strengthen.
                  </p>

                  <div className="mt-7 space-y-3">
                    {roadmap.slice(0, 4).map(
                      (item, index) => (
                        <motion.div
                          key={`${item.skill_name}-visual`}
                          initial={{
                            opacity: 0,
                            x: 15,
                          }}
                          whileInView={{
                            opacity: 1,
                            x: 0,
                          }}
                          viewport={{
                            once: true,
                          }}
                          transition={{
                            delay: index * 0.1,
                          }}
                          className="flex items-center gap-3 rounded-2xl border border-white bg-white/70 p-3 backdrop-blur"
                        >
                          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-indigo-50 text-xs font-black text-indigo-600">
                            {index + 1}
                          </div>

                          <span className="text-sm font-semibold text-gray-800">
                            {formatSkill(
                              item.skill_name
                            )}
                          </span>
                        </motion.div>
                      )
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =================================================
            CAREER OPPORTUNITIES
        ================================================= */}

        <section className="mt-8">
          <div className="rounded-[2rem] border border-indigo-100 bg-gradient-to-r from-white via-indigo-50/40 to-violet-50/50 p-6 shadow-sm sm:p-8">
            <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
              <SectionTitle
                eyebrow="Career Opportunities"
                title="Roles That Match Your Genome"
                description="These recommendations come directly from the job-matching analysis and are ranked by your current skill alignment."
                icon={BriefcaseBusiness}
              />

              <div className="flex items-center gap-2 rounded-full bg-white px-4 py-2 text-xs font-bold text-indigo-600 shadow-sm">
                <BriefcaseBusiness size={14} />
                {recommendations.length} roles found
              </div>
            </div>

            <div className="mt-6 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {recommendations.length > 0 ? (
                recommendations.slice(0, 10).map((job, index) => (
                  <JobCard
                    key={`${job.job_id || job.job_title}-${index}`}
                    job={job}
                    index={index}
                  />
                ))
              ) : (
                <div className="rounded-3xl border border-orange-100 bg-orange-50 p-8 text-sm font-medium text-orange-700 md:col-span-2 lg:col-span-3">
                  No career recommendations were returned for this analysis.
                </div>
              )}
            </div>
          </div>
        </section>

        {/* =================================================
            FINAL CTA
        ================================================= */}

        <motion.section
          initial={{
            opacity: 0,
            scale: 0.98,
          }}
          whileInView={{
            opacity: 1,
            scale: 1,
          }}
          viewport={{
            once: true,
          }}
          className="relative mt-8 overflow-hidden rounded-[2rem] bg-gradient-to-br from-indigo-600 via-violet-600 to-indigo-700 p-8 text-white shadow-2xl shadow-indigo-200 sm:p-10"
        >
          {/* Decorative circles */}
          <motion.div
            className="absolute -right-20 -top-20 h-64 w-64 rounded-full border border-white/10"
            animate={{
              rotate: 360,
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
            }}
          />

          <motion.div
            className="absolute -bottom-32 right-32 h-72 w-72 rounded-full border border-white/10"
            animate={{
              rotate: -360,
            }}
            transition={{
              duration: 25,
              repeat: Infinity,
              ease: "linear",
            }}
          />

          <div className="relative flex flex-col items-start justify-between gap-8 md:flex-row md:items-center">
            <div className="max-w-2xl">
              <div className="flex items-center gap-2 text-sm font-semibold text-indigo-100">
                <Sparkles size={16} />
                Career Opportunities
              </div>

              <h2 className="mt-4 text-3xl font-black tracking-tight sm:text-4xl">
                You're closer than you think.
              </h2>

              <p className="mt-3 text-sm leading-7 text-indigo-100 sm:text-base">
                Your current profile already contains{" "}
                <strong>
                  {matchingSkills.length}
                </strong>{" "}
                matching skills. Strengthen the right
                missing skills and keep building toward
                your {targetRole} career path.
              </p>
            </div>

            <Link
              to="/analyze"
              className="group inline-flex shrink-0 items-center gap-2 rounded-2xl bg-white px-6 py-3.5 font-bold text-indigo-600 shadow-xl transition hover:bg-indigo-50"
            >
              Analyze Again
              <ArrowRight
                size={18}
                className="transition group-hover:translate-x-1"
              />
            </Link>
          </div>
        </motion.section>

        {/* Bottom spacing */}
        <div className="h-8" />
      </div>
    </main>
  );
}

export default Dashboard;