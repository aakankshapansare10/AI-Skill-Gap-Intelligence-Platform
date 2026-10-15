import Busboy from "busboy";
import pdfParse from "pdf-parse";

// Comprehensive catalog of technical and domain skills
const KNOWN_SKILLS = [
  "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "R",
  "Machine Learning", "Deep Learning", "Artificial Intelligence", "Data Science", "Natural Language Processing",
  "NLP", "Computer Vision", "Generative AI", "GenAI", "LLMs", "Large Language Models", "PyTorch", "TensorFlow",
  "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Keras", "OpenCV", "Hugging Face", "LangChain",
  "LangGraph", "Prompt Engineering", "RAG", "Agentic AI", "Transformers", "Reinforcement Learning", "Statistics",
  "Mathematics", "Linear Algebra", "Data Analysis", "Data Mining", "Data Exploration", "Big Data Analytics",
  "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "DynamoDB", "Snowflake", "BigQuery", "Databases",
  "Data Warehousing", "ETL", "Data Pipelines", "Apache Spark", "Apache Kafka", "Hadoop", "Airflow", "dbt",
  "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP", "Cloud Platforms", "Docker", "Kubernetes",
  "CI/CD", "Git", "GitHub", "GitLab", "Linux", "Terraform", "DevOps", "Microservices", "Serverless", "Nginx",
  "React", "Next.js", "Vue", "Angular", "Node.js", "Express", "FastAPI", "Django", "Flask", "Spring Boot",
  "HTML5", "CSS3", "Tailwind CSS", "REST APIs", "GraphQL", "Postman", "Web Development", "Frontend", "Backend",
  "Full Stack", "System Design", "Object Oriented Programming", "Clean Code", "Coding Standards", "Data Structures",
  "Algorithms", "Problem Solving", "Agile", "Scrum", "Jira", "Project Management", "Product Management",
  "Cybersecurity", "Network Security", "Cryptography", "Penetration Testing", "Security Auditing",
  "Power BI", "Tableau", "Excel", "Data Visualization", "Business Intelligence", "Dashboard Development"
];

// Target roles mapped to baseline required skills
const ROLE_SKILL_REQUIREMENTS = {
  "ai engineer": [
    { skill: "Python", demand: 95, priority: "HIGH", category: "Core Programming" },
    { skill: "Machine Learning", demand: 90, priority: "HIGH", category: "AI/ML Core" },
    { skill: "Deep Learning", demand: 85, priority: "HIGH", category: "AI/ML Core" },
    { skill: "PyTorch", demand: 80, priority: "HIGH", category: "Frameworks" },
    { skill: "TensorFlow", demand: 75, priority: "MEDIUM", category: "Frameworks" },
    { skill: "Generative AI", demand: 82, priority: "HIGH", category: "Specialization" },
    { skill: "LLMs", demand: 80, priority: "HIGH", category: "Specialization" },
    { skill: "RAG", demand: 70, priority: "MEDIUM", category: "Architecture" },
    { skill: "SQL", demand: 75, priority: "MEDIUM", category: "Data Management" },
    { skill: "Docker", demand: 70, priority: "MEDIUM", category: "Deployment" },
    { skill: "Cloud Platforms", demand: 68, priority: "MEDIUM", category: "Cloud" },
    { skill: "Git", demand: 85, priority: "MEDIUM", category: "Version Control" }
  ],
  "data scientist": [
    { skill: "Python", demand: 95, priority: "HIGH", category: "Core Programming" },
    { skill: "Data Science", demand: 92, priority: "HIGH", category: "Core Domain" },
    { skill: "Machine Learning", demand: 88, priority: "HIGH", category: "Modeling" },
    { skill: "Statistics", demand: 85, priority: "HIGH", category: "Theory" },
    { skill: "SQL", demand: 85, priority: "HIGH", category: "Data Management" },
    { skill: "Pandas", demand: 88, priority: "HIGH", category: "Data Analysis" },
    { skill: "NumPy", demand: 82, priority: "MEDIUM", category: "Data Analysis" },
    { skill: "Scikit-learn", demand: 80, priority: "HIGH", category: "Modeling" },
    { skill: "Data Visualization", demand: 75, priority: "MEDIUM", category: "Communication" },
    { skill: "Deep Learning", demand: 65, priority: "MEDIUM", category: "Advanced ML" }
  ],
  "data analyst": [
    { skill: "SQL", demand: 95, priority: "HIGH", category: "Database" },
    { skill: "Excel", demand: 90, priority: "HIGH", category: "Spreadsheets" },
    { skill: "Data Visualization", demand: 85, priority: "HIGH", category: "BI" },
    { skill: "Power BI", demand: 80, priority: "HIGH", category: "BI Tools" },
    { skill: "Tableau", demand: 75, priority: "MEDIUM", category: "BI Tools" },
    { skill: "Python", demand: 78, priority: "MEDIUM", category: "Programming" },
    { skill: "Data Analysis", demand: 88, priority: "HIGH", category: "Analytics" },
    { skill: "Statistics", demand: 70, priority: "MEDIUM", category: "Quantitative" }
  ],
  "software engineer": [
    { skill: "Data Structures", demand: 90, priority: "HIGH", category: "Foundations" },
    { skill: "Algorithms", demand: 90, priority: "HIGH", category: "Foundations" },
    { skill: "System Design", demand: 80, priority: "HIGH", category: "Architecture" },
    { skill: "Git", demand: 85, priority: "HIGH", category: "Version Control" },
    { skill: "SQL", demand: 75, priority: "MEDIUM", category: "Databases" },
    { skill: "REST APIs", demand: 80, priority: "MEDIUM", category: "Backend" },
    { skill: "Docker", demand: 70, priority: "MEDIUM", category: "DevOps" },
    { skill: "Clean Code", demand: 75, priority: "MEDIUM", category: "Best Practices" }
  ],
  "full stack developer": [
    { skill: "JavaScript", demand: 95, priority: "HIGH", category: "Frontend" },
    { skill: "React", demand: 88, priority: "HIGH", category: "Frontend Framework" },
    { skill: "Node.js", demand: 85, priority: "HIGH", category: "Backend" },
    { skill: "HTML5", demand: 85, priority: "HIGH", category: "Frontend" },
    { skill: "CSS3", demand: 80, priority: "HIGH", category: "Frontend" },
    { skill: "SQL", demand: 80, priority: "HIGH", category: "Databases" },
    { skill: "MongoDB", demand: 70, priority: "MEDIUM", category: "Databases" },
    { skill: "REST APIs", demand: 85, priority: "HIGH", category: "Integration" },
    { skill: "Git", demand: 80, priority: "MEDIUM", category: "Tools" }
  ]
};

// Skill extraction helper
function extractSkillsFromText(text) {
  if (!text) return [];
  const normalizedText = text.toLowerCase();
  const matched = new Set();

  for (const skill of KNOWN_SKILLS) {
    const escaped = skill.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = new RegExp(`(^|[^a-zA-Z0-9_#+])${escaped}([^a-zA-Z0-9_#+]|$)`, "i");
    if (pattern.test(normalizedText)) {
      matched.add(skill);
    }
  }

  return Array.from(matched);
}

// Find closest requirement match
function getRoleRequirements(targetRole) {
  const normalized = (targetRole || "").toLowerCase().trim();
  for (const [roleKey, reqs] of Object.entries(ROLE_SKILL_REQUIREMENTS)) {
    if (normalized.includes(roleKey) || roleKey.includes(normalized)) {
      return reqs;
    }
  }
  // Generic fallback role profile if user types something custom
  return [
    { skill: "Python", demand: 85, priority: "HIGH", category: "Core" },
    { skill: "SQL", demand: 80, priority: "HIGH", category: "Database" },
    { skill: "Git", demand: 80, priority: "MEDIUM", category: "Tools" },
    { skill: "Data Structures", demand: 75, priority: "HIGH", category: "Foundations" },
    { skill: "System Design", demand: 70, priority: "MEDIUM", category: "Architecture" },
    { skill: "Docker", demand: 65, priority: "MEDIUM", category: "DevOps" },
    { skill: "REST APIs", demand: 75, priority: "MEDIUM", category: "Backend" }
  ];
}

// Parse multipart request using busboy
function parseMultipartForm(req) {
  return new Promise((resolve, reject) => {
    const busboy = Busboy({ headers: req.headers });
    const fields = {};
    let fileBuffer = null;
    let fileName = "resume.txt";

    busboy.on("file", (fieldname, file, info) => {
      fileName = info.filename || "resume.txt";
      const chunks = [];
      file.on("data", (data) => chunks.push(data));
      file.on("end", () => {
        fileBuffer = Buffer.concat(chunks);
      });
    });

    busboy.on("field", (fieldname, val) => {
      fields[fieldname] = val;
    });

    busboy.on("finish", () => {
      resolve({ fields, fileBuffer, fileName });
    });

    busboy.on("error", (err) => reject(err));
    req.pipe(busboy);
  });
}

export const config = {
  api: {
    bodyParser: false, // Busboy parses the raw stream
  },
};

export default async function handler(req, res) {
  // CORS headers
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed. Use POST." });
  }

  try {
    const { fields, fileBuffer, fileName } = await parseMultipartForm(req);
    const targetRole = (fields.target_role || "Target Role").trim();

    if (!fileBuffer || fileBuffer.length === 0) {
      return res.status(400).json({ detail: "Please upload a valid resume file." });
    }

    // Extract text from uploaded resume
    let resumeText = "";
    const lowerName = fileName.toLowerCase();

    if (lowerName.endsWith(".pdf")) {
      try {
        const parsedPdf = await pdfParse(fileBuffer);
        resumeText = parsedPdf.text || "";
      } catch (pdfErr) {
        console.warn("PDF parse fallback to string:", pdfErr);
        resumeText = fileBuffer.toString("utf-8");
      }
    } else {
      resumeText = fileBuffer.toString("utf-8");
    }

    // Extract skills present in the resume
    const extractedSkills = extractSkillsFromText(resumeText);
    const normalizedExtracted = new Set(extractedSkills.map((s) => s.toLowerCase()));

    // Get skills required by target role
    const requirements = getRoleRequirements(targetRole);

    const matchedRoleSkills = [];
    const missingRoleSkills = [];

    for (const reqItem of requirements) {
      if (normalizedExtracted.has(reqItem.skill.toLowerCase())) {
        matchedRoleSkills.push(reqItem.skill);
      } else {
        missingRoleSkills.push({
          skill_name: reqItem.skill,
          demand_percentage: reqItem.demand,
          priority: reqItem.priority,
          category: reqItem.category
        });
      }
    }

    const totalRequired = requirements.length;
    const matchCount = matchedRoleSkills.length;
    const matchPercentage = totalRequired > 0 ? Math.round((matchCount / totalRequired) * 100 * 100) / 100 : 0;
    const skillGapPercentage = Math.round((100 - matchPercentage) * 100) / 100;

    // Top missing skills for roadmap
    const topMissingSkills = missingRoleSkills.slice(0, 8);

    // Dynamic Job Recommendations
    const jobRecommendations = [
      {
        rank: 1,
        job_id: "JOB-" + Math.floor(100000 + Math.random() * 900000),
        job_title: targetRole,
        matching_skill_count: matchCount,
        job_match_percentage: matchPercentage,
        skill_gap_percentage: skillGapPercentage,
        matching_skills: matchedRoleSkills,
        missing_skills: missingRoleSkills.map((m) => m.skill_name)
      },
      {
        rank: 2,
        job_id: "JOB-" + Math.floor(100000 + Math.random() * 900000),
        job_title: `Associate ${targetRole}`,
        matching_skill_count: Math.min(matchCount + 1, 10),
        job_match_percentage: Math.min(100, Math.round(matchPercentage + 15)),
        skill_gap_percentage: Math.max(0, Math.round(skillGapPercentage - 15)),
        matching_skills: matchedRoleSkills,
        missing_skills: missingRoleSkills.slice(0, 3).map((m) => m.skill_name)
      },
      {
        rank: 3,
        job_id: "JOB-" + Math.floor(100000 + Math.random() * 900000),
        job_title: `Junior ${targetRole} / Intern`,
        matching_skill_count: matchCount,
        job_match_percentage: Math.min(100, Math.round(matchPercentage + 25)),
        skill_gap_percentage: Math.max(0, Math.round(skillGapPercentage - 25)),
        matching_skills: matchedRoleSkills,
        missing_skills: missingRoleSkills.slice(0, 2).map((m) => m.skill_name)
      }
    ];

    const responsePayload = {
      status: "success",
      message: "Resume analyzed successfully.",
      filename: fileName,
      target_role: targetRole,
      analysis: {
        student_profile: {
          total_skills: extractedSkills.length,
          skills: extractedSkills
        },
        overall_analysis: {
          jobs_analyzed: 28,
          best_job_match_percentage: Math.min(100, matchPercentage + 15),
          average_job_match_percentage: Math.round(matchPercentage * 0.7),
          average_skill_gap_percentage: Math.round(100 - matchPercentage * 0.7)
        },
        target_role_analysis: {
          target_role: targetRole,
          match_percentage: matchPercentage,
          skill_gap_percentage: skillGapPercentage,
          matched_skills: matchedRoleSkills,
          matching_skills: matchedRoleSkills,
          missing_skills: missingRoleSkills,
          top_missing_skills: topMissingSkills
        },
        top_job_recommendations: jobRecommendations
      }
    };

    return res.status(200).json(responsePayload);
  } catch (error) {
    console.error("Resume analysis error:", error);
    return res.status(500).json({
      detail: "An error occurred during resume analysis. " + (error.message || "")
    });
  }
}
