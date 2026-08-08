import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Market Trends Analysis", layout="wide")

st.title("📈 Market Trends Analysis")
st.header("Most Demanding Skills")

top_n = st.slider("Kitni top skills dikhani hain?", min_value=5, max_value=20, value=10)

try:
    response = requests.get(f"http://127.0.0.1:8000/api/skills/top?n={top_n}")
    
    if response.status_code == 200:
        data = response.json()
        df_skills = pd.DataFrame(data)

        if not df_skills.empty and "skill_name" in df_skills.columns:
            def format_k(val):
                return f"{val/1000:.1f}k" if val >= 1000 else str(val)

            df_skills["display_count"] = df_skills["frequency_count"].apply(format_k)

            fig = px.bar(
                df_skills,
                x="skill_name",
                y="frequency_count",
                color="frequency_count",
                text="display_count",
                title="🔥 Interactive Top Skills Demand",
                labels={"skill_name": "", "frequency_count": "Frequency Count"},
                color_continuous_scale="Viridis",
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(tickangle=-45),
                height=550,
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Skills data nahi mila.")
    else:
        st.error("Backend se connection fail ho gaya.")
except Exception as e:
    st.error(f"Error: {e}")