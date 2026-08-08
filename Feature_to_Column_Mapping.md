# 🎯 FEATURE-TO-COLUMN MAPPING
## Job Market Intelligence Platform

---

## **PAGE 1: HOMEPAGE**

### Required Columns:
```
┌─────────────────────────────────────────────────┐
│ FEATURE: Key Statistics Cards                   │
├─────────────────────────────────────────────────┤
│                                                 │
│ Total Jobs Analyzed                             │
│  └─ COUNT(job_id)                              │
│                                                 │
│ Total Unique Locations                          │
│  └─ DISTINCT(location)                         │
│                                                 │
│ Total Unique Skills                             │
│  └─ DISTINCT(required_skills)                  │
│                                                 │
│ Average Salary                                  │
│  └─ AVG(salary_avg)                            │
│                                                 │
│ Most Demanded Skill (This Month)                │
│  └─ MODE(required_skills)                      │
│                                                 │
│ Top Hiring Company                              │
│  └─ MOST FREQUENT(company_name)                │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Search Feature:
```
┌─────────────────────────────────────────────────┐
│ FEATURE: Quick Job Search                       │
├─────────────────────────────────────────────────┤
│ Search by Job Title                             │
│  └─ FILTER(job_title_normalized LIKE '%input%')│
│                                                 │
│ Returns:                                        │
│  - job_id, job_title, company_name             │
│  - location, salary_avg, work_type             │
│  - job_posting_url                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## **PAGE 2: MARKET TRENDS ANALYSIS**

### **2.1 - Most Demanding Skills**

#### Feature 1: Top 10 Skills Overall
```
Required Columns:
  - required_skills (parse and split by comma)

Logic:
  1. Split each required_skills string by comma
  2. Create skill frequency distribution
  3. Sort by frequency descending
  4. Select top 10
  
Example Processing:
  Job 1: "Python, SQL, ML" → [Python, SQL, ML]
  Job 2: "Python, Java, SQL" → [Python, Java, SQL]
  Job 3: "Python, ML" → [Python, ML]
  
  Frequency Count:
  Python: 3 (appears in all)
  SQL: 2
  ML: 2
  Java: 1

Output Columns:
  - skill_name
  - frequency_count
  - percentage_of_jobs = (frequency / total_jobs) × 100
  - rank
```

#### Feature 2: Top Skills by Job Role
```
Required Columns:
  - job_title_normalized (for grouping)
  - required_skills

Logic:
  1. Filter by selected job_title_normalized
  2. Extract all required_skills for that role
  3. Calculate frequency
  4. Sort and get top 8-10

Example:
  Input: Job Role = "Data Scientist"
  
  Step 1: Filter jobs where job_title_normalized = "Data Scientist"
          Result: 450 Data Scientist jobs
          
  Step 2: Extract all required_skills
          [Python, SQL, ML, AWS, Docker, ...]
          
  Step 3: Count frequency among these 450 jobs
          Python: 382/450 = 84.9%
          SQL: 351/450 = 78%
          ML: 324/450 = 72%
          Pandas: 292/450 = 64.9%
          
  Output Table:
  Rank | Skill | Count | % of Demand
  -----|-------|-------|------------
  1    | Python| 382   | 84.9%
  2    | SQL   | 351   | 78%
  3    | ML    | 324   | 72%

Output Columns:
  - rank
  - skill_name
  - count_in_role
  - percentage_demand_in_role
  - job_role_selected
```

---

### **2.2 - Top Hiring Locations**

```
Required Columns:
  - location (or city/state combination)
  - salary_avg
  - job_id (for counting)

Logic:
  1. Group by location
  2. Count jobs per location
  3. Calculate average salary per location
  4. Sort by job count descending
  5. Take top 15-20

Calculation:
  Location: Bangalore
  ├─ Total Jobs: 45,000
  ├─ Total Salary Sum: ₹594 Crores
  ├─ Average Salary: ₹13.2 LPA
  ├─ Salary Range: ₹8 LPA - ₹25 LPA
  └─ Dominant Skills: Python, SQL, ML

  Location: Mumbai
  ├─ Total Jobs: 38,000
  ├─ Average Salary: ₹12.8 LPA
  └─ Dominant Skills: Python, Java, SQL

Output Columns:
  - location
  - city
  - job_count
  - avg_salary
  - median_salary
  - salary_min_range
  - salary_max_range
  - hiring_growth_rate (month-over-month)
```

#### Visualization Suggestions:

```
Option 1: 3D Bar Chart
  X-axis: Cities
  Y-axis: Job Count
  Z-axis: Average Salary
  
Option 2: Geospatial Heatmap
  Map of India with color intensity = job density
  Darker = more jobs
  
Option 3: Bubble Chart
  X: Number of jobs
  Y: Average salary
  Bubble size: Location (larger = bigger city)
  Color: Hiring growth
```

---

### **2.3 - Top High Paying Roles**

```
Required Columns:
  - job_title_normalized (for grouping)
  - salary_avg
  - salary_max
  - salary_min
  - job_id (for counting)

Logic:
  1. Group by job_title_normalized
  2. Calculate:
     - AVG(salary_avg)
     - MEDIAN(salary_avg)
     - COUNT(job_id)
     - MIN(salary_min)
     - MAX(salary_max)
  3. Sort by average salary descending
  4. Select top 10

Example Calculation:
  Job Title: "Principal Data Scientist"
  ├─ Jobs Found: 342
  ├─ Salary Min (across all): ₹18 LPA
  ├─ Salary Max (across all): ₹35 LPA
  ├─ Average Salary: ₹25.5 LPA
  └─ Median Salary: ₹24 LPA

  Job Title: "Senior ML Engineer"
  ├─ Jobs Found: 1,240
  ├─ Salary Min: ₹14 LPA
  ├─ Salary Max: ₹28 LPA
  ├─ Average Salary: ₹19.8 LPA
  └─ Median Salary: ₹19 LPA

Output Columns:
  - rank
  - job_title_normalized
  - job_count
  - salary_avg
  - salary_median
  - salary_min
  - salary_max
  - salary_range
  - salary_std_deviation (variation in salaries)
  - entry_level_salary (for this role)
  - senior_level_salary (for this role)

Output Table Format:
┌────┬──────────────────┬──────────┬──────────┬────────┬────────────┐
│Rank│Job Title         │Avg Salary│Median    │Count   │Salary Range│
├────┼──────────────────┼──────────┼──────────┼────────┼────────────┤
│1   │Principal DS      │₹25.5 LPA │₹24.0 LPA │342     │₹18-35 LPA  │
│2   │ML Eng Manager    │₹22.1 LPA │₹21.0 LPA │286     │₹16-32 LPA  │
│3   │Senior ML Eng     │₹19.8 LPA │₹19.0 LPA │1,240   │₹14-28 LPA  │
└────┴──────────────────┴──────────┴──────────┴────────┴────────────┘
```

---

### **2.4 - Skill Ecosystem Network**

```
Required Columns:
  - required_skills (string of comma-separated skills)
  - job_id

Logic (Build Co-occurrence Matrix):
  1. For each job, extract all required_skills
  2. Create skill pairs: (skill1, skill2)
  3. Count frequency of each pair
  4. Build adjacency matrix
  
Example:
  Job 1 skills: [Python, SQL, ML, Pandas]
  Pairs created:
  - (Python, SQL): +1
  - (Python, ML): +1
  - (Python, Pandas): +1
  - (SQL, ML): +1
  - (SQL, Pandas): +1
  - (ML, Pandas): +1
  
  Job 2 skills: [Python, SQL, Java]
  Pairs:
  - (Python, SQL): +1 (now count=2)
  - (Python, Java): +1
  - (SQL, Java): +1
  
  Final Matrix:
  Python ↔ SQL: 2 (appears together in 2 jobs)
  Python ↔ ML: 1
  Python ↔ Java: 1
  SQL ↔ ML: 1
  etc.

Output Columns (for network graph):
  - skill_1
  - skill_2
  - co_occurrence_count
  - co_occurrence_percentage = (count / total_jobs) × 100
  - edge_strength = count (for visualization thickness)
  - node_frequency_skill1 = how often skill1 appears overall
  - node_frequency_skill2 = how often skill2 appears overall

Data Structure for Visualization:
{
  "nodes": [
    {"id": "Python", "frequency": 8500, "size": 85},
    {"id": "SQL", "frequency": 7800, "size": 78},
    {"id": "ML", "frequency": 5200, "size": 52}
  ],
  "edges": [
    {"source": "Python", "target": "SQL", "weight": 0.87, "strength": 7400},
    {"source": "Python", "target": "ML", "weight": 0.84, "strength": 6500},
    {"source": "SQL", "target": "ML", "weight": 0.65, "strength": 3200}
  ]
}

Visualization:
  - Node size = skill frequency (bigger = more demanded)
  - Edge thickness = co-occurrence strength
  - Edge color = intensity of relationship (darker = stronger)
  - Interactive: Click on node to highlight connected skills
```

---
# 💰 PAGE 3: CAREER & MARKET SALARY ESTIMATOR

---

## 3.1 - Resume & Groq API Real-Time Salary Prediction Pipeline

### 1. Data Source & Extraction Pipeline
* **Input Document:** Candidate Resume (PDF File Upload)
* **Text Extraction Engine:** PyPDF / PDF Parser (Extracts raw resume content)
* **Real-Time Intelligence Layer:** **Groq API** (`llama-3.3-70b-versatile` Model)
* **Extracted Candidate Profile:**
  * **`detected_skills`** *(List of technical & soft skills parsed from Resume)*
  * **`candidate_experience_years`** *(Parsed actual total experience in years)*
  * **`target_job_role`** *(Target Role chosen by Candidate)*
  * **`preferred_location`** *(Preferred Tech Hub / Location)*

---

### 2. Groq AI Processing & Feature Encoding Logic
1. **`target_job_role` Analysis**
   * Real-time semantic matching of candidate skills with current tech market standards.
   * **Result Alignment:** `Data Scientist`, `ML Engineer`, `Frontend Developer`, etc.

2. **`candidate_experience_years` Encoding**
   * **Type:** Numeric Feature (Extracted from resume timeline, Range: 0–30 years).

3. **`preferred_location` Tier Grouping**
   * **Tier 1:** Bengaluru, Mumbai, Delhi/NCR, Hyderabad *(Highest Market Base)*
   * **Tier 2:** Pune, Ahmedabad, Chennai *(Medium Market Base)*
   * **Tier 3 / Remote:** Other Cities / Remote

4. **`detected_skills` Vectorization (Option B - One-Hot Skill Mapping)**
   * Groq API parses text and evaluates against top 50 in-demand industry skills.
   * **Feature Vector:** `[1, 1, 0, 1, 0, ..., 0, 1]` *(Binary representation of candidate's skill coverage)*

5. **`company_tier_mapping`**
   * `Early-Stage Startup` = **0**
   * `Mid-Sized Product Firm` = **1**
   * `Tier 1 Tech Product MNC / Service Giant` = **2**

---

### 3. Real-Time Output Metrics (Powered by Groq API)
* **`predicted_salary_avg_lpa`** *(Real-Time Market Average Valuation in LPA)*
* **`salary_range_min_lpa`** *(25th Percentile Market Bracket)*
* **`salary_range_max_lpa`** *(75th Percentile Market Bracket)*
* **`confidence_score`** *(0.0 – 1.0 based on resume skill match quality)*
* **`role_mismatch`** *(Boolean Flag: `True` if parsed resume skills diverge from target role)*
* **`mismatch_reason`** *(Real-time feedback on skill gap)*

---

## 3.2 - Real-Time Skill Recommendation & Salary Lift Engine

### 1. Processing Logic
Groq API target role ke requirements aur parsed resume skills ke beech ka **Gap Analysis** perform karke salary hike evaluate karta hai.

---

### 2. Execution Pipeline

#### Step 1: Resume Text Parsing & Base Valuation
* **Resume Parsed Skills:** `["Python", "SQL", "Pandas", "Scikit-Learn"]`
* **Groq Market Valuation:** `₹12.8 LPA`

#### Step 2: Real-Time Market Benchmark Query (Via Groq API)
* Target Role selected: `"Data Scientist"`
* Groq AI current 2026 industry demand benchmarks query karta hai:
  * **Python:** 85% Demand
  * **SQL:** 78% Demand
  * **Machine Learning:** 72% Demand
  * **Statistics:** 68% Demand
  * **Pandas:** 65% Demand
  * **Scikit-Learn:** 60% Demand
  * **TensorFlow:** 55% Demand
  * **Deep Learning:** 52% Demand
  * **AWS:** 50% Demand
  * **Docker:** 48% Demand

#### Step 3: Skill Gap Detection
* **Formula:** `Target Role Industry Demands - Parsed Resume Skills`
  * Python *(Present in Resume)* ✓
  * SQL *(Present in Resume)* ✓
  * **Machine Learning** ✗ *(MISSING IN RESUME)*
  * **Statistics** ✗ *(MISSING IN RESUME)*
  * Pandas *(Present in Resume)* ✓
  * Scikit-Learn *(Present in Resume)* ✓
  * **TensorFlow** ✗ *(MISSING IN RESUME)*
  * **Deep Learning** ✗ *(MISSING IN RESUME)*
  * **AWS** ✗ *(MISSING IN RESUME)*
  * **Docker** ✗ *(MISSING IN RESUME)*

#### Step 4: Live Salary Hike Simulation
* Har missing skill ke liye Groq AI valuation simulation run karta hai:
  * `Simulated Profile = Parsed Resume Skills + Missing Skill`
  * Net Valuation Increase (`₹ LPA Hike` & `% Uplift`) calculate hoti hai.

> **Simulation Example (Adding AWS):**
> * **Base Valuation from Resume:** ₹12.8 LPA
> * **Projected Valuation with AWS:** ₹14.2 LPA
> * **Net Salary Lift:** **+₹1.4 LPA (+10.9%)**

#### Step 5: High-Impact Recommendation Rendering
* Highest `% Hike` waale top **4–5 missing skills** ka JSON generate hota hai aur frontend UI par cards form me display hota hai.

---

### 3. Payload Output Attributes
* **`recommended_skill`** *(Missing skill name)*
* **`predicted_salary_after_skill`** *(New projected valuation in LPA)*
* **`salary_increase_amount`** *(Net LPA hike)*
* **`salary_increase_percentage`** *(Percentage lift %)*
* **`skill_demand_percentage`** *(% of market job postings requiring this skill)*
* **`learning_difficulty`** *(Easy / Medium / Hard)*
* **`estimated_learning_time`** *(Estimated time in weeks)*
* **`learning_resources`** *(Recommended learning platform/course)*

## **PAGE 4: MODEL PERFORMANCE & DECISION ANALYSIS**

### Required Columns for Model Training:
```
Same as PAGE 3 (all features)

Additional Metrics Calculation:

For each model trained:
  - Model name
  - R² Score (coefficient of determination)
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - MAPE (Mean Absolute Percentage Error)
  - Training time (seconds)
  - Prediction time (milliseconds per sample)
  - Model size (MB on disk)
  - Hyperparameters used
  - Cross-validation score (5-fold average)
  - Feature importance (top 10 features)

Output Columns:
  - model_name
  - r2_score
  - rmse_value
  - mae_value
  - mape_value
  - training_time_seconds
  - prediction_time_ms
  - model_size_mb
  - cv_score
  - is_selected (1 or 0)
  - notes (why selected or not)
  
Comparison Table:
┌──────────────────┬────────┬──────────┬────────┬──────────┬──────────┐
│Model             │R² Score│RMSE      │MAE     │Pred Time │Selected  │
├──────────────────┼────────┼──────────┼────────┼──────────┼──────────┤
│Linear Regression │0.62    │3.2 LPA   │2.1 LPA │0.2ms     │❌        │
│Ridge             │0.64    │3.1 LPA   │2.0 LPA │0.2ms     │❌        │
│Random Forest     │0.82    │1.8 LPA   │1.2 LPA │15ms      │❌        │
│XGBoost           │0.88    │1.4 LPA   │0.9 LPA │8ms       │✅        │
└──────────────────┴────────┴──────────┴────────┴──────────┴──────────┘
```

---

## **PAGE 5: SKILL GAP ANALYZER**

```
Required Columns:
  - job_title_normalized (for filtering by role)
  - required_skills

Input:
  - User selected job title
  - User current skills (array)

Logic:

Step 1: Get Top Required Skills for Role
  Filter jobs by job_title_normalized
  Extract all required_skills
  Calculate frequency
  Get top 10 skills

Step 2: Calculate Match Score
  Weighted Match Score = 
    (Sum of frequencies of user's skills) / 
    (Sum of frequencies of top 10 skills) × 100
  
  Example:
  User has: Python (85%), SQL (78%), Pandas (65%), Scikit-learn (60%), Git (40%)
  Top 10: Python (85%), SQL (78%), ML (72%), Stats (68%), Pandas (65%), 
          Scikit-learn (60%), TensorFlow (55%), DL (52%), AWS (50%), Docker (48%)
  
  User score = (85+78+65+60+0) / (85+78+72+68+65+60+55+52+50+48) × 100
             = 288 / 633 × 100
             = 45.5% (Oops! Low score)
  
  Actual calculation should include all 10:
  User score = (85+78+0+0+65+60+0+0+0+0) / (85+78+72+68+65+60+55+52+50+48)
             = 288 / 633 × 100 = 45.5%

Step 3: Identify Gaps
  Gap = Required skill - User has it
  
  Skills User Has ✓:
  ├─ Python (85%)
  ├─ SQL (78%)
  ├─ Pandas (65%)
  ├─ Scikit-learn (60%)
  └─ Git (40%, not in top 10)
  
  Skills Missing ✗:
  ├─ Machine Learning (72%) - HIGH PRIORITY
  ├─ Statistics (68%) - HIGH PRIORITY
  ├─ TensorFlow (55%) - MEDIUM PRIORITY
  ├─ Deep Learning (52%) - MEDIUM PRIORITY
  ├─ AWS (50%) - MEDIUM PRIORITY
  └─ Docker (48%) - LOW PRIORITY

Step 4: Prioritize
  Priority = Demand % × Learning Difficulty
  Or just by demand %

Output Columns:
  - job_title_target
  - match_score_percentage
  - skills_user_has (array)
  - skills_missing (array)
  - priority_rank
  - skill_name
  - demand_percentage
  - priority_level (HIGH/MEDIUM/LOW)
  - learning_time_estimate (weeks)
  - learning_resources
  - match_visualization_data (for bar chart)
```

---

## **PAGE 6: JOB RECOMMENDATION SYSTEM** (BONUS)

```
Required Columns:
  - job_id
  - job_title
  - job_title_normalized
  - required_skills
  - required_experience
  - location
  - salary_avg
  - work_type
  - company_name
  - company_size
  - job_description

User Input:
  - Skills array: [Python, SQL, ML, Pandas, Statistics]
  - Experience: 2 years
  - Preferred location: Bangalore
  - Expected salary: ₹12 LPA
  - Work type: Hybrid
  - Flexibility: ±20% salary range, ±3 months experience

Algorithm: TF-IDF + Cosine Similarity

Step 1: Vectorize Job Descriptions
  For each job:
    Text = job_title + required_skills + job_description
    Example: "Data Scientist Python SQL ML AWS Docker..."
    → TF-IDF Vector (1000+ dimensions)

Step 2: Vectorize User Profile
  Text = "Python SQL Machine Learning Pandas Statistics"
  → TF-IDF Vector (same dimensions)

Step 3: Calculate Cosine Similarity
  similarity = dot_product(user_vector, job_vector) / 
              (magnitude(user_vector) × magnitude(job_vector))
  
  Result: Similarity score 0-1
  - 1.0 = Perfect match
  - 0.9+ = Excellent match
  - 0.8-0.9 = Very good match
  - 0.7-0.8 = Good match
  - <0.7 = Not ideal match

Step 4: Filter by Constraints
  Filter by:
    - Location preference (exact or nearby)
    - Salary range (expected ±20%)
    - Work type (must match if specified)
    - Experience (required exp ≤ user exp × 1.2)

Step 5: Rank
  Sort by similarity score descending
  Display top 5-10 jobs

Output Columns:
  - rank
  - job_title
  - company_name
  - location
  - match_percentage
  - match_reason (which skills matched)
  - missing_skills (skills they want you to have)
  - salary_predicted
  - work_type
  - job_posting_url
  - apply_button

Output Format:
┌────┬──────────────┬──────────┬─────────────┬──────────────┐
│Rank│Job Title     │Match%    │Company      │Salary        │
├────┼──────────────┼──────────┼─────────────┼──────────────┤
│1   │Data Scientist│96%       │TCS          │₹12.5 LPA     │
│2   │ML Engineer   │91%       │Flipkart     │₹13.2 LPA     │
│3   │AI Engineer   │87%       │Google       │₹15.8 LPA     │
└────┴──────────────┴──────────┴─────────────┴──────────────┘
```

---

## 📊 COMPLETE DATASET COLUMNS CHECKLIST

### **Minimal Required Dataset:**

```csv
✅ job_id
✅ job_title
✅ job_title_normalized
✅ company_name
✅ location
✅ city
✅ state
✅ required_experience
✅ required_skills
✅ salary_min
✅ salary_max
✅ salary_avg
✅ salary_currency
✅ salary_frequency
✅ work_type
✅ company_size
✅ job_description
✅ job_posting_date
✅ job_posting_url
```

### **Enhanced Dataset (Recommended):**

```csv
✅ job_id
✅ job_title
✅ job_title_normalized
✅ company_name
✅ company_size
✅ industry
✅ location
✅ city
✅ state
✅ country
✅ required_experience
✅ experience_level
✅ education_required
✅ required_skills
✅ preferred_skills
✅ number_of_skills
✅ salary_min
✅ salary_max
✅ salary_avg
✅ salary_median
✅ salary_currency
✅ salary_frequency
✅ salary_range
✅ work_type
✅ job_description
✅ job_posting_date
✅ job_posting_url
✅ applications_count (optional)
```

---

## 🔧 DATA TRANSFORMATION EXAMPLES

### **Example 1: Skill Parsing**
```
Raw Data:
job_id=1, required_skills="Python, SQL, Machine Learning, AWS, Docker"

Processing:
skills_list = required_skills.split(", ")
Result: ["Python", "SQL", "Machine Learning", "AWS", "Docker"]

Storage:
new_columns = {
  'skill_python': 1,
  'skill_sql': 1,
  'skill_ml': 1,
  'skill_aws': 1,
  'skill_docker': 1,
  'total_skills': 5
}
```

### **Example 2: Salary Range Calculation**
```
Raw Data:
job_id=1, salary_min=10, salary_max=15 (in LPA)

Processing:
salary_avg = (salary_min + salary_max) / 2 = 12.5 LPA
salary_range = salary_max - salary_min = 5 LPA
salary_percentile_25 = salary_min + 0.25 × salary_range = 11.25 LPA
salary_percentile_75 = salary_min + 0.75 × salary_range = 13.75 LPA
```

### **Example 3: Location Clustering**
```
Raw Data:
location = ["Bangalore", "bengaluru", "BANGALORE", "Bangalore, India"]

Normalization:
1. Remove state/country info
2. Convert to lowercase
3. Handle variations
4. Cluster by tier

Result:
Tier 1: Bangalore (metro)
Tier 2: Pune (metro-adjacent)
Tier 3: Indore (tier-2 city)
```

---

## 🎯 DATA VALIDATION RULES

```
Before using data, validate:

1. job_id
   ✓ Unique and not null
   ✗ Reject duplicates

2. required_skills
   ✓ Not empty (has at least 1 skill)
   ✗ Reject null values

3. salary_avg
   ✓ salary_min ≤ salary_avg ≤ salary_max
   ✓ salary_avg > 0
   ✗ Reject negative or 0 salaries

4. required_experience
   ✓ 0 ≤ experience ≤ 50
   ✗ Reject negative or unrealistic (>50)

5. location
   ✓ Valid city/state
   ✗ Reject invalid locations

6. work_type
   ✓ In ['Remote', 'Hybrid', 'Onsite']
   ✗ Reject unknown values

7. company_size
   ✓ In ['Small', 'Medium', 'Large']
   ✗ Reject unknown values
```

---

## 📈 SAMPLE CSV FORMAT

```csv
job_id,job_title,job_title_normalized,company_name,company_size,industry,location,city,state,required_experience,experience_level,education_required,required_skills,preferred_skills,number_of_skills,salary_min,salary_max,salary_avg,salary_currency,salary_frequency,work_type,job_posting_date,job_description,job_posting_url,applications_count

1,Data Scientist,Data Scientist,TCS,Large,IT,Bangalore,Bangalore,Karnataka,2,Mid Level,B.Tech,"Python, SQL, Machine Learning, Pandas, Statistics",AWS;Docker,5,11,14,12.5,INR,Annual,Hybrid,2024-01-15,"We are looking for a Data Scientist to join our AI team. Required: Python, SQL, ML, Pandas, Statistics. Nice to have: AWS, Docker",https://example.com/jobs/1,245

2,Senior ML Engineer,ML Engineer,Google,Large,Technology,Bangalore,Bangalore,Karnataka,5,Senior,B.Tech;M.Tech,"Python, TensorFlow, Deep Learning, AWS, Kubernetes, Docker, PyTorch",CUDA;JAX,8,18,25,21.5,INR,Annual,Hybrid,2024-01-16,"Join our ML team at Google. Requirements: Python, TensorFlow, DL, AWS, Kubernetes, Docker, PyTorch",https://example.com/jobs/2,1250

3,Data Analyst,Data Analyst,Flipkart,Large,E-commerce,Mumbai,Mumbai,Maharashtra,1,Entry Level,B.Tech,"SQL, Excel, Python, Tableau, Statistics",Power BI;R,5,8,12,10,INR,Annual,Remote,2024-01-17,"Analyze business data and create insights. Required: SQL, Excel, Python, Tableau, Statistics",https://example.com/jobs/3,892

4,DevOps Engineer,DevOps Engineer,Amazon,Large,Cloud,Hyderabad,Hyderabad,Telangana,3,Mid Level,B.Tech,"Docker, Kubernetes, AWS, Linux, CI/CD, Git",Terraform;Jenkins,6,12,16,14,INR,Annual,Onsite,2024-01-18,"Manage cloud infrastructure. Required: Docker, K8s, AWS, Linux, CI/CD, Git",https://example.com/jobs/4,567
```

---

## ✅ FINAL CHECKLIST

Before starting development:

- [ ] Dataset collected (min 10,000 jobs)
- [ ] All columns extracted
- [ ] Data cleaned & validated
- [ ] Missing values handled
- [ ] Outliers removed
- [ ] Skills normalized (capitalization, variations)
- [ ] Locations standardized
- [ ] Salaries in consistent currency/unit
- [ ] Train-test split done (80-20)
- [ ] Feature engineering completed
- [ ] Models trained & compared
- [ ] Best model selected & saved
- [ ] Backend API ready
- [ ] Frontend pages designed
- [ ] Integration tested

**Ready to launch! 🚀**
