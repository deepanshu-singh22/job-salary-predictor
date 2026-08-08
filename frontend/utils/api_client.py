"""
Thin wrapper around the FastAPI backend so pages don't repeat requests logic.
Change API_BASE_URL if your backend runs on a different host/port.
"""

import os
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL", "https://job-salary-predictor-backend.onrender.com")


def _get(path: str, params: dict | None = None):
    try:
        # Clean path & URL joining
        url = f"{API_BASE_URL}{path}"
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "⚠️ Backend se connect nahi ho paya. Kya FastAPI server chal raha hai? "
            "`uvicorn main:app --reload --port 8000`"
        )
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"API error: {e}")
        st.stop()

# 🟢 FIXED: Added missing get_overview_stats function
@st.cache_data(ttl=60)
def get_overview_stats() -> dict:
    return _get("/api/overview")


@st.cache_data(ttl=60)
def get_overview() -> dict:
    return _get("/api/overview")


@st.cache_data(ttl=60)
def get_top_skills(n: int = 10) -> pd.DataFrame:
    data = _get("/api/skills/top", {"n": n})
    return pd.DataFrame(data) if data else pd.DataFrame()


@st.cache_data(ttl=60)
def get_job_roles() -> list:
    """Fetches unique normalized job roles for the dropdown."""
    data = _get("/api/job-roles")
    if isinstance(data, dict):
        return data.get("job_roles", [])
    return []


@st.cache_data(ttl=60)
def get_skills_by_role(role: str, top_n: int = 10) -> pd.DataFrame:
    """Fetches top skills for a specific selected job role."""
    data = _get("/api/skills/by-role", {"role": role, "top_n": top_n})
    if data:
        return pd.DataFrame(data)
    return pd.DataFrame()


@st.cache_data(ttl=60)
def get_top_locations(top_n=20):
    """Fetch top hiring locations from FastAPI backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/locations/top", params={"top_n": top_n})
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching locations: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def get_top_high_paying_roles(top_n=10):
    """Fetch Top High Paying Roles from FastAPI backend with Fallback Sample Data"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/roles/top-paying", params={"top_n": top_n}, timeout=3)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        print(f"Error fetching top paying roles: {e}")

    # Fallback Sample Data if API fails
    sample_roles = [
        {"rank": 1, "job_title_normalized": "Data Engineer", "salary_avg": 530532.67, "salary_median": 0.0, "job_count": 1056, "salary_range": "₹0.0 - ₹7,000,000.0"},
        {"rank": 2, "job_title_normalized": "Finance & Accounting", "salary_avg": 308647.51, "salary_median": 0.0, "job_count": 1905, "salary_range": "₹0.0 - ₹30,000,000.0"},
        {"rank": 3, "job_title_normalized": "DevOps & Cloud Architect", "salary_avg": 285351.53, "salary_median": 0.0, "job_count": 3361, "salary_range": "₹0.0 - ₹6,500,000.0"},
        {"rank": 4, "job_title_normalized": "Sales & Business Development", "salary_avg": 281978.09, "salary_median": 112500.0, "job_count": 8067, "salary_range": "₹0.0 - ₹10,000,000.0"},
        {"rank": 5, "job_title_normalized": "Product & Project Management", "salary_avg": 278904.44, "salary_median": 0.0, "job_count": 8565, "salary_range": "₹0.0 - ₹95,000,000.0"},
        {"rank": 6, "job_title_normalized": "AI / ML Engineer", "salary_avg": 272815.03, "salary_median": 0.0, "job_count": 5556, "salary_range": "₹0.0 - ₹30,000,000.0"},
        {"rank": 7, "job_title_normalized": "Data Scientist", "salary_avg": 267852.35, "salary_median": 0.0, "job_count": 447, "salary_range": "₹0.0 - ₹8,000,000.0"},
        {"rank": 8, "job_title_normalized": "HR & Recruitment", "salary_avg": 264700.77, "salary_median": 0.0, "job_count": 2077, "salary_range": "₹0.0 - ₹15,000,000.0"},
        {"rank": 9, "job_title_normalized": "Data / Business Analyst", "salary_avg": 212008.20, "salary_median": 0.0, "job_count": 1037, "salary_range": "₹0.0 - ₹5,500,000.0"},
        {"rank": 10, "job_title_normalized": "Other", "salary_avg": 200500.57, "salary_median": 0.0, "job_count": 30483, "salary_range": "₹0.0 - ₹30,000,000.0"}
    ]
    return pd.DataFrame(sample_roles)


def get_skill_network_html(top_n=22):
    try:
        res = requests.get(f"{API_BASE_URL}/api/skills/network?top_n_skills={top_n}")
        if res.status_code == 200:
            return res.text
    except Exception as e:
        print(f"Error fetching skill network HTML: {e}")
    return None


def get_salary_prediction(file_bytes, filename: str, target_role: str, location: str):
    """FastAPI Backend `/api/predict-salary` ko Uploaded PDF bhejta hai."""
    try:
        files = {"file": (filename, file_bytes, "application/pdf")}
        data = {"target_role": target_role, "location": location}

        response = requests.post(f"{API_BASE_URL}/api/predict-salary", files=files, data=data, timeout=60)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error Code: {response.status_code}, Detail: {response.text}")
            return {"status": "error", "message": f"Server Error ({response.status_code})"}
    except Exception as e:
        print(f"API Exception Error: {e}")
        return {"status": "error", "message": str(e)}
    



# ==========================================
# 🎯 9. Skill Gap Analysis Endpoint Wrapper
# ==========================================
@st.cache_data(ttl=60)
def get_skill_gap_analysis(target_role: str, user_skills: list) -> dict:
    """
    Sends target role and user skills to FastAPI backend 
    and returns weighted match score & priority levels.
    """
    try:
        payload = {
            "target_role": target_role,
            "user_skills": user_skills
        }
        url = f"{API_BASE_URL}/api/skills/gap-analysis"
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error ({response.status_code}): {response.text}")
            return {"status": "error", "message": f"Server Error {response.status_code}"}
            
    except Exception as e:
        print(f"Error fetching skill gap analysis: {e}")
        return {"status": "error", "message": str(e)}
    

# 🎯 10. Job Recommendation System Wrapper
@st.cache_data(ttl=60)
def get_job_recommendations(user_skills: list, preferred_location: str = "All", top_n: int = 10) -> dict:
    """Sends user skills and preferred location to backend for job recommendations."""
    try:
        payload = {
            "user_skills": user_skills,
            "preferred_location": preferred_location,
            "top_n": top_n
        }
        response = requests.post(f"{API_BASE_URL}/api/jobs/recommend", json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"Server Error ({response.status_code})"}
    except Exception as e:
        print(f"Error fetching job recommendations: {e}")
        return {"status": "error", "message": str(e)}