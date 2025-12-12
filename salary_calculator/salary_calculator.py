#!/usr/bin/env python3
"""
Salary Calculator - Calculate take-home pay with pension contributions
Assumes UK tax system (2024/2025 tax year)
"""

import csv
from datetime import datetime


class SalaryCalculator:
    """Calculate net salary with pension contributions and tax deductions"""

    # UK Tax rates for 2024/2025
    PERSONAL_ALLOWANCE = 12570
    BASIC_RATE_THRESHOLD = 50270
    HIGHER_RATE_THRESHOLD = 125140

    BASIC_RATE = 0.20
    HIGHER_RATE = 0.40
    ADDITIONAL_RATE = 0.45

    # National Insurance rates 2024/2025
    NI_THRESHOLD = 12570
    NI_UPPER_THRESHOLD = 50270
    NI_RATE_STANDARD = 0.08  # 8% on earnings between thresholds
    NI_RATE_ADDITIONAL = 0.02  # 2% on earnings above upper threshold

    # Employer National Insurance rates 2024/2025
    EMPLOYER_NI_THRESHOLD = 9100  # Secondary Threshold
    EMPLOYER_NI_RATE = 0.138  # 13.8%

    def __init__(
        self,
        gross_salary: float,
        salary_sacrifice_percent: float = 0,
        employer_contribution_percent: float = 0,
    ):
        """
        Initialize calculator with gross salary and optional salary sacrifice

        Args:
            gross_salary: Annual gross salary
            salary_sacrifice_percent: Percentage of salary to sacrifice for pension (0-100)
            employer_contribution_percent: Additional employer pension contribution percentage (0-100)
        """
        self.gross_salary = gross_salary
        self.salary_sacrifice_percent = salary_sacrifice_percent
        self.employer_contribution_percent = employer_contribution_percent

    def calculate_pension_contribution(self) -> float:
        """Calculate employee pension contribution from salary sacrifice"""
        return self.gross_salary * (self.salary_sacrifice_percent / 100)

    def calculate_employer_ni_without_sacrifice(self) -> float:
        """Calculate employer NI on full gross salary (without salary sacrifice)"""
        if self.gross_salary <= self.EMPLOYER_NI_THRESHOLD:
            return 0
        return (self.gross_salary - self.EMPLOYER_NI_THRESHOLD) * self.EMPLOYER_NI_RATE

    def calculate_employer_ni_with_sacrifice(self) -> float:
        """Calculate employer NI after salary sacrifice"""
        adjusted_salary = self.calculate_adjusted_salary()
        if adjusted_salary <= self.EMPLOYER_NI_THRESHOLD:
            return 0
        return (adjusted_salary - self.EMPLOYER_NI_THRESHOLD) * self.EMPLOYER_NI_RATE

    def calculate_employer_ni_savings(self) -> float:
        """Calculate employer NI savings from salary sacrifice"""
        return (
            self.calculate_employer_ni_without_sacrifice()
            - self.calculate_employer_ni_with_sacrifice()
        )

    def calculate_employer_contribution(self) -> float:
        """Calculate employer pension contribution as flat percentage of gross salary"""
        return self.gross_salary * (self.employer_contribution_percent / 100)

    def calculate_total_pension_pot(self) -> float:
        """Calculate total pension contributions (employee + employer + NI savings)"""
        return (
            self.calculate_pension_contribution()
            + self.calculate_employer_contribution()
            + self.calculate_employer_ni_savings()
        )

    def calculate_adjusted_salary(self) -> float:
        """Calculate salary after pension sacrifice (taxable income base)"""
        return self.gross_salary - self.calculate_pension_contribution()

    def calculate_tax_free_allowance(self) -> float:
        """
        Calculate tax-free personal allowance
        Reduces by £1 for every £2 earned over £100,000
        """
        adjusted_salary = self.calculate_adjusted_salary()

        if adjusted_salary <= 100000:
            return self.PERSONAL_ALLOWANCE

        reduction = (adjusted_salary - 100000) / 2
        allowance = max(0, self.PERSONAL_ALLOWANCE - reduction)
        return allowance

    def calculate_income_tax(self) -> float:
        """Calculate total income tax"""
        adjusted_salary = self.calculate_adjusted_salary()
        tax_free_allowance = self.calculate_tax_free_allowance()
        taxable_income = max(0, adjusted_salary - tax_free_allowance)

        tax = 0

        # Basic rate (20%)
        if taxable_income > 0:
            basic_band = min(
                taxable_income, self.BASIC_RATE_THRESHOLD - tax_free_allowance
            )
            tax += basic_band * self.BASIC_RATE

        # Higher rate (40%)
        if taxable_income > (self.BASIC_RATE_THRESHOLD - tax_free_allowance):
            higher_band_start = self.BASIC_RATE_THRESHOLD - tax_free_allowance
            higher_band_end = self.HIGHER_RATE_THRESHOLD - tax_free_allowance
            higher_band = min(
                taxable_income - higher_band_start, higher_band_end - higher_band_start
            )
            if higher_band > 0:
                tax += higher_band * self.HIGHER_RATE

        # Additional rate (45%)
        if taxable_income > (self.HIGHER_RATE_THRESHOLD - tax_free_allowance):
            additional_band = taxable_income - (
                self.HIGHER_RATE_THRESHOLD - tax_free_allowance
            )
            tax += additional_band * self.ADDITIONAL_RATE

        return tax

    def calculate_national_insurance(self) -> float:
        """Calculate National Insurance contributions"""
        adjusted_salary = self.calculate_adjusted_salary()
        ni = 0

        if adjusted_salary > self.NI_THRESHOLD:
            # Standard rate on earnings between thresholds
            standard_band = min(
                adjusted_salary - self.NI_THRESHOLD,
                self.NI_UPPER_THRESHOLD - self.NI_THRESHOLD,
            )
            ni += standard_band * self.NI_RATE_STANDARD

            # Additional rate on earnings above upper threshold
            if adjusted_salary > self.NI_UPPER_THRESHOLD:
                additional_band = adjusted_salary - self.NI_UPPER_THRESHOLD
                ni += additional_band * self.NI_RATE_ADDITIONAL

        return ni

    def calculate_total_deductions(self) -> float:
        """Calculate total deductions (tax + NI, excluding pension)"""
        return self.calculate_income_tax() + self.calculate_national_insurance()

    def calculate_net_income(self) -> float:
        """Calculate net income after all deductions"""
        adjusted_salary = self.calculate_adjusted_salary()
        deductions = self.calculate_total_deductions()
        return adjusted_salary - deductions

    def calculate_effective_tax_rate(self) -> float:
        """Calculate effective tax rate as percentage of gross salary"""
        total_deductions = self.calculate_total_deductions()
        pension_contribution = self.calculate_pension_contribution()
        total_reductions = total_deductions + pension_contribution

        if self.gross_salary == 0:
            return 0

        return (total_reductions / self.gross_salary) * 100

    def get_annual_breakdown(self) -> dict:
        """Get complete annual salary breakdown"""
        return {
            "gross_income": self.gross_salary,
            "employee_pension_contributions": self.calculate_pension_contribution(),
            "employer_pension_contribution": self.calculate_employer_contribution(),
            "employer_ni_savings": self.calculate_employer_ni_savings(),
            "total_pension_pot": self.calculate_total_pension_pot(),
            "adjusted_gross": self.calculate_adjusted_salary(),
            "tax_free_allowance": self.calculate_tax_free_allowance(),
            "income_tax": self.calculate_income_tax(),
            "national_insurance": self.calculate_national_insurance(),
            "total_deductions": self.calculate_total_deductions(),
            "net_income": self.calculate_net_income(),
            "effective_tax_rate": self.calculate_effective_tax_rate(),
        }

    def get_monthly_breakdown(self) -> dict:
        """Get complete monthly salary breakdown"""
        annual = self.get_annual_breakdown()
        return {
            "gross_income": annual["gross_income"] / 12,
            "employee_pension_contributions": annual["employee_pension_contributions"]
            / 12,
            "employer_pension_contribution": annual["employer_pension_contribution"]
            / 12,
            "employer_ni_savings": annual["employer_ni_savings"] / 12,
            "total_pension_pot": annual["total_pension_pot"] / 12,
            "adjusted_gross": annual["adjusted_gross"] / 12,
            "tax_free_allowance": annual["tax_free_allowance"] / 12,
            "income_tax": annual["income_tax"] / 12,
            "national_insurance": annual["national_insurance"] / 12,
            "total_deductions": annual["total_deductions"] / 12,
            "net_income": annual["net_income"] / 12,
            "effective_tax_rate": annual["effective_tax_rate"],
        }

    def print_breakdown(self):
        """Print formatted salary breakdown"""
        annual = self.get_annual_breakdown()
        monthly = self.get_monthly_breakdown()

        print("\n" + "=" * 60)
        print("SALARY CALCULATOR BREAKDOWN")
        print("=" * 60)
        print(f"\nInput Parameters:")
        print(f"  Gross Salary: £{self.gross_salary:,.2f}")
        print(f"  Employee Salary Sacrifice: {self.salary_sacrifice_percent}%")
        print(f"  Employer Contribution: {self.employer_contribution_percent}%")

        print("\n" + "-" * 60)
        print(f"{'ITEM':<35} {'ANNUAL':>12} {'MONTHLY':>12}")
        print("-" * 60)

        print(
            f"{'Gross Income':<35} £{annual['gross_income']:>10,.2f} £{monthly['gross_income']:>10,.2f}"
        )
        print(
            f"{'Employee Pension Contribution':<35} £{annual['employee_pension_contributions']:>10,.2f} £{monthly['employee_pension_contributions']:>10,.2f}"
        )
        print(
            f"{'Employer Pension Contribution':<35} £{annual['employer_pension_contribution']:>10,.2f} £{monthly['employer_pension_contribution']:>10,.2f}"
        )
        print(
            f"{'  (incl. Employer NI Savings)':<35} £{annual['employer_ni_savings']:>10,.2f} £{monthly['employer_ni_savings']:>10,.2f}"
        )
        print(
            f"{'TOTAL PENSION POT':<35} £{annual['total_pension_pot']:>10,.2f} £{monthly['total_pension_pot']:>10,.2f}"
        )
        print(
            f"{'Adjusted Gross (Taxable)':<35} £{annual['adjusted_gross']:>10,.2f} £{monthly['adjusted_gross']:>10,.2f}"
        )

        print("\n" + "-" * 60)
        print(
            f"{'Tax-Free Allowance':<35} £{annual['tax_free_allowance']:>10,.2f} £{monthly['tax_free_allowance']:>10,.2f}"
        )

        print("\n" + "-" * 60)
        print("DEDUCTIONS:")
        print(
            f"{'  Income Tax':<35} £{annual['income_tax']:>10,.2f} £{monthly['income_tax']:>10,.2f}"
        )
        print(
            f"{'  National Insurance':<35} £{annual['national_insurance']:>10,.2f} £{monthly['national_insurance']:>10,.2f}"
        )
        print(
            f"{'  Total Deductions':<35} £{annual['total_deductions']:>10,.2f} £{monthly['total_deductions']:>10,.2f}"
        )

        print("\n" + "-" * 60)
        print(
            f"{'NET INCOME':<35} £{annual['net_income']:>10,.2f} £{monthly['net_income']:>10,.2f}"
        )
        print(f"{'Effective Tax Rate':<35} {annual['effective_tax_rate']:>10.2f}%")
        print("=" * 60 + "\n")


def generate_range_csv(
    gross_salary: float,
    start_percent: float,
    end_percent: float,
    step: float,
    output_file: str,
    employer_contribution_percent: float = 0,
):
    """Generate CSV file with calculations for a range of salary sacrifice percentages

    Args:
        gross_salary: Annual gross salary
        start_percent: Starting salary sacrifice percentage
        end_percent: Ending salary sacrifice percentage
        step: Step size for the range
        output_file: Output CSV filename
        employer_contribution_percent: Employer pension contribution percentage
    """
    # Generate range of percentages
    current = start_percent
    percentages = []
    while current <= end_percent:
        percentages.append(round(current, 2))
        current += step

    # Open CSV file for writing
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = [
            "salary_sacrifice_percent",
            "annual_gross_income",
            "annual_employee_pension_contributions",
            "annual_employer_pension_contribution",
            "annual_employer_ni_savings",
            "annual_total_pension_pot",
            "annual_tax_free_allowance",
            "annual_income_tax",
            "annual_national_insurance",
            "annual_total_deductions",
            "annual_net_income",
            "monthly_gross_income",
            "monthly_employee_pension_contributions",
            "monthly_employer_pension_contribution",
            "monthly_employer_ni_savings",
            "monthly_total_pension_pot",
            "monthly_tax_free_allowance",
            "monthly_income_tax",
            "monthly_national_insurance",
            "monthly_total_deductions",
            "monthly_net_income",
            "effective_tax_rate_percent",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Calculate for each percentage
        for percent in percentages:
            calc = SalaryCalculator(
                gross_salary, percent, employer_contribution_percent
            )
            annual = calc.get_annual_breakdown()
            monthly = calc.get_monthly_breakdown()

            writer.writerow(
                {
                    "salary_sacrifice_percent": percent,
                    "annual_gross_income": round(annual["gross_income"], 2),
                    "annual_employee_pension_contributions": round(
                        annual["employee_pension_contributions"], 2
                    ),
                    "annual_employer_pension_contribution": round(
                        annual["employer_pension_contribution"], 2
                    ),
                    "annual_employer_ni_savings": round(
                        annual["employer_ni_savings"], 2
                    ),
                    "annual_total_pension_pot": round(annual["total_pension_pot"], 2),
                    "annual_tax_free_allowance": round(annual["tax_free_allowance"], 2),
                    "annual_income_tax": round(annual["income_tax"], 2),
                    "annual_national_insurance": round(annual["national_insurance"], 2),
                    "annual_total_deductions": round(annual["total_deductions"], 2),
                    "annual_net_income": round(annual["net_income"], 2),
                    "monthly_gross_income": round(monthly["gross_income"], 2),
                    "monthly_employee_pension_contributions": round(
                        monthly["employee_pension_contributions"], 2
                    ),
                    "monthly_employer_pension_contribution": round(
                        monthly["employer_pension_contribution"], 2
                    ),
                    "monthly_employer_ni_savings": round(
                        monthly["employer_ni_savings"], 2
                    ),
                    "monthly_total_pension_pot": round(monthly["total_pension_pot"], 2),
                    "monthly_tax_free_allowance": round(
                        monthly["tax_free_allowance"], 2
                    ),
                    "monthly_income_tax": round(monthly["income_tax"], 2),
                    "monthly_national_insurance": round(
                        monthly["national_insurance"], 2
                    ),
                    "monthly_total_deductions": round(monthly["total_deductions"], 2),
                    "monthly_net_income": round(monthly["net_income"], 2),
                    "effective_tax_rate_percent": round(
                        annual["effective_tax_rate"], 2
                    ),
                }
            )

    print(f"\nCSV file generated: {output_file}")
    print(
        f"Calculated {len(percentages)} scenarios from {start_percent}% to {end_percent}% (step: {step}%)"
    )


def main():
    """Main function to run the calculator"""
    print("UK Salary Calculator (2024/2025 Tax Year)")
    print("=" * 60)
    print("\nModes:")
    print("  1. Single calculation (interactive)")
    print("  2. Range calculation (CSV export)")

    try:
        mode = input("\nSelect mode (1 or 2): ").strip()

        if mode == "1":
            # Single calculation mode
            gross_salary = (
                float(input("\nEnter your annual gross salary (£k): ")) * 1000
            )
            salary_sacrifice = float(
                input("Enter employee salary sacrifice percentage for pension (%): ")
            )
            employer_contribution = float(
                input("Enter employer pension contribution percentage (%): ")
            )

            if gross_salary < 0:
                print("Error: Salary cannot be negative")
                return

            if salary_sacrifice < 0 or salary_sacrifice > 100:
                print("Error: Salary sacrifice must be between 0 and 100")
                return

            if employer_contribution < 0 or employer_contribution > 100:
                print("Error: Employer contribution must be between 0 and 100")
                return

            # Create calculator and print breakdown
            calculator = SalaryCalculator(
                gross_salary, salary_sacrifice, employer_contribution
            )
            calculator.print_breakdown()

        elif mode == "2":
            # Range calculation mode
            gross_salary = (
                float(input("\nEnter your annual gross salary (£k): ")) * 1000
            )
            employer_contribution = float(
                input("Enter employer pension contribution percentage (%): ")
            )
            start_percent = float(
                input("Enter starting salary sacrifice percentage (%): ")
            )
            end_percent = float(input("Enter ending salary sacrifice percentage (%): "))
            step = float(input("Enter step size (%, e.g., 0.5 or 1): "))

            if gross_salary < 0:
                print("Error: Salary cannot be negative")
                return

            if employer_contribution < 0 or employer_contribution > 100:
                print("Error: Employer contribution must be between 0 and 100")
                return

            if start_percent < 0 or end_percent > 100 or start_percent > end_percent:
                print("Error: Invalid range (must be 0-100 and start <= end)")
                return

            if step <= 0:
                print("Error: Step must be positive")
                return

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"salary_calc_range_{int(gross_salary)}_{timestamp}.csv"

            generate_range_csv(
                gross_salary,
                start_percent,
                end_percent,
                step,
                output_file,
                employer_contribution,
            )

        else:
            print("Error: Invalid mode selection")

    except ValueError:
        print("Error: Please enter valid numbers")
    except KeyboardInterrupt:
        print("\n\nCalculation cancelled.")


if __name__ == "__main__":
    main()
