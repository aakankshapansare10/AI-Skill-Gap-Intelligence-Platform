import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { motion } from "framer-motion";
import {
  Upload,
  FileText,
  X,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  LoaderCircle,
} from "lucide-react";

function Analyze() {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [targetRole, setTargetRole] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFile = (file) => {
    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "text/plain",
    ];

    const fileExtension = file.name
      .split(".")
      .pop()
      .toLowerCase();

    if (!allowedTypes.includes(file.type) && !["pdf", "txt"].includes(fileExtension)) {
      setErrorMessage("Please upload a PDF or TXT resume.");
      return;
    }

    setErrorMessage("");
    setSelectedFile(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    const file = event.dataTransfer.files[0];

    handleFile(file);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    handleFile(file);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setErrorMessage("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleAnalyze = async () => {
    setErrorMessage("");

    if (!selectedFile) {
      setErrorMessage("Please upload your resume first.");
      return;
    }

    if (!targetRole.trim()) {
      setErrorMessage("Please enter your target role.");
      return;
    }

    setIsAnalyzing(true);

    try {
      const formData = new FormData();

      formData.append("resume", selectedFile);
      formData.append("target_role", targetRole.trim());

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze-resume",
        formData
      );

      console.log("Backend response:", response.data);

      navigate("/dashboard", {
        state: {
          analysis: response.data.analysis,
          targetRole: response.data.target_role,
          filename: response.data.filename,
        },
      });

    } catch (error) {
      console.error("Resume analysis error:", error);

      let message = "Something went wrong while analyzing your resume.";

      if (error.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error.message) {
        message = error.message;
      }

      setErrorMessage(message);
      setIsAnalyzing(false);

      return;
    }

    setIsAnalyzing(false);
  };

  return (
    <main className="min-h-[85vh] px-6 py-16 md:py-20">
      <div className="mx-auto max-w-4xl">

        {/* HEADER */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <div className="mx-auto flex w-fit items-center gap-2 rounded-full bg-indigo-50 px-4 py-2 text-sm font-semibold text-indigo-700">
            <Sparkles size={16} />
            AI Resume Analysis
          </div>

          <h1 className="mt-5 text-4xl font-bold tracking-tight text-gray-900 md:text-5xl">
            Discover Your{" "}
            <span className="text-indigo-600">Career DNA</span>
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-gray-600">
            Upload your resume and tell us where you want to go.
            We'll help you understand your current skills and identify
            the gaps between you and your target career.
          </p>
        </motion.div>

        {/* MAIN CARD */}
        <motion.div
          initial={{ opacity: 0, y: 35 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.15 }}
          className="mt-12 rounded-3xl border border-gray-100 bg-white p-6 shadow-xl shadow-gray-200/50 md:p-10"
        >

          {/* STEP 1 */}
          <div>

            <div className="mb-4 flex items-center gap-3">

              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-600 text-sm font-bold text-white">
                1
              </div>

              <div>
                <h2 className="font-bold text-gray-900">
                  Upload your resume
                </h2>

                <p className="text-sm text-gray-500">
                  We'll extract your skills automatically
                </p>
              </div>

            </div>

            {!selectedFile ? (

              <div
                onDragOver={(event) => event.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className="group cursor-pointer rounded-2xl border-2 border-dashed border-gray-200 bg-[#F7F8FC] p-10 text-center transition-all duration-300 hover:border-indigo-400 hover:bg-indigo-50/30 md:p-14"
              >

                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.txt"
                  onChange={handleFileChange}
                  className="hidden"
                />

                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-100 text-indigo-600"
                >
                  <Upload size={28} />
                </motion.div>

                <h3 className="mt-5 text-lg font-bold text-gray-900">
                  Drop your resume here
                </h3>

                <p className="mt-2 text-sm text-gray-500">
                  or{" "}
                  <span className="font-semibold text-indigo-600">
                    browse files
                  </span>
                </p>

                <p className="mt-4 text-xs text-gray-400">
                  Supported formats: PDF, TXT
                </p>

              </div>

            ) : (

              <div className="rounded-2xl border border-green-200 bg-green-50 p-5">

                <div className="flex items-center justify-between gap-4">

                  <div className="flex min-w-0 items-center gap-4">

                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm">
                      <FileText size={23} />
                    </div>

                    <div className="min-w-0">

                      <p className="truncate font-semibold text-gray-900">
                        {selectedFile.name}
                      </p>

                      <p className="mt-1 text-sm text-gray-500">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>

                    </div>

                  </div>

                  <div className="flex items-center gap-3">

                    <CheckCircle2
                      size={22}
                      className="text-green-600"
                    />

                    <button
                      type="button"
                      onClick={removeFile}
                      className="rounded-lg p-2 text-gray-400 transition hover:bg-white hover:text-red-500"
                    >
                      <X size={20} />
                    </button>

                  </div>

                </div>

              </div>

            )}

          </div>

          {/* DIVIDER */}

          <div className="my-10 h-px bg-gray-100" />

          {/* STEP 2 */}

          <div>

            <div className="mb-4 flex items-center gap-3">

              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-600 text-sm font-bold text-white">
                2
              </div>

              <div>
                <h2 className="font-bold text-gray-900">
                  Choose your target role
                </h2>

                <p className="text-sm text-gray-500">
                  Tell us which career you're aiming for
                </p>
              </div>

            </div>

            <label className="mb-2 block text-sm font-semibold text-gray-700">
              Target Role
            </label>

            <input
              type="text"
              value={targetRole}
              onChange={(event) => setTargetRole(event.target.value)}
              placeholder="e.g. Data Scientist"
              className="w-full rounded-xl border border-gray-200 bg-[#F7F8FC] px-4 py-3.5 text-gray-900 outline-none transition focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-100"
            />

            <div className="mt-3 flex flex-wrap gap-2">

              {[
                "Data Scientist",
                "Data Analyst",
                "ML Engineer",
                "Software Engineer",
              ].map((role) => (

                <button
                  key={role}
                  type="button"
                  onClick={() => setTargetRole(role)}
                  className="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-600 transition hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-600"
                >
                  {role}
                </button>

              ))}

            </div>

          </div>

          {/* ERROR */}

          {errorMessage && (

            <div className="mt-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
              {errorMessage}
            </div>

          )}

          {/* ANALYZE BUTTON */}

          <button
            type="button"
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="group mt-10 flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-4 font-semibold text-white shadow-lg shadow-indigo-100 transition hover:bg-indigo-700 hover:shadow-xl disabled:cursor-not-allowed disabled:opacity-80"
          >

            {isAnalyzing ? (

              <>
                <LoaderCircle
                  size={20}
                  className="animate-spin"
                />

                Analyzing Your Resume...
              </>

            ) : (

              <>
                Analyze My Resume

                <ArrowRight
                  size={19}
                  className="transition-transform duration-200 group-hover:translate-x-1"
                />
              </>

            )}

          </button>

          {/* LOADING */}

          {isAnalyzing && (

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 rounded-2xl bg-indigo-50 p-5"
            >

              <div className="flex items-center gap-3">

                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm">
                  <Sparkles size={19} />
                </div>

                <div>

                  <p className="text-sm font-semibold text-indigo-900">
                    AI is analyzing your resume
                  </p>

                  <p className="mt-1 text-xs text-indigo-600">
                    Extracting skills and comparing career requirements...
                  </p>

                </div>

              </div>

              <div className="mt-4 h-2 overflow-hidden rounded-full bg-indigo-100">

                <motion.div
                  initial={{ x: "-100%" }}
                  animate={{ x: "100%" }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="h-full w-1/2 rounded-full bg-indigo-600"
                />

              </div>

            </motion.div>

          )}

          {!isAnalyzing && !errorMessage && (

            <p className="mt-4 text-center text-xs text-gray-400">
              Your resume will be analyzed against relevant job skill
              requirements.
            </p>

          )}

        </motion.div>

        {/* INFO */}

        <div className="mt-8 grid gap-4 text-center sm:grid-cols-3">

          <Info text="AI-powered skill extraction" />

          <Info text="Real-world job comparison" />

          <Info text="Personalized skill roadmap" />

        </div>

      </div>
    </main>
  );
}

function Info({ text }) {
  return (
    <div className="rounded-xl border border-gray-100 bg-white px-4 py-3 text-sm text-gray-600 shadow-sm">
      <span className="mr-2 text-green-500">✓</span>
      {text}
    </div>
  );
}

export default Analyze;