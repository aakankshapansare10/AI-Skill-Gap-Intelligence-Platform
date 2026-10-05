const API_URL = "http://127.0.0.1:8000";

function startAnalysis() {
    const analysisSection = document.getElementById("analysis");

    if (analysisSection) {
        analysisSection.scrollIntoView({
            behavior: "smooth"
        });
    }
}


async function loadSkillGap() {

    const skillsInput = document.getElementById("skillsInput");
    const loading = document.getElementById("loading");
    const results = document.getElementById("results");

    if (!skillsInput) {
        console.error("skillsInput element not found.");
        return;
    }

    const inputValue = skillsInput.value.trim();

    if (!inputValue) {

        results.innerHTML = `
            <div class="error-message">
                Please enter at least one skill.
            </div>
        `;

        return;
    }


    // Convert input into a list of skills
    const skills = inputValue
        .split(",")
        .map(skill => skill.trim())
        .filter(skill => skill.length > 0);


    console.log("Skills entered by user:", skills);


    // Show loading message
    loading.style.display = "block";

    results.innerHTML = "";


    try {

        const response = await fetch(
            `${API_URL}/skill-gap/analyze`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },

                body: JSON.stringify({
                    skills: skills
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server returned HTTP ${response.status}`
            );

        }


        const data = await response.json();


        console.log(
            "Backend response:",
            data
        );


        if (data.status !== "success") {

            throw new Error(
                data.message ||
                "Backend returned an error."
            );

        }


        // Display results
        displaySkillGapResults(
            data,
            skills
        );


    } catch (error) {

        console.error(
            "Skill gap analysis error:",
            error
        );


        results.innerHTML = `
            <div class="error-message">

                <h3>Connection Error</h3>

                <p>
                    Could not connect to the FastAPI backend.
                </p>

                <p>
                    Make sure your backend is running on:
                </p>

                <strong>
                    http://192.168.31.96:8000
                </strong>

                <p>
                    Error: ${escapeHtml(error.message)}
                </p>

            </div>
        `;

    } finally {

        // Hide loading message
        loading.style.display = "none";

    }
}


function displaySkillGapResults(
    data,
    studentSkills
) {

    const results =
        document.getElementById("results");


    const skillGaps =
        data.skill_gaps || [];


    if (skillGaps.length === 0) {

        results.innerHTML = `
            <div class="no-results">

                <h3>
                    No results found
                </h3>

                <p>
                    No job recommendations were returned
                    by the backend.
                </p>

            </div>
        `;

        return;
    }


    let html = `

        <div class="results-header">

            <h2>
                Skill Gap Results
            </h2>

            <p>
                Your skills were compared with
                real-world job requirements.
            </p>


            <div class="student-skills">

                <h3>
                    Your Skills
                </h3>


                <div class="skill-tags">
    `;


    // Display student's skills
    studentSkills.forEach(
        skill => {

            html += `
                <span class="skill-tag">
                    ${escapeHtml(skill)}
                </span>
            `;

        }
    );


    html += `

                </div>

            </div>


            <div class="job-count">

                <strong>
                    ${skillGaps.length}
                </strong>

                job recommendations analyzed.

            </div>

        </div>

    `;


    // Display each job
    skillGaps.forEach(
        (job, index) => {


            const requiredSkills =
                convertToArray(
                    job.required_skills
                );


            const matchingSkills =
                convertToArray(
                    job.matching_skills
                );


            const missingSkills =
                convertToArray(
                    job.missing_skills
                );


            const gapPercentage =
                Number(
                    job.skill_gap_percentage || 0
                );


            const totalRequired =
                job.total_required_skills ??
                requiredSkills.length;


            const totalMatching =
                job.total_matching_skills ??
                matchingSkills.length;


            const totalMissing =
                job.total_missing_skills ??
                missingSkills.length;


            html += `

                <div class="job-card">


                    <h3 class="job-title">

                        ${index + 1}.
                        ${escapeHtml(job.job_title)}

                    </h3>


                    <div class="gap-badge">

                        Skill Gap:

                        <strong>
                            ${gapPercentage}%
                        </strong>

                    </div>


                    <div class="skill-section">

                        <h4>
                            Required Skills
                        </h4>

                        <p>

                            ${
                                requiredSkills.length > 0
                                ? escapeHtml(
                                    requiredSkills.join(", ")
                                  )
                                : "None"
                            }

                        </p>

                    </div>


                    <div class="skill-section matching-section">

                        <h4>
                            Matching Skills
                        </h4>

                        <p class="matching-skills">

                            ${
                                matchingSkills.length > 0
                                ? escapeHtml(
                                    matchingSkills.join(", ")
                                  )
                                : "None"
                            }

                        </p>

                    </div>


                    <div class="skill-section missing-section">

                        <h4>
                            Missing Skills
                        </h4>

                        <p class="missing-skills">

                            ${
                                missingSkills.length > 0
                                ? escapeHtml(
                                    missingSkills.join(", ")
                                  )
                                : "None"
                            }

                        </p>

                    </div>


                    <div class="job-summary">


                        <div>

                            <strong>
                                ${totalRequired}
                            </strong>

                            Required

                        </div>


                        <div>

                            <strong>
                                ${totalMatching}
                            </strong>

                            Matching

                        </div>


                        <div>

                            <strong>
                                ${totalMissing}
                            </strong>

                            Missing

                        </div>


                    </div>


                </div>

            `;

        }
    );


    results.innerHTML = html;


    // Scroll to results
    results.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


function convertToArray(value) {

    if (Array.isArray(value)) {

        return value
            .map(item => String(item).trim())
            .filter(
                item => item.length > 0
            );

    }


    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return [];

    }


    return String(value)
        .split(",")
        .map(item => item.trim())
        .filter(
            item => item.length > 0
        );

}


function escapeHtml(value) {

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "AI Skill Gap Intelligence Platform loaded."
        );

        console.log(
            "Backend API:",
            API_URL
        );

    }
);