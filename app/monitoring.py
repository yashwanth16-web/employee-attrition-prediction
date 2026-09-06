import streamlit as st
import pandas as pd
import plotly.express as px


def show_monitoring(df):

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.html(
        """
        <div class="hero">

            <div class="hero-label">
                OPERATIONAL WORKFORCE MONITORING
            </div>

            <div class="hero-title">
                Monitor workforce
                <span>risk.</span>
            </div>

            <div class="hero-description">
                Monitor employee attrition risk, prediction
                coverage, workforce distribution and priority
                employees requiring proactive review.
            </div>

        </div>
        """
    )

    # =========================================================
    # SAFETY CHECK
    # =========================================================

    required = [
        "Employee_ID",
        "Attrition_Probability",
        "Risk_Category",
        "Department",
        "JobRole"
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:

        st.error(
            "The monitoring dataset is missing: "
            + ", ".join(missing)
        )

        st.write("Available columns:")

        st.write(
            df.columns.tolist()
        )

        return

    # =========================================================
    # CLEAN DATA
    # =========================================================

    monitoring_df = df.copy()

    monitoring_df[
        "Attrition_Probability"
    ] = pd.to_numeric(
        monitoring_df[
            "Attrition_Probability"
        ],
        errors="coerce"
    )

    monitoring_df = monitoring_df.dropna(
        subset=[
            "Attrition_Probability",
            "Risk_Category"
        ]
    )

    # =========================================================
    # SUMMARY
    # =========================================================

    st.html(
        """
        <div class="section-label">
            MONITORING SUMMARY
        </div>

        <div class="section-title">
            Workforce risk status.
        </div>

        <div class="section-description">
            Current predictive risk indicators across the
            monitored employee population.
        </div>
        """
    )

    total_employees = len(
        monitoring_df
    )

    high_risk = (
        monitoring_df[
            "Risk_Category"
        ]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
    )

    medium_risk = (
        monitoring_df[
            "Risk_Category"
        ]
        .astype(str)
        .str.lower()
        .eq("medium")
        .sum()
    )

    low_risk = (
        monitoring_df[
            "Risk_Category"
        ]
        .astype(str)
        .str.lower()
        .eq("low")
        .sum()
    )

    average_risk = (
        monitoring_df[
            "Attrition_Probability"
        ].mean()
        * 100
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    EMPLOYEES MONITORED
                </div>

                <div class="metric-value">
                    {total_employees:,}
                </div>

            </div>
            """
        )

    with c2:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    HIGH-RISK SIGNALS
                </div>

                <div class="metric-value orange">
                    {high_risk:,}
                </div>

            </div>
            """
        )

    with c3:

        st.html(
            f"""
            <div class="metric-card blue">

                <div class="metric-label">
                    MEDIUM-RISK SIGNALS
                </div>

                <div class="metric-value blue-text">
                    {medium_risk:,}
                </div>

            </div>
            """
        )

    with c4:

        st.html(
            f"""
            <div class="metric-card green">

                <div class="metric-label">
                    AVERAGE PREDICTED RISK
                </div>

                <div class="metric-value orange">
                    {average_risk:.1f}%
                </div>

            </div>
            """
        )

    # =========================================================
    # SYSTEM HEALTH
    # =========================================================

    st.html(
        """
        <div class="section-label">
            SYSTEM HEALTH
        </div>

        <div class="section-title">
            Prediction pipeline health.
        </div>

        <div class="section-description">
            Basic data-quality checks for the active prediction
            dataset.
        </div>
        """
    )

    prediction_missing = (
        df[
            "Attrition_Probability"
        ].isna().sum()
    )

    risk_missing = (
        df[
            "Risk_Category"
        ].isna().sum()
    )

    duplicate_count = (
        df.duplicated().sum()
    )

    prediction_status = (
        "HEALTHY"
        if prediction_missing == 0
        else "CHECK"
    )

    risk_status = (
        "HEALTHY"
        if risk_missing == 0
        else "CHECK"
    )

    integrity_status = (
        "HEALTHY"
        if duplicate_count == 0
        else "CHECK"
    )

    h1, h2, h3 = st.columns(3)

    with h1:

        status_class = (
            "green-text"
            if prediction_missing == 0
            else "orange"
        )

        st.html(
            f"""
            <div class="info-card green-card">

                <div class="info-number {status_class}">
                    {prediction_status}
                </div>

                <div class="info-title">
                    Prediction Coverage
                </div>

                <div class="info-text">
                    Missing prediction values:
                    {prediction_missing}
                </div>

            </div>
            """
        )

    with h2:

        status_class = (
            "green-text"
            if risk_missing == 0
            else "orange"
        )

        st.html(
            f"""
            <div class="info-card blue-card">

                <div class="info-number {status_class}">
                    {risk_status}
                </div>

                <div class="info-title">
                    Risk Classification
                </div>

                <div class="info-text">
                    Missing risk categories:
                    {risk_missing}
                </div>

            </div>
            """
        )

    with h3:

        status_class = (
            "green-text"
            if duplicate_count == 0
            else "orange"
        )

        st.html(
            f"""
            <div class="info-card">

                <div class="info-number {status_class}">
                    {integrity_status}
                </div>

                <div class="info-title">
                    Data Integrity
                </div>

                <div class="info-text">
                    Duplicate rows:
                    {duplicate_count}
                </div>

            </div>
            """
        )

    # =========================================================
    # RISK DISTRIBUTION
    # =========================================================

    st.html(
        """
        <div class="section-label">
            RISK MONITORING
        </div>

        <div class="section-title">
            Current workforce risk distribution.
        </div>
        """
    )

    risk_distribution = pd.DataFrame(
        {
            "Risk Category": [
                "Low",
                "Medium",
                "High"
            ],
            "Employees": [
                low_risk,
                medium_risk,
                high_risk
            ]
        }
    )

    fig = px.bar(
        risk_distribution,
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
        paper_bgcolor="#0c0c0c",
        plot_bgcolor="#0c0c0c",
        font=dict(
            color="#ffffff"
        ),
        height=430,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            gridcolor="#242424",
            title="Employees"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="monitoring_risk_distribution"
    )

    # =========================================================
    # DEPARTMENT MONITORING
    # =========================================================

    st.html(
        """
        <div class="section-label">
            DEPARTMENT MONITORING
        </div>

        <div class="section-title">
            Risk concentration by department.
        </div>

        <div class="section-description">
            Compare average predicted attrition risk and
            high-risk employee counts across departments.
        </div>
        """
    )

    department_df = (
        monitoring_df
        .groupby("Department")
        .agg(
            Employees=(
                "Employee_ID",
                "count"
            ),
            Average_Risk=(
                "Attrition_Probability",
                "mean"
            ),
            High_Risk=(
                "Risk_Category",
                lambda x:
                x.astype(str)
                .str.lower()
                .eq("high")
                .sum()
            ),
            Medium_Risk=(
                "Risk_Category",
                lambda x:
                x.astype(str)
                .str.lower()
                .eq("medium")
                .sum()
            )
        )
        .reset_index()
    )

    department_df[
        "Average_Risk"
    ] = (
        department_df[
            "Average_Risk"
        ] * 100
    ).round(2)

    st.dataframe(
        department_df.sort_values(
            "Average_Risk",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    if len(department_df) > 0:

        department_chart = px.bar(
            department_df,
            x="Department",
            y="Average_Risk",
            text="Average_Risk"
        )

        department_chart.update_traces(
            marker_color="#2f5bff",
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        department_chart.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0c0c0c",
            plot_bgcolor="#0c0c0c",
            font=dict(
                color="#ffffff"
            ),
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                gridcolor="#242424",
                title="Average Risk (%)"
            )
        )

        st.plotly_chart(
            department_chart,
            use_container_width=True,
            key="monitoring_department_chart"
        )

    # =========================================================
    # JOB ROLE MONITORING
    # =========================================================

    st.html(
        """
        <div class="section-label">
            ROLE MONITORING
        </div>

        <div class="section-title">
            Risk concentration by job role.
        </div>
        """
    )

    role_df = (
        monitoring_df
        .groupby(
            [
                "Department",
                "JobRole"
            ]
        )
        .agg(
            Employees=(
                "Employee_ID",
                "count"
            ),
            Average_Risk=(
                "Attrition_Probability",
                "mean"
            ),
            High_Risk=(
                "Risk_Category",
                lambda x:
                x.astype(str)
                .str.lower()
                .eq("high")
                .sum()
            )
        )
        .reset_index()
    )

    role_df[
        "Average_Risk"
    ] = (
        role_df[
            "Average_Risk"
        ] * 100
    ).round(2)

    st.dataframe(
        role_df.sort_values(
            "Average_Risk",
            ascending=False
        ).head(20),
        use_container_width=True,
        hide_index=True
    )

    # =========================================================
    # PRIORITY WATCHLIST
    # =========================================================

    st.html(
        """
        <div class="section-label">
            PRIORITY WATCHLIST
        </div>

        <div class="section-title">
            Highest predicted attrition risk.
        </div>

        <div class="section-description">
            These employees have the highest predicted
            attrition probabilities in the monitored population.
        </div>
        """
    )

    watchlist = monitoring_df[
        monitoring_df[
            "Risk_Category"
        ]
        .astype(str)
        .str.lower()
        .eq("high")
    ][
        [
            "Employee_ID",
            "Department",
            "JobRole",
            "Attrition_Probability",
            "Risk_Category"
        ]
    ].copy()

    watchlist[
        "Attrition_Probability"
    ] = (
        watchlist[
            "Attrition_Probability"
        ] * 100
    ).round(1)

    watchlist = watchlist.sort_values(
        "Attrition_Probability",
        ascending=False
    ).head(20)

    if len(watchlist) > 0:

        st.dataframe(
            watchlist,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No high-risk employees are currently "
            "present in the monitored population."
        )

    # =========================================================
    # THRESHOLD MONITORING
    # =========================================================

    st.html(
        """
        <div class="section-label">
            RISK THRESHOLD
        </div>

        <div class="section-title">
            Monitor employees above a selected threshold.
        </div>
        """
    )

    threshold = st.slider(
        "Attrition probability threshold",
        min_value=0.30,
        max_value=0.90,
        value=0.60,
        step=0.05,
        format="%.0f%%",
        key="monitoring_threshold"
    )

    threshold_employees = monitoring_df[
        monitoring_df[
            "Attrition_Probability"
        ] >= threshold
    ].copy()

    threshold_count = len(
        threshold_employees
    )

    st.html(
        f"""
        <div class="scenario-card">

            <div class="scenario-title">
                {threshold_count:,} employees
            </div>

            <div class="scenario-text">
                have a predicted attrition probability
                greater than or equal to
                <strong>{threshold:.0%}</strong>.
            </div>

        </div>
        """
    )

    if threshold_count > 0:

        threshold_table = threshold_employees[
            [
                "Employee_ID",
                "Department",
                "JobRole",
                "Attrition_Probability",
                "Risk_Category"
            ]
        ].copy()

        threshold_table[
            "Attrition_Probability"
        ] = (
            threshold_table[
                "Attrition_Probability"
            ] * 100
        ).round(1)

        st.dataframe(
            threshold_table.sort_values(
                "Attrition_Probability",
                ascending=False
            ).head(20),
            use_container_width=True,
            hide_index=True
        )

    # =========================================================
    # MONITORING GUIDANCE
    # =========================================================

    st.html(
        """
        <div class="scenario-card">

            <div class="scenario-title">
                Monitoring Guidance
            </div>

            <div class="scenario-text">
                Predicted attrition risk is a decision-support
                signal. High-risk employees should receive
                appropriate human review rather than automatic
                employment decisions. HR teams should consider
                employee context, fairness, privacy and other
                relevant organizational information.
            </div>

        </div>
        """
    )

    # =========================================================
    # FOOTER
    # =========================================================

    st.html(
        """
        <div class="footer">

            OPERATIONAL WORKFORCE MONITORING
            &nbsp;&nbsp;•&nbsp;&nbsp;
            MACHINE LEARNING
            &nbsp;&nbsp;•&nbsp;&nbsp;
            EXPLAINABLE AI
            &nbsp;&nbsp;•&nbsp;&nbsp;
            PREDICTIVE ANALYTICS

        </div>
        """
    )