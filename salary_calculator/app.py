#!/usr/bin/env python3
"""
Streamlit app for UK Salary Calculator (2024/2025 Tax Year)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from salary_calculator import SalaryCalculator


def format_currency(value):
    """Format value as currency"""
    return f"£{value:,.2f}"


def create_breakdown_chart(annual_data, monthly_data):
    """Create a comparison chart of annual vs monthly breakdown"""
    categories = [
        "Gross Income",
        "Employee Pension",
        "Income Tax",
        "National Insurance",
        "Net Income",
    ]

    annual_values = [
        annual_data["gross_income"],
        annual_data["employee_pension_contributions"],
        annual_data["income_tax"],
        annual_data["national_insurance"],
        annual_data["net_income"],
    ]

    monthly_values = [
        monthly_data["gross_income"],
        monthly_data["employee_pension_contributions"],
        monthly_data["income_tax"],
        monthly_data["national_insurance"],
        monthly_data["net_income"],
    ]

    fig = go.Figure(
        data=[
            go.Bar(name="Annual (£)", x=categories, y=annual_values),
            go.Bar(name="Monthly (£)", x=categories, y=monthly_values),
        ]
    )

    fig.update_layout(
        barmode="group",
        title="Salary Breakdown Comparison",
        xaxis_title="Category",
        yaxis_title="Amount (£)",
        height=400,
    )

    return fig


def create_waterfall_chart(annual_data):
    """Create a waterfall chart showing deductions from gross to net"""
    fig = go.Figure(
        go.Waterfall(
            name="Salary Breakdown",
            orientation="v",
            measure=[
                "relative",
                "relative",
                "relative",
                "relative",
                "relative",
                "total",
            ],
            x=[
                "Gross Income",
                "Employee Pension",
                "Employer Pension",
                "Income Tax",
                "National Insurance",
                "Net Income",
            ],
            textposition="outside",
            text=[
                format_currency(annual_data["gross_income"]),
                format_currency(-annual_data["employee_pension_contributions"]),
                format_currency(annual_data["employer_pension_contribution"]),
                format_currency(-annual_data["income_tax"]),
                format_currency(-annual_data["national_insurance"]),
                format_currency(annual_data["net_income"]),
            ],
            y=[
                annual_data["gross_income"],
                -annual_data["employee_pension_contributions"],
                annual_data["employer_pension_contribution"],
                -annual_data["income_tax"],
                -annual_data["national_insurance"],
                annual_data["net_income"],
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )

    fig.update_layout(
        title="Annual Salary Waterfall (Gross to Net)",
        showlegend=False,
        height=500,
    )

    return fig


def create_pension_chart(sacrifice_range, net_income_values, pension_pot_values):
    """Create a chart showing the relationship between salary sacrifice and net income/pension"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=sacrifice_range,
            y=net_income_values,
            mode="lines+markers",
            name="Annual Net Income",
            yaxis="y",
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=sacrifice_range,
            y=pension_pot_values,
            mode="lines+markers",
            name="Annual Pension Pot",
            yaxis="y2",
            line=dict(color="green"),
        )
    )

    fig.update_layout(
        title="Impact of Salary Sacrifice on Net Income and Pension",
        xaxis_title="Salary Sacrifice (%)",
        yaxis=dict(title="Net Income (£)", side="left", showgrid=False),
        yaxis2=dict(
            title="Pension Pot (£)",
            side="right",
            overlaying="y",
            showgrid=False,
        ),
        height=500,
        hovermode="x unified",
    )

    return fig


def main():
    st.set_page_config(
        page_title="UK Salary Calculator",
        page_icon="💷",
        layout="wide",
    )

    st.title("💷 UK Salary Calculator")
    st.markdown("**2024/2025 Tax Year**")

    st.sidebar.header("Input Parameters")

    # Input fields
    gross_salary_k = st.sidebar.number_input(
        "Annual Gross Salary (£k)",
        min_value=0.0,
        max_value=500.0,
        value=135.0,
        step=1.0,
        help="Your annual gross salary in thousands of pounds",
    )

    gross_salary = gross_salary_k * 1000

    salary_sacrifice = st.sidebar.slider(
        "Employee Salary Sacrifice (%)",
        min_value=0.0,
        max_value=50.0,
        value=28.0,
        step=0.5,
        help="Percentage of salary sacrificed for pension contributions",
    )

    employer_contribution = st.sidebar.slider(
        "Employer Pension Contribution (%)",
        min_value=0.0,
        max_value=30.0,
        value=8.0,
        step=0.5,
        help="Employer's pension contribution as percentage of gross salary",
    )

    # Create calculator
    calc = SalaryCalculator(gross_salary, salary_sacrifice, employer_contribution)
    annual = calc.get_annual_breakdown()
    monthly = calc.get_monthly_breakdown()

    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Annual Net Income", format_currency(annual["net_income"]))

    with col2:
        st.metric("Monthly Net Income", format_currency(monthly["net_income"]))

    with col3:
        st.metric(
            "Total Pension Pot (Annual)", format_currency(annual["total_pension_pot"])
        )

    with col4:
        st.metric("Effective Tax Rate", f"{annual['effective_tax_rate']:.2f}%")

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Breakdown", "💧 Waterfall", "📈 Scenario Analysis", "📋 Details"]
    )

    with tab1:
        st.subheader("Salary Breakdown")
        chart = create_breakdown_chart(annual, monthly)
        st.plotly_chart(chart, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Annual Breakdown")
            breakdown_df = pd.DataFrame(
                {
                    "Category": [
                        "Gross Income",
                        "Employee Pension",
                        "Employer Pension",
                        "Employer NI Savings",
                        "Total Pension Pot",
                        "Adjusted Gross",
                        "Tax-Free Allowance",
                        "Income Tax",
                        "National Insurance",
                        "Total Deductions",
                        "Net Income",
                    ],
                    "Amount": [
                        format_currency(annual["gross_income"]),
                        format_currency(annual["employee_pension_contributions"]),
                        format_currency(annual["employer_pension_contribution"]),
                        format_currency(annual["employer_ni_savings"]),
                        format_currency(annual["total_pension_pot"]),
                        format_currency(annual["adjusted_gross"]),
                        format_currency(annual["tax_free_allowance"]),
                        format_currency(annual["income_tax"]),
                        format_currency(annual["national_insurance"]),
                        format_currency(annual["total_deductions"]),
                        format_currency(annual["net_income"]),
                    ],
                }
            )
            st.dataframe(breakdown_df, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("### Monthly Breakdown")
            monthly_df = pd.DataFrame(
                {
                    "Category": [
                        "Gross Income",
                        "Employee Pension",
                        "Employer Pension",
                        "Employer NI Savings",
                        "Total Pension Pot",
                        "Adjusted Gross",
                        "Tax-Free Allowance",
                        "Income Tax",
                        "National Insurance",
                        "Total Deductions",
                        "Net Income",
                    ],
                    "Amount": [
                        format_currency(monthly["gross_income"]),
                        format_currency(monthly["employee_pension_contributions"]),
                        format_currency(monthly["employer_pension_contribution"]),
                        format_currency(monthly["employer_ni_savings"]),
                        format_currency(monthly["total_pension_pot"]),
                        format_currency(monthly["adjusted_gross"]),
                        format_currency(monthly["tax_free_allowance"]),
                        format_currency(monthly["income_tax"]),
                        format_currency(monthly["national_insurance"]),
                        format_currency(monthly["total_deductions"]),
                        format_currency(monthly["net_income"]),
                    ],
                }
            )
            st.dataframe(monthly_df, hide_index=True, use_container_width=True)

    with tab2:
        st.subheader("Waterfall Chart: From Gross to Net")
        waterfall = create_waterfall_chart(annual)
        st.plotly_chart(waterfall, use_container_width=True)

        st.info(
            """
            This waterfall chart shows how your gross income transforms into net income:
            - Starting with gross income
            - Deducting employee pension contributions (salary sacrifice)
            - Adding employer pension contributions
            - Deducting income tax
            - Deducting National Insurance
            - Arriving at your net income
            """
        )

    with tab3:
        st.subheader("Scenario Analysis: Salary Sacrifice Impact")

        st.markdown(
            """
            This analysis shows how varying your salary sacrifice percentage affects:
            - Your net take-home pay
            - Your total pension pot (including employer contributions and NI savings)
        """
        )

        # Generate range of scenarios
        sacrifice_range = list(range(0, 51, 1))  # 0% to 50% in 1% steps
        net_income_values = []
        pension_pot_values = []

        for sacrifice_pct in sacrifice_range:
            temp_calc = SalaryCalculator(
                gross_salary, sacrifice_pct, employer_contribution
            )
            temp_annual = temp_calc.get_annual_breakdown()
            net_income_values.append(temp_annual["net_income"])
            pension_pot_values.append(temp_annual["total_pension_pot"])

        pension_chart = create_pension_chart(
            sacrifice_range, net_income_values, pension_pot_values
        )
        st.plotly_chart(pension_chart, use_container_width=True)

        # Create comparison table
        st.markdown("### Comparison Table")
        comparison_data = []
        for i, sacrifice_pct in enumerate(sacrifice_range[::5]):  # Every 5%
            temp_calc = SalaryCalculator(
                gross_salary, sacrifice_pct, employer_contribution
            )
            temp_annual = temp_calc.get_annual_breakdown()
            comparison_data.append(
                {
                    "Sacrifice %": f"{sacrifice_pct}%",
                    "Net Income": format_currency(temp_annual["net_income"]),
                    "Pension Pot": format_currency(temp_annual["total_pension_pot"]),
                    "Effective Tax Rate": f"{temp_annual['effective_tax_rate']:.2f}%",
                }
            )

        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, hide_index=True, use_container_width=True)

    with tab4:
        st.subheader("Tax System Details (2024/2025)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Income Tax Rates")
            tax_df = pd.DataFrame(
                {
                    "Band": [
                        "Personal Allowance",
                        "Basic Rate (20%)",
                        "Higher Rate (40%)",
                        "Additional Rate (45%)",
                    ],
                    "Threshold": [
                        "Up to £12,570",
                        "£12,571 to £50,270",
                        "£50,271 to £125,140",
                        "Over £125,140",
                    ],
                }
            )
            st.dataframe(tax_df, hide_index=True, use_container_width=True)

            st.markdown("### National Insurance Rates")
            ni_df = pd.DataFrame(
                {
                    "Band": [
                        "Below Threshold",
                        "Standard Rate (8%)",
                        "Additional Rate (2%)",
                    ],
                    "Threshold": [
                        "Up to £12,570",
                        "£12,571 to £50,270",
                        "Over £50,270",
                    ],
                }
            )
            st.dataframe(ni_df, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("### Employer National Insurance")
            emp_ni_df = pd.DataFrame(
                {
                    "Description": [
                        "Secondary Threshold",
                        "Employer NI Rate",
                    ],
                    "Value": [
                        "£9,100",
                        "13.8%",
                    ],
                }
            )
            st.dataframe(emp_ni_df, hide_index=True, use_container_width=True)

            st.markdown("### About Salary Sacrifice")
            st.info(
                """
                **Salary Sacrifice** reduces your taxable income by contributing 
                to your pension before tax is calculated. This means:
                
                - You pay less income tax
                - You pay less National Insurance
                - Your employer saves on National Insurance
                - Employer NI savings can boost your pension pot
                - Your take-home pay decreases, but your pension grows more efficiently
                """
            )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p><small>UK Tax Year 2024/2025 | This calculator provides estimates based on standard UK tax rules.</small></p>
            <p><small>For specific financial advice, please consult a qualified financial advisor.</small></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
