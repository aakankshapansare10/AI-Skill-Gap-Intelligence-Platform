

11_student_skill_gap_report.py
Code

10_recommendation_engine.py
Code

09_skill_gap_analysis.py
Code
in which folders should i add this
Yes — these 3 Python files are part of your AI Skill Gap Intelligence Platform, and based on the code, they should go into your src / scripts area, while their CSV outputs go into data/processed.

The important part is that all three scripts use:

Path(__file__).resolve().parents[2]

So they expect the project root to be two folders above each Python file. 

Recommended folder structure
AI-Skill-Gap-Intelligence-Platform/
│
├── data/
│   ├── raw/
│   │   └── job_postings.csv
│   │
│   └── processed/
│       ├── skill_gap_predictions.csv
│       ├── skill_gap_analysis.csv
│       ├── recommendations.csv
│       ├── student_skill_gap_report.csv
│       └── student_skill_gap_report.txt
│
├── src/
│   └── skill_gap/
│       ├── 09_skill_gap_analysis.py
│       ├── 10_recommendation_engine.py
│       └── 11_student_skill_gap_report.py
│
├── models/
│
├── notebooks/
│
├── app/
│   └── app.py
│
├── requirements.txt
└── README.md
Put your 3 files here
File	Folder
09_skill_gap_analysis.py	src/skill_gap/
10_recommendation_engine.py	src/skill_gap/
11_student_skill_gap_report.py	src/skill_gap/
The sequence is also important:

skill_gap_predictions.csv
        ↓
09_skill_gap_analysis.py
        ↓
skill_gap_analysis.csv
        ↓
10_recommendation_engine.py
        ↓
recommendations.csv
        ↓
11_student_skill_gap_report.py
        ↓
student_skill_gap_report.csv
student_skill_gap_report.txt
That's directly reflected in the scripts: 09 reads skill_gap_predictions.csv and produces skill_gap_analysis.csv; 10 reads that analysis and produces recommendations.csv; 11 reads recommendations.csv and produces the final student report. 
 
 

One important thing: if you put them exactly in src/skill_gap/, parents[2] will point to your project root:

skill_gap/
    ↑ parents[0] = src/skill_gap
    ↑ parents[1] = src
    ↑ parents[2] = project root
So your paths like:

ROOT / "data" / "processed"

will work correctly.

If you show me your current project folders (a screenshot of VS Code Explorer is enough), I can tell you exactly where each existing file should go and what folders/files you still need to create.

RAW JOB DATASET
                               │
                               ↓
┌─────────────────────────────────────────────────┐
│ STEP 1: DATA / SKILL EXTRACTION                 │
│                                                 │
│ Job Dataset                                     │
│      ↓                                          │
│ Normalized Job Skills                           │
│      ↓                                          │
│ Remove duplicates & organize skills             │
└───────────────────────┬─────────────────────────┘
                        ↓
              normalized_job_skills.csv
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 2: FEATURE ENGINEERING                     │
│                                                 │
│ Job Titles                                      │
│      ↓                                          │
│ TF-IDF Vectorization                            │
│      ↓                                          │
│ 3,000 TF-IDF Features                           │
└───────────────────────┬─────────────────────────┘
                        ↓
             title_tfidf_features.npz
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 3: TRAIN / TEST SPLIT                      │
│                                                 │
│ Dataset                                         │
│      ↓                                          │
│ 80% Training Data                               │
│ 20% Testing Data                                │
└───────────────────────┬─────────────────────────┘
                        ↓
       X_train / X_test / Y_train / Y_test
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 4: ML MODEL TRAINING                       │
│                                                 │
│ TF-IDF Features                                 │
│      +                                          │
│ Top 300 Job Skills                              │
│      ↓                                          │
│ One-vs-Rest SGD Classifier                      │
│      ↓                                          │
│ Multi-Label Skill Prediction Model              │
└───────────────────────┬─────────────────────────┘
                        ↓
             skill_prediction_model.pkl
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 5: MODEL EVALUATION                        │
│                                                 │
│ Predictions vs Actual Skills                    │
│      ↓                                          │
│ Precision                                       │
│ Recall                                          │
│ F1 Score                                        │
│ Hamming Loss                                    │
└───────────────────────┬─────────────────────────┘
                        ↓
       Precision = 0.6817
       Recall    = 0.0641
       F1 Score  = 0.1171
       Hamming Loss = 0.008580
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 6: SKILL GAP PREDICTION                    │
│                                                 │
│ Target Job                                      │
│      ↓                                          │
│ Predicted Required Skills                       │
│      +                                          │
│ Student Skills                                  │
│      ↓                                          │
│ Matching Skills                                 │
│ Missing Skills                                  │
│ Skill Gap %                                     │
└───────────────────────┬─────────────────────────┘
                        ↓
            skill_gap_predictions.csv
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 7: RECOMMENDATION ENGINE                   │
│                                                 │
│ Missing Skills                                  │
│      ↓                                          │
│ Skill → Learning Recommendation Mapping         │
│      ↓                                          │
│ Personalized Learning Recommendations           │
└───────────────────────┬─────────────────────────┘
                        ↓
             skill_recommendations.csv
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 8: STUDENT SKILL GAP REPORT                │
│                                                 │
│ Student Skills                                  │
│ Target Job                                      │
│ Missing Skills                                  │
│ Skill Gap %                                     │
│ Recommendations                                 │
│      ↓                                          │
│ Student Skill Gap Report                        │
└───────────────────────┬─────────────────────────┘
                        ↓
        student_skill_gap_report.csv
        student_skill_gap_report.txt
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 9: SKILL GAP ANALYSIS                      │
│                                                 │
│ Analyze required vs student skills              │
│      ↓                                          │
│ Matching Skills                                 │
│ Missing Skills                                  │
│ Total Skills                                    │
│ Skill Gap Percentage                            │
└───────────────────────┬─────────────────────────┘
                        ↓
             skill_gap_analysis.csv
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 10: RECOMMENDATION ENGINE                  │
│                                                 │
│ Missing Skills                                  │
│      ↓                                          │
│ Identify each skill gap                        │
│      ↓                                          │
│ Generate learning recommendation               │
└───────────────────────┬─────────────────────────┘
                        ↓
                recommendations.csv
                        │
                        ↓
┌─────────────────────────────────────────────────┐
│ STEP 11: FINAL STUDENT SKILL GAP REPORT         │
│                                                 │
│ Combine:                                        │
│ • Student Skills                               │
│ • Target Job                                   │
│ • Missing Skills                               │
│ • Number of Missing Skills                     │
│ • Skill Gap %                                  │
│ • Learning Recommendations                     │
└───────────────────────┬─────────────────────────┘
                        ↓
       student_skill_gap_report.csv
       student_skill_gap_report.txt
…
Yes — looking at your full pipeline, I would organize the project slightly differently than my previous answer. Your diagram has 11 steps, so the cleanest structure is to keep each processing stage in src/ and keep all generated CSV/NPZ/PKL files in data/processed/ or models/.

Recommended final project structure
AI-Skill-Gap-Intelligence-Platform/
│
├── data/
│   ├── raw/
│   │   └── job_dataset.csv
│   │
│   └── processed/
│       ├── normalized_job_skills.csv
│       ├── title_tfidf_features.npz
│       ├── skill_gap_predictions.csv
│       ├── skill_gap_analysis.csv
│       ├── skill_recommendations.csv
│       ├── recommendations.csv
│       ├── student_skill_gap_report.csv
│       └── student_skill_gap_report.txt
│
├── models/
│   └── skill_prediction_model.pkl
│
├── src/
│   ├── data_processing/
│   │   └── 01_skill_extraction.py
│   │
│   ├── feature_engineering/
│   │   └── 02_tfidf_features.py
│   │
│   ├── model/
│   │   ├── 03_train_test_split.py
│   │   ├── 04_model_training.py
│   │   └── 05_model_evaluation.py
│   │
│   ├── prediction/
│   │   └── 06_skill_gap_prediction.py
│   │
│   ├── analysis/
│   │   └── 09_skill_gap_analysis.py
│   │
│   ├── recommendations/
│   │   └── 10_recommendation_engine.py
│   │
│   └── reports/
│       └── 11_student_skill_gap_report.py
│
├── app/
│   └── app.py
│
├── notebooks/
│   └── exploration.ipynb
│
├── requirements.txt
│
└── README.md
Where your 3 uploaded files go
1. 09_skill_gap_analysis.py

Put it here:

src/
└── analysis/
    └── 09_skill_gap_analysis.py
It takes:

data/processed/skill_gap_predictions.csv
and creates:

data/processed/skill_gap_analysis.csv
That's exactly what your current code specifies. 

2. 10_recommendation_engine.py

Put it here:

src/
└── recommendations/
    └── 10_recommendation_engine.py
It takes:

data/processed/skill_gap_analysis.csv
and creates:

data/processed/recommendations.csv
Your code already has those paths defined. 

3. 11_student_skill_gap_report.py

Put it here:

src/
└── reports/
    └── 11_student_skill_gap_report.py
It takes:

data/processed/recommendations.csv
and creates:

data/processed/student_skill_gap_report.csv
data/processed/student_skill_gap_report.txt
Those input/output paths are already specified in your file. 

One correction to your flow
Your diagram currently has:

STEP 8: STUDENT SKILL GAP REPORT
        ↓
STEP 9: SKILL GAP ANALYSIS
        ↓
STEP 10: RECOMMENDATION ENGINE
        ↓
STEP 11: FINAL STUDENT SKILL GAP REPORT
But based on the actual Python files you uploaded, the logical order is:

STEP 6
Skill Gap Prediction
        ↓
skill_gap_predictions.csv
        ↓
STEP 9
Skill Gap Analysis
        ↓
skill_gap_analysis.csv
        ↓
STEP 10
Recommendation Engine
        ↓
recommendations.csv
        ↓
STEP 11
Final Student Skill Gap Report
        ↓
student_skill_gap_report.csv
student_skill_gap_report.txt
So I would remove the earlier duplicate STEP 8 from the architecture diagram. Your three scripts already implement the final three stages.

Your complete pipeline should therefore be
RAW JOB DATASET
       ↓
01 Skill Extraction
       ↓
normalized_job_skills.csv
       ↓
02 TF-IDF Feature Engineering
       ↓
title_tfidf_features.npz
       ↓
03 Train/Test Split
       ↓
04 Model Training
       ↓
skill_prediction_model.pkl
       ↓
05 Model Evaluation
       ↓
06 Skill Gap Prediction
       ↓
skill_gap_predictions.csv
       ↓
09 Skill Gap Analysis
       ↓
skill_gap_analysis.csv
       ↓
10 Recommendation Engine
       ↓
recommendations.csv
       ↓
11 Student Skill Gap Report
       ↓
student_skill_gap_report.csv
student_skill_gap_report.txt
This is the structure I recommend you use in VS Code. It will also make your project look much more professional for your portfolio/GitHub and for your Master's applications.

User attachment
this much work this done
Yes ❤️ I can see your VS Code structure. You’ve already completed a substantial part of the project.

From your screenshot, you currently have:

✅ Already completed
AI Skill Gap Intelligence Platform
│
├── app/
│
├── data/
│   ├── external/
│   ├── processed/
│   └── raw/
│
├── database/
│   ├── domain_skill_demand.csv
│   ├── domains.csv
│   ├── job_domains.csv
│   ├── job_skills.csv
│   ├── jobs.csv
│   ├── skill_demand.csv
│   ├── skill_gap_db.sql
│   └── skills.csv
│
├── nlp/
│
├── notebooks/
│   ├── models/
│   ├── 01_data_understanding.py
│   ├── 02_data_cleaning.py
│   ├── 03_skill_analysis.py
│   ├── 04_create_skill_mapping.py
│   ├── 05_skill_normalization.py
│   ├── 06_domain_mapping.py
│   ├── 07_skill_demand_analysis.py
│   ├── 08_database_export.py
│   └── tempCodeRunnerFile.py
│
└── tests/
So do not rearrange everything. Your existing work is already organized enough.

🔥 What you need to add now
Based on the 3 files you just uploaded, I recommend adding these after your existing 08_database_export.py:

notebooks/
│
├── 01_data_understanding.py
├── 02_data_cleaning.py
├── 03_skill_analysis.py
├── 04_create_skill_mapping.py
├── 05_skill_normalization.py
├── 06_domain_mapping.py
├── 07_skill_demand_analysis.py
├── 08_database_export.py
│
├── 09_skill_gap_analysis.py        ← ADD
├── 10_recommendation_engine.py     ← ADD
└── 11_student_skill_gap_report.py  ← ADD
Since your existing project is using notebooks/ for numbered Python pipeline scripts, keeping 09–11 there is the least disruptive option.

⚠️ BUT there's one thing we need to check
Your new files expect these files to exist:

data/processed/
│
├── skill_gap_predictions.csv
├── skill_gap_analysis.csv
└── recommendations.csv
For example, 09 expects:

data/processed/skill_gap_predictions.csv
and generates:

data/processed/skill_gap_analysis.csv

Then 10 takes that output and generates recommendations.csv. 

Then 11 takes recommendations.csv and generates the final student reports. 

So your next pipeline is:

08_database_export.py
          ↓
   [ML prediction stage]
          ↓
skill_gap_predictions.csv
          ↓
09_skill_gap_analysis.py
          ↓
skill_gap_analysis.csv
          ↓
10_recommendation_engine.py
          ↓
recommendations.csv
          ↓
11_student_skill_gap_report.py
          ↓
student_skill_gap_report.csv
student_skill_gap_report.txt
Don't create random folders yet. Your existing structure is clear from the screenshot. The next thing I'd do is check your data/raw, data/processed, nlp, and models folders and then map exactly which of Steps 1–11 you've already completed and which scripts are still missing.

PS C:\Users\ANTARA\OneDrive\Documents\Career\AI Skill Gap Intelligence Platform> python -u "c:\Users\ANTARA\OneDrive\Documents\Career\AI Skill Gap Intelligence Platform\notebooks\09_skill_gap_analysis.py"
Loading skill gap predictions...
Traceback (most recent call last):
  File "c:\Users\ANTARA\OneDrive\Documents\Career\AI Skill Gap Intelligence Platform\notebooks\09_skill_gap_analysis.py", line 28, in <module>
    df = pd.read_csv(INPUT_FILE)
  File "C:\Users\ANTARA\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 873, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\ANTARA\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 300, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "C:\Users\ANTARA\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 1645, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\ANTARA\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\parsers\readers.py", line 1904, in _make_engine
    self.handles = get_handle(
                   ~~~~~~~~~~^
        f,
        ^^
    ...<6 lines>...
        storage_options=self.options.get("storage_options", None),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\ANTARA\AppData\Local\Programs\Python\Python314\Lib\site-packages\pandas\io\common.py", line 930, in get_handle
    handle = open(
        handle,
    ...<3 lines>...
        newline="",
    )
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\ANTARA\\OneDrive\\Documents\\Career\\data\\processed\\skill_gap_predictions.csv'
…
Yes — the error is clear, and your 09_skill_gap_analysis.py code itself is not the immediate problem.

What is happening
Your script is looking for:

C:\Users\ANTARA\OneDrive\Documents\Career\data\processed\skill_gap_predictions.csv
But your actual project is:

C:\Users\ANTARA\OneDrive\Documents\Career\AI Skill Gap Intelligence Platform\
The reason is this line in 09_skill_gap_analysis.py:

ROOT = Path(__file__).resolve().parents[2]
Because your file is currently here:

AI Skill Gap Intelligence Platform/
└── notebooks/
    └── 09_skill_gap_analysis.py
parents[2] goes one level too far up, to Career.

✅ Fix this
Open:

notebooks/09_skill_gap_analysis.py
Find:

ROOT = Path(__file__).resolve().parents[2]
Change it to:

ROOT = Path(__file__).resolve().parents[1]
Your beginning should become:

from pathlib import Path
import pandas as pd

# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_predictions.csv"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_analysis.csv"
)
Why parents[1]?
Your actual structure is:

AI Skill Gap Intelligence Platform   ← parents[1]
│
└── notebooks                         ← parents[0]
    └── 09_skill_gap_analysis.py
So:

Path(__file__).resolve().parents[1]
correctly points to:

AI Skill Gap Intelligence Platform
⚠️ But there's a second issue
After fixing this, run:

python -u "notebooks\09_skill_gap_analysis.py"
You may then get:

FileNotFoundError:
data\processed\skill_gap_predictions.csv
if that CSV hasn't been created yet.

Your 09 script specifically requires skill_gap_predictions.csv as its input. 

So before Step 9, you need to have completed the Skill Gap Prediction stage that generates:

data/
└── processed/
    └── skill_gap_predictions.csv
Your pipeline right now should be
08_database_export.py
        ↓
   ML prediction script
        ↓
skill_gap_predictions.csv
        ↓
09_skill_gap_analysis.py
        ↓
skill_gap_analysis.csv
        ↓
10_recommendation_engine.py
        ↓
recommendations.csv
        ↓
11_student_skill_gap_report.py
One more important correction
Your 10 and 11 scripts have the same parents[2] issue, because they're also inside notebooks/.

So change this in both:

ROOT = Path(__file__).resolve().parents[2]
to:

ROOT = Path(__file__).resolve().parents[1]
Your 10 script will then correctly use data/processed/skill_gap_analysis.csv and create recommendations.csv. 

Your 11 script will correctly use data/processed/recommendations.csv and create the final reports. 

Don't move the files. Keep them in your existing notebooks folder and fix parents[2] → parents[1].

If you send me a screenshot of your data → processed folder, I can tell you whether skill_gap_predictions.csv already exists and exactly which script you need to run next.




from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT / "data" / "processed"
    / "skill_gap_analysis.csv"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "recommendations.csv"
)


# ============================================================
# 2. LOAD SKILL GAP ANALYSIS
# ============================================================

print("Loading skill gap analysis...")

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. RECOMMENDATION DATABASE
# ============================================================

recommendation_map = {

    # Programming
    "python":
        "Learn Python programming, data structures, functions, OOP and practical problem solving.",

    "java":
        "Learn Java programming, OOP, collections, exception handling and application development.",

    "c++":
        "Learn C++ programming, OOP, STL and problem solving.",

    "c#":
        "Learn C# programming, .NET fundamentals and object-oriented programming.",

    "javascript":
        "Learn JavaScript fundamentals, ES6, DOM manipulation and web development.",


    # Database
    "sql":
        "Learn SQL queries, joins, subqueries, aggregation, views and database design.",

    "dbms":
        "Learn database concepts, normalization, transactions, indexing and SQL.",

    "oracle":
        "Learn Oracle Database, SQL, PL/SQL and database administration fundamentals.",


    # Data
    "data analysis":
        "Learn data cleaning, exploratory data analysis, visualization and statistical analysis.",

    "data analytics":
        "Learn Python, Pandas, NumPy, visualization and statistical techniques for data analytics.",

    "statistics":
        "Learn descriptive statistics, probability, hypothesis testing, correlation and regression.",

    "data modeling":
        "Learn data modeling, ER diagrams, dimensional modeling and database design.",


    # Web
    "html":
        "Learn HTML5, semantic elements, forms and webpage structure.",

    "css":
        "Learn CSS, layouts, Flexbox, Grid, responsive design and styling.",

    "rest api":
        "Learn REST API concepts, HTTP methods, JSON, authentication and API development.",

    "web services":
        "Learn web services, REST, SOAP, HTTP and API integration.",
