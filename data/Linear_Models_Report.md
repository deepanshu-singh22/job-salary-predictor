# 📄 DIAGNOSTIC & TUNING REPORT: LINEAR MODELS & ITS VARIANTS

---

## 📍 Part 1: Linear Regression & Regularized Variants (Regression)

### 1. Iss Family Me Kya Dikkat Hai? (Root Cause Analysis)
* **Target Variable Skewness:** Salary data Right-skewed hota hai (kuch logon ki salary 30–80 LPA tak chali jaati hai). Linear line in extreme outliers ki wajah se upward pull hoti hai, jisse standard error ($	ext{RMSE} = 6.85	ext{ LPA}$) high rehta hai.
* **Non-Linear Relationships Miss Hona:** Experience aur top skills ka impact standard linear sum nahi hota (pehle 2 saal vs 10 saal experience ka rate of growth alag hota hai).
* **Unstable Weights in Base Linear Regression:** One-hot encoding ke baad multi-collinear features par standard Linear Regression coefficients unstable assignment deta hai.

### 2. Isko Sahi Kaise Kar Sakte Hain? (Solutions & Feature Engineering)
* **Target Log Transformation ($\log1p$ Scaling):** Target salary ko $\log(y+1)$ transform karne se right-tail distribution Gaussian normal distribution me badal jaati hai.
* **Feature Standard Scaling (StandardScaler):** Features ko mean = 0, std = 1 par laane se L1/L2 penalties standardly function karti hain.
* **L2 / L1 Penalty Adjustment (Ridge / Lasso):** Multi-collinear noise ko suppress karne ke liye penalization use karna.

### 3. Kaun-Kaun Se Hyperparameters Tune Kar Sakte Hain?

| Algorithm Name | Key Hyperparameters to Tune | Tuning Search Space |
| :--- | :--- | :--- |
| **Linear Regression** | `fit_intercept`, `positive` | `fit_intercept=[True, False]` |
| **Ridge Regression** | `alpha`, `solver` | `alpha=[0.001, 0.01, 0.1, 1.0, 10.0, 100.0]`, `solver=['auto', 'svd', 'cholesky', 'lsqr']` |
| **Lasso Regression** | `alpha`, `max_iter`, `tol` | `alpha=[0.0001, 0.001, 0.01, 0.1]`, `max_iter=[1000, 5000]` |
| **Linear SVR** | `C`, `epsilon`, `loss` | `C=[0.1, 1.0, 10.0]`, `epsilon=[0.01, 0.1, 0.2]`, `loss=['epsilon_insensitive', 'squared_epsilon_insensitive']` |

---

### 📈 Accuracy Jump & Performance Comparison (Regression)

| Model Configuration | Baseline Score | Tuned / Scaled Score | RMSE Reduction | Accuracy Gain |
| :--- | :---: | :---: | :---: | :--- |
| **Linear Regression** | $R^2 = 0.4262$ | **$R^2 = 0.3884$** | $6.85 \rightarrow 7.07\text{ LPA}$ | **+-3.78% Absolute $R^2$ Jump** |
| **Ridge Regression** | $R^2 = 0.4262$ | **$R^2 = 0.3884$** | $6.85 \rightarrow 7.07\text{ LPA}$ | **+-3.78% Absolute $R^2$ Jump** |
| **Lasso Regression** | $R^2 = 0.4073$ | **$R^2 = 0.3884$** | $6.96 \rightarrow 7.07\text{ LPA}$ | **+-1.89% Absolute $R^2$ Jump** |
| **Linear SVR** | $R^2 = 0.3794$ | **$R^2 = 0.3623$** | $7.12 \rightarrow 7.22\text{ LPA}$ | **+-1.71% Absolute $R^2$ Jump** |

---

## 📍 Part 2: Logistic Regression & Linear SVC (Classification)

### 1. Iss Family Me Kya Dikkat Hai? (Root Cause Analysis)
* **Unscaled Feature Coefficients:** Logistic Regression aur Linear SVC sub-features ke scale difference ke karan bad-boundary decisions create kar sakte hain.
* **Outlier Boundary Distortion:** High extreme values decision threshold ko tilt kar deti hain, jisse Recall score Precision se kam ho jata hai.

### 2. Isko Sahi Kaise Kar Sakte Hain? (Solutions & Feature Engineering)
* **Threshold Adjustment (Probability Tuning):** Decision threshold ko standard 0.50 se badal kar optimal set karna.
* **Class Weight Balancing (`class_weight='balanced'`):** High-salary class instance density ko weight balance dena.
* **Regularization Strength ($C$ Parameter):** Overfitting vs underfitting trade-off balance karna.

---

### 📈 Accuracy Jump & Performance Comparison (Classification)

| Model Configuration | Baseline Accuracy | Tuned Accuracy | Baseline F1-Score | Tuned F1-Score | Accuracy Gain |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | $82.01\%$ | **$81.91\%$** | $81.54\%$ | **$81.41\%$** | **+-0.10% Overall Jump** |
| **Linear SVC** | $81.91\%$ | **$81.93\%$** | $81.21\%$ | **$81.23\%$** | **+0.02% Overall Jump** |
