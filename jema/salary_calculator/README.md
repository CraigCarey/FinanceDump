# Salary Calculator

A Python application to calculate take-home pay with salary sacrifice pension contributions using UK tax rules (2024/2025 tax year).

## Features

Calculates the following (both monthly and yearly):
- Gross income
- Employee pension contributions (via salary sacrifice)
- Employer pension contributions (including employer NI savings)
- Total pension pot
- Tax-free allowance
- Income tax
- National Insurance
- Total deductions
- Net income
- Effective tax rate

## Usage

Run the calculator:

```bash
python salary_calculator.py
```

The calculator has two modes:

### Mode 1: Single Calculation (Interactive)
Calculates and displays results for a single salary sacrifice percentage.

You'll be prompted to enter:
1. Annual gross salary (£k)
2. Employee salary sacrifice percentage for pension (%)
3. Employer pension contribution percentage (%)

### Mode 2: Range Calculation (CSV Export)
Generates a CSV file with calculations for a range of salary sacrifice percentages.

You'll be prompted to enter:
1. Annual gross salary (£)
2. Employer pension contribution percentage (%)
3. Starting salary sacrifice percentage (%)
4. Ending salary sacrifice percentage (%)
5. Step size (%, e.g., 0.5 or 1)

## Examples

### Single Calculation Example

```
Select mode (1 or 2): 1

Enter your annual gross salary (£k): 60
Enter employee salary sacrifice percentage for pension (%): 8
Enter employer pension contribution percentage (%): 3

SALARY CALCULATOR BREAKDOWN
============================================================

Input Parameters:
  Gross Salary: £60,000.00
  Employee Salary Sacrifice: 8%
  Employer Contribution: 3%

------------------------------------------------------------
ITEM                                      ANNUAL      MONTHLY
------------------------------------------------------------
Gross Income                          £60,000.00   £5,000.00
Employee Pension Contribution          £4,800.00     £400.00
Employer Pension Contribution          £2,462.40     £205.20
  (incl. Employer NI Savings)            £662.40      £55.20
TOTAL PENSION POT                      £7,262.40     £605.20
Adjusted Gross (Taxable)              £55,200.00   £4,600.00

------------------------------------------------------------
Tax-Free Allowance                    £12,570.00   £1,047.50

------------------------------------------------------------
DEDUCTIONS:
  Income Tax                           £9,512.00     £792.67
  National Insurance                   £3,114.60     £259.55
  Total Deductions                    £12,626.60   £1,052.22

------------------------------------------------------------
NET INCOME                            £42,573.40   £3,547.78
Effective Tax Rate                        29.04%
============================================================
```

### Range Calculation Example

```
Select mode (1 or 2): 2

Enter your annual gross salary (£): 60000
Enter employer pension contribution percentage (%): 3
Enter starting salary sacrifice percentage (%): 0
Enter ending salary sacrifice percentage (%): 10
Enter step size (%, e.g., 0.5 or 1): 2

CSV file generated: salary_calc_range_60000_20251211_133606.csv
Calculated 6 scenarios from 0.0% to 10.0% (step: 2.0%)
```

The CSV file will contain columns for:
- Salary sacrifice percentage
- Annual values: gross income, employee pension contributions, employer pension contribution, employer NI savings, total pension pot, tax-free allowance, income tax, national insurance, total deductions, net income
- Monthly values: gross income, employee pension contributions, employer pension contribution, employer NI savings, total pension pot, tax-free allowance, income tax, national insurance, total deductions, net income
- Effective tax rate percentage

## Tax Information

Based on UK 2024/2025 tax year:
- Personal Allowance: £12,570
- Basic rate (20%): £12,571 - £50,270
- Higher rate (40%): £50,271 - £125,140
- Additional rate (45%): Over £125,140

National Insurance (Employee):
- 8% on earnings between £12,570 - £50,270
- 2% on earnings above £50,270

Employer National Insurance:
- 13.8% on earnings above £9,100 (Secondary Threshold)

## Notes

- Salary sacrifice reduces your taxable income before tax and NI calculations
- Employer NI savings from salary sacrifice are added to the employer pension contribution
- Personal allowance is reduced by £1 for every £2 earned over £100,000
- This calculator assumes you are an employee (not self-employed)
- Employer contributions help maximize your pension pot at no extra cost to you
