import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Premium Dark Mode Custom Styling
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #38BDF8;
        margin-top: 5px;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-sub {
        font-size: 12px;
        color: #4ADE80;
        margin-top: 4px;
    }

    /* Badges */
    .badge-high {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-med {
        background-color: #78350F;
        color: #FDE047;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-low {
        background-color: #064E3B;
        color: #6EE7B7;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }

    /* Custom Table Styling */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        text-align: left;
        padding: 10px;
    }
    td {
        padding: 10px;
        border-bottom: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATA LOADER WITH FALLBACK PATHS
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_dataset():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

    possible_paths = [
        os.path.join(PROJECT_ROOT, "backend", "jobs_dataset_final.xls"),
        os.path.join(PROJECT_ROOT, "backend", "jobs_dataset_final.csv"),
        os.path.join(PROJECT_ROOT, "backend", "jobs_dataset.csv"),
        os.path.join(PROJECT_ROOT, "data", "jobs_dataset_final.xls"),
        os.path.join(PROJECT_ROOT, "data", "jobs_dataset_final.csv"),
        "jobs_dataset_final.xls",
        "jobs_dataset_final.csv",
        "jobs_dataset.csv"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                # First attempt reading as CSV (since dataset file is CSV formatted)
                df = pd.read_csv(path, low_memory=False)
                return df
            except Exception:
                try:
                    df = pd.read_excel(path)
                    return df
                except Exception:
                    continue
    return None

df_raw = load_dataset()

if df_raw is None:
    st.error("⚠️ Dataset (`jobs_dataset_final.xls` / `.csv`) nahi milaa! Please check your file paths in `backend/` or `data/` folder.")
    st.stop()

# Filter out empty job titles
df = df_raw.dropna(subset=['job_title_normalized']).copy()

# ---------------------------------------------------------
# 3. HELPER LOGIC: SKILL EXTRACTION & GAP COMPUTATION
# ---------------------------------------------------------
def get_role_top_skills(role_df, top_n=10):
    """Extracts top required skills and demand percentage for a target role."""
    total_jobs = len(role_df)
    if total_jobs == 0:
        return pd.DataFrame()

    # Split comma-separated skills
    skills_series = role_df['tagsAndSkills'].dropna().str.split(',').explode().str.strip()
    skills_df = pd.DataFrame({'skill': skills_series})
    skills_df = skills_df[skills_df['skill'] != '']
    skills_df['skill_lower'] = skills_df['skill'].str.lower()

    # Group and calculate frequency
    grouped = skills_df.groupby('skill_lower').agg(
        display_name=('skill', lambda x: x.mode()[0] if not x.empty else x.iloc[0]),
        count=('skill', 'count')
    ).reset_index()

    grouped['demand_pct'] = (grouped['count'] / total_jobs * 100).round(1)
    top_skills = grouped.sort_values(by='count', ascending=False).head(top_n).reset_index(drop=True)
    return top_skills


def compute_skill_gap_analysis(top_skills, user_skills):
    """
    Computes Weighted Match Score, Gap Analysis, and Priority Categorization.
    """
    if top_skills.empty:
        return 0.0, pd.DataFrame()

    user_skills_clean = [s.strip().lower() for s in user_skills if s.strip()]

    # Check if user has each top skill
    top_skills['user_has'] = top_skills['skill_lower'].isin(user_skills_clean)

    # Weighted Score Calculation
    sum_user_freq = top_skills[top_skills['user_has']]['count'].sum()
    sum_total_freq = top_skills['count'].sum()

    match_score = round((sum_user_freq / sum_total_freq * 100), 1) if sum_total_freq > 0 else 0.0

    # Priority Categorization based on relative demand
    max_demand = top_skills['demand_pct'].max()

    def set_priority(demand):
        ratio = demand / max_demand if max_demand > 0 else 0
        if ratio >= 0.65:
            return "HIGH"
        elif ratio >= 0.35:
            return "MEDIUM"
        else:
            return "LOW"

    def set_learning_time(priority):
        if priority == "HIGH":
            return "3-4 Weeks"
        elif priority == "MEDIUM":
            return "2-3 Weeks"
        else:
            return "1-2 Weeks"

    def set_resources(skill_name):
        return f"Coursera / Udemy: {skill_name} Mastery + Hands-on Projects"

    top_skills['priority_level'] = top_skills['demand_pct'].apply(set_priority)
    top_skills['learning_time_estimate'] = top_skills['priority_level'].apply(set_learning_time)
    top_skills['learning_resources'] = top_skills['display_name'].apply(set_resources)

    return match_score, top_skills


# ---------------------------------------------------------
# 4. HEADER & INPUT SECTION
# ---------------------------------------------------------
st.title("🎯 Skill Gap Analyzer")
st.caption("Compare your current skillset against real job market demands, identify key skill gaps, and get a prioritized learning roadmap.")

st.write("")

col_input1, col_input2 = st.columns([1, 2])

# Role Selector
with col_input1:
    st.subheader("1️⃣ Select Target Role")
    available_roles = sorted(df['job_title_normalized'].unique().tolist())
    
    # Default selection preference
    default_index = 0
    for idx, r in enumerate(available_roles):
        if "AI" in r or "Software" in r:
            default_index = idx
            break

    target_role = st.selectbox(
        "Target Job Designation:",
        options=available_roles,
        index=default_index,
        help="Select the role you are aiming for to fetch market skill requirements."
    )

    role_filtered_df = df[df['job_title_normalized'] == target_role]
    st.info(f"📊 Analyzing **{len(role_filtered_df):,}** active job postings for **{target_role}**.")

# Skill Frequency for Target Role
top_market_skills = get_role_top_skills(role_filtered_df, top_n=10)
suggested_skills_list = top_market_skills['display_name'].tolist() if not top_market_skills.empty else []

# User Skill Selector
with col_input2:
    st.subheader("2️⃣ Enter / Select Your Current Skills")
    
    # Pre-select first 2 top skills as default demo input
    default_user_skills = suggested_skills_list[:2] if len(suggested_skills_list) >= 2 else []

    user_selected_skills = st.multiselect(
        "Select skills you currently possess:",
        options=sorted(list(set(suggested_skills_list + ["Python", "SQL", "Pandas", "Git", "Docker", "AWS", "Machine Learning", "Communication"]))),
        default=default_user_skills,
        help="Type or select skills from the dropdown list."
    )

    # Quick Add Buttons for Target Role Skills
    st.write("**⚡ Quick Add Top Required Skills for this Role:**")
    pill_cols = st.columns(5)
    for idx, skill in enumerate(suggested_skills_list[:5]):
        with pill_cols[idx % 5]:
            if st.button(f"+ {skill}", key=f"btn_skill_{idx}"):
                if skill not in user_selected_skills:
                    user_selected_skills.append(skill)
                    st.rerun()

st.divider()

# ---------------------------------------------------------
# 5. GAP ANALYSIS & MATCH SCORE COMPUTATION
# ---------------------------------------------------------
if not top_market_skills.empty:
    match_score, analysis_df = compute_skill_gap_analysis(top_market_skills, user_selected_skills)

    matched_count = len(analysis_df[analysis_df['user_has']])
    missing_count = len(analysis_df[~analysis_df['user_has']])

    # ---------------------------------------------------------
    # 6. OVERVIEW METRICS CARDS
    # ---------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        score_color = "#4ADE80" if match_score >= 70 else "#FACC15" if match_score >= 45 else "#EF4444"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Weighted Match Score</div>
            <div class="metric-value" style="color: {score_color};">{match_score}%</div>
            <div class="metric-sub">Role Alignment Score</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Matched Skills</div>
            <div class="metric-value" style="color: #4ADE80;">{matched_count} / {len(analysis_df)}</div>
            <div class="metric-sub">Skills You Possess ✓</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Missing Skill Gaps</div>
            <div class="metric-value" style="color: #F87171;">{missing_count}</div>
            <div class="metric-sub">High Demand Gaps ✗</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Target Role</div>
            <div class="metric-value" style="font-size: 18px; color: #38BDF8;">{target_role}</div>
            <div class="metric-sub">Based on {len(role_filtered_df)} Jobs</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ---------------------------------------------------------
    # 7. INTERACTIVE VISUALIZATIONS (DEMAND VS POSSESSION)
    # ---------------------------------------------------------
    col_chart, col_gaps = st.columns([1.2, 1])

    with col_chart:
        st.subheader("📊 Skill Demand vs. Your Profile")

        analysis_df['status'] = analysis_df['user_has'].apply(lambda x: 'Matched ✓' if x else 'Missing Gap ✗')
        
        # Color Map
        color_discrete_map = {'Matched ✓': '#10B981', 'Missing Gap ✗': '#EF4444'}

        fig_bar = px.bar(
            analysis_df,
            x='demand_pct',
            y='display_name',
            orientation='h',
            color='status',
            color_discrete_map=color_discrete_map,
            text='demand_pct',
            labels={'demand_pct': 'Market Demand (% of Job Postings)', 'display_name': 'Required Skill'},
            title=f"Top 10 Required Skills for {target_role}"
        )

        fig_bar.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_bar.update_layout(
            yaxis=dict(autorange="reversed"),
            template="plotly_dark",
            height=420,
            legend_title_text="Skill Status",
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col_gaps:
        st.subheader("📋 Matched vs. Missing Summary")

        tab_has, tab_missing = st.tabs(["✅ Skills You Have", "❌ Missing Skills (Gaps)"])

        with tab_has:
            user_has_df = analysis_df[analysis_df['user_has']]
            if not user_has_df.empty:
                for _, row in user_has_df.iterrows():
                    st.markdown(f"🟢 **{row['display_name']}** — Required in `{row['demand_pct']}%` job postings")
            else:
                st.warning("None of the top 10 required skills are selected. Add skills to increase match score!")

        with tab_missing:
            missing_df = analysis_df[~analysis_df['user_has']]
            if not missing_df.empty:
                for _, row in missing_df.iterrows():
                    priority = row['priority_level']
                    badge_class = "badge-high" if priority == "HIGH" else "badge-med" if priority == "MEDIUM" else "badge-low"
                    
                    st.markdown(f"""
                    🔴 **{row['display_name']}** 
                    <span class="{badge_class}">{priority} PRIORITY</span> 
                    *(Required in {row['demand_pct']}% jobs)*
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 Outstanding! You possess all top 10 required skills for this role!")

    st.divider()

    # ---------------------------------------------------------
    # 8. PRIORITIZED LEARNING ROADMAP & RECOMMENDATIONS
    # ---------------------------------------------------------
    st.subheader("🛣️ Prioritized Skill Upskilling Plan")
    st.caption("Focus on HIGH priority skills first to maximize your job application callback rate.")

    missing_df = analysis_df[~analysis_df['user_has']].sort_values(by='demand_pct', ascending=False)

    if not missing_df.empty:
        # Format table for display
        roadmap_data = []
        for rank, (_, row) in enumerate(missing_df.iterrows(), start=1):
            roadmap_data.append({
                "Rank": f"#{rank}",
                "Skill Name": row['display_name'],
                "Market Demand": f"{row['demand_pct']}% of jobs",
                "Priority Level": row['priority_level'],
                "Est. Learning Time": row['learning_time_estimate'],
                "Recommended Resource": row['learning_resources']
            })

        roadmap_table = pd.DataFrame(roadmap_data)

        # Display formatted dataframe
        st.dataframe(
            roadmap_table,
            column_config={
                "Priority Level": st.column_config.TextColumn(
                    "Priority Level",
                    help="Categorized based on job requirement frequency"
                )
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.balloons()
        st.success("You are 100% matched with the top market skills for this role! Ready to apply.")

else:
    st.warning("No skill data available for the selected target role.")