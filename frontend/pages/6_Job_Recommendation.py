import os
import sys

# Parent directory (frontend root) ko sys.path me add kar rahe hain
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import streamlit as st
import pandas as pd

# 'utils.api_client' se import kar rahe hain
from utils.api_client import get_job_recommendations, get_top_locations

st.set_page_config(page_title="Job Recommendations", page_icon="💼", layout="wide")

st.title("💼 Job Recommendation System")
st.markdown("Apni **Skills** aur **Preferred Location** enter kijiye, aur paayein personalized matching job roles!")

st.divider()

# Input Section
col1, col2 = st.columns([2, 1])

with col1:
    # 🟢 FIX: value khali kar di hai taaki pehle se kuch na aaye
    user_skills_input = st.text_input(
        "⚡ Enter Your Skills (Comma Separated):",
        value="",
        placeholder="e.g. Python, SQL, Java, Data Analysis...",
        help="Jaise: Python, Data Analysis, SQL, Power BI"
    )

with col2:
    # Fetch locations for dropdown from API
    locations_df = get_top_locations(top_n=50)
    location_list = ["All"]
    if not locations_df.empty and "location" in locations_df.columns:
        location_list += locations_df["location"].tolist()

    selected_location = st.selectbox("📍 Preferred Location:", location_list)

top_n_jobs = st.slider("Kitne jobs recommend karein?", min_value=5, max_value=20, value=10)

# Search Button
if st.button("🚀 Find Matching Jobs", use_container_width=True):
    if not user_skills_input.strip():
        st.warning("Kripya kam se kam ek skill type karein.")
    else:
        user_skills = [s.strip() for s in user_skills_input.split(",") if s.strip()]

        with st.spinner("Dataset se best matching jobs dhundhe ja rahe hain..."):
            res = get_job_recommendations(
                user_skills=user_skills,
                preferred_location=selected_location,
                top_n=top_n_jobs
            )

        if res.get("status") == "success":
            jobs = res.get("recommended_jobs", [])

            if jobs:
                st.subheader(f"🎯 Top {len(jobs)} Recommended Jobs Found:")

                for idx, job in enumerate(jobs, 1):
                    match_score = job.get("match_score", 0)
                    
                    # Score color tag
                    score_color = "🟢" if match_score >= 60 else ("🟡" if match_score >= 30 else "🔴")

                    with st.expander(f"**{idx}. {job.get('job_title', 'Job Role')}** | Match: {score_color} {match_score}%"):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write(f"🏢 **Company:** {job.get('company_name', 'N/A')}")
                            st.write(f"📍 **Location:** {job.get('location', 'N/A')}")
                        with c2:
                            # Safe salary handling
                            raw_salary = job.get('salary_avg', 0)
                            try:
                                salary = float(raw_salary) if raw_salary is not None else 0.0
                            except (ValueError, TypeError):
                                salary = 0.0

                            salary_text = f"₹{salary:,.0f}" if salary > 0 else "Not Disclosed"
                            st.write(f"💰 **Average Salary:** {salary_text}")

                        st.write(f"🛠️ **Required Skills:** {job.get('skills', 'N/A')}")
            else:
                st.info("Koi matching jobs nahi mile. Kripya different location ya skills try karein.")
        else:
            st.error(f"Error: {res.get('message', 'Failed to fetch recommendations')}")