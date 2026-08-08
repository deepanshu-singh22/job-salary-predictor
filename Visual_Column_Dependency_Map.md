# 📊 VISUAL COLUMN DEPENDENCY MAP
## At a Glance - Which Columns You Need For What

---

## 🎯 THE BIG PICTURE

```
                    RAW DATA (CSV)
                        |
            ┌───────────┴────────────┐
            |                        |
       ┌────▼─────────┐      ┌──────▼──────┐
       │   CLEAN &    │      │   FEATURE   │
       │  NORMALIZE   │      │ ENGINEERING │
       └────┬─────────┘      └──────┬──────┘
            |                       |
            ├── Parse Skills ───────┤
            ├── Normalize Titles ───┤
            ├── Validate Salary ────┤
            └── Handle Nulls ───────┤
                                    |
                         ┌──────────▼──────────┐
                         │  PROCESSED DATA     │
                         │  (Ready for ML)     │
                         └──────────┬──────────┘
                                    |
        ┌───────────────┬───────────┼───────────┬───────────┐
        |               |           |           |           |
    ┌───▼────┐  ┌──────▼───┐ ┌────▼─────┐ ┌──▼──────┐ ┌──▼──────┐
    │ PAGE 1 │  │  PAGE 2  │ │ PAGE 3   │ │ PAGE 4  │ │ PAGE 5  │
    │ TRENDS │  │  SKILLS  │ │PREDICTOR │ │ MODELS  │ │ SKILL   │
    │        │  │          │ │          │ │ ANALYSIS│ │ GAP     │
    └────────┘  └──────────┘ └──────────┘ └─────────┘ └─────────┘
```

---

## 🔍 COLUMN REQUIREMENT BY FEATURE

### **FEATURE: Homepage Statistics Cards** 📊

```
┌─────────────────────────────────────────┐
│ "Total Jobs in Dataset"                 │
│ COUNT(job_id)                           │
│ ✅ NEED: job_id                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ "Average Salary"                        │
│ AVG(salary_avg)                         │
│ ✅ NEED: salary_avg                     │
│           salary_min + salary_max       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ "Total Unique Locations"                │
│ DISTINCT COUNT(location)                │
│ ✅ NEED: location                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ "Top Hiring City"                       │
│ MODE(city) or MOST FREQUENT(city)       │
│ ✅ NEED: city                           │
│           (or location if city not avail)│
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ "Most Demanded Skill"                   │
│ TOP 1 FROM required_skills frequency    │
│ ✅ NEED: required_skills                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ "Top Hiring Company"                    │
│ MOST FREQUENT(company_name)             │
│ ✅ NEED: company_name                   │
└─────────────────────────────────────────┘
```

### **FEATURE: Top 10 Most Demanding Skills** 📈

```
┌─────────────────────────────────────────────────┐
│ Data Processing Required:                       │
│                                                 │
│ 1. Parse required_skills string                 │
│    "Python,SQL,ML" → ["Python","SQL","ML"]     │
│                                                 │
│ 2. Count frequency in entire dataset            │
│    Python: 8500 occurrences                     │
│    SQL: 7800 occurrences                        │
│    ML: 5200 occurrences                         │
│                                                 │
│ 3. Calculate percentage                         │
│    Python: 8500/10000 = 85%                     │
│    SQL: 7800/10000 = 78%                        │
│                                                 │
│ 4. Sort descending & take top 10                │
│                                                 │
│ ✅ COLUMNS NEEDED: required_skills              │
│ ✅ OPTIONAL: job_id (for total count)           │
└─────────────────────────────────────────────────┘

Output Table:
┌────┬────────────┬───────────┬────────────┐
│Rank│Skill       │Frequency  │% of Jobs   │
├────┼────────────┼───────────┼────────────┤
│ 1  │Python      │8,500      │85%         │
│ 2  │SQL         │7,800      │78%         │
│ 3  │ML          │5,200      │52%         │
│ 4  │Pandas      │4,800      │48%         │
│ 5  │AWS         │4,200      │42%         │
└────┴────────────┴───────────┴────────────┘
```

### **FEATURE: Top Skills by Specific Job Role** 🎯

```
┌───────────────────────────────────────────────────────┐
│ User selects: "Data Scientist"                        │
│                                                       │
│ 1. Filter jobs                                       │
│    WHERE job_title_normalized = "Data Scientist"      │
│    Result: 450 matching jobs                          │
│                                                       │
│ 2. Extract all required_skills from these 450 jobs   │
│    [Python, SQL, ML, ...] [Python, ML, AWS, ...]    │
│                                                       │
│ 3. Count skill frequency among these 450             │
│    Python: 382/450 = 84.9%                            │
│    SQL: 351/450 = 78%                                 │
│    ML: 324/450 = 72%                                  │
│                                                       │
│ 4. Sort & display top 8-10                           │
│                                                       │
│ ✅ COLUMNS NEEDED:                                    │
│    - job_title_normalized (for filtering)            │
│    - required_skills (for skill extraction)           │
└───────────────────────────────────────────────────────┘

Output Table:
┌────┬────────────┬──────────────┬────────────────┐
│Rank│Skill       │Occurrences   │% for DS        │
├────┼────────────┼──────────────┼────────────────┤
│ 1  │Python      │382/450       │84.9%           │
│ 2  │SQL         │351/450       │78%             │
│ 3  │ML          │324/450       │72%             │
│ 4  │Statistics  │306/450       │68%             │
│ 5  │Pandas      │292/450       │64.9%           │
└────┴────────────┴──────────────┴────────────────┘
```

### **FEATURE: Top Hiring Locations (with Salary)** 🌍

```
┌──────────────────────────────────────────────┐
│ For each location:                           │
│                                              │
│ 1. Count total jobs                          │
│    Bangalore: COUNT = 45,000 jobs           │
│                                              │
│ 2. Calculate average salary                  │
│    Bangalore: AVG(salary_avg) = ₹13.2 LPA   │
│                                              │
│ 3. Calculate salary range                    │
│    Bangalore: MIN = ₹8 LPA, MAX = ₹25 LPA   │
│                                              │
│ 4. Sort by job count descending              │
│    Bangalore (45k) > Mumbai (38k) > ...      │
│                                              │
│ 5. Take top 15-20 locations                  │
│                                              │
│ ✅ COLUMNS NEEDED:                          │
│    - location (or city)                     │
│    - job_id (for counting)                  │
│    - salary_avg (for average)               │
│    - salary_min, salary_max (for range)     │
└──────────────────────────────────────────────┘

Output Table:
┌────┬──────────┬──────────┬────────────┬──────────────┐
│Rank│Location  │Jobs Count│Avg Salary  │Salary Range  │
├────┼──────────┼──────────┼────────────┼──────────────┤
│ 1  │Bangalore │45,000    │₹13.2 LPA   │₹8-25 LPA     │
│ 2  │Mumbai    │38,000    │₹12.8 LPA   │₹7-24 LPA     │
│ 3  │Delhi     │28,000    │₹12.1 LPA   │₹6-22 LPA     │
│ 4  │Hyderabad │32,000    │₹12.5 LPA   │₹7-23 LPA     │
│ 5  │Pune      │22,000    │₹11.9 LPA   │₹6-20 LPA     │
└────┴──────────┴──────────┴────────────┴──────────────┘

Visualization: 3D Bar Chart or Geospatial Heatmap
```

### **FEATURE: Top 10 High Paying Roles** 💰

```
┌──────────────────────────────────────────────┐
│ For each job role:                           │
│                                              │
│ 1. Group all jobs with same title            │
│    job_title_normalized = "ML Engineer"      │
│    Found: 1,500 jobs                         │
│                                              │
│ 2. Calculate salary statistics               │
│    Average: ₹19.8 LPA                        │
│    Median: ₹19.0 LPA                         │
│    Range: ₹14-28 LPA                         │
│                                              │
│ 3. Sort by average salary descending         │
│    Principal Data Scientist: ₹25.5 LPA      │
│    Senior ML Engineer: ₹19.8 LPA            │
│    Data Scientist: ₹12.5 LPA                │
│                                              │
│ 4. Take top 10 roles                         │
│                                              │
│ ✅ COLUMNS NEEDED:                          │
│    - job_title_normalized (for grouping)    │
│    - salary_avg (for average)               │
│    - salary_min, salary_max (for stats)     │
│    - job_id (for count)                     │
└──────────────────────────────────────────────┘

Output Table:
┌────┬──────────────────┬──────────┬───────────┬────────┐
│Rank│Job Title         │Avg Sal   │Median Sal │Count   │
├────┼──────────────────┼──────────┼───────────┼────────┤
│ 1  │Principal DS      │₹25.5 LPA │₹24.0 LPA  │342     │
│ 2  │ML Eng Manager    │₹22.1 LPA │₹21.0 LPA  │286     │
│ 3  │Senior ML Eng     │₹19.8 LPA │₹19.0 LPA  │1,240   │
│ 4  │Data Science Lead │₹19.2 LPA │₹18.5 LPA  │892     │
│ 5  │Cloud Architect   │₹18.9 LPA │₹18.0 LPA  │654     │
└────┴──────────────────┴──────────┴───────────┴────────┘
```

### **FEATURE: Skill Ecosystem Network Graph** 🕸️

```
┌────────────────────────────────────────────────┐
│ Building Co-Occurrence Matrix:                 │
│                                                │
│ For each job's required_skills:                │
│   Skills: [Python, SQL, ML]                    │
│   Create pairs: (Python-SQL), (Python-ML),     │
│                 (SQL-ML)                       │
│   Increment count for each pair                │
│                                                │
│ Job 1: [Python, SQL, ML, Pandas]              │
│   Pairs: P-S(+1), P-M(+1), P-Pa(+1),          │
│           S-M(+1), S-Pa(+1), M-Pa(+1)         │
│                                                │
│ Job 2: [Python, SQL, Java]                    │
│   Pairs: P-S(+1), P-J(+1), S-J(+1)            │
│                                                │
│ Result:                                        │
│   Python-SQL: 2 occurrences                    │
│   Python-ML: 1 occurrence                      │
│   ...                                          │
│                                                │
│ ✅ COLUMNS NEEDED:                            │
│    - required_skills (parse into array)       │
│    - job_id (optional, for normalization)     │
└────────────────────────────────────────────────┘

Network Structure:
{
  "nodes": [
    {"id": "Python", "frequency": 8500, "size": 85},
    {"id": "SQL", "frequency": 7800, "size": 78},
    {"id": "ML", "frequency": 5200, "size": 52},
    {"id": "AWS", "frequency": 4200, "size": 42},
    {"id": "Docker", "frequency": 3800, "size": 38}
  ],
  "edges": [
    {"source": "Python", "target": "SQL", "weight": 0.87},
    {"source": "Python", "target": "ML", "weight": 0.84},
    {"source": "Python", "target": "AWS", "weight": 0.65},
    {"source": "Docker", "target": "Kubernetes", "weight": 0.92},
    {"source": "AWS", "target": "Docker", "weight": 0.72}
  ]
}

Visualization: Interactive network graph with nodes (skills) 
and edges (co-occurrence relationships)
```

---

## 🤖 SALARY PREDICTOR - MOST COMPLEX

```
┌─────────────────────────────────────────────────────────┐
│ TRAINING PHASE                                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Input Data from ALL jobs:                              │
│                                                         │
│ RAW COLUMNS:                                            │
│ ├─ job_title_normalized → Feature                      │
│ ├─ required_experience → Feature                       │
│ ├─ location → Feature                                  │
│ ├─ required_skills → Feature (needs parsing!)         │
│ ├─ company_size → Feature                             │
│ ├─ work_type → Feature                                │
│ └─ salary_avg → TARGET VARIABLE                       │
│                                                         │
│ FEATURE ENGINEERING:                                    │
│ ├─ job_title_normalized                                │
│ │   └─ One-Hot Encode: [is_DS, is_ML, is_DA, ...]     │
│ │                                                      │
│ ├─ required_experience                                 │
│ │   └─ Already numeric, maybe add polynomial           │
│ │                                                      │
│ ├─ location                                            │
│ │   └─ One-Hot Encode: [is_bangalore, is_mumbai, ...]  │
│ │                                                      │
│ ├─ required_skills (COMPLEX!)                          │
│ │   Option 1: Count skills → 1 feature                │
│ │   Option 2: One-Hot top 50 skills → 50 features     │
│ │   Option 3: TF-IDF encode → dense vector            │
│ │   Option 4: Skill importance score → 1 feature      │
│ │                                                      │
│ ├─ company_size                                        │
│ │   └─ Encode: Small=0, Medium=1, Large=2             │
│ │                                                      │
│ └─ work_type                                           │
│    └─ One-Hot Encode: [is_remote, is_hybrid, is_on]    │
│                                                         │
│ FINAL FEATURE MATRIX:                                   │
│ Shape: (50000 jobs, 75 features)                        │
│                                                         │
│ Train 7 Models:                                         │
│ ├─ Linear Regression (R²: 0.62)                        │
│ ├─ Ridge (R²: 0.64)                                    │
│ ├─ Lasso (R²: 0.63)                                    │
│ ├─ Decision Tree (R²: 0.55, overfits)                 │
│ ├─ Random Forest (R²: 0.82)                            │
│ ├─ XGBoost (R²: 0.88) ← WINNER!                        │
│ └─ CatBoost (R²: 0.87)                                 │
│                                                         │
│ Save XGBoost Model → salary_model.pkl                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ PREDICTION PHASE (User Input)                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ User Inputs:                                            │
│ ├─ Job Title: "Data Scientist"                         │
│ ├─ Experience: 2 years                                 │
│ ├─ Location: "Bangalore"                               │
│ ├─ Skills: ["Python", "SQL", "ML", "Pandas"]          │
│ ├─ Company Size: "Large"                               │
│ └─ Work Type: "Hybrid"                                 │
│                                                         │
│ Transform inputs using same encoder as training:        │
│ ├─ job_title → [1,0,0,...] (one-hot)                   │
│ ├─ experience → 2 (numeric)                            │
│ ├─ location → [1,0,0,...] (one-hot)                    │
│ ├─ skills → [1,1,1,1,0,...] (top 50 skills encoding)   │
│ ├─ company_size → 2 (Large)                            │
│ └─ work_type → [0,1,0] (one-hot)                       │
│                                                         │
│ Load XGBoost Model & Predict:                           │
│ feature_vector → Model → PREDICTED SALARY              │
│ [1,0,0,...,2,...,1,0,0] → ₹12.8 LPA                    │
│                                                         │
│ Output:                                                 │
│ └─ Predicted Salary: ₹12.8 LPA                         │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ SKILL RECOMMENDATION PHASE                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. Get Top 10 Skills for "Data Scientist" Role         │
│    (from skill frequency in DS jobs)                   │
│    Python (85%), SQL (78%), ML (72%), ...             │
│                                                         │
│ 2. Identify Missing Skills from User's Profile         │
│    User has: Python, SQL, ML, Pandas                   │
│    Missing: Statistics, TensorFlow, AWS, Docker, ...   │
│                                                         │
│ 3. For Each Missing Skill:                             │
│    ├─ Add skill to user profile                        │
│    │  Modified: [Python, SQL, ML, Pandas, AWS]        │
│    │                                                   │
│    ├─ Transform: [1,0,0,...,2,...,1,1,0]              │
│    │  (AWS feature now = 1 instead of 0)              │
│    │                                                   │
│    ├─ Predict Salary: ₹14.2 LPA                       │
│    │  (was ₹12.8 without AWS)                         │
│    │                                                   │
│    └─ Calculate Increase:                             │
│       (14.2 - 12.8) / 12.8 × 100 = +10.9%             │
│                                                         │
│ 4. Repeat for All Missing Skills                       │
│    AWS: +10.9% (₹12.8 → ₹14.2)                        │
│    TensorFlow: +17% (₹12.8 → ₹15.0)                   │
│    Docker: +8.6% (₹12.8 → ₹13.9)                      │
│    Kubernetes: +13.3% (₹12.8 → ₹14.5)                 │
│                                                         │
│ 5. Rank by Salary Increase & Display Top 5             │
│                                                         │
│ ✅ COLUMNS NEEDED:                                     │
│    - job_title_normalized (to filter role's skills)   │
│    - required_skills (to find high-demand skills)     │
│    - salary_avg (for modeling)                        │
│    - ALL features used in model training              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 MODEL ANALYSIS & COMPARISON

```
┌────────────────────────────────────────────────┐
│ For Each Trained Model:                        │
│                                                │
│ Required Calculations:                         │
│ ├─ R² Score (from test predictions)           │
│ ├─ RMSE (Root Mean Squared Error)             │
│ ├─ MAE (Mean Absolute Error)                  │
│ ├─ MAPE (Mean Absolute Percentage Error)      │
│ ├─ Training Time (seconds)                    │
│ ├─ Prediction Time (ms per sample)            │
│ ├─ Model File Size (MB)                       │
│ └─ Cross-Validation Score (5-fold avg)        │
│                                                │
│ ✅ COLUMNS NEEDED:                            │
│    - All features (for model training)        │
│    - salary_avg (target variable)             │
│    - Test predictions (for scoring)           │
│    - y_test actual values (for comparison)    │
│                                                │
│ Output: Comparison table with visual analysis │
└────────────────────────────────────────────────┘

Model Comparison Table:
┌────────────────────┬────────┬──────┬─────┬──────────┬─────────┐
│ Model              │ R² Tst │ RMSE │ MAE │ Train tm │ Selected│
├────────────────────┼────────┼──────┼─────┼──────────┼─────────┤
│ Linear Regression  │ 0.62   │ 3.2L │ 2.1 │ 0.01s    │    ✗    │
│ Ridge              │ 0.64   │ 3.1L │ 2.0 │ 0.02s    │    ✗    │
│ Lasso              │ 0.63   │ 3.1L │ 2.1 │ 0.01s    │    ✗    │
│ Decision Tree      │ 0.55   │ 3.0L │ 1.9 │ 0.05s    │    ✗    │
│ Random Forest      │ 0.82   │ 1.8L │ 1.2 │ 12s      │    ✗    │
│ XGBoost (FINAL)    │ 0.88   │ 1.4L │ 0.9 │ 8s       │    ✅   │
│ CatBoost          │ 0.87   │ 1.5L │ 0.95│ 6s       │    -    │
└────────────────────┴────────┴──────┴─────┴──────────┴─────────┘
```

---

## 🎯 SKILL GAP ANALYZER

```
┌─────────────────────────────────────────┐
│ User Input: Job Role & Current Skills   │
├─────────────────────────────────────────┤
│                                         │
│ Job Role: "Data Scientist"              │
│ Current Skills: [Python, SQL, Git]      │
│                                         │
│ ✅ COLUMNS NEEDED:                     │
│    - job_title_normalized (to filter)  │
│    - required_skills (to extract)      │
│    - job_id (optional, for count)      │
│                                         │
│ Processing:                             │
│ 1. Filter: job_title_normalized        │
│    = "Data Scientist"                   │
│    → Found 450 DS jobs                 │
│                                         │
│ 2. Extract all required_skills          │
│    from these 450 jobs                  │
│                                         │
│ 3. Calculate skill frequency:           │
│    Python: 382/450 = 84.9%             │
│    SQL: 351/450 = 78%                  │
│    ML: 324/450 = 72%                   │
│    Statistics: 306/450 = 68%           │
│    Pandas: 292/450 = 64.9%             │
│    Scikit-learn: 270/450 = 60%         │
│    TensorFlow: 247/450 = 54.9%         │
│    Deep Learning: 234/450 = 52%        │
│    AWS: 225/450 = 50%                  │
│    Docker: 216/450 = 48%               │
│                                         │
│ 4. Identify Gaps:                       │
│    User has: Python (84.9%), SQL (78%)  │
│    User has: Git (frequency unknown)    │
│                                         │
│    User Missing:                        │
│    ✗ ML (72%)                          │
│    ✗ Statistics (68%)                  │
│    ✗ Pandas (64.9%)                    │
│    ✗ Scikit-learn (60%)                │
│    ✗ TensorFlow (54.9%)                │
│    ✗ Deep Learning (52%)               │
│    ✗ AWS (50%)                         │
│    ✗ Docker (48%)                      │
│                                         │
│ 5. Calculate Match Score:               │
│    Match = (User skills frequency sum)  │
│            / (Top 10 skills freq sum)   │
│          = (84.9 + 78 + 0 + 0 + 0      │
│             + 0 + 0 + 0 + 0 + 0)       │
│            / (84.9+78+72+68+64.9+60    │
│              +54.9+52+50+48)           │
│          = 162.9 / 632.8 × 100         │
│          = 25.7% (Low! Need skills)   │
│                                         │
│ Output: Show missing skills with        │
│         priority (based on frequency)   │
│         and learning recommendations    │
└─────────────────────────────────────────┘

Output Table:
┌────┬──────────────┬──────────┬──────────┐
│Rank│Skill         │Demand %  │Priority  │
├────┼──────────────┼──────────┼──────────┤
│ 1  │ML            │72%       │HIGH      │
│ 2  │Statistics    │68%       │HIGH      │
│ 3  │Pandas        │64.9%     │HIGH      │
│ 4  │Scikit-learn  │60%       │MEDIUM    │
│ 5  │TensorFlow    │54.9%     │MEDIUM    │
│ 6  │Deep Learning │52%       │MEDIUM    │
│ 7  │AWS           │50%       │LOW       │
│ 8  │Docker        │48%       │LOW       │
└────┴──────────────┴──────────┴──────────┘
```

---

## 💼 JOB RECOMMENDER (Optional)

```
┌──────────────────────────────────────────┐
│ User Input:                              │
│ ├─ Skills: [Python, SQL, ML, Pandas]    │
│ ├─ Experience: 2 years                  │
│ ├─ Preferred Location: Bangalore        │
│ ├─ Expected Salary: ₹12 LPA            │
│ └─ Work Type: Hybrid                    │
│                                          │
│ ✅ COLUMNS NEEDED:                      │
│    - job_id                             │
│    - job_title                          │
│    - job_description                    │
│    - required_skills                    │
│    - location                           │
│    - salary_avg                         │
│    - work_type                          │
│    - required_experience                │
│    - company_name                       │
│                                          │
│ Algorithm: TF-IDF + Cosine Similarity   │
│                                          │
│ Step 1: Vectorize All Jobs              │
│   Job 1 text: "Data Scientist Python    │
│    SQL ML AWS Docker..."                │
│   → TF-IDF Vector (1000 dimensions)    │
│                                          │
│ Step 2: Vectorize User Profile          │
│   User text: "Python SQL ML Pandas"     │
│   → TF-IDF Vector (same 1000 dims)     │
│                                          │
│ Step 3: Calculate Similarity             │
│   For each job:                         │
│   similarity = cosine(user_vec, job_vec)│
│   Range: 0 (no match) to 1 (perfect)   │
│                                          │
│   Job 1: 0.96 (96% match)              │
│   Job 2: 0.91 (91% match)              │
│   Job 3: 0.78 (78% match)              │
│                                          │
│ Step 4: Filter & Rank                   │
│   Filter by location, salary, exp       │
│   Sort by similarity score              │
│   Show top 5-10 jobs                    │
│                                          │
│ Output: Personalized job recommendations│
└──────────────────────────────────────────┘
```

---

## 📋 MINIMAL vs RECOMMENDED DATASET

### Minimal (Minimum 10 columns)
```
✅ job_id
✅ job_title
✅ job_title_normalized
✅ location
✅ required_experience
✅ required_skills
✅ salary_min
✅ salary_max
✅ company_size
✅ work_type
```

### Recommended (20+ columns)
```
✅ job_id
✅ job_title
✅ job_title_normalized
✅ company_name
✅ company_size
✅ industry
✅ location
✅ city
✅ state
✅ required_experience
✅ experience_level
✅ education_required
✅ required_skills
✅ preferred_skills
✅ salary_min
✅ salary_max
✅ salary_avg
✅ salary_currency
✅ salary_frequency
✅ work_type
✅ job_description
✅ job_posting_date
✅ job_posting_url
```

---

## 🎓 COLUMN PRIORITY MATRIX

```
┌─────────────────────┬────────┬────────┬────────┬────────┐
│ Column              │ Page 1 │ Page 2 │ Page 3 │ Page 5 │
├─────────────────────┼────────┼────────┼────────┼────────┤
│ job_id              │   ✓    │   ✓    │   ✓    │   ✓    │
│ job_title_norm      │   -    │   ✓    │   ✓    │   ✓    │
│ location            │   ✓    │   ✓    │   ✓    │   ✓    │
│ required_skills     │   ✓    │   ✓    │   ✓    │   ✓    │
│ required_exp        │   -    │   -    │   ✓    │   ✓    │
│ company_size        │   -    │   -    │   ✓    │   -    │
│ work_type           │   -    │   -    │   ✓    │   -    │
│ salary_avg/min/max  │   ✓    │   ✓    │   ✓    │   ✓    │
│ salary_currency     │   -    │   -    │   -    │   -    │
│ company_name        │   ✓    │   -    │   -    │   -    │
│ city/state          │   ✓    │   ✓    │   ✓    │   ✓    │
│ job_description     │   -    │   -    │   -    │   -    │
│ experience_level    │   -    │   -    │   -    │   ✓    │
│ job_posting_date    │   -    │   -    │   -    │   -    │
│ job_posting_url     │   -    │   -    │   -    │   -    │
└─────────────────────┴────────┴────────┴────────┴────────┘

Legend:
✓ = Definitely Need
- = Optional/Not Used
(Page 3 also needs salary_avg for model training)
(Page 4 is model analysis, doesn't need specific columns)
```

---

## ✅ FINAL CHECKLIST

Before you start coding:

```
DATASET PREPARATION
☐ 10,000+ jobs collected
☐ Columns extracted:
  ☐ job_id
  ☐ job_title
  ☐ job_title_normalized
  ☐ location
  ☐ required_experience
  ☐ required_skills
  ☐ salary_min
  ☐ salary_max
  ☐ company_size
  ☐ work_type
  
☐ Data Cleaned:
  ☐ Duplicates removed
  ☐ Null values handled
  ☐ Skills parsing done
  ☐ Job titles standardized
  ☐ Salaries validated
  
FEATURES READY
☐ Can calculate top 10 skills
☐ Can group by location
☐ Can group by job title
☐ Can parse skills for each job
☐ Can train ML models
☐ Can generate predictions

YOU'RE READY TO BUILD!
```

---

**Now you have a clear map of what data you need and for what! 🗺️**
