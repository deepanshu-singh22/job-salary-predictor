import os
import sys

# Add project root and backend folder to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR) if "pages" in CURRENT_DIR else os.path.dirname(os.path.dirname(CURRENT_DIR))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

for p in [ROOT_DIR, BACKEND_DIR, CURRENT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
import streamlit.components.v1 as components

# MUST BE THE FIRST STREAMLIT COMMAND IN THE SCRIPT!
st.set_page_config(page_title="Market Trends Analysis", page_icon="📈", layout="wide")

from utils import api_client as api
from utils.charts import top_skills_bar_chart

# Custom Metric Cards CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e222d;
        border: 1px solid #2e3440;
        border-radius: 12px;
        padding: 18px 24px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        color: #8892b0;
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
    }
    .metric-value {
        color: #64ffda;
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Market Trends Analysis")
st.markdown("Explore overall top-demanding skills and role-specific skill distributions across job markets.")

st.markdown("---")

# =========================================================
# SECTION 1: OVERALL MOST DEMANDING SKILLS
# =========================================================
st.header("🔥 Overall Most Demanding Skills")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("Analyze general skill demand across all job roles.")
with col2:
    n = st.slider("Number of skills to display:", min_value=5, max_value=20, value=10, key="overall_skills_slider")

top_skills_df = api.get_top_skills(n=n)

if top_skills_df.empty:
    st.warning("Overall skills data nahi mila.")
else:
    fig = top_skills_bar_chart(top_skills_df)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 View Table Data"):
        st.dataframe(
            top_skills_df[["rank", "skill_name", "frequency_count", "percentage_of_jobs"]],
            use_container_width=True,
            hide_index=True,
        )

st.markdown("---")

# =========================================================
# SECTION 2: TOP SKILLS BY SPECIFIC JOB ROLE
# =========================================================
st.header("🎯 Top Skills by Job Role")
st.markdown("Filter and drill down into required skills for specific job roles.")

roles = api.get_job_roles()

if roles:
    col_drop, col_slider = st.columns([2.5, 1.5])

    with col_drop:
        selected_role = st.selectbox("📌 Choose Job Role:", options=roles, index=0)

    with col_slider:
        top_n_skills = st.slider("🔢 Number of Top Skills:", min_value=3, max_value=10, value=5, key="role_skills_slider")

    skills_df = api.get_skills_by_role(role=selected_role, top_n=top_n_skills)

    if not skills_df.empty:
        top_skill = skills_df.iloc[0]["skill_name"]
        top_pct = skills_df.iloc[0]["percentage_demand_in_role"]

        # Metric Cards
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Selected Role</div><div class="metric-value" style="font-size:18px;">{selected_role}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">#1 Top Skill</div><div class="metric-value">{top_skill}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Demand Share</div><div class="metric-value">{top_pct}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts & Tables
        chart_col, table_col = st.columns([1.4, 1])

        with chart_col:
            st.subheader("📊 Skills Demand Chart")
            role_fig = px.bar(
                skills_df,
                x="percentage_demand_in_role",
                y="skill_name",
                orientation="h",
                text=skills_df["percentage_demand_in_role"].apply(lambda x: f"{x}%"),
                color="percentage_demand_in_role",
                color_continuous_scale=["#1f77b4", "#64ffda"]
            )
            role_fig.update_traces(textposition="outside", marker_line_width=0)
            role_fig.update_layout(
                yaxis=dict(autorange="reversed", title=""),
                xaxis=dict(title="% Demand", showgrid=True, gridcolor="#2e3440"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                height=350,
                margin=dict(l=10, r=40, t=10, b=30),
                font=dict(color="#8892b0")
            )
            st.plotly_chart(role_fig, use_container_width=True)

        with table_col:
            st.subheader("📋 Data Breakdown")
            table_display = skills_df.copy()
            table_display["percentage_demand_in_role"] = table_display["percentage_demand_in_role"].astype(str) + "%"
            st.dataframe(
                table_display[["rank", "skill_name", "count_in_role", "percentage_demand_in_role"]],
                column_config={
                    "rank": "Rank",
                    "skill_name": "Skill",
                    "count_in_role": "Count",
                    "percentage_demand_in_role": "% Demand"
                },
                hide_index=True,
                use_container_width=True
            )
    else:
        st.warning(f"'{selected_role}' ke liye skills data nahi mila.")
else:
    st.error("⚠️ Backend se job roles fetch nahi ho sake. Please ensure FastAPI backend is running.")

st.markdown("---")

# =========================================================
# SECTION 3: TOP HIRING LOCATIONS IN INDIA (GEOSPATIAL)
# =========================================================
CITY_COORDINATES = {
    'Bengaluru': [12.9716, 77.5946],
    'Hyderabad': [17.3850, 78.4867],
    'Pune': [18.5204, 73.8567],
    'Mumbai': [19.0760, 72.8777],
    'Chennai': [13.0827, 80.2707],
    'Gurugram': [28.4595, 77.0266],
    'Noida': [28.5355, 77.3910],
    'Ahmedabad': [23.0225, 72.5714],
    'Kolkata': [22.5726, 88.3639],
    'Navi Mumbai': [19.0330, 73.0297],
    'Jaipur': [26.9124, 75.7873],
    'Chandigarh': [30.7333, 76.7794],
    'Kochi': [9.9312, 76.2673],
    'Indore': [22.7196, 75.8577],
    'Coimbatore': [11.0168, 76.9558],
    'Vadodara': [22.3072, 73.1812],
    'Surat': [21.1702, 72.8311],
    'Nagpur': [21.1458, 79.0882],
    'Lucknow': [26.8467, 80.9462],
    'Bhubaneswar': [20.2961, 85.8245]
}

def render_top_locations_section():
    st.markdown("### 📍 Feature 2.2: Top Hiring Locations in India")
    st.write("Geospatial analysis showing tech job density, average salaries, and dominant skills across Indian tech hubs.")

    with st.spinner("Loading Geospatial Location Data..."):
        top_locations_df = api.get_top_locations(top_n=20)

    if top_locations_df.empty:
        st.error("No location data available.")
        return

    col1, col2, col3, col4 = st.columns(4)
    top_city = top_locations_df.iloc[0]['city']
    top_city_jobs = top_locations_df.iloc[0]['job_count']
    top_salary_city = top_locations_df.sort_values(by='avg_salary_lpa', ascending=False).iloc[0]

    with col1:
        st.metric("Top Hiring Hub", top_city, f"{top_city_jobs:,} Jobs")
    with col2:
        st.metric("Highest Avg Package", top_salary_city['city'], f"₹{top_salary_city['avg_salary_lpa']} LPA")
    with col3:
        st.metric("Total Active Locations Analyzed", f"{len(top_locations_df)}")
    with col4:
        st.metric("Overall Avg Market Salary", f"₹{round(top_locations_df['avg_salary_lpa'].mean(), 2)} LPA")

    st.markdown("---")

    india_map = folium.Map(
        location=[21.7679, 78.8718],
        zoom_start=5,
        min_zoom=5,
        max_zoom=9,
        max_bounds=True,
        min_lat=6.5,
        max_lat=35.5,
        min_lon=68.0,
        max_lon=97.5,
        tiles="CartoDB dark_matter"
    )

    for idx, row in top_locations_df.iterrows():
        city = row['city']
        if city in CITY_COORDINATES:
            lat, lon = CITY_COORDINATES[city]
            rank_badge = f"#{idx + 1} Top City"
            
            popup_html = f"""
            <style>
                .leaflet-popup-content-wrapper, .leaflet-popup-tip {{
                    background: #0F172A !important;
                    color: #F8FAFC !important;
                    border-radius: 14px !important;
                    padding: 0px !important;
                    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
                }}
                .leaflet-popup-content {{
                    margin: 0 !important;
                    line-height: 1.4 !important;
                }}
            </style>
            
            <div style="font-family: system-ui, -apple-system, sans-serif; background-color: #0F172A; color: #F8FAFC; padding: 18px; border-radius: 14px; width: 230px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-size: 18px;">📍</span>
                        <span style="font-size: 20px; font-weight: 700; color: #38BDF8;">{city}</span>
                    </div>
                    <span style="background-color: #1E293B; color: #94A3B8; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 12px; border: 1px solid #334155;">
                        {rank_badge}
                    </span>
                </div>
                
                <hr style="border: 0; border-top: 1px solid #1E293B; margin: 0 0 12px 0;">
                
                <div style="font-size: 13px; font-weight: 500;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #94A3B8;">Total Jobs:</span>
                        <span style="color: #34D399; font-weight: 700;">{row['job_count']:,}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #94A3B8;">Avg Salary:</span>
                        <span style="color: #FBBF24; font-weight: 700;">₹{row['avg_salary_lpa']} LPA</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #94A3B8;">Median Salary:</span>
                        <span style="color: #E2E8F0;">₹{row['median_salary_lpa']} LPA</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <span style="color: #94A3B8;">Salary Range:</span>
                        <span style="color: #E2E8F0;">₹{row['salary_min_lpa']} - ₹{row['salary_max_lpa']} LPA</span>
                    </div>
                </div>
                
                <div style="border-top: 1px dashed #334155; margin-bottom: 10px;"></div>
                
                <div>
                    <div style="color: #94A3B8; font-size: 11px; font-weight: 600; margin-bottom: 4px;">Top Demanded Skills:</div>
                    <div style="color: #38BDF8; font-size: 12px; font-weight: 700;">{row['dominant_skills']}</div>
                </div>
            </div>
            """
            
            circle_radius = max(8, min(22, int(np.sqrt(row['job_count']) / 3.5)))
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=circle_radius,
                color='#38BDF8',
                weight=2,
                fill=True,
                fill_color='#0284C7',
                fill_opacity=0.75,
                popup=popup_html
            ).add_to(india_map)

    left_col, right_col = st.columns([1.6, 1.0])

    with left_col:
        st.subheader("🌐 Geospatial Interactive Heatmap")
        map_html = india_map._repr_html_()
        components.html(map_html, height=520, scrolling=False)

    with right_col:
        st.subheader("📊 Top Locations Ranking")
        display_df = top_locations_df[['city', 'job_count', 'avg_salary_lpa', 'dominant_skills']].copy()
        display_df.columns = ['City', 'Jobs Count', 'Avg Package (LPA)', 'Top Skills']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=460,
            hide_index=True
        )

render_top_locations_section()

st.markdown("---")
# =========================================================
# SECTION 4: TOP HIGH PAYING JOB ROLES
# =========================================================
def render_top_high_paying_roles_section():
    st.markdown("### 💼 Feature 2.3: Top High Paying Job Roles")
    st.write("Detailed analysis of highest compensation roles, job openings, and overall market distribution.")

    with st.spinner("Loading High Paying Roles Data..."):
        top_roles_df = api.get_top_high_paying_roles(top_n=10)

    if top_roles_df.empty:
        st.error("No High Paying Roles data available.")
        return

    col1, col2, col3 = st.columns(3)
    top_role = top_roles_df.iloc[0]
    highest_demand = top_roles_df.sort_values(by='job_count', ascending=False).iloc[0]

    with col1:
        st.metric("🥇 Top Paid Role", top_role.get('job_title_normalized', 'N/A'), f"₹{top_role.get('salary_avg', 0):,.2f} Avg")
    with col2:
        st.metric("🔥 Most Active Role", highest_demand.get('job_title_normalized', 'N/A'), f"{highest_demand.get('job_count', 0):,} Jobs")
    with col3:
        st.metric("📊 Total High-Pay Jobs", f"{top_roles_df['job_count'].sum():,} Openings")

    st.markdown("---")

    fig = px.bar(
        top_roles_df.sort_values(by='salary_avg', ascending=True),
        x='salary_avg',
        y='job_title_normalized',
        orientation='h',
        text='salary_avg',
        title="<b>Top 10 High Paying Roles by Average Salary</b>",
        labels={'salary_avg': 'Average Salary (₹)', 'job_title_normalized': 'Job Role'},
        color='salary_avg',
        color_continuous_scale='Viridis'
    )

    fig.update_traces(
        texttemplate=' ₹%{text:,.0f}', 
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Avg Salary: ₹%{x:,.2f}<br>'
    )

    fig.update_layout(
        template='plotly_dark',
        height=480,
        margin=dict(l=20, r=40, t=50, b=20),
        xaxis_title="Average Salary (₹)",
        yaxis_title=None,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💼 Top High Paying Job Roles Breakdown")

    display_df = top_roles_df[['rank', 'job_title_normalized', 'salary_avg', 'salary_median', 'job_count', 'salary_range']].copy()
    
    styled_df = display_df.style.format({
        'salary_avg': '₹{:,.2f}',
        'salary_median': '₹{:,.2f}',
        'job_count': '{:,}'
    })

    st.dataframe(
        styled_df,
        column_config={
            "rank": "Rank",
            "job_title_normalized": "Job Title",
            "salary_avg": "Average Salary",
            "salary_median": "Median Salary",
            "job_count": "Job Openings",
            "salary_range": "Salary Range"
        },
        use_container_width=True,
        hide_index=True,
        height=380
    )

# # =========================================================
# SECTION 5: NETWORK SKILL ECOSYSTEM (FIXED)
# =========================================================
def render_skill_ecosystem_network():
    st.markdown("---")
    st.header("🕸️ Network Skill Ecosystem")
    st.markdown("Explore co-occurring skills, demand tiers, and skill clusters in interactive continuous 360° rotation.")

    col_net1, col_net2 = st.columns([3, 1])
    with col_net1:
        st.caption("💡 Hover or click any skill node to reveal connected skills & demand tier in the dark GUI panel.")
    with col_net2:
        net_skills_count = st.slider("Max Skill Nodes:", min_value=10, max_value=40, value=22, key="network_nodes_slider")

    network_html = None
    
    # Attempt 1: Fetch via API Client
    if hasattr(api, 'get_skill_network_html'):
        try:
            network_html = api.get_skill_network_html(top_n=net_skills_count)
        except Exception:
            network_html = None

    # Attempt 2: Direct Local Backend Imports (Multi-fallback for imports)
    if not network_html:
        try:
            import data_loader as dl
            network_html = dl.get_skill_network_html(top_n_skills=net_skills_count)
        except Exception:
            try:
                from backend import data_loader as dl
                network_html = dl.get_skill_network_html(top_n_skills=net_skills_count)
            except Exception as e:
                st.error(f"⚠️ Unable to render Skill Ecosystem Network: {e}")

    if network_html:
        components.html(network_html, height=640, scrolling=False)

# Explicit Execution
render_top_high_paying_roles_section()
render_skill_ecosystem_network()