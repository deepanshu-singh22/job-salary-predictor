import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM CSS FOR PREMIUM UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Model Diagnostics & Performance",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for UI Enhancement
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 14px;
        color: #94A3B8;
    }
    /* Tab Container Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #0F172A;
        border-radius: 8px 8px 0px 0px;
        padding-x: 20px;
    }
    /* Highlight Markdown Tables */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. HEADER & TOP METRICS CARDS
# ---------------------------------------------------------
st.title("⚡ Model Diagnostic & Performance Dashboard")
st.caption("Deep-dive Analysis, Root Cause Diagnosis & Hyperparameter Tuning Performance")

st.write("")

# 4 Core Highlight Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">🏆 Best Overall Regressor</div>
        <div class="metric-value">Random Forest</div>
        <span style="color: #4ADE80; font-size: 12px;">R² = 0.4499 (+51.4% Jump)</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">🎯 Best Overall Classifier</div>
        <div class="metric-value">XGBoost</div>
        <span style="color: #4ADE80; font-size: 12px;">Accuracy = 82.66%</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">📉 Max Error Reduction</div>
        <div class="metric-value">7.59 LPA</div>
        <span style="color: #38BDF8; font-size: 12px;">Decision Tree RMSE Dropped</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">🛠️ Tuning Recovery</div>
        <div class="metric-value">-1.54 ➔ +0.42</div>
        <span style="color: #4ADE80; font-size: 12px;">Overfitted Tree Fixed</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()
import os
import streamlit as st
# ---------------------------------------------------------
# 3. HELPER FUNCTION TO LOAD MARKDOWN (SMART MATCHING FIX)
# ---------------------------------------------------------
def load_markdown_file(filename):
    CURRENT_FILE_PATH = os.path.abspath(__file__)
    dir_pointer = os.path.dirname(CURRENT_FILE_PATH)
    
    # Strip extension (e.g. 'Linear_Models_Report')
    base_name = os.path.splitext(filename)[0]
    
    for _ in range(5):
        for sub_dir in ["data", "docx", ""]:
            folder = os.path.join(dir_pointer, sub_dir)
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    # Exact match OR starts with base_name (e.g., 'Linear_Models_Report (1).md')
                    if f == filename or (f.startswith(base_name) and f.endswith(".md")):
                        full_path = os.path.join(folder, f)
                        try:
                            with open(full_path, "r", encoding="utf-8") as file:
                                return file.read()
                        except Exception as e:
                            st.error(f"Error reading file: {e}")
                            return None
                            
        parent = os.path.dirname(dir_pointer)
        if parent == dir_pointer:
            break
        dir_pointer = parent

    st.error(f"❌ File '{filename}' nahi mili!")
    return None


    # Fallback paths (just in case terminal running location is different)
    fallback_paths = [
        os.path.join(os.getcwd(), "data", filename),
        os.path.join("data", filename),
        filename
    ]
    
    for path in fallback_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
                
    return None

# ---------------------------------------------------------
# 4. TAB NAVIGATION
# ---------------------------------------------------------
tab_leaderboard, tab_linear, tab_trees = st.tabs([
    "📊 Leaderboard & Interactive Comparison", 
    "📈 Linear Family Report", 
    "🌲 Tree & Boosting Family Report"
])

# =========================================================
# TAB 1: VISUAL LEADERBOARD & COMPARISON
# =========================================================
with tab_leaderboard:
    st.subheader("📌 Regressor Models Performance ($R^2$ Jump Comparison)")
    
    # Regression Data Frame
    reg_data = pd.DataFrame({
        "Model": ["Decision Tree", "Random Forest", "LightGBM", "MLP Neural Net", "Linear Regression", "Ridge", "Lasso", "Linear SVR", "KNN"],
        "Baseline R2": [-1.5475, -0.0642, 0.4634, 0.4772, 0.4262, 0.4262, 0.4073, 0.3794, 0.3740],
        "Tuned R2": [0.4282, 0.4499, 0.4432, 0.3985, 0.3884, 0.3884, 0.3884, 0.3623, 0.3731]
    })
    
    # Plotly Grouped Bar Chart
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Bar(
        x=reg_data["Model"], 
        y=reg_data["Baseline R2"], 
        name="Baseline R²", 
        marker_color="#EF4444"
    ))
    fig_reg.add_trace(go.Bar(
        x=reg_data["Model"], 
        y=reg_data["Tuned R2"], 
        name="Tuned / Scaled R²", 
        marker_color="#10B981"
    ))
    
    fig_reg.update_layout(
        barmode='group',
        title="Baseline vs Tuned R² Score (Higher is Better)",
        xaxis_title="Algorithms",
        yaxis_title="R² Score",
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig_reg, use_container_width=True)

    col_df1, col_df2 = st.columns(2)
    
    with col_df1:
        st.write("### 📜 Regression Summary Table")
        st.dataframe(reg_data.style.highlight_max(subset=["Tuned R2"], color="#15803D"), use_container_width=True)
        
    with col_df2:
        st.write("### 🎯 Classification Summary Table")
        cls_data = pd.DataFrame({
            "Model": ["XGBoost", "Random Forest", "Decision Tree", "Linear SVC", "Logistic Regression", "MLP Neural Net"],
            "Baseline Acc (%)": [82.60, 82.48, 80.11, 81.91, 82.01, 81.10],
            "Tuned Acc (%)": [82.66, 82.05, 81.45, 81.93, 81.91, 81.02]
        })
        st.dataframe(cls_data.style.highlight_max(subset=["Tuned Acc (%)"], color="#15803D"), use_container_width=True)

# =========================================================
# TAB 2: LINEAR MODELS REPORT
# =========================================================
with tab_linear:
    report_1 = load_markdown_file("Linear_Models_Report.md")
    if report_1:
        st.markdown(report_1)
    else:
        st.warning("⚠️ `Linear_Models_Report.md` file nahi mili! Kripya check karein ki file root folder ya `data/` directory me saved hai.")

# =========================================================
# TAB 3: TREE & BOOSTING REPORT
# =========================================================
with tab_trees:
    report_2 = load_markdown_file("Tree_Boosting_Other_Models_Report.md")
    if report_2:
        st.markdown(report_2)
    else:
        st.warning("⚠️ `Tree_Boosting_Other_Models_Report.md` file nahi mili! Kripya check karein ki file root folder ya `data/` directory me saved hai.")