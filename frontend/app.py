"""
Root entry point. Streamlit isko `streamlit run app.py` se chalata hai,
aur `pages/` folder ke andar ki saari files sidebar mein auto-list ho
jaati hain. Actual Home Page content pages/1_Home_Page.py mein hai.
"""

import streamlit as st

st.set_page_config(page_title="Job Market Intelligence", page_icon="📊", layout="wide")
st.switch_page("pages/1_Home_Page.py")