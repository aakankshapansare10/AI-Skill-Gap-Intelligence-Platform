import { Link } from "react-router-dom";
import { ArrowRight, Brain, Target, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";

function Home() {
  return (
    <main>

      {/* HERO SECTION */}
      <section className="relative overflow-hidden">
        <div className="mx-auto grid max-w-7xl items-center gap-16 px-6 py-24 md:grid-cols-2 lg:py-32">

          {/* Left */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700">
              <Brain size={16} />
              AI-Powered Career Intelligence
            </div>

            <h1 className="max-w-3xl text-5xl font-bold leading-tight tracking-tight text-gray-900 md:text-6xl">
              Turn Your Resume Into Your{" "}
              <span className="text-indigo-600">
                Career Roadmap.
              </span>
            </h1>

            <p className="mt-6 max-w-xl text-lg leading-8 text-gray-600">
              Discover the skills you already have, identify the skills
              you're missing, and understand exactly what you need to
              reach your target career.
            </p>

            <div className="mt-8 flex flex-col gap-4 sm:flex-row">

              <Link
                to="/analyze"
                className="group inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3.5 font-semibold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700"
              >
                Analyze My Resume
                <ArrowRight
                  size={18}
                  className="transition group-hover:translate-x-1"
                />
              </Link>

              <a
                href="#how-it-works"
                className="inline-flex items-center justify-center rounded-xl border border-gray-200 bg-white px-6 py-3.5 font-semibold text-gray-700 transition hover:border-indigo-200 hover:text-indigo-600"
              >
                How It Works
              </a>

            </div>
          </motion.div>

          {/* Right visual */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="relative mx-auto max-w-md">

              <div className="absolute -right-6 -top-6 h-32 w-32 rounded-full bg-purple-200/50 blur-3xl" />

              <div className="absolute -bottom-10 -left-10 h-40 w-40 rounded-full bg-indigo-200/50 blur-3xl" />

              <div className="relative rounded-3xl border border-gray-100 bg-white p-7 shadow-2xl shadow-indigo-100">

                <div className="mb-6 flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">
                      Career Match
                    </p>

                    <p className="mt-1 text-4xl font-bold text-gray-900">
                      87%
                    </p>
                  </div>

                  <div className="flex h-16 w-16 items-center justify-center rounded-full border-8 border-indigo-100 text-sm font-bold text-indigo-600">
                    87
                  </div>
                </div>

                <div className="space-y-4">

                  <div>
                    <div className="mb-2 flex justify-between text-sm">
                      <span className="font-medium">Python</span>
                      <span className="text-green-600">Strong</span>
                    </div>

                    <div className="h-2 rounded-full bg-gray-100">
                      <div className="h-2 w-[92%] rounded-full bg-indigo-600" />
                    </div>
                  </div>

                  <div>
                    <div className="mb-2 flex justify-between text-sm">
                      <span className="font-medium">SQL</span>
                      <span className="text-green-600">Strong</span>
                    </div>

                    <div className="h-2 rounded-full bg-gray-100">
                      <div className="h-2 w-[84%] rounded-full bg-indigo-600" />
                    </div>
                  </div>

                  <div>
                    <div className="mb-2 flex justify-between text-sm">
                      <span className="font-medium">Machine Learning</span>
                      <span className="text-orange-500">Develop</span>
                    </div>

                    <div className="h-2 rounded-full bg-gray-100">
                      <div className="h-2 w-[58%] rounded-full bg-purple-500" />
                    </div>
                  </div>

                </div>

                <div className="mt-7 rounded-2xl bg-indigo-50 p-4">
                  <p className="text-sm font-semibold text-indigo-900">
                    Next Skill to Develop
                  </p>

                  <p className="mt-1 text-sm text-indigo-700">
                    Advanced Machine Learning
                  </p>
                </div>

              </div>
            </div>
          </motion.div>

        </div>
      </section>

      {/* CAREER DNA SECTION */}
      <section className="bg-[#F7F8FC] py-24">
        <div className="mx-auto grid max-w-7xl items-center gap-16 px-6 md:grid-cols-2">

          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
              Your Career DNA
            </p>

            <h2 className="mt-4 text-3xl font-bold leading-tight text-gray-900 md:text-4xl">
              See where your skills{" "}
              <span className="text-indigo-600">
                connect to your career.
              </span>
            </h2>

            <p className="mt-5 max-w-xl text-lg leading-8 text-gray-600">
              CareerGenome builds a personalized view of your skills,
              compares them with your target role, and highlights the
              areas that can make the biggest difference.
            </p>

            <div className="mt-8 space-y-5">

              <DNAItem
                title="Skills You Have"
                description="Skills already present in your resume."
                icon="✓"
              />

              <DNAItem
                title="Skills to Develop"
                description="Important skills missing for your target role."
                icon="!"
              />

              <DNAItem
                title="Career Opportunities"
                description="Roles that align with your current skill profile."
                icon="→"
              />

            </div>
          </motion.div>

          {/* Career DNA Visual */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className="relative"
          >
            <div className="relative mx-auto max-w-lg rounded-3xl border border-gray-100 bg-white p-7 shadow-xl">

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">
                    Your Skill Profile
                  </p>

                  <h3 className="mt-1 text-xl font-bold text-gray-900">
                    Data Scientist
                  </h3>
                </div>

                <div className="rounded-full bg-indigo-50 px-4 py-2 text-sm font-bold text-indigo-600">
                  87% Match
                </div>
              </div>

              {/* Skill Connections */}
              <div className="relative mt-10 h-72">

                {/* Center */}
                <div className="absolute left-1/2 top-1/2 z-10 flex h-28 w-28 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-indigo-600 text-center text-sm font-bold text-white shadow-xl shadow-indigo-200">
                  Career
                  <br />
                  Goal
                </div>

                {/* Lines */}
                <div className="absolute left-1/2 top-1/2 h-px w-40 -translate-x-1/2 rotate-[-30deg] bg-indigo-200" />
                <div className="absolute left-1/2 top-1/2 h-px w-40 -translate-x-1/2 rotate-[30deg] bg-indigo-200" />
                <div className="absolute left-1/2 top-1/2 h-px w-40 -translate-x-1/2 rotate-[90deg] bg-indigo-200" />
                <div className="absolute left-1/2 top-1/2 h-px w-40 -translate-x-1/2 rotate-[150deg] bg-purple-200" />

                {/* Skill Nodes */}
                <SkillNode
                  label="Python"
                  position="left-4 top-8"
                  type="strong"
                />

                <SkillNode
                  label="SQL"
                  position="right-4 top-8"
                  type="strong"
                />

                <SkillNode
                  label="Machine Learning"
                  position="left-0 bottom-8"
                  type="develop"
                />

                <SkillNode
                  label="Statistics"
                  position="right-0 bottom-8"
                  type="develop"
                />

              </div>

              <div className="rounded-2xl bg-indigo-50 p-4">
                <p className="text-sm font-semibold text-indigo-900">
                  Recommended Next Step
                </p>

                <p className="mt-1 text-sm text-indigo-700">
                  Strengthen Machine Learning fundamentals
                </p>
              </div>

            </div>
          </motion.div>

        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-6">

          <div className="mx-auto max-w-2xl text-center">
            <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
              How It Works
            </p>

            <h2 className="mt-3 text-3xl font-bold text-gray-900 md:text-4xl">
              From Resume to Career Roadmap
            </h2>

            <p className="mt-4 text-gray-600">
              Our platform analyzes your skills against real job
              requirements to show you where you stand.
            </p>
          </div>

          <div className="mt-16 grid gap-8 md:grid-cols-3">

            <FeatureCard
              icon={<Brain size={24} />}
              number="01"
              title="Understand Your Skills"
              description="Upload your resume and let our AI identify your existing technical and professional skills."
            />

            <FeatureCard
              icon={<Target size={24} />}
              number="02"
              title="Find Your Skill Gaps"
              description="Compare your current skill profile with the requirements of your target career."
            />

            <FeatureCard
              icon={<TrendingUp size={24} />}
              number="03"
              title="Build Your Roadmap"
              description="Get personalized recommendations for the skills you should develop next."
            />

          </div>
        </div>
      </section>

    </main>
  );
}

function FeatureCard({ icon, number, title, description }) {
  return (
    <motion.div
      whileHover={{ y: -6 }}
      className="rounded-2xl border border-gray-100 bg-[#F7F8FC] p-7 transition-shadow hover:shadow-xl"
    >
      <div className="flex items-center justify-between">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600">
          {icon}
        </div>

        <span className="text-sm font-bold text-gray-300">
          {number}
        </span>
      </div>

      <h3 className="mt-6 text-xl font-bold text-gray-900">
        {title}
      </h3>

      <p className="mt-3 leading-7 text-gray-600">
        {description}
      </p>
    </motion.div>
  );
}
function DNAItem({ title, description, icon }) {
  return (
    <div className="flex gap-4">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-100 font-bold text-indigo-600">
        {icon}
      </div>

      <div>
        <h3 className="font-semibold text-gray-900">
          {title}
        </h3>

        <p className="mt-1 text-sm leading-6 text-gray-500">
          {description}
        </p>
      </div>
    </div>
  );
}

function SkillNode({ label, position, type }) {
  const isStrong = type === "strong";

  return (
    <div
      className={`absolute ${position} rounded-xl border bg-white px-4 py-3 shadow-md ${
        isStrong
          ? "border-indigo-100"
          : "border-purple-100"
      }`}
    >
      <div className="flex items-center gap-2">
        <span
          className={`h-2.5 w-2.5 rounded-full ${
            isStrong ? "bg-indigo-500" : "bg-purple-500"
          }`}
        />

        <span className="text-xs font-semibold text-gray-700">
          {label}
        </span>
      </div>
    </div>
  );
}

export default Home;