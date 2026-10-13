# AI Skill Gap Intelligence Platform

An AI-powered platform that helps students understand the gap between their existing skills and the skills required for different job roles. The system aims to analyze resume skills, identify missing skills, and provide personalized recommendations to support career development.

## 📌 Project Overview

Students often find it difficult to understand which technical and professional skills they need to develop for their desired careers. This project aims to bridge that gap using Natural Language Processing (NLP), Machine Learning (ML), and data analysis.

The platform is designed to extract skills from a student's resume, compare them with job-related skills, identify missing skills, and generate recommendations for improvement.

## 🎯 Objectives

* Analyze job-market data to identify relevant skills.
* Extract skills from resumes using NLP.
* Use machine learning to predict skills associated with job roles.
* Identify matching and missing skills.
* Calculate the skill-gap percentage.
* Generate personalized skill-development recommendations.
* Present the results in an understandable report or dashboard.

## ✨ Key Features

* Resume upload and skill extraction.
* Job-role-based skill prediction.
* Matching and missing skill identification.
* Skill-gap percentage calculation.
* Personalized learning recommendations.
* Student skill-gap report.
* Job-market skill analysis.

*Note: These features describe the intended integrated platform. Their availability depends on the final integration of the NLP, ML, backend, database, and frontend modules.*

## 🛠️ Technologies Used

* **Python** — Core programming language.
* **Pandas and NumPy** — Data processing and analysis.
* **Scikit-learn** — Machine learning and model evaluation.
* **TF-IDF** — Text feature extraction for job titles.
* **NLP** — Resume and skill text processing.
* **FastAPI** — Backend API development.
* **PostgreSQL** — Database management.
* **React and web technologies** — Frontend development.
* **Git and GitHub** — Version control and collaboration.

## ⚙️ System Workflow

1. Collect job-market data.
2. Clean and preprocess the dataset.
3. Extract and normalize job-related skills.
4. Convert job-title text into numerical features using TF-IDF.
5. Train and evaluate the machine-learning model.
6. Predict relevant skills for different job roles.
7. Extract the student's skills from the uploaded resume.
8. Compare student skills with job requirements.
9. Identify matching and missing skills.
10. Calculate the skill-gap percentage.
11. Generate personalized skill-development recommendations.
12. Display the results through the dashboard and student report.

## 📊 Machine Learning Module

The ML module is responsible for predicting job-related skills and identifying skill gaps.

### Major Components

* **Feature Engineering:** Converts job-title text into numerical TF-IDF features.
* **Train-Test Split:** Divides the dataset into training and testing sets.
* **Model Training:** Uses a One-vs-Rest SGD Classifier for multi-label skill prediction.
* **Model Evaluation:** Evaluates performance using precision, recall, F1-score, and Hamming loss.
* **Skill Prediction:** Selects the top relevant skills for job roles.
* **Skill-Gap Analysis:** Identifies matching and missing skills.
* **Recommendation Engine:** Generates suggestions for developing missing skills.
* **Student Report:** Produces a report containing skill-gap results and recommendations.

### Model Evaluation Results

The current saved model evaluation produced the following results:

| Metric       |   Result |
| ------------ | -------: |
| Precision    |   0.6817 |
| Recall       |   0.0641 |
| F1-score     |   0.1171 |
| Hamming Loss | 0.008580 |

The model demonstrates that the prediction pipeline can be executed, but its low recall indicates that many relevant skills are missed. Improving the model's ability to identify relevant skills is an important area for future work.

## 📁 Project Structure

The following is a simplified view of the ML module and its generated outputs:

```text
AI_Skill_Gap_Intelligence_Platform/
├── data/
│   └── processed/
│       ├── model_evaluation_results.csv
│       ├── model_skill_names.csv
│       ├── recommendations.csv
│       ├── skill_gap_analysis.csv
│       ├── skill_gap_predictions.csv
│       ├── student_skill_gap_report.csv
│       └── student_skill_gap_report.txt
├── notebooks/
│   └── models/
│       ├── 01_skill_features.py
│       ├── 02_feature_engineering.py
│       ├── 03_train_test_split.py
│       ├── 04_ml_model.py
│       ├── 05_model_evaluation.py
│       ├── 06_skill_gap_prediction.py
│       ├── 09_skill_gap_analysis.py
│       ├── 10_recommendation_engine.py
│       └── 11_student_skill_gap_report.py
├── requirements.txt
├── .gitignore
└── README.md
```

*This structure represents the ML contribution. The complete shared repository may contain additional frontend, backend, NLP, and database files.*

## 🚀 Getting Started

### Prerequisites

* Python installed on your system.
* Git installed.
* VS Code or another Python editor.
* Access to the required project dataset and model files.

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/aakankshapansare10/AI-Skill-Gap-Intelligence-Platform.git
```

**2. Open the project directory**

```bash
cd AI-Skill-Gap-Intelligence-Platform
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the virtual environment on Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**5. Install the required dependencies**

```bash
python -m pip install -r requirements.txt
```

Use the scikit-learn version compatible with the saved model. The current saved model was created with scikit-learn 1.8.0.

### Running the ML Module

The ML scripts depend on the required dataset and intermediate files being available.

To generate the student skill-gap report using an existing recommendations file, run:

```bash
python notebooks/models/11_student_skill_gap_report.py
```

The script reads the recommendations data and generates the student skill-gap report.

**Note:** This command tests the report-generation stage, not the entire application. The complete resume-upload workflow requires the integrated frontend, backend, NLP module, and database configuration. Follow the team's final setup instructions to launch the full application.

## 📈 Expected Output

The platform is designed to provide:

* Job titles and associated required skills.
* Student skills extracted from a resume.
* Matching skills between the student and job requirements.
* Missing skills that need improvement.
* Skill-gap percentage for different job roles.
* Personalized recommendations for learning missing skills.
* A student skill-gap report.

## 👥 Team Responsibilities

| Member                           | Main Responsibility                        | What They Handle                                                                                                                                                        |
| -------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Member 1 – Antara Pardeshi**   | 🗄️ Backend & Database                     | Data processing, backend development, database management, API endpoints, and communication between the backend and frontend.                                           |
| **Member 2 – Aakanksha Pansare** | 🧠 NLP & Frontend                          | Natural Language Processing, resume text processing, skill extraction, skill normalization, frontend development, and displaying results on the dashboard.              |
| **Member 3 – Ruhi Gandhi**       | 🤖 Machine Learning / Skill Gap Prediction | Feature engineering, model training and evaluation, skill prediction, skill-gap analysis, identification of matching and missing skills, and recommendation generation. |

## 🔮 Future Enhancements

* Improve recall and overall model performance.
* Support more resume formats and skill variations.
* Expand the dataset with updated job postings.
* Improve the accuracy and relevance of recommendations.
* Add more job domains and career paths.
* Improve the dashboard and user experience.
* Integrate all modules into a complete end-to-end application.

## ⚠️ Limitations

* Prediction quality depends on the dataset and trained model.
* The current model has low recall and needs improvement.
* Resume parsing depends on the NLP module.
* End-to-end functionality depends on successful integration of all project modules.
* Recommendations are based on the available skills and generated outputs.

## 📄 Conclusion

The AI Skill Gap Intelligence Platform aims to help students understand the skills required for different job roles and identify areas for improvement. By combining Natural Language Processing, Machine Learning, data analysis, and recommendation techniques, the project provides a foundation for personalized skill-gap analysis and career planning.

## 📚 References

* Python Documentation — https://docs.python.org/3/
* Pandas Documentation — https://pandas.pydata.org/docs/
* Scikit-learn Documentation — https://scikit-learn.org/stable/
* FastAPI Documentation — https://fastapi.tiangolo.com/
* PostgreSQL Documentation — https://www.postgresql.org/docs/
* React Documentation — https://react.dev/
* GitHub Documentation — https://docs.github.com/
