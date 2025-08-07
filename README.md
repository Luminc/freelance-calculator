# Dutch Freelance vs Employment Calculator

A comprehensive financial calculator for comparing freelance income versus employment in the Netherlands, with accurate 2025 Dutch tax calculations.

## Features

### 🧮 Accurate Tax Calculations
- **Income Tax (IB) & Social Security Premiums (PVV)**: Proper 2025 tax brackets and rates
- **Tax Credits (Heffingskortingen)**: 
  - General Tax Credit (Algemene Heffingskorting - AHK)
  - Labor Tax Credit (Arbeidskorting - AK)
- **ZVW Healthcare Premium**: Income-dependent healthcare contributions
- **Entrepreneurial Deductions**: Self-employed and starter deductions
- **SME Profit Exemption**: MKB winstvrijstelling (12.70% in 2025)

### 💼 Two Calculation Modes
1. **Rate-based**: Start with hourly rate, calculate net income
2. **Target-based**: Start with desired net income, find required hourly rate

### 👥 Employee Comparison Scenarios
1. **Equal Employer Costs**: What employee salary equals freelancer revenue?
2. **Equal Net Income**: What employer costs are needed for same net income?

### 📊 Comprehensive Output
- Detailed financial breakdowns
- Tax component analysis
- Professional disclaimers and assumptions
- Side-by-side comparison tables

## Quick Start

### Installation
```bash
git clone <repository-url>
cd freelance-calculator
python3 -m venv calc_env
source calc_env/bin/activate  # On Windows: calc_env\Scripts\activate
pip install -r requirements.txt
```

### Usage
```bash
source calc_env/bin/activate
python freelance_calculator.py
```

### Configuration
Edit the input parameters in `freelance_calculator.py`:

```python
# Choose calculation mode
calculation_mode = "rate_based"  # or "target_net_based"

# Freelancer inputs
freelance_hourly_rate_ex_vat_input = 24.00
hours_per_month_input = 130
freelance_aov_monthly_input = 200.00  # Business costs
freelance_other_costs_monthly_input = 50.00

# Tax settings
apply_entrepreneurial_deductions_input = True
desired_freelance_buffer_percentage_input = 0.16
```

## Example Output

For a €24/hour freelancer working 130 hours/month:

- **Net disposable income**: €2,209/month
- **Effective hourly rate**: €16.99/hour
- **Annual tax burden**: €2,421 (7% of revenue)
- **Equivalent employee salary**: €3,220/month gross

## Tax Year Compatibility

Currently supports:
- ✅ **2025**: Latest rates and brackets (primary focus)
- ✅ **2024**: Full support with historical rates
- 🔄 **Future years**: Easily configurable parameters

## Project Structure

```
freelance-calculator/
├── freelance_calculator.py    # Main calculator (v3.1)
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── archive/                 # Historical versions
│   ├── calculator_freelance.py  # Basic version
│   ├── calc.py              # Buggy intermediate version
│   ├── c4.py               # v4.0 - Good structure
│   └── c5.py               # v5.0 - Over-engineered
└── docs/                   # Future documentation
```

## Key Assumptions & Disclaimers

⚠️ **Important**: This is a model calculation for educational purposes.

### Freelancer Assumptions
- Tax calculations exclude potential heffingskortingen phase-outs
- AOV and business costs are fully deductible
- Buffer percentage applied to profit before fiscal deductions
- Pension contributions are personal (not business deductible)

### Employee Assumptions
- Net retention rates are estimated (75%/68%/62% by salary band)
- Holiday pay taxed at simplified rate (55% retention)
- Employer costs use standard multiplier (1.30x)
- Pension contributions: 5% employee + 8% employer

### General
- Based on 2025 tax legislation (some rates estimated)
- Actual results may vary based on personal circumstances
- Always consult a professional tax advisor for real decisions

## Validation Results

Tested against multiple scenarios with realistic outcomes:

| Hourly Rate | Net Monthly | Tax Rate | Status |
|-------------|-------------|----------|---------|
| €24.00      | €2,209      | 7.0%     | ✅ Realistic |
| €35.00      | €3,200      | 12.5%    | ✅ Realistic |
| €50.00      | €4,100      | 18.2%    | ✅ Realistic |

## Contributing

This calculator was developed through iterative testing and validation. See `/archive/` for development history.

### Future Improvements
- [ ] Web interface
- [ ] Export to PDF/Excel
- [ ] Multiple client scenarios
- [ ] Pension optimization calculator
- [ ] Updated 2026 tax rates

## License

MIT License - Feel free to use and modify for personal/educational purposes.

---

**Disclaimer**: This calculator provides estimates based on current Dutch tax law. Always consult qualified professionals for actual financial decisions.