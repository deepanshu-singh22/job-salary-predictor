import os
import sys

# Parent path setup for imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)

for path in [CURRENT_DIR, FRONTEND_DIR, PROJECT_ROOT]:
    if path not in sys.path:
        sys.path.insert(0, path)

import streamlit as st

try:
    from utils.api_client import get_overview_stats, get_top_skills
except ModuleNotFoundError:
    from frontend.utils.api_client import get_overview_stats, get_top_skills

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Job Market Intelligence & Career Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI & Top Navbar
st.markdown("""
    <style>
    /* Styling for Top Navigation Buttons */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #334155;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        border-color: #38BDF8;
        color: #38BDF8;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #CBD5E1;
        font-weight: 500;
        margin-top: 5px;
    }
    .feature-box {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 22px;
        height: 100%;
        color: #F8FAFC !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .feature-box h3 {
        color: #38BDF8 !important;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .feature-box p {
        color: #94A3B8 !important;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 🔝 TOP NAVBAR IMPLEMENTATION
# -----------------------------------------------------------------------------
nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(6)

with nav1:
    if st.button("🏠 Home Page", use_container_width=True):
        st.switch_page("pages/1_Home_Page.py")  # File name ke mutabiq adjust karein

with nav2:
    if st.button("📈 Market Trends", use_container_width=True):
        st.switch_page("pages/2_Market_Trends_Analysis.py")  # Aapki page file ka path

with nav3:
    if st.button("💰 Salary Predictor", use_container_width=True):
        st.switch_page("pages/3_Salary_Predictor.py")

with nav4:
    if st.button("📊 Model Performance", use_container_width=True):
        st.switch_page("pages/4_Model_Performance.py")

with nav5:
    if st.button("🎯 Skill Gap Analyzer", use_container_width=True):
        st.switch_page("pages/5_Skill_Gap_Analyzer.py")

with nav6:
    if st.button("💼 Job Recommendation", use_container_width=True):
        st.switch_page("pages/6_Job_Recommendation.py")

st.divider()

# -----------------------------------------------------------------------------
# 2. Hero Section
# -----------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>📊 Job Market Intelligence & Salary Prediction Platform</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Real-time Job Data Analysis,Resume Salary Prediction, Skill Gap Analyzer & Smart Job Recommendations</p>", unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------------------------
# 3. Live Analytics Overview (Metric Cards)
# -----------------------------------------------------------------------------
st.subheader("📈 Live Market Overview")

try:
    stats = get_overview_stats()
    top_skills = get_top_skills(n=5)
except Exception:
    stats = {}
    top_skills = []

m1, m2, m3, m4 = st.columns(4)

with m1:
    total_jobs = stats.get("total_jobs", 0) if isinstance(stats, dict) else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_jobs:,}</div>
            <div class="metric-label">💼 Total Jobs Analyzed</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    total_skills = stats.get("total_skills", 0) if isinstance(stats, dict) else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_skills:,}</div>
            <div class="metric-label">🛠️ Unique Skills Tracked</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    avg_salary = stats.get("avg_salary", 0) if isinstance(stats, dict) else 0
    salary_str = f"₹{avg_salary:,.0f}" if avg_salary > 0 else "Data Updated"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{salary_str}</div>
            <div class="metric-label">💰 Avg Market Salary</div>
        </div>
    """, unsafe_allow_html=True)

with m4:
    top_skill_name = "Python"
    if isinstance(top_skills, list) and len(top_skills) > 0:
        top_skill_name = top_skills[0].get("skill", "Python")
    elif hasattr(top_skills, "empty") and not top_skills.empty:
        top_skill_name = top_skills.iloc[0].get("skill", "Python")

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{top_skill_name}</div>
            <div class="metric-label">🔥 #1 In-Demand Skill</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------------------------------------------------------
# 4. Explore Modules & Features
# -----------------------------------------------------------------------------
st.subheader("🛠️ Explore Platform Modules")
st.caption("Navbar ya Sidebar se kisi bhi page par navigate kar sakte hain:")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="feature-box">
            <h3>📈 Market Trends Analysis</h3>
            <p>Dekhiye top skills demand, hiring geographies, aur overall market distribution.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
        <div class="feature-box">
            <h3>🎯 Skill Gap Analyzer</h3>
            <p>Apne skills daal kar target role ke sath gap check karein aur priority skills paayein.</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="feature-box">
            <h3>💰 Salary Predictor</h3>
            <p>AI engine dwara resume upload karke estimated salary insights evaluate karein.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
        <div class="feature-box">
            <h3>💼 Job Recommendation</h3>
            <p>Skills aur preferred location filter karke top matching job profiles dhundhein.</p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="feature-box">
            <h3>📊 Model Performance</h3>
            <p>Backend ML/AI models ki accuracy, metrics aur training metrics inspect karein.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()
# -----------------------------------------------------------------------------
# 5. Workflow Guide (All 6 Steps Explicitly Covered)
# -----------------------------------------------------------------------------
st.subheader("🚀 How To Get Started?")
st.caption("Aap platform ko step-by-step is tarah use kar sakte hain:")

# Row 1: Steps 1 to 3
c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        "**Step 1: Market Trends Analysis**\n\n"
        "Sabse pehle industry trends, top skills, aur overall market demand ka visual analysis dekhein."
    )

with c2:
    st.info(
        "**Step 2: Salary Predictor**\n\n"
        "Apna Resume PDF upload karke AI dwara expected salary insights aur feedback paayein."
    )

with c3:
    st.info(
        "**Step 3: Model Performance**\n\n"
        "Backend ML models ki accuracy, algorithms aur evaluation metrics inspect karein."
    )

st.write("") # Margin gap

# Row 2: Steps 4 to 6
c4, c5, c6 = st.columns(3)

with c4:
    st.warning(
        "**Step 4: Skill Gap Analyzer**\n\n"
        "Apni current skills select karke target role ke mutabiq required skill gaps identity karein."
    )

with c5:
    st.warning(
        "**Step 5: Job Recommendation**\n\n"
        "Apni technical skills aur location filter ke basis par best matching jobs khojein."
    )

with c6:
    st.success(
        "**Step 6: Home / Dashboard Overview**\n\n"
        "Overview metrics par aakar live jobs data aur top in-demand skills ka high-level summary dekhein."
    )

st.divider()
st.caption("⚡ Powered by FastAPI Backend, Streamlit Frontend & Groq LLM Engine.")