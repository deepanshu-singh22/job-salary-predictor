import os

# Base directory (backend folder) ka path dynamically set karein:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute Path set karein taaki Render/Streamlit kahin se bhi file dhoond sake
DATA_PATH = os.environ.get("DATA_PATH", os.path.join(BASE_DIR, "jobs_dataset_final.csv"))
ROLE_SKILLS_DATA_PATH = DATA_PATH

# Logical name -> actual column name in your CSV
COLUMNS = {
    "job_id": "job_id",
    "title": "job_title",
    "job_title_normalized": "job_title_normalized",
    "companyName": "company_name",
    "company_size": "company_size",
    "location": "location",
    "minimumExperience": "min_experience",
    "maximumExperience": "max_experience",
    "minimumSalary": "salary_min",
    "maximumSalary": "salary_max",
    "salary_avg": "salary_avg",
    "tagsAndSkills": "skills",  # Main skills column
    "work_type": "work_type",
    "jobDescription": "job_description",
    "jobUploaded": "job_uploaded"
}

CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "0"))