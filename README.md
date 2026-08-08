<div align="center">

# 📊 Job Market Intelligence & Salary Prediction Platform

**An end-to-end data science web platform that analyzes real job market data and gives users AI-powered salary predictions, skill-gap analysis, and personalized job recommendations.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#-license)

</div>

Built with **FastAPI** (backend/API) + **Streamlit** (multi-page frontend) + **Groq LLM (Llama 3.3 70B)** for resume-based salary intelligence.

---
🔗 **Live Demo:** [Click Here to View Live App](https://job-salary-predictor-ds.streamlit.app)
⚙️ **Backend API:** [Live Render Backend](https://job-salary-predictor-backend.onrender.com)

<!--
Add your screenshots to a `screenshots/` folder in the repo root, then update the
paths below to match your filenames. Example:
  screenshots/home.png
  screenshots/market_trends.png
  screenshots/salary_predictor.png
  screenshots/skill_gap.png
  screenshots/job_recommendation.png
-->
<!-- 
| Home Page | Market Trends |
|---|---|
| ![Home Page](screenshots/home.png) | ![Market Trends](screenshots/market_trends.png) |

| Salary Predictor | Skill Gap Analyzer |
|---|---|
| ![Salary Predictor](screenshots/salary_predictor.png) | ![Skill Gap Analyzer](screenshots/skill_gap.png) |

| Job Recommendation |
|---|
| ![Job Recommendation](screenshots/job_recommendation.png) |

--- -->

## 📑 Table of Contents

<!-- - [Screenshots](#️-screenshots) -->
- [Problem It Solves](#-problem-it-solves)
- [Features](#-features-pages)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints-backend)
- [Dataset](#️-dataset)
- [Setup & Installation](#️-setup--installation)
- [How Salary Prediction Works](#-how-the-salary-prediction-works)
- [How Skill Gap & Job Recommendation Work](#-how-skill-gap--job-recommendation-work)
- [Notebooks](#-notebooks)
- [Future Improvements](#-future-improvements)
- [Author](#-author)
- [License](#-license)

---

## 🎯 Problem It Solves

Job seekers and students rarely get real, data-backed answers to questions like:
- What salary should I expect for a given role and city?
- Which skills are actually in demand for my target role?
- What skills am I missing, and how much would learning them boost my pay?
- Which live job postings actually match my current skill set?

This platform answers all of these using a large dataset of real job postings, classic ML/analytics on the backend, and an LLM for resume parsing + salary reasoning.

---

## ✨ Features (Pages)

| Page | Description |
|------|-------------|
| **1. Home** | Platform overview, key stats (total jobs, skills, locations), quick navigation |
| **2. Market Trends Analysis** | Top in-demand skills overall & by role, top hiring locations, top-paying roles, and an interactive **skill co-occurrence network graph** |
| **3. Salary Predictor** | Upload a resume (PDF) → LLM extracts experience & skills → predicts salary range, future salary projections by experience tier, and role-mismatch detection |
| **4. Model Performance** | Reports/metrics comparing Linear Models vs Tree/Boosting Models used during experimentation |
| **5. Skill Gap Analyzer** | Compares a user's skills against the top skills required for a target role, returns a weighted match score and prioritized skill gaps (HIGH/MEDIUM/LOW) |
| **6. Job Recommendation** | Recommends real job postings ranked by skill-overlap match score, with optional location filtering |

---

## 🏗️ Tech Stack

**Backend**
- FastAPI + Uvicorn — REST API layer
- Pandas / NumPy — data cleaning & analytics
- scikit-learn — salary prediction modeling (see `notebook/`)
- Groq API (`llama-3.3-70b-versatile`) — resume parsing & AI salary reasoning
- `pypdf` — resume PDF text extraction
- `python-dotenv` — environment variable management

**Frontend**
- Streamlit (multi-page app)
- Requests — API client to talk to the FastAPI backend

**Analysis / Modeling**
- Jupyter notebooks for EDA and model experimentation (Linear Models, Tree/Boosting Models)

---

## 📁 Project Structure

```
job project/
├── backend/
│   ├── main.py                 # FastAPI app & all API routes
│   ├── data_loader.py          # Dataset loading, cleaning & analytics helpers
│   ├── config.py               # Column-name mapping & data path config
│   ├── resume_parser.py        # PDF → text extraction
│   ├── salary_engine.py        # Groq LLM-powered salary prediction logic
│   ├── Streamlit_app.py
│   ├── requirements.txt
│   └── jobs_dataset*.csv       # Raw / cleaned job listing datasets
│
├── frontend/
│   ├── app.py                  # Entry point (redirects to Home page)
│   ├── pages/
│   │   ├── 1_Home_Page.py
│   │   ├── 2_Market_Trends_Analysis.py
│   │   ├── 3_Salary_Predictor.py
│   │   ├── 4_Model_Performance.py
│   │   ├── 5_Skill_Gap_Analyzer.py
│   │   └── 6_Job_Recommendation.py
│   ├── utils/
│   │   ├── api_client.py       # Wrapper around backend API calls
│   │   └── charts.py           # Chart/visualization helpers
│   └── requirements.txt
│
<!-- ├── notebook/ -->
<!-- │   ├── experimental_analysis_1.ipynb   # EDA -->
<!-- │   └── experimental_analysis_2.ipynb   # Model experimentation -->
│
├── data/                       # Feature/target extracts used for modeling
<!-- ├── docx/                       # Generated reports (Linear & Tree/Boosting models, network graphs) -->
├── Feature_to_Column_Mapping.md
├── Project_Summary_and_Dataset_Structure.md
├── Quick_Reference_Guide.md
└── Visual_Column_Dependency_Map.md
```

---

## 🔌 API Endpoints (Backend)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/overview` | Overall dataset stats (total jobs, total skills) |
| GET | `/api/skills/top?n=` | Top N most in-demand skills |
| GET | `/api/job-roles` | List of unique job roles/titles |
| GET | `/api/skills/by-role?role=&top_n=` | Top skills for a specific job role |
| GET | `/api/locations/top?top_n=` | Top hiring locations |
| GET | `/api/roles/top-paying?top_n=&min_job_count=` | Highest paying job roles |
| GET | `/api/skills/network?top_n=` | Interactive HTML skill co-occurrence network graph |
| POST | `/api/predict-salary` | Upload resume (PDF) + target role + location → AI salary prediction |
| POST | `/api/skills/gap-analysis` | Body: `{ target_role, user_skills[] }` → match score + skill gaps |
| POST | `/api/jobs/recommend` | Body: `{ user_skills[], preferred_location, top_n }` → ranked job matches |

Full interactive API docs are auto-generated by FastAPI at `/docs` once the backend is running.

---

## 🗂️ Dataset

The core dataset (`backend/jobs_dataset_final.csv`) contains real job postings with fields mapped in `config.py`, including:

- `job_title`, `job_title_normalized`, `company_name`, `company_size`
- `location`
- `min_experience`, `max_experience`
- `salary_min`, `salary_max`, `salary_avg`
- `skills` (tags/skills per job posting)
- `work_type`, `job_description`, `job_uploaded`

See **`Feature_to_Column_Mapping.md`**, **`Project_Summary_and_Dataset_Structure.md`**, and **`Visual_Column_Dependency_Map.md`** for the full column dictionary, cleaning logic, and how raw columns map to features used by each page/model.

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd "job project"
```

### 2. Backend setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with your Groq API key (used by the Salary Predictor page):
```
GROQ_API_KEY=your_groq_api_key_here
```

Run the API server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be live at `http://127.0.0.1:8000` and docs at `http://127.0.0.1:8000/docs`.

### 3. Frontend setup
Open a new terminal:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

By default the frontend talks to the backend at `http://127.0.0.1:8000`. To point it elsewhere, set:
```
API_BASE_URL=http://your-backend-host:8000
```

---

## 🧠 How the Salary Prediction Works

1. User uploads a resume (PDF) + selects target role & location.
2. `resume_parser.py` extracts raw text from the PDF using `pypdf`.
3. `salary_engine.py` sends the resume text + target role/location to Groq's `llama-3.3-70b-versatile` model with a structured prompt.
4. The model returns strict JSON containing: detected experience & skills, predicted salary range, experience-based salary projections, role-mismatch detection, and specific skill recommendations with estimated salary lift for each.
5. The frontend (`3_Salary_Predictor.py`) renders this as an interactive report.

---

## 🎯 How Skill Gap & Job Recommendation Work

- **Skill Gap Analyzer:** Pulls the top skills for a target role from the dataset, checks overlap with the user's entered skills, and computes a frequency-weighted match score. Each required skill is tagged HIGH / MEDIUM / LOW priority based on its relative demand.
- **Job Recommendation:** Filters postings by preferred location, then scores each job by the percentage overlap between the job's required skills and the user's skills, returning the top-N ranked matches.

---

## 📓 Notebooks

- `experimental_analysis_1.ipynb` — Exploratory Data Analysis (EDA) on the raw dataset.
- `experimental_analysis_2.ipynb` — Model experimentation (Linear Models vs Tree/Boosting Models) used to inform the salary prediction logic.

Model comparison write-ups are available in `docx/Linear_Models_Report (1).md` and `docx/Tree_Boosting_Other_Models_Report (1).md`.

---

## 🚀 Future Improvements

- Persist the trained ML salary model and serve predictions without depending solely on the LLM
- Add authentication so users can save resumes/recommendations
- Deploy backend + frontend (e.g., Render/Railway for FastAPI, Streamlit Community Cloud for frontend)
- Expand dataset with more recent job postings and additional industries

---

## 👤 Author

**Deepanshu Singh**

[![GitHub](https://img.shields.io/badge/GitHub-deepanshu--singh22-181717?logo=github&logoColor=white)](https://github.com/deepanshu-singh22)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Deepanshu%20Singh-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deepanshu-singh-6748b22ba)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

If you found this project useful, consider giving it a ⭐ on GitHub!

</div>
