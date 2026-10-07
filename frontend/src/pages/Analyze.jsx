import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload,
  FileText,
  X,
  Sparkles,
  CheckCircle2,
  Loader2,
  Brain,
  Target,
  Search,
  Route,
  AlertCircle,
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000/analyze-resume";

const processingSteps = [
  {
    label: "Resume uploaded",
    description: "Your resume is ready for analysis.",
    icon: FileText,
  },
  {
    label: "Extracting skills",
    description: "Identifying skills and experience from your resume.",
    icon: Search,
  },
  {
    label: "Comparing job requirements",
    description: "Matching your profile with job-market requirements.",
    icon: Target,
  },
  {
    label: "Finding skill gaps",
    description: "Identifying skills you can develop next.",
    icon: Brain,
  },
  {
    label: "Building your roadmap",
    description: "Preparing personalized career recommendations.",
    icon: Route,
  },
];

function Analyze() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [targetRole, setTargetRole] = useState("");
  const [dragActive, setDragActive] = useState(false);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  const [error, setError] = useState("");

  const validateFile = (file) => {
    if (!file) return false;

    const fileName = file.name.toLowerCase();

    if (!fileName.endsWith(".pdf") && !fileName.endsWith(".txt")) {
      setError("Please upload a PDF or TXT resume.");
      return false;
    }

    if (file.size === 0) {
      setError("The uploaded file is empty.");
      return false;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("File size must be less than 10 MB.");
      return false;
    }

    setError("");
    return true;
  };

  const handleFileSelect = (file) => {
    if (!validateFile(file)) {
      return;
    }

    setSelectedFile(file);
    setError("");
  };

  const handleInputChange = (event) => {
    const file = event.target.files?.[0];

    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragActive(false);

    const file = event.dataTransfer.files?.[0];

    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please upload your resume first.");
      return;
    }

    if (!targetRole.trim()) {
      setError("Please enter your target role.");
      return;
    }

    setError("");
    setIsAnalyzing(true);
    setActiveStep(0);

    const formData = new FormData();

    formData.append("resume", selectedFile);
    formData.append("target_role", targetRole.trim());

    try {
      /*
        Move through the visual analysis stages while
        the real backend request is running.
      */

      const stepTimer = setInterval(() => {
        setActiveStep((currentStep) => {
          if (currentStep < processingSteps.length - 1) {
            return currentStep + 1;
          }

          return currentStep;
        });
      }, 1800);

      const response = await axios.post(API_URL, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      clearInterval(stepTimer);

      setActiveStep(processingSteps.length - 1);

      /*
        Small delay so the user can see the final
        "roadmap ready" step before navigating.
      */

      await new Promise((resolve) => setTimeout(resolve, 700));

      navigate("/dashboard", {
        state: {
          analysis: response.data.analysis,
          targetRole: response.data.target_role,
          filename: response.data.filename,
        },
      });
    } catch (err) {
      setIsAnalyzing(false);

      const backendMessage =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Something went wrong while analyzing your resume.";

      setError(backendMessage);
    }
  };

  /*
    -------------------------------------------------------
    PROCESSING SCREEN
    -------------------------------------------------------
  */

  if (isAnalyzing) {
    return (
      <main className="min-h-screen bg-[#F7F8FC] px-6 py-12">
        <div className="mx-auto flex min-h-[calc(100vh-150px)] max-w-4xl items-center justify-center">
          <motion.div
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full rounded-3xl border border-gray-100 bg-white p-8 shadow-sm sm:p-12"
          >
            {/* Header */}

            <div className="text-center">
              <motion.div
                animate={{
                  scale: [1, 1.08, 1],
                  rotate: [0, 4, -4, 0],
                }}
                transition={{
                  duration: 2.2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-indigo-50 text-indigo-600"
              >
                <Sparkles size={34} />
              </motion.div>

              <h1 className="mt-7 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Analyzing your career profile
              </h1>

              <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-gray-500 sm:text-base">
                Our AI is analyzing your resume against job-market
                requirements and preparing your personalized career insights.
              </p>
            </div>

            {/* Progress */}

            <div className="mx-auto mt-10 max-w-2xl">
              <div className="mb-3 flex items-center justify-between text-xs font-semibold text-gray-400">
                <span>Analysis progress</span>

                <span>
                  {Math.min(
                    Math.round(
                      ((activeStep + 1) / processingSteps.length) * 100
                    ),
                    100
                  )}
                  %
                </span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-gray-100">
                <motion.div
                  className="h-full rounded-full bg-indigo-600"
                  initial={{ width: "0%" }}
                  animate={{
                    width: `${
                      ((activeStep + 1) / processingSteps.length) * 100
                    }%`,
                  }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </div>

            {/* Steps */}

            <div className="mx-auto mt-10 max-w-2xl space-y-3">
              {processingSteps.map((step, index) => {
                const Icon = step.icon;

                const completed = index < activeStep;
                const current = index === activeStep;

                return (
                  <motion.div
                    key={step.label}
                    initial={{ opacity: 0, x: -15 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{
                      delay: index * 0.08,
                    }}
                    className={`flex items-center gap-4 rounded-2xl border p-4 transition ${
                      current
                        ? "border-indigo-100 bg-indigo-50"
                        : completed
                        ? "border-emerald-100 bg-emerald-50/60"
                        : "border-gray-100 bg-gray-50"
                    }`}
                  >
                    <div
                      className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${
                        completed
                          ? "bg-emerald-100 text-emerald-600"
                          : current
                          ? "bg-indigo-100 text-indigo-600"
                          : "bg-gray-100 text-gray-400"
                      }`}
                    >
                      {completed ? (
                        <CheckCircle2 size={21} />
                      ) : current ? (
                        <Loader2
                          size={21}
                          className="animate-spin"
                        />
                      ) : (
                        <Icon size={21} />
                      )}
                    </div>

                    <div className="min-w-0 flex-1">
                      <p
                        className={`font-semibold ${
                          current
                            ? "text-indigo-700"
                            : completed
                            ? "text-emerald-700"
                            : "text-gray-500"
                        }`}
                      >
                        {step.label}
                      </p>

                      <p className="mt-1 text-xs text-gray-400">
                        {step.description}
                      </p>
                    </div>

                    {completed && (
                      <span className="text-xs font-semibold text-emerald-600">
                        Done
                      </span>
                    )}

                    {current && (
                      <span className="text-xs font-semibold text-indigo-600">
                        Working
                      </span>
                    )}
                  </motion.div>
                );
              })}
            </div>

            {/* Bottom info */}

            <div className="mt-8 flex items-center justify-center gap-2 text-xs text-gray-400">
              <Sparkles size={14} />
              <span>
                This may take a few moments while we build your career profile.
              </span>
            </div>
          </motion.div>
        </div>
      </main>
    );
  }

  /*
    -------------------------------------------------------
    NORMAL ANALYZE PAGE
    -------------------------------------------------------
  */

  return (
    <main className="min-h-screen bg-[#F7F8FC] px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">

        {/* Header */}

        <section className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="mx-auto inline-flex items-center gap-2 rounded-full bg-indigo-50 px-4 py-2 text-sm font-semibold text-indigo-600"
          >
            <Sparkles size={16} />
            AI Career Intelligence
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08 }}
            className="mx-auto mt-5 max-w-3xl text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl"
          >
            Turn your resume into a{" "}
            <span className="text-indigo-600">
              career roadmap.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.16 }}
            className="mx-auto mt-4 max-w-2xl text-base leading-7 text-gray-500"
          >
            Upload your resume, choose your target role, and let
            CareerGenome identify your skills, gaps, and career opportunities.
          </motion.p>
        </section>

        {/* Main Card */}

        <motion.section
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mx-auto mt-10 max-w-4xl rounded-3xl border border-gray-100 bg-white p-6 shadow-sm sm:p-8"
        >
          {/* Step indicator */}

          <div className="mb-8 flex items-center justify-center gap-3 text-xs font-semibold text-gray-400">
            <div className="flex items-center gap-2 text-indigo-600">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-indigo-600 text-white">
                1
              </span>
              Upload Resume
            </div>

            <div className="h-px w-10 bg-gray-200 sm:w-20" />

            <div className="flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-gray-100">
                2
              </span>
              Target Role
            </div>

            <div className="h-px w-10 bg-gray-200 sm:w-20" />

            <div className="flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-gray-100">
                3
              </span>
              Get Insights
            </div>
          </div>

          {/* Upload */}

          <div>
            <div className="mb-3 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-gray-900">
                  Upload your resume
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                  We currently support PDF and TXT files.
                </p>
              </div>

              <span className="hidden rounded-full bg-gray-50 px-3 py-1 text-xs font-medium text-gray-400 sm:block">
                Max 10 MB
              </span>
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt"
              onChange={handleInputChange}
              className="hidden"
            />

            <AnimatePresence mode="wait">
              {!selectedFile ? (
                <motion.button
                  key="upload"
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  whileHover={{ scale: 1.005 }}
                  whileTap={{ scale: 0.995 }}
                  className={`w-full rounded-2xl border-2 border-dashed p-10 text-center transition sm:p-14 ${
                    dragActive
                      ? "border-indigo-500 bg-indigo-50"
                      : "border-gray-200 bg-gray-50 hover:border-indigo-300 hover:bg-indigo-50/40"
                  }`}
                >
                  <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-indigo-600 shadow-sm">
                    <Upload size={28} />
                  </div>

                  <h3 className="mt-5 text-base font-bold text-gray-900">
                    {dragActive
                      ? "Drop your resume here"
                      : "Drag & drop your resume"}
                  </h3>

                  <p className="mt-2 text-sm text-gray-500">
                    or click to browse from your computer
                  </p>

                  <span className="mt-5 inline-flex rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white">
                    Choose Resume
                  </span>
                </motion.button>
              ) : (
                <motion.div
                  key="file"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="flex items-center gap-4 rounded-2xl border border-emerald-100 bg-emerald-50/60 p-5"
                >
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white text-emerald-600 shadow-sm">
                    <FileText size={24} />
                  </div>

                  <div className="min-w-0 flex-1">
                    <p className="truncate font-semibold text-gray-900">
                      {selectedFile.name}
                    </p>

                    <p className="mt-1 text-xs text-gray-500">
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </p>

                    <div className="mt-2 flex items-center gap-1.5 text-xs font-semibold text-emerald-600">
                      <CheckCircle2 size={14} />
                      Resume ready for analysis
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={removeFile}
                    className="rounded-xl p-2 text-gray-400 transition hover:bg-white hover:text-red-500"
                    aria-label="Remove resume"
                  >
                    <X size={20} />
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Target Role */}

          <div className="mt-8">
            <label
              htmlFor="targetRole"
              className="mb-3 block text-lg font-bold text-gray-900"
            >
              What role are you targeting?
            </label>

            <p className="mb-3 text-sm text-gray-500">
              Enter the job role you want to prepare for.
            </p>

            <div className="relative">
              <Target
                size={20}
                className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
              />

              <input
                id="targetRole"
                type="text"
                value={targetRole}
                onChange={(event) => {
                  setTargetRole(event.target.value);
                  setError("");
                }}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleAnalyze();
                  }
                }}
                placeholder="e.g. Data Scientist, Software Engineer, Data Analyst"
                className="w-full rounded-2xl border border-gray-200 bg-gray-50 py-4 pl-12 pr-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50"
              />
            </div>
          </div>

          {/* Error */}

          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, height: 0, y: -5 }}
                animate={{ opacity: 1, height: "auto", y: 0 }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-5 overflow-hidden"
              >
                <div className="flex items-start gap-3 rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-600">
                  <AlertCircle
                    size={19}
                    className="mt-0.5 shrink-0"
                  />

                  <p>{error}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Analyze Button */}

          <button
            type="button"
            onClick={handleAnalyze}
            disabled={!selectedFile || !targetRole.trim()}
            className="mt-8 flex w-full items-center justify-center gap-2 rounded-2xl bg-indigo-600 px-6 py-4 text-sm font-bold text-white shadow-sm transition hover:bg-indigo-700 hover:shadow-md disabled:cursor-not-allowed disabled:bg-gray-200 disabled:text-gray-400"
          >
            <Sparkles size={19} />
            Analyze My Resume
          </button>

          <p className="mt-4 text-center text-xs text-gray-400">
            Your resume will be analyzed against job-market skill requirements.
          </p>
        </motion.section>

        {/* What happens next */}

        <section className="mx-auto mt-8 max-w-4xl">
          <div className="rounded-3xl border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
            <div className="text-center">
              <p className="text-sm font-semibold text-indigo-600">
                What happens next?
              </p>

              <h2 className="mt-2 text-2xl font-bold text-gray-900">
                From resume to career intelligence
              </h2>
            </div>

            <div className="mt-8 grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl bg-gray-50 p-5 text-center">
                <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                  <Search size={20} />
                </div>

                <h3 className="mt-4 font-bold text-gray-900">
                  Extract Skills
                </h3>

                <p className="mt-2 text-xs leading-5 text-gray-500">
                  AI identifies skills and knowledge from your resume.
                </p>
              </div>

              <div className="rounded-2xl bg-gray-50 p-5 text-center">
                <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                  <Target size={20} />
                </div>

                <h3 className="mt-4 font-bold text-gray-900">
                  Find Skill Gaps
                </h3>

                <p className="mt-2 text-xs leading-5 text-gray-500">
                  Your skills are compared with job-market requirements.
                </p>
              </div>

              <div className="rounded-2xl bg-gray-50 p-5 text-center">
                <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                  <Route size={20} />
                </div>

                <h3 className="mt-4 font-bold text-gray-900">
                  Build Roadmap
                </h3>

                <p className="mt-2 text-xs leading-5 text-gray-500">
                  Get personalized career opportunities and learning direction.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Trust line */}

        <div className="mt-8 flex items-center justify-center gap-2 pb-8 text-xs text-gray-400">
          <Sparkles size={14} />
          AI-powered career intelligence
        </div>
      </div>
    </main>
  );
}

export default Analyze;