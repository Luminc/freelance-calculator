# Dutch Freelance Rate Calculator & Justification Suite

Professional toolkit for calculating and justifying freelance rates in the Netherlands based on 2025 tax law, employment equivalents, and market standards.

## Quick Start

```bash
# Setup
python3 -m venv calc_env
./calc_env/bin/pip install -r requirements.txt

# Run main calculator
./calc_env/bin/python3 freelance_calculator.py

# Get rate justification breakdown
./calc_env/bin/python3 tools/rate_justification_v2.py
```

## Key Results: €24/Hour Analysis

Your €24/hour rate is **47% below market value** (€35-57/hour range):
- **€14.37** - Actual take-home (59.9%)
- **€6.16** - Employment-equivalent benefits (25.6%)
- **€1.92** - Business costs (8.0%)
- **€1.56** - Taxes after advantages (6.5%)

**Client saves €34,320/year** vs market rates and **€65/hour** vs employee costs.

## Project Structure

```
├── freelance_calculator.py          # Main tax calculator (2025 rates)
├── tools/                          # Analysis tools
│   ├── rate_justification_v2.py    # Employment-equivalent breakdown  
│   ├── professional_rate_analysis.py # Market rate analysis
│   └── employment_benefits_analysis.py # Benefits cost analysis
├── docs/
│   ├── strategy/                   # Communication & negotiation
│   └── analysis/                   # Situation analysis
└── archive/                        # Previous versions
```

## Core Tools

1. **Main Calculator**: Comprehensive Dutch tax calculation with 2025 rates
2. **Rate Justification**: Employment-equivalent rate breakdown for clients  
3. **Market Analysis**: Multi-disciplinary skill set valuation
4. **Strategy Docs**: Complete negotiation framework and communication templates

## Features

### 🧮 Accurate Tax Calculations
- **Income Tax (IB) & Social Security Premiums (PVV)**: Proper 2025 tax brackets and rates
- **Tax Credits**: General Tax Credit (AHK) and Labor Tax Credit (AK)
- **ZVW Healthcare Premium**: Income-dependent healthcare contributions
- **Entrepreneurial Deductions**: Self-employed and starter deductions
- **SME Profit Exemption**: MKB winstvrijstelling (12.70% in 2025)

### 💼 Two Calculation Modes
1. **Rate-based**: Start with hourly rate, calculate net income
2. **Target-based**: Start with desired net income, find required hourly rate

### 📊 Employment-Equivalent Justification
- Vacation/sick buffer: **15.6%** (25 vacation days + sick leave insurance)
- Pension: **12.8%** (conservative vs 12-22% employment standard)
- All percentages based on actual Dutch employment benefits

## Documentation

- **PROJECT_OVERVIEW.md** - Complete project documentation
- **RATE_JUSTIFICATION_SUMMARY.md** - Quick client discussion reference
- **docs/strategy/** - Communication templates and negotiation strategy

## Example Output

For a €24/hour freelancer working 130 hours/month:
- **Net disposable income**: €1,869/month
- **Client savings**: €34,320/year vs market rates
- **Employee equivalent cost**: €89/hour total
- **Market position**: 68% of low-end market rate

## Validation Results

Your rate justification is based on:
- ✅ Market research showing €35-57/hour range
- ✅ Employment-equivalent cost analysis
- ✅ 2025 Dutch tax law compliance
- ✅ Multi-disciplinary expertise valuation

## Bottom Line

Your €24/hour rate is professionally justified and significantly below market value. The toolkit provides complete documentation to defend this conservative rate structure with confidence.

---

**Disclaimer**: This calculator provides estimates based on current Dutch tax law. Always consult qualified professionals for actual financial decisions.