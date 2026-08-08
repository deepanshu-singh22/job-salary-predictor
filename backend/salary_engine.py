
import json
import os
from groq import Groq
from dotenv import load_dotenv  # 👈 Ye add karein

# .env file se variables load karein
load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

def predict_salary_from_resume(resume_text: str, target_role: str, location: str) -> dict:
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
    Act as a Tech HR, AI Career Advisor, and Salary Analyst for the 2026 Indian Tech Market.
    Analyze the following resume text for Target Role: '{target_role}' in Location: '{location}'.

    RESUME TEXT:
    \"\"\"{resume_text[:3000]}\"\"\"

    Task:
    1. Extract actual experience (in years) and skills from resume.
    2. Perform mismatch check between resume skills and target role '{target_role}'.
    3. Predict current realistic market salary (min, max, avg in LPA).
    4. Provide Experience-Based Future Salary Projections.
    5. Identify 4-5 missing high-impact skills for '{target_role}' that candidate lacks. Simulate the potential salary lift for adding EACH missing skill (predicted_salary_after_skill, salary_increase_amount, salary_increase_percentage, learning_difficulty, estimated_learning_time, learning_resources).

    Return ONLY STRICT VALID JSON with NO markdown blocks or prose:
    {{
      "candidate_experience_years": 1.5,
      "detected_skills": ["Python", "SQL", "Pandas"],
      "predicted_salary_avg_lpa": 10.5,
      "salary_range_min_lpa": 8.0,
      "salary_range_max_lpa": 13.0,
      "confidence_score": 0.75,
      "role_mismatch": true,
      "mismatch_reason": "Your resume leans heavily on Data Science, but target role is Frontend Developer.",
      "experience_projections": [
         {{"experience_tier": "Current", "expected_salary": "₹10.5 LPA", "growth_percent": "Base"}},
         {{"experience_tier": "3 Years Exp", "expected_salary": "₹15.0 - 18.0 LPA", "growth_percent": "+45%"}},
         {{"experience_tier": "5 Years Exp", "expected_salary": "₹22.0 - 28.0 LPA", "growth_percent": "+110%"}},
         {{"experience_tier": "8+ Years (Lead/Architect)", "expected_salary": "₹35.0 - 45.0 LPA", "growth_percent": "+230%"}}
      ],
      "hiring_company_types": [
         {{"type": "Early-stage Startups", "pay_range": "₹8-12 LPA"}},
         {{"type": "Mid-sized Product Firms", "pay_range": "₹10-14 LPA"}},
         {{"type": "Service-based Companies", "pay_range": "₹7-11 LPA"}}
      ],
      "salary_booster_skills": ["React", "TypeScript", "System Design"],
      "skill_recommendations": [
         {{
           "recommended_skill": "AWS Cloud",
           "skill_demand_percentage": 65,
           "predicted_salary_after_skill": 12.2,
           "salary_increase_amount": 1.7,
           "salary_increase_percentage": 16.2,
           "learning_difficulty": "Medium",
           "estimated_learning_time": "4-6 weeks",
           "learning_resources": "AWS Certified Solutions Architect Course (Udemy/Coursera)"
         }},
         {{
           "recommended_skill": "Docker & Kubernetes",
           "skill_demand_percentage": 52,
           "predicted_salary_after_skill": 11.5,
           "salary_increase_amount": 1.0,
           "salary_increase_percentage": 9.5,
           "learning_difficulty": "Medium",
           "estimated_learning_time": "3-4 weeks",
           "learning_resources": "Docker & Kubernetes Bootcamp (FreeCodeCamp/Udemy)"
         }}
      ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        raw_content = response.choices[0].message.content.strip()

        if raw_content.startswith("```"):
            raw_content = raw_content.strip("`").replace("json\n", "", 1).strip()

        data = json.loads(raw_content)
        return data
    except Exception as e:
        print(f"❌ Groq API Execution Error: {e}")
        return {}