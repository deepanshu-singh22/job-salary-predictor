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
    if not locations_df.empty:
        # Fallback for city / location keys
        loc_col = "location" if "location" in locations_df.columns else ("city" if "city" in locations_df.columns else None)
        if loc_col:
            location_list += locations_df[loc_col].dropna().tolist()

    selected_location = st.selectbox("📍 Preferred Location:", location_list)

top_n_jobs = st.slider("Kitne jobs recommend karein?", min_value=5, max_value=20, value=10)

# Search Button
# Search Button Fix
if st.button("🚀 Find Matching Jobs", use_container_width=True):
    if not user_skills_input.strip():
        st.warning("Kripya kam se kam ek skill type karein.")
    else:
        # Pass both list and raw string to ensure API client compatibility
        user_skills_list = [s.strip() for s in user_skills_input.split(",") if s.strip()]
        user_skills_str = ", ".join(user_skills_list)

        with st.spinner("Dataset se best matching jobs dhundhe ja rahe hain..."):
            # Dono formats pass karke safe fallback
            try:
                res = get_job_recommendations(
                    user_skills=user_skills_list,
                    preferred_location=selected_location,
                    top_n=top_n_jobs
                )
            except Exception:
                res = get_job_recommendations(
                    skills=user_skills_str,
                    location=selected_location,
                    top_n=top_n_jobs
                )

        # Robust Response Resolution
        jobs = []
        if isinstance(res, dict):
            jobs = res.get("recommended_jobs") or res.get("data") or res.get("jobs") or []
        elif isinstance(res, list):
            jobs = res

        if jobs:
            st.subheader(f"🎯 Top {len(jobs)} Recommended Jobs Found:")

            for idx, job in enumerate(jobs, 1):
                match_score = job.get("match_score") or job.get("match_percentage") or 100
                
                job_title = (
                    job.get("job_title_normalized") 
                    or job.get("job_title") 
                    or job.get("title") 
                    or job.get("role")
                    or "Job Role"
                )

                company = job.get("company_name") or job.get("company") or "N/A"
                location = job.get("location") or job.get("city") or "N/A"
                skills = job.get("skills") or job.get("required_skills") or "N/A"

                score_color = "🟢" if match_score >= 60 else ("🟡" if match_score >= 30 else "🔴")

                with st.expander(f"**{idx}. {job_title}** | Match: {score_color} {match_score}%"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"🏢 **Company:** {company}")
                        st.write(f"📍 **Location:** {location}")
                    with c2:
                        raw_salary = job.get('salary_avg') or job.get('salary') or 0
                        try:
                            salary = float(raw_salary) if raw_salary is not None else 0.0
                        except (ValueError, TypeError):
                            salary = 0.0

                        salary_text = f"₹{salary:,.0f}" if salary > 0 else "Not Disclosed"
                        st.write(f"💰 **Average Salary:** {salary_text}")

                    st.write(f"🛠️ **Required Skills:** {skills}")
        else:
            st.info("Koi matching jobs nahi mile. Kripya different location ya skills try karein.")