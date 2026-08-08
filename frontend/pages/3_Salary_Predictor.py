import sys
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import api_client as api

st.set_page_config(page_title="AI Resume Salary Predictor", page_icon="💰", layout="wide")

st.title("💰 Smart Market Valuation & Compensation Calculator")
st.markdown("Upload your Resume and discover your **Real-Time Market Valuation & Salary Brackets** powered by Live AI analysis.")

st.markdown("---")

# 1. Inputs Section
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

col_in1, col_in2 = st.columns(2)
with col_in1:
    available_roles = api.get_job_roles()
    if available_roles:
        target_role = st.selectbox("Target Job Role", available_roles)
    else:
        target_role = st.text_input("Target Job Role", value="Frontend Developer")

with col_in2:
    location = st.selectbox("Preferred Location", ["Remote", "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Noida", "Delhi / NCR"])

predict_btn = st.button("🚀 Predict Market Value", type="primary", use_container_width=True)

st.markdown("---")

# 2. Results Section
if predict_btn:
    if not uploaded_file:
        st.error("⚠️ Please upload a PDF resume first!")
    else:
        with st.spinner("Parsing Resume & Calculating Market Value via Groq AI..."):
            file_bytes = uploaded_file.getvalue()
            res = api.get_salary_prediction(file_bytes, uploaded_file.name, target_role, location)
            
            if res and res.get("status") == "success":
                data = res["data"]
                
                # SMART MISMATCH ALERT
                is_mismatch = data.get("role_mismatch", False)
                mismatch_reason = data.get("mismatch_reason", "")
                if is_mismatch is True or str(is_mismatch).lower() == "true":
                    st.warning(f"⚠️ **Skill Alignment Warning:** {mismatch_reason}")
                
                col_left, col_right = st.columns([1, 1.2])
                
                with col_left:
                    # METRICS ROW
                    m1, m2, m3 = st.columns(3)
                    avg_val = data.get('predicted_salary_avg_lpa', 0)
                    min_val = data.get('salary_range_min_lpa', 0)
                    max_val = data.get('salary_range_max_lpa', 0)
                    exp_years = data.get('candidate_experience_years', 0)
                    
                    with m1:
                        st.metric("Predicted Average", f"₹{avg_val} LPA")
                    with m2:
                        st.metric("Salary Range", f"₹{min_val} - {max_val} LPA")
                    with m3:
                        st.metric("Detected Exp.", f"{exp_years} Yrs")
                    
                    # GAUGE CHART
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=avg_val,
                        number={'suffix': " LPA", 'font': {'size': 24, 'color': '#00CC96'}},
                        title={'text': "Current Valuation Gauge", 'font': {'size': 16}},
                        gauge={
                            'axis': {'range': [0, max(max_val * 1.3, 20)], 'tickwidth': 1},
                            'bar': {'color': "#00CC96"},
                            'bgcolor': "white",
                            'steps': [
                                {'range': [0, min_val], 'color': '#FF6666'},
                                {'range': [min_val, max_val], 'color': '#FFCC00'},
                                {'range': [max_val, max(max_val * 1.3, 20)], 'color': '#66B2FF'}
                            ],
                        }
                    ))
                    fig.update_layout(height=230, margin=dict(l=20, r=20, t=30, b=10))
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("**Detected High-Value Skills:**")
                    skills = data.get("detected_skills", [])
                    st.write(", ".join([f"`{s}`" for s in skills]))

                with col_right:
                    st.subheader("📈 Experience vs Growth Projections")
                    projections = data.get("experience_projections", [])
                    if projections:
                        df_proj = pd.DataFrame(projections)
                        df_proj.columns = ["Experience Level", "Expected Salary Range", "Estimated Growth %"]
                        st.table(df_proj)
                    
                    st.subheader("🏢 Hiring Company Categories")
                    companies = data.get("hiring_company_types", [])
                    if companies:
                        df_comp = pd.DataFrame(companies)
                        df_comp.columns = ["Company Type / Tier", "Expected Pay Band"]
                        st.table(df_comp)

                # -------------------------------------------------------------
                # FULL WIDTH SKILL RECOMMENDATIONS SECTION
                # -------------------------------------------------------------
                st.markdown("---")
                st.subheader("🎯 High-Impact Skill Recommendations & Salary Lift")
                st.caption(f"Missing skills for **{target_role}** and predicted salary valuation if learned:")
                
                recommendations = data.get("skill_recommendations", [])
                if recommendations:
                    for rec in recommendations:
                        with st.container(border=True):
                            col_rec1, col_rec2, col_rec3 = st.columns([3, 2.5, 4.5])
                            
                            with col_rec1:
                                st.markdown(f"### 💡 **{rec.get('recommended_skill')}**")
                                demand_pct = rec.get('skill_demand_percentage', 0)
                                st.caption(f"🔥 **{demand_pct}%** of jobs ask for this skill")
                            
                            with col_rec2:
                                inc_amt = rec.get('salary_increase_amount', 0)
                                inc_pct = rec.get('salary_increase_percentage', 0)
                                new_sal = rec.get('predicted_salary_after_skill', 0)
                                st.metric(
                                    label="Valuation After Skill",
                                    value=f"₹{new_sal} LPA",
                                    delta=f"+₹{inc_amt} LPA (+{inc_pct}%)"
                                )
                            
                            with col_rec3:
                                st.markdown(f"**Difficulty:** `{rec.get('learning_difficulty')}`")
                                st.markdown(f"⏱️ **Est. Time:** {rec.get('estimated_learning_time')}")
                                st.markdown(f"📚 **Course:** {rec.get('learning_resources')}")
                else:
                    st.success("🎉 Excellent Profile! Your resume covers all key skills required for this role.")

            else:
                st.error("Failed to fetch predictions. Ensure FastAPI backend is running and GROQ_API_KEY is valid.")