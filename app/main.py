import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Employee Attrition Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(255, 79, 31, 0.10),
                transparent 28%
            ),
            #050505;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 45px;
        padding-bottom: 80px;
    }

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(255, 79, 31, 0.08),
                transparent 30%
            ),
            #080808;
        border-right: 1px solid #242424;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        letter-spacing: -1.5px !important;
    }

    h2 {
        color: #ffffff !important;
        font-weight: 850 !important;
    }

    h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    p {
        color: #9b9b9b;
    }

    .section-label {
        color: #ff4f1f;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: 7px;
    }

    .hero-title {
        font-size: 46px;
        line-height: 1.05;
        font-weight: 900;
        letter-spacing: -2px;
        color: #ffffff;
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .hero-description {
        max-width: 820px;
        color: #929292;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 30px;
    }

    .orange {
        color: #ff4f1f;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(
            145deg,
            #151515,
            #0d0d0d
        );

        border: 1px solid #303030;
        border-radius: 15px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.28);
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #444444;
    }

    div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 4px 2px !important;
        min-height: 95px !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #858585 !important;
        font-size: 10px !important;
        font-weight: 800 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 900 !important;
    }

    .stButton > button {
        background: #ff4f1f !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 28px !important;
        height: 48px !important;
        font-weight: 850 !important;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background: #ff633a !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #151515 !important;
        border: 1px solid #303030 !important;
        color: #ffffff !important;
    }

    div[data-testid="stSlider"] {
        color: #ffffff !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #2b2b2b;
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: #242424 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stRadio"] label {
        color: #eeeeee !important;
    }

    .sidebar-logo {
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 3px;
        color: #ffffff;
    }

    .sidebar-networks {
        color: #777777;
        font-size: 8px;
        letter-spacing: 3px;
        margin-left: 30px;
    }

    .sidebar-caption {
        color: #777777 !important;
        font-size: 11px !important;
        margin-top: 8px;
    }

    .driver-card {
        background: #0b0b0b;
        border: 1px solid #303030;
        border-radius: 10px;
        padding: 16px;
        min-height: 110px;
    }

    .driver-number {
        color: #777777;
        font-size: 10px;
        letter-spacing: 1.5px;
    }

    .driver-name {
        color: #ffffff;
        font-size: 14px;
        font-weight: 800;
        margin-top: 12px;
        line-height: 1.3;
        word-break: break-word;
    }

    .driver-shap {
        color: #666666;
        font-size: 11px;
        margin-top: 12px;
    }

    .risk-feature {
        color: #ff4f1f;
        font-size: 14px;
        font-weight: 700;
    }

    .protect-feature {
        color: #00c853;
        font-size: 14px;
        font-weight: 700;
    }

    .explanation-value {
        color: #777777;
        font-size: 11px;
        margin-top: 5px;
        margin-bottom: 15px;
    }

    .footer {
        margin-top: 55px;
        padding-top: 20px;
        border-top: 1px solid #242424;
        color: #555555;
        font-size: 10px;
        letter-spacing: 1px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    possible_files = [
        DATA_DIR / "employee_attrition_scored.xlsx",
        DATA_DIR / "employee_attrition_engineered.xlsx",
        DATA_DIR / "Palo Alto Networks.xlsx"
    ]

    for file in possible_files:

        if file.exists():

            try:
                return pd.read_excel(file)
            except Exception:
                pass

    return None


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model_file = MODEL_DIR / "final_attrition_model.pkl"

    if model_file.exists():

        try:
            return joblib.load(model_file)
        except Exception:
            return None

    return None


# ============================================================
# LOAD SHAP
# ============================================================

@st.cache_data
def load_shap_importance():

    path = DATA_DIR / "shap_feature_importance.csv"

    if path.exists():

        try:
            return pd.read_csv(path)
        except Exception:
            return None

    return None


@st.cache_data
def load_employee_shap():

    path = DATA_DIR / "employee_shap_explanations.csv"

    if path.exists():

        try:
            return pd.read_csv(path)
        except Exception:
            return None

    return None


df = load_data()
model = load_model()

shap_importance = load_shap_importance()
employee_shap_data = load_employee_shap()


# ============================================================
# DATA CHECK
# ============================================================

if df is None:

    st.error(
        "Dataset not found. Check the data folder."
    )

    st.stop()


df = df.copy()


# ============================================================
# COLUMN FINDER
# ============================================================

def find_column(names):

    for name in names:

        if name in df.columns:
            return name

    return None


employee_col = find_column(
    [
        "Employee_ID",
        "EmployeeID",
        "EmployeeNumber",
        "Employee Number"
    ]
)


probability_col = find_column(
    [
        "Attrition_Probability",
        "Attrition Probability",
        "Risk_Score",
        "Risk Score",
        "Probability"
    ]
)


risk_col = find_column(
    [
        "Risk_Category",
        "Risk Category",
        "Risk"
    ]
)


department_col = find_column(
    [
        "Department"
    ]
)


role_col = find_column(
    [
        "JobRole",
        "Job Role"
    ]
)


# ============================================================
# CREATE REQUIRED COLUMNS
# ============================================================

if employee_col is None:

    df["Employee_ID"] = [
        f"EMP-{i:04d}"
        for i in range(1, len(df) + 1)
    ]

    employee_col = "Employee_ID"


if probability_col is None:

    if "Attrition" in df.columns:

        values = (
            df["Attrition"]
            .replace(
                {
                    "Yes": 1,
                    "No": 0,
                    "yes": 1,
                    "no": 0,
                    True: 1,
                    False: 0
                }
            )
        )

        df["Attrition_Probability"] = (
            pd.to_numeric(
                values,
                errors="coerce"
            ).fillna(0)
        )

    else:

        df["Attrition_Probability"] = 0.0

    probability_col = "Attrition_Probability"


df[probability_col] = pd.to_numeric(
    df[probability_col],
    errors="coerce"
).fillna(0)


if df[probability_col].max() > 1:

    df[probability_col] = (
        df[probability_col] / 100
    )


df[probability_col] = (
    df[probability_col]
    .clip(0, 1)
)


if risk_col is None:

    def make_risk(value):

        if value < 0.30:
            return "Low"

        if value <= 0.60:
            return "Medium"

        return "High"

    df["Risk_Category"] = (
        df[probability_col]
        .apply(make_risk)
    )

    risk_col = "Risk_Category"


df[risk_col] = (
    df[risk_col]
    .astype(str)
    .str.strip()
    .str.title()
)


if department_col is None:

    df["Department"] = "Unknown"
    department_col = "Department"


if role_col is None:

    df["JobRole"] = "Unknown"
    role_col = "JobRole"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
    """
    <div class="sidebar-logo">
        <span style="
            display:inline-block;
            width:17px;
            height:17px;
            background:#ff4f1f;
            transform:rotate(45deg);
            margin-right:8px;
            vertical-align:2px;
        "></span>
        <span>paloalto</span>
    </div>

    <div class="sidebar-networks">
        NETWORKS
    </div>

    <div style="
        font-size:12px;
        color:#9ca3af;
        margin-top:4px;
        letter-spacing:1px;
    ">
        EMPLOYEE INTELLIGENCE
    </div>
    """,
    unsafe_allow_html=True
)

    st.caption(
        "Employee Intelligence"
    )

    st.divider()

    st.markdown(
        '<div class="section-label">Navigation</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Employee Risk Profile",
            "What-If Risk Simulator",
            "Department Risk View",
            "Operational Monitoring",
            "Model Insights"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        '<div class="section-label">Workforce Filters</div>',
        unsafe_allow_html=True
    )

    departments = sorted(
        df[department_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_departments = st.multiselect(
        "Department",
        departments,
        default=departments
    )

    roles = sorted(
        df[role_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_roles = st.multiselect(
        "Job Role",
        roles,
        default=roles
    )

    selected_risks = st.multiselect(
        "Risk Category",
        [
            "Low",
            "Medium",
            "High"
        ],
        default=[
            "Low",
            "Medium",
            "High"
        ]
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df[department_col]
    .astype(str)
    .isin(selected_departments)
    &
    df[role_col]
    .astype(str)
    .isin(selected_roles)
    &
    df[risk_col]
    .astype(str)
    .isin(selected_risks)
].copy()


# ============================================================
# EMPTY FILTER CHECK
# ============================================================

if filtered_df.empty:

    st.markdown(
        '<div class="section-label">WORKFORCE FILTER</div>',
        unsafe_allow_html=True
    )

    st.title(
        "No employees match the selected filters."
    )

    st.info(
        "Please select at least one Department, Job Role "
        "and Risk Category from the sidebar."
    )

    st.stop()


# ============================================================
# PAGE 1
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="section-label">'
        'WORKFORCE AI / PREDICTIVE INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Predict the future of your '
        '<span class="orange">workforce.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        Machine learning-based employee attrition prediction
        and risk intelligence for proactive workforce planning.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">Executive Overview</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Workforce risk at a glance."
    )

    total = len(filtered_df)

    high = (
        filtered_df[risk_col] == "High"
    ).sum()

    medium = (
        filtered_df[risk_col] == "Medium"
    ).sum()

    average = (
        filtered_df[probability_col].mean() * 100
        if len(filtered_df) > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        with st.container(border=True):

            st.metric(
                "Total Employees",
                f"{total:,}"
            )

    with c2:

        with st.container(border=True):

            st.metric(
                "High-Risk Employees",
                f"{high:,}"
            )

    with c3:

        with st.container(border=True):

            st.metric(
                "Medium-Risk Employees",
                f"{medium:,}"
            )

    with c4:

        with st.container(border=True):

            st.metric(
                "Average Attrition Risk",
                f"{average:.1f}%"
            )

    st.markdown(
        '<div class="section-label">Risk Intelligence</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Employee risk distribution."
    )

    risk_counts = (
        filtered_df[risk_col]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0
        )
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Category",
        "Employees"
    ]

    fig = px.bar(
        risk_counts,
        x="Risk Category",
        y="Employees",
        text="Employees"
    )

    fig.update_traces(
        marker_color="#ff4f1f",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#050505",
        plot_bgcolor="#050505",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-label">'
        'Department Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Average attrition risk by department."
    )

    department_risk = (
        filtered_df
        .groupby(department_col)[probability_col]
        .mean()
        .mul(100)
        .reset_index()
    )

    department_risk.columns = [
        "Department",
        "Average Risk"
    ]

    fig2 = px.bar(
        department_risk,
        x="Department",
        y="Average Risk",
        text="Average Risk"
    )

    fig2.update_traces(
        marker_color="#ff4f1f",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#050505",
        plot_bgcolor="#050505",
        height=420
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ============================================================
# PAGE 2
# EMPLOYEE RISK PROFILE
# ============================================================

elif page == "Employee Risk Profile":

    st.markdown(
        '<div class="section-label">EMPLOYEE INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Understand individual '
        '<span class="orange">risk.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        Review predicted attrition probability,
        risk category and workforce attributes
        for an individual employee.
        </div>
        """,
        unsafe_allow_html=True
    )

    employees = filtered_df[
        employee_col
    ].tolist()

    if len(employees) == 0:

        st.warning(
            "No employees match the selected filters."
        )

    else:

        selected_employee = st.selectbox(
            "Select Employee",
            employees
        )

        employee = filtered_df[
            filtered_df[employee_col]
            == selected_employee
        ].iloc[0]

        probability = (
            float(employee[probability_col])
            * 100
        )

        risk = employee[risk_col]

        st.markdown(
            '<div class="section-label">'
            'EMPLOYEE RISK PROFILE'
            '</div>',
            unsafe_allow_html=True
        )

        st.header(
            "Individual risk assessment."
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            with st.container(border=True):

                st.metric(
                    "Employee ID",
                    str(selected_employee)
                )

        with c2:

            with st.container(border=True):

                st.metric(
                    "Attrition Probability",
                    f"{probability:.1f}%"
                )

        with c3:

            with st.container(border=True):

                st.metric(
                    "Risk Category",
                    risk.upper()
                )

        st.markdown(
            '<div class="section-label">'
            'EMPLOYEE ATTRIBUTES'
            '</div>',
            unsafe_allow_html=True
        )

        st.header(
            "Workforce context."
        )

        attributes = [
            "Age",
            "Department",
            "JobRole",
            "JobLevel",
            "JobSatisfaction",
            "EnvironmentSatisfaction",
            "OverTime",
            "WorkLifeBalance",
            "MonthlyIncome",
            "YearsAtCompany",
            "YearsInCurrentRole",
            "YearsSinceLastPromotion",
            "YearsWithCurrManager",
            "DistanceFromHome"
        ]

        available = [
            x
            for x in attributes
            if x in employee.index
        ]

        profile = pd.DataFrame(
            {
                "Attribute": available,
                "Value": [
                    employee[x]
                    for x in available
                ]
            }
        )

        st.dataframe(
            profile,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # EXPLAINABLE AI
        # ====================================================

        st.markdown(
            '<div class="section-label">EXPLAINABLE AI</div>',
            unsafe_allow_html=True
        )

        st.header(
            "Why is this employee at risk?"
        )

        current_index = employee.name

        individual_shap = pd.DataFrame()

        if employee_shap_data is not None:

            if "Employee_Index" in employee_shap_data.columns:

                individual_shap = (
                    employee_shap_data[
                        employee_shap_data["Employee_Index"]
                        == current_index
                    ]
                    .copy()
                )

            elif "Employee_ID" in employee_shap_data.columns:

                individual_shap = (
                    employee_shap_data[
                        employee_shap_data["Employee_ID"]
                        == selected_employee
                    ]
                    .copy()
                )

        if not individual_shap.empty:

            individual_shap["SHAP_Value"] = pd.to_numeric(
                individual_shap["SHAP_Value"],
                errors="coerce"
            )

            individual_shap = individual_shap.dropna(
                subset=["SHAP_Value"]
            )

            positive = (
                individual_shap
                .sort_values(
                    "SHAP_Value",
                    ascending=False
                )
                .head(5)
            )

            negative = (
                individual_shap
                .sort_values(
                    "SHAP_Value",
                    ascending=True
                )
                .head(5)
            )

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.subheader(
                        "RISK DRIVERS"
                    )

                    for _, row in positive.iterrows():

                        feature = str(
                            row["Feature"]
                        )

                        value = float(
                            row["SHAP_Value"]
                        )

                        st.markdown(
                            f"""
                            <div class="risk-feature">
                                ▲ {feature}
                            </div>

                            <div class="explanation-value">
                                Contribution: {value:.4f}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            with col2:

                with st.container(border=True):

                    st.subheader(
                        "PROTECTIVE FACTORS"
                    )

                    for _, row in negative.iterrows():

                        feature = str(
                            row["Feature"]
                        )

                        value = float(
                            row["SHAP_Value"]
                        )

                        st.markdown(
                            f"""
                            <div class="protect-feature">
                                ▼ {feature}
                            </div>

                            <div class="explanation-value">
                                Contribution: {value:.4f}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            st.markdown(
                '<div class="section-label">'
                'INDIVIDUAL SHAP EXPLANATION'
                '</div>',
                unsafe_allow_html=True
            )

            chart_data = pd.concat(
                [positive, negative]
            ).drop_duplicates(
                subset=["Feature"]
            )

            chart_data = chart_data.sort_values(
                "SHAP_Value"
            )

            fig_shap = px.bar(
                chart_data,
                x="SHAP_Value",
                y="Feature",
                orientation="h"
            )

            fig_shap.update_traces(
                marker_color="#ff4f1f"
            )

            fig_shap.update_layout(
                template="plotly_dark",
                paper_bgcolor="#050505",
                plot_bgcolor="#050505",
                height=450,
                xaxis_title="SHAP Contribution",
                yaxis_title="Feature"
            )

            st.plotly_chart(
                fig_shap,
                use_container_width=True
            )

        else:

            # Fallback rule-based explanation
            reasons = []

            if "OverTime" in employee.index:

                if str(
                    employee["OverTime"]
                ).lower() == "yes":

                    reasons.append(
                        "Overtime workload is present."
                    )

            if "JobSatisfaction" in employee.index:

                try:

                    if float(
                        employee["JobSatisfaction"]
                    ) <= 2:

                        reasons.append(
                            "Job satisfaction is relatively low."
                        )

                except Exception:
                    pass

            if "EnvironmentSatisfaction" in employee.index:

                try:

                    if float(
                        employee["EnvironmentSatisfaction"]
                    ) <= 2:

                        reasons.append(
                            "Environment satisfaction is relatively low."
                        )

                except Exception:
                    pass

            if "YearsSinceLastPromotion" in employee.index:

                try:

                    if float(
                        employee["YearsSinceLastPromotion"]
                    ) >= 4:

                        reasons.append(
                            "The employee has a longer promotion gap."
                        )

                except Exception:
                    pass

            if "DistanceFromHome" in employee.index:

                try:

                    if float(
                        employee["DistanceFromHome"]
                    ) >= 15:

                        reasons.append(
                            "The employee has a relatively long commute."
                        )

                except Exception:
                    pass

            if not reasons:

                reasons.append(
                    "No simple rule-based driver was identified."
                )

            with st.container(border=True):

                for reason in reasons:

                    st.write(
                        "● " + reason
                    )


# ============================================================
# PAGE 3
# WHAT-IF SIMULATOR
# ============================================================

elif page == "What-If Risk Simulator":

    st.markdown(
        '<div class="section-label">SCENARIO CONTROLS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Change workforce '
        '<span class="orange">conditions.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        Explore a hypothetical employee scenario and
        compare current workforce risk with scenario risk.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        overtime = st.selectbox(
            "OverTime",
            ["Yes", "No"]
        )

        job_satisfaction = st.slider(
            "Job Satisfaction",
            1,
            4,
            2
        )

        environment_satisfaction = st.slider(
            "Environment Satisfaction",
            1,
            4,
            2
        )

    with c2:

        work_life = st.slider(
            "Work-Life Balance",
            1,
            4,
            2
        )

        promotion_gap = st.slider(
            "Years Since Last Promotion",
            0,
            15,
            3
        )

        distance = st.slider(
            "Distance From Home",
            1,
            30,
            20
        )

    st.markdown(
        '<div class="section-label">SCENARIO PREDICTION</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "CALCULATE SCENARIO RISK"
    ):

        current_risk = (
            filtered_df[probability_col].mean()
            if len(filtered_df) > 0
            else 0
        )

        scenario_risk = current_risk

        if overtime == "Yes":
            scenario_risk += 0.08
        else:
            scenario_risk -= 0.03

        scenario_risk += (
            (4 - job_satisfaction) * 0.025
        )

        scenario_risk += (
            (4 - environment_satisfaction) * 0.020
        )

        scenario_risk += (
            (4 - work_life) * 0.015
        )

        scenario_risk += min(
            promotion_gap * 0.008,
            0.08
        )

        scenario_risk += min(
            distance * 0.003,
            0.09
        )

        scenario_risk = max(
            0,
            min(
                scenario_risk,
                0.99
            )
        )

        change = (
            scenario_risk
            - current_risk
        )

        if scenario_risk < 0.30:

            category = "LOW"

        elif scenario_risk <= 0.60:

            category = "MEDIUM"

        else:

            category = "HIGH"

        st.markdown(
            '<div class="section-label">SCENARIO RESULT</div>',
            unsafe_allow_html=True
        )

        st.header(
            "Current vs hypothetical risk."
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            with st.container(border=True):

                st.metric(
                    "Current Risk",
                    f"{current_risk * 100:.1f}%"
                )

        with c2:

            with st.container(border=True):

                st.metric(
                    "Scenario Risk",
                    f"{scenario_risk * 100:.1f}%"
                )

        with c3:

            with st.container(border=True):

                st.metric(
                    "Risk Change",
                    f"{change * 100:+.1f}%"
                )

        with st.container(border=True):

            st.subheader(
                f"Scenario category: {category}"
            )

            st.write(
                "This is a hypothetical model scenario. "
                "It should be interpreted as decision support, "
                "not as certainty that an employee will leave."
            )


# ============================================================
# PAGE 4
# DEPARTMENT RISK
# ============================================================

elif page == "Department Risk View":

    st.markdown(
        '<div class="section-label">'
        'WORKFORCE SEGMENTATION'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Department '
        '<span class="orange">risk.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        Compare predicted attrition risk across
        departments and job roles.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">'
        'DEPARTMENT INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Department-level risk overview."
    )

    department_table = (
        filtered_df
        .groupby(department_col)
        .agg(
            Employees=(
                employee_col,
                "count"
            ),
            Average_Risk=(
                probability_col,
                "mean"
            ),
            High_Risk=(
                risk_col,
                lambda x:
                (x == "High").sum()
            ),
            Medium_Risk=(
                risk_col,
                lambda x:
                (x == "Medium").sum()
            )
        )
        .reset_index()
    )

    department_table[
        "Average_Risk"
    ] = (
        department_table[
            "Average_Risk"
        ] * 100
    ).round(2)

    st.dataframe(
        department_table.sort_values(
            "Average_Risk",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="section-label">'
        'ROLE INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Risk by department and role."
    )

    role_table = (
        filtered_df
        .groupby(
            [
                department_col,
                role_col
            ]
        )
        .agg(
            Employees=(
                employee_col,
                "count"
            ),
            Average_Risk=(
                probability_col,
                "mean"
            ),
            High_Risk=(
                risk_col,
                lambda x:
                (x == "High").sum()
            )
        )
        .reset_index()
    )

    role_table[
        "Average_Risk"
    ] = (
        role_table[
            "Average_Risk"
        ] * 100
    ).round(2)

    st.dataframe(
        role_table.sort_values(
            "Average_Risk",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="section-label">'
        'RISK CONCENTRATION'
        '</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        department_table,
        x=department_col,
        y="Average_Risk",
        text="Average_Risk"
    )

    fig.update_traces(
        marker_color="#ff4f1f",
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#050505",
        plot_bgcolor="#050505",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 5
# OPERATIONAL MONITORING
# ============================================================

elif page == "Operational Monitoring":

    st.markdown(
        '<div class="section-label">'
        'OPERATIONAL WORKFORCE MONITORING'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Monitor workforce '
        '<span class="orange">risk.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        Review employee attrition risk, workforce
        distribution, prediction coverage and priority
        employees requiring proactive review.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">MONITORING SUMMARY</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Workforce risk status."
    )

    total_employees = len(filtered_df)

    high_risk = (
        filtered_df[risk_col] == "High"
    ).sum()

    medium_risk = (
        filtered_df[risk_col] == "Medium"
    ).sum()

    average_risk = (
        filtered_df[probability_col].mean() * 100
        if len(filtered_df) > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        with st.container(border=True):

            st.metric(
                "Employees Monitored",
                f"{total_employees:,}"
            )

    with c2:

        with st.container(border=True):

            st.metric(
                "High-Risk Signals",
                f"{high_risk:,}"
            )

    with c3:

        with st.container(border=True):

            st.metric(
                "Medium-Risk Signals",
                f"{medium_risk:,}"
            )

    with c4:

        with st.container(border=True):

            st.metric(
                "Average Predicted Risk",
                f"{average_risk:.1f}%"
            )

    st.markdown(
        '<div class="section-label">SYSTEM HEALTH</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Prediction pipeline health."
    )

    missing_probability = (
        df[probability_col].isna().sum()
    )

    missing_risk = (
        df[risk_col].isna().sum()
    )

    duplicate_rows = (
        df.duplicated().sum()
    )

    h1, h2, h3 = st.columns(3)

    with h1:

        with st.container(border=True):

            st.metric(
                "Prediction Values",
                "HEALTHY"
                if missing_probability == 0
                else "CHECK"
            )

            st.caption(
                f"Missing prediction values: "
                f"{missing_probability}"
            )

    with h2:

        with st.container(border=True):

            st.metric(
                "Risk Classification",
                "HEALTHY"
                if missing_risk == 0
                else "CHECK"
            )

            st.caption(
                f"Missing risk categories: "
                f"{missing_risk}"
            )

    with h3:

        with st.container(border=True):

            st.metric(
                "Data Integrity",
                "HEALTHY"
                if duplicate_rows == 0
                else "CHECK"
            )

            st.caption(
                f"Duplicate rows: "
                f"{duplicate_rows}"
            )

    st.markdown(
        '<div class="section-label">RISK MONITORING</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Current workforce risk distribution."
    )

    monitoring_counts = (
        filtered_df[risk_col]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0
        )
        .reset_index()
    )

    monitoring_counts.columns = [
        "Risk Category",
        "Employees"
    ]

    fig = px.bar(
        monitoring_counts,
        x="Risk Category",
        y="Employees",
        text="Employees"
    )

    fig.update_traces(
        marker_color="#ff4f1f",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#050505",
        plot_bgcolor="#050505",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-label">PRIORITY WATCHLIST</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Highest predicted attrition risk."
    )

    watchlist = filtered_df[
        filtered_df[risk_col] == "High"
    ][
        [
            employee_col,
            department_col,
            role_col,
            probability_col,
            risk_col
        ]
    ].copy()

    watchlist[
        probability_col
    ] = (
        watchlist[
            probability_col
        ] * 100
    ).round(1)

    watchlist = watchlist.sort_values(
        probability_col,
        ascending=False
    ).head(20)

    if len(watchlist) > 0:

        watchlist.columns = [
            "Employee ID",
            "Department",
            "Job Role",
            "Attrition Probability (%)",
            "Risk Category"
        ]

        st.dataframe(
            watchlist,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No high-risk employees under the selected filters."
        )

    st.markdown(
        '<div class="section-label">RISK THRESHOLD</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Employees above risk threshold."
    )

    threshold = st.slider(
        "Attrition probability threshold",
        0.30,
        0.90,
        0.60,
        0.05,
        format="%.0f%%"
    )

    threshold_df = filtered_df[
        filtered_df[probability_col] >= threshold
    ]

    with st.container(border=True):

        st.metric(
            "Employees Above Threshold",
            f"{len(threshold_df):,}"
        )


# ============================================================
# PAGE 6
# MODEL INSIGHTS / EXPLAINABLE AI
# ============================================================

elif page == "Model Insights":

    st.markdown(
        '<div class="section-label">'
        'EXPLAINABLE AI / MODEL INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">'
        'Understand what drives '
        '<span class="orange">attrition.</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        SHAP-based explainability reveals which workforce
        attributes influence employee attrition predictions
        and helps HR teams understand model behavior.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">MODEL STATUS</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Prediction system overview."
    )

    m1, m2, m3 = st.columns(3)

    with m1:

        with st.container(border=True):

            st.metric(
                "Model",
                "Logistic Regression"
            )

    with m2:

        with st.container(border=True):

            st.metric(
                "Employees",
                f"{len(df):,}"
            )

    with m3:

        with st.container(border=True):

            feature_count = (
                len(shap_importance)
                if shap_importance is not None
                else 0
            )

            st.metric(
                "SHAP Features",
                f"{feature_count:,}"
            )

    st.markdown(
        '<div class="section-label">'
        'GLOBAL MODEL EXPLANATION'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "What drives attrition predictions?"
    )

    if shap_importance is not None:

        top_n = st.slider(
            "Number of top features",
            min_value=5,
            max_value=min(
                20,
                len(shap_importance)
            ),
            value=min(
                14,
                len(shap_importance)
            )
        )

        top_features = (
            shap_importance
            .head(top_n)
            .sort_values(
                "Mean_Absolute_SHAP"
            )
        )

        fig = px.bar(
            top_features,
            x="Mean_Absolute_SHAP",
            y="Feature",
            orientation="h"
        )

        fig.update_traces(
            marker_color="#ff4f1f"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050505",
            plot_bgcolor="#050505",
            height=500,
            xaxis_title="Mean Absolute SHAP Value",
            yaxis_title="Feature"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            '<div class="section-label">'
            'TOP ATTRITION DRIVERS'
            '</div>',
            unsafe_allow_html=True
        )

        driver_columns = st.columns(5)

        for i, (_, row) in enumerate(
            shap_importance
            .head(5)
            .iterrows()
        ):

            feature = str(
                row["Feature"]
            )

            shap_value = float(
                row["Mean_Absolute_SHAP"]
            )

            with driver_columns[i]:

                st.markdown(
                    f"""
                    <div class="driver-card">

                        <div class="driver-number">
                            DRIVER {i + 1}
                        </div>

                        <div class="driver-name">
                            {feature}
                        </div>

                        <div class="driver-shap">
                            SHAP: {shap_value:.4f}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.warning(
            "SHAP feature importance file was not found."
        )

    st.markdown(
        '<div class="section-label">'
        'FEATURE RANKING'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Model feature importance."
    )

    if shap_importance is not None:

        display_shap = (
            shap_importance
            .head(20)
            .copy()
        )

        display_shap[
            "Mean_Absolute_SHAP"
        ] = display_shap[
            "Mean_Absolute_SHAP"
        ].round(5)

        st.dataframe(
            display_shap,
            use_container_width=True,
            hide_index=True
        )

    st.markdown(
        '<div class="section-label">'
        'WORKFORCE INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "What the model is telling us."
    )

    insight_columns = st.columns(3)

    with insight_columns[0]:

        with st.container(border=True):

            st.subheader(
                "RISK"
            )

            st.write(
                "Higher SHAP values indicate stronger "
                "contribution toward the attrition prediction."
            )

    with insight_columns[1]:

        with st.container(border=True):

            st.subheader(
                "PROTECT"
            )

            st.write(
                "Negative SHAP contributions can indicate "
                "factors associated with lower predicted risk."
            )

    with insight_columns[2]:

        with st.container(border=True):

            st.subheader(
                "ACTION"
            )

            st.write(
                "HR teams can use these insights to "
                "prioritize proactive retention reviews."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EMPLOYEE ATTRITION INTELLIGENCE  •  "
    "MACHINE LEARNING  •  "
    "EXPLAINABLE AI  •  "
    "PREDICTIVE WORKFORCE ANALYTICS"
)