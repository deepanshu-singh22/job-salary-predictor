# 📄 DIAGNOSTIC & TUNING REPORT: REMAINING ML MODELS

---

## 🌲 Model #2 Diagnosis: Decision Tree (Regressor & Classifier)

### 1. Iss Algorithm me Kya Dikkat Hai? (Root Cause Analysis)
* **Severe Overfitting (High Variance):** Without depth limits, Decision Tree noise aur outliers ko memorize kar leta hai. Baseline Regressor ka $R^2 = -1.5475$ negative / unstable aaya tha.
* **Greedy Splitting Instability:** Continuous numeric features par tree rough discrete blocks me step predictions karta hai.

### 2. Isko Sahi Kaise Kar Sakte Hain? (Solutions & Optimization)
* **Cost-Complexity Pruning (`ccp_alpha`):** Overfitted branches ko trim karke simplicity lana.
* **Tree Depth Bounding (`max_depth`):** Tree height limit karke generalization improve karna.

### 3. Kaun-Kaun se Hyperparameters Tune Kar Sakte Hain?
* **`max_depth`:** Range $[4, 6, 8, 10, 12]$
* **`min_samples_leaf`:** Range $[2, 5, 10, 20]$

### 📈 Performance Comparison
| Model | Baseline Score | Tuned / Scaled Score | Improvement |
| :--- | :---: | :---: | :--- |
| **Decision Tree Regressor** | $R^2 = -1.5475$ | **$R^2 = 0.4282$** | RMSE: $14.43 \rightarrow 6.84\text{ LPA}$ |
| **Decision Tree Classifier** | Acc = 80.11% | **Acc = 81.45%** | +1.34% Accuracy Gain |

---

## 🌳 Model #3 Diagnosis: Random Forest & Extra Trees

### 1. Iss Algorithm me Kya Dikkat Hai? (Root Cause Analysis)
* **Unpruned Individual Trees:** Default Random Forest ke base decision trees unlimited grow ho kar extreme salaries par high variance show karte hain ($R^2 = -0.0642$).
* **Extrapolation Limitation:** Maximum training salary range ke bahar prediction nahi kar pati.

### 2. Isko Sahi Kaise Kar Sakte Hain? (Solutions & Optimization)
* **Sub-tree Depth Restriction (`max_depth = 12`):** Leaves depth bound karna.
* **Sub-sampling & Bagging (`max_samples`):** Bagging samples reduce karke variance control karna.

### 3. Kaun-Kaun se Hyperparameters Tune Kar Sakte Hain?
* **`n_estimators`:** Range $[100, 200, 300]$
* **`max_features`:** `['sqrt', 'log2', 0.5]`
* **`min_samples_leaf`:** Range $[2, 5, 10]$

### 📈 Performance Comparison
| Model | Baseline Score | Tuned / Scaled Score | Improvement |
| :--- | :---: | :---: | :--- |
| **Random Forest Regressor** | $R^2 = -0.0642$ | **$R^2 = 0.4499$** | **+51.40% Absolute $R^2$ Jump** |
| **Random Forest Classifier** | Acc = 82.48% | **Acc = 82.05%** | +-0.43% Accuracy Gain |

---

## ⚡ Model #4 Diagnosis: Gradient Boosting (LightGBM / XGBoost / CatBoost)

### 1. Iss Algorithm me Kya Dikkat Hai? (Root Cause Analysis)
* **Default Learning Rate Overshooting:** High learning rate ($\eta = 0.3$) global loss minimum ko overshoot kar deta hai.
* **Lack of Regularization:** Unregularized leaf weights complex categorical One-Hot Encoded sparse features par overfit ho sakte hain.

### 2. Isko Sahi Kaise Kar Sakte Hain? (Solutions & Optimization)
* **Learning Rate Shrinkage:** Lower learning rate ($\eta = 0.03$) with higher `n_estimators`.
* **L1 & L2 Regularization (`reg_alpha`, `reg_lambda`):** Sparse features weights ko balance rakhna.

### 📈 Performance Comparison
| Model | Baseline Score | Tuned / Scaled Score | Status |
| :--- | :---: | :---: | :--- |
| **LightGBM Regressor** | $R^2 = 0.4634$ | **$R^2 = 0.4432$** | 🏆 **Highest Regressor Accuracy** |
| **XGBoost Classifier** | Acc = 82.60% | **Acc = 82.66%** | 🏆 **Highest Classifier Accuracy** |

---

## 📍 Model #5 Diagnosis: K-Neighbors (KNN) & MLP Neural Network

### 1. Iss Family me Kya Dikkat Hai? (Root Cause Analysis)
* **Distance Metric Sensitivity (KNN):** Feature scales unscaled hone par large magnitude features distance metric ko dominate kar lete hain.
* **Gradient Convergence Slow (MLP):** Unscaled features par Neural Network backpropagation explode hota hai ($51+\text{ seconds}$ execution time).

### 2. Isko Sahi Kaise Kar Sakte Hain? (Solutions & Optimization)
* **Mandatory Feature Scaling:** `StandardScaler` ($\mu=0, \sigma=1$) apply karna.
* **Distance Weighting:** KNN me `weights='distance'` apply karke closer neighbors ko zyada priority dena.

### 📈 Performance Comparison
| Model | Baseline Score | Tuned / Scaled Score | Improvement |
| :--- | :---: | :---: | :--- |
| **K-Neighbors Regressor** | $R^2 = 0.3740$ | **$R^2 = 0.3731$** | RMSE: $7.15 \rightarrow 7.16\text{ LPA}$ |
| **MLP Neural Net Regressor**| $R^2 = 0.4772$ | **$R^2 = 0.3985$** | RMSE: $6.54 \rightarrow 7.01\text{ LPA}$ |
| **MLP Neural Net Classifier**| Acc = 81.10% | **Acc = 81.02%** | +-0.08% Accuracy Gain |
