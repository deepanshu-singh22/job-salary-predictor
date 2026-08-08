
# import os
# import sys

# # Ensure backend and parent directories are in sys.path
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PARENT_DIR = os.path.dirname(CURRENT_DIR)

# if CURRENT_DIR not in sys.path:
#     sys.path.insert(0, CURRENT_DIR)
# if PARENT_DIR not in sys.path:
#     sys.path.insert(0, PARENT_DIR)


# from fastapi import FastAPI, Query, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from data_loader import get_top_hiring_locations
# from data_loader import get_top_high_paying_roles
# import data_loader as dl

# # from fastapi import FastAPI, Query
# from fastapi.responses import HTMLResponse

# app = FastAPI(title="Job Market Analysis API")

# # CORS setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {"message": "API Running Successfully!"}

# # 1. Top Skills Endpoint
# @app.get("/api/skills/top")
# def get_top_skills(n: int = 10):
#     df = dl.get_skill_counts().head(n)
#     return df.to_dict(orient="records")

# # 2. Overview Stats Endpoint
# @app.get("/api/overview")
# def get_overview():
#     try:
#         stats = dl.get_overview_stats()
#         return stats
#     except Exception:
#         df = dl.get_df()
#         return {
#             "total_jobs": len(df),
#             "total_skills": len(dl.get_skill_counts())
#         }

# # 3. FIXED: Unique Job Roles Endpoint (Jo 404 de raha tha)
# @app.get("/api/job-roles")
# def get_job_roles():
#     roles = dl.get_unique_job_roles()
#     return {"job_roles": roles}

# # 4. FIXED: Skills by Role Endpoint
# @app.get("/api/skills/by-role")
# def get_skills_by_role(role: str = Query(...), top_n: int = Query(5), n: int = Query(None)):
#     # Agar frontend 'n' ya 'top_n' me se koi bhi bheje, handle ho jayega
#     limit = n if n is not None else top_n
#     result = dl.get_skills_by_job_role(job_role=role, top_n=limit)
#     return result.to_dict(orient="records")






# @app.get("/api/locations/top")
# def read_top_locations(top_n: int = 20):
#     df = get_top_hiring_locations(top_n=top_n)
#     return df.to_dict(orient="records")



# @app.get("/api/roles/top-paying")
# def read_top_high_paying_roles(top_n: int = 10, min_job_count: int = 1):
#     """Fetch Top High Paying Roles directly from data_loader"""
#     try:
#         # Call the new function from data_loader.py
#         roles_df = get_top_high_paying_roles(top_n=top_n, min_job_count=min_job_count)
        
#         if roles_df is None or roles_df.empty:
#             return []
            
#         return roles_df.to_dict(orient="records")
#     except Exception as e:
#         print(f"Error processing high paying roles: {e}")
#         return []

# from fastapi import FastAPI, Query
# from fastapi.responses import HTMLResponse

# # @app.get("/api/skills/network", response_class=HTMLResponse)
# @app.get("/api/skills/network", response_class=HTMLResponse)
# def get_skill_network(top_n: int = Query(default=22, ge=5, le=50)):
#     """
#     Skill Ecosystem Network Graph ka interactive HTML return karta hai.
#     """
#     try:
#         # Fallback handling for module imports
#         try:
#             import data_loader as dl
#         except ModuleNotFoundError:
#             from backend import data_loader as dl

#         # Function call check
#         if hasattr(dl, 'get_skill_network_html'):
#             html_content = dl.get_skill_network_html(top_n_skills=top_n)
#         else:
#             return HTMLResponse(
#                 content="<h3 style='color: orange;'>'get_skill_network_html' function data_loader.py me nahi milaa.</h3>",
#                 status_code=500
#             )

#         if html_content:
#             return HTMLResponse(content=html_content, status_code=200)
#         else:
#             return HTMLResponse(
#                 content="<h3 style='color: white;'>Graph data render nahi ho saka.</h3>", 
#                 status_code=404
#             )

#     except Exception as e:
#         return HTMLResponse(
#             content=f"<h3 style='color: red;'>Backend Network Graph Error: {str(e)}</h3>", 
#             status_code=500
#         )




# # 7. AI Resume Salary Prediction Endpoint
# @app.post("/api/predict-salary")
# async def predict_salary_endpoint(
#     target_role: str = Form(...),
#     location: str = Form(...),
#     file: UploadFile = File(...)
# ):
#     try:
#         pdf_bytes = await file.read()
#         resume_text = extract_text_from_pdf(pdf_bytes)

#         if not resume_text:
#             return {"status": "error", "message": "PDF se text read nahi ho paya. Valid PDF upload karein."}

#         # Real-time Prediction via Groq AI Engine
#         result = predict_salary_from_resume(
#             resume_text=resume_text,
#             target_role=target_role,
#             location=location
#         )

#         return {"status": "success", "data": result}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}




import os
import sys

# Ensure backend and parent directories are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from fastapi import FastAPI, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from pydantic import BaseModel  # <-- Fix 1
from typing import List

from data_loader import get_top_hiring_locations, get_top_high_paying_roles
import data_loader as dl

# 🔴 FIX: Missing Imports Add Kiye Hain Yahan
from resume_parser import extract_text_from_pdf
from salary_engine import predict_salary_from_resume

app = FastAPI(title="Job Market Analysis API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🟢 FIX: SkillGapRequest Class Yahan Add Ho Gayi Hai
class SkillGapRequest(BaseModel):
    target_role: str
    user_skills: List[str]

@app.get("/")
def home():
    return {"message": "API Running Successfully!"}

# 1. Top Skills Endpoint
@app.get("/api/skills/top")
def get_top_skills(n: int = 10):
    df = dl.get_skill_counts().head(n)
    return df.to_dict(orient="records")

# 2. Overview Stats Endpoint
@app.get("/api/overview")
def get_overview():
    try:
        stats = dl.get_overview_stats()
        return stats
    except Exception:
        df = dl.get_df()
        return {
            "total_jobs": len(df),
            "total_skills": len(dl.get_skill_counts())
        }

# 3. Unique Job Roles Endpoint
@app.get("/api/job-roles")
def get_job_roles():
    roles = dl.get_unique_job_roles()
    return {"job_roles": roles}

# 4. Skills by Role Endpoint
@app.get("/api/skills/by-role")
def get_skills_by_role(role: str = Query(...), top_n: int = Query(5), n: int = Query(None)):
    limit = n if n is not None else top_n
    result = dl.get_skills_by_job_role(job_role=role, top_n=limit)
    return result.to_dict(orient="records")

# 5. Top Locations Endpoint
@app.get("/api/locations/top")
def read_top_locations(top_n: int = 20):
    df = get_top_hiring_locations(top_n=top_n)
    return df.to_dict(orient="records")

# 6. Top High Paying Roles Endpoint
@app.get("/api/roles/top-paying")
def read_top_high_paying_roles(top_n: int = 10, min_job_count: int = 1):
    try:
        roles_df = get_top_high_paying_roles(top_n=top_n, min_job_count=min_job_count)
        if roles_df is None or roles_df.empty:
            return []
        return roles_df.to_dict(orient="records")
    except Exception as e:
        print(f"Error processing high paying roles: {e}")
        return []

# 7. Skill Network Graph Endpoint
@app.get("/api/skills/network", response_class=HTMLResponse)
def get_skill_network(top_n: int = Query(default=22, ge=5, le=50)):
    try:
        if hasattr(dl, 'get_skill_network_html'):
            html_content = dl.get_skill_network_html(top_n_skills=top_n)
            if html_content:
                return HTMLResponse(content=html_content, status_code=200)
        return HTMLResponse(content="<h3>Graph data unavailable</h3>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>", status_code=500)

# 8. AI Resume Salary Prediction Endpoint
@app.post("/api/predict-salary")
async def predict_salary_endpoint(
    target_role: str = Form(...),
    location: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)

        if not resume_text or len(resume_text.strip()) == 0:
            return {"status": "error", "message": "PDF se text read nahi ho paya. Valid Text PDF upload karein."}

        # Real-time Prediction via Groq AI Engine
        result = predict_salary_from_resume(
            resume_text=resume_text,
            target_role=target_role,
            location=location
        )

        if not result:
            return {"status": "error", "message": "Groq AI prediction return karne me fail ho gaya."}

        return {"status": "success", "data": result}
    except Exception as e:
        print(f"❌ Backend Prediction Route Error: {e}")
        return {"status": "error", "message": str(e)}


# 9. 🎯 PAGE 5: Skill Gap Analyzer Endpoint
@app.post("/api/skills/gap-analysis")
def calculate_skill_gap(req: SkillGapRequest):
    try:
        # Fetch Top 10 skills for the requested role
        top_skills_df = dl.get_skills_by_job_role(job_role=req.target_role, top_n=10)

        if top_skills_df.empty:
            return {
                "status": "error",
                "message": f"No data found for target role: {req.target_role}"
            }

        user_skills_clean = [s.strip().lower() for s in req.user_skills if s.strip()]

        top_skills_df['skill_lower'] = top_skills_df['skill'].str.lower()
        top_skills_df['user_has'] = top_skills_df['skill_lower'].isin(user_skills_clean)

        sum_user_freq = top_skills_df[top_skills_df['user_has']]['count'].sum()
        sum_total_freq = top_skills_df['count'].sum()

        # Weighted Score Calculation
        match_score = round((sum_user_freq / sum_total_freq * 100), 1) if sum_total_freq > 0 else 0.0

        max_count = top_skills_df['count'].max()

        def set_priority(count):
            ratio = count / max_count if max_count > 0 else 0
            if ratio >= 0.65:
                return "HIGH"
            elif ratio >= 0.35:
                return "MEDIUM"
            else:
                return "LOW"

        top_skills_df['priority_level'] = top_skills_df['count'].apply(set_priority)

        return {
            "status": "success",
            "target_role": req.target_role,
            "match_score_percentage": match_score,
            "top_skills": top_skills_df.to_dict(orient="records")
        }
    except Exception as e:
        print(f"❌ Error calculating skill gap: {e}")
        return {"status": "error", "message": str(e)}
    
    

# Pydantic Model for Job Recommendation Request
class JobRecommendationRequest(BaseModel):
    user_skills: List[str]
    preferred_location: str = "All"
    top_n: int = 10


# 🎯 10. Job Recommendation System Endpoint
@app.post("/api/jobs/recommend")
def recommend_jobs(req: JobRecommendationRequest):
    try:
        df = dl.get_df().copy()
        
        if df.empty:
            return {"status": "error", "message": "Dataset empty hai."}

        user_skills_clean = set(s.strip().lower() for s in req.user_skills if s.strip())

        if not user_skills_clean:
            return {"status": "error", "message": "At least ek skill enter kijiye."}

        # Location Filter (agar "All" na ho)
        if req.preferred_location and req.preferred_location.lower() != "all":
            df = df[df['location'].str.contains(req.preferred_location, case=False, na=False)]

        if df.empty:
            return {"status": "success", "recommended_jobs": []}

        # Skill Matching Score Logic
        def calculate_match(job_skills):
            if not isinstance(job_skills, str):
                return 0.0
            
            job_skills_list = [s.strip().lower() for s in job_skills.split(",")]
            matched = set(job_skills_list).intersection(user_skills_clean)
            
            if not job_skills_list:
                return 0.0
            
            # Match score percentage based on user skill overlap
            score = (len(matched) / len(user_skills_clean)) * 100
            return round(score, 1)

        # Assuming 'skills' column exists in dataset
        if 'skills' in df.columns:
            df['match_score'] = df['skills'].apply(calculate_match)
        else:
            df['match_score'] = 0.0

        # Sort by Match Score
        recommended_df = df.sort_values(by="match_score", ascending=False).head(req.top_n)

        # Select relevant columns safely
        cols_to_return = [col for col in ['job_title', 'company_name', 'location', 'skills', 'salary_avg', 'match_score'] if col in recommended_df.columns]
        
        return {
            "status": "success",
            "recommended_jobs": recommended_df[cols_to_return].to_dict(orient="records")
        }

    except Exception as e:
        print(f"❌ Error in job recommendation: {e}")
        return {"status": "error", "message": str(e)}