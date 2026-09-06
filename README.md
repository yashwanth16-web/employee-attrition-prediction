# Machine Learning-Based Employee Attrition Prediction and Risk Scoring System

## 🚀 Project Overview

This project presents a machine learning-based employee attrition prediction and risk scoring system that analyzes employee demographic, job, compensation, satisfaction, career progression, work-life balance, overtime, and organizational factors to estimate employee attrition risk.

The system classifies employees into **Low, Medium, and High attrition-risk categories** and provides explainable predictions using SHAP. An interactive Streamlit dashboard allows HR teams and management to explore workforce risk, employee-level predictions, department-level risk, what-if scenarios, operational monitoring, and model insights.

> **Note:** The dataset is used for educational and analytical purposes and should not be interpreted as verified confidential employee data from Palo Alto Networks. The interface is Palo Alto Networks-inspired.

## 🎯 Objectives

- Analyze employee workforce and attrition data.
- Perform exploratory data analysis.
- Engineer employee-related risk features.
- Preprocess numerical and categorical variables.
- Train and compare machine learning models.
- Predict employee attrition probability.
- Classify employees into Low, Medium, and High risk.
- Identify important factors influencing attrition.
- Provide individual prediction explanations using SHAP.
- Develop an interactive HR risk intelligence dashboard.
- Deploy the application using Streamlit Community Cloud.

## 👥 Dataset

The dataset contains **1,470 employee records** and **31 attributes**.

### Main data categories

| Category | Parameters |
|---|---|
| Employee Information | Age, Gender, Marital Status |
| Job Information | Department, Job Role, Job Level |
| Compensation | Monthly Income, Daily Rate, Hourly Rate, Monthly Rate |
| Satisfaction | Job Satisfaction, Environment Satisfaction, Relationship Satisfaction |
| Work Conditions | Overtime, Business Travel, Work-Life Balance |
| Career | Years at Company, Years in Current Role, Years Since Last Promotion |
| Experience | Total Working Years, Years With Current Manager |
| Target | Attrition |

### Dataset Distribution

| Attrition Status | Employees |
|---|---:|
| Stayed | 1,233 |
| Left | 237 |
| Total | 1,470 |

Overall attrition rate:

**16.12%**

## ⚙️ Feature Engineering

The project creates additional features to capture relationships between employee characteristics and attrition risk.

### Engineered features

- **Income-to-Experience Ratio**
- **Promotion Delay Indicator**
- **Engagement Composite**
- **Workload Stress Flag**

These features provide additional information about compensation, career progression, employee engagement, and workload conditions.

## 🧹 Data Preprocessing

The preprocessing pipeline includes:

- Numerical feature scaling
- Categorical feature encoding
- Train-test splitting
- Stratified sampling
- Class imbalance handling
- Feature transformation

The target variable is converted into binary classification:

```text
0 → Employee Stayed
1 → Employee Left