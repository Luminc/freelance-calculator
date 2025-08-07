#!/usr/bin/env python3
"""
Employment-Equivalent Rate Justification Tool v2.0
==================================================

Based on actual Dutch employment benefits and costs.
Every percentage is justified by employment equivalent data.
"""

def calculate_employment_equivalent_rate_breakdown(hourly_rate_ex_vat=24.00, hours_per_month=130):
    """
    Calculate rate breakdown based on actual employment equivalent costs.
    Every allocation percentage is justified by real employment benefits.
    """
    
    # === BASIC CALCULATIONS ===
    monthly_revenue = hourly_rate_ex_vat * hours_per_month
    annual_revenue = monthly_revenue * 12
    
    # === BUSINESS COSTS (Tax Deductible) ===
    # These are direct business expenses that employees don't pay
    aov_monthly = 200.00  # Professional insurance (employees get this free)
    other_costs_monthly = 50.00  # Tools, software, office (employees get this free)
    business_costs_monthly = aov_monthly + other_costs_monthly
    business_costs_annual = business_costs_monthly * 12
    
    # Profit after business costs (equivalent to employee gross salary)
    profit_after_business_costs = annual_revenue - business_costs_annual
    
    # === EMPLOYMENT-EQUIVALENT BENEFIT ALLOCATIONS ===
    
    # 1. VACATION & SICK LEAVE BUFFER (15.6% - employment justified)
    # Based on: 25 vacation days + 8 holidays + 3% sick leave risk
    # Calculation: (33 paid non-work days / 261 work days) + 3% sick risk = 15.6%
    vacation_sick_buffer_rate = 0.156
    vacation_sick_buffer_annual = profit_after_business_costs * vacation_sick_buffer_rate
    vacation_sick_buffer_monthly = vacation_sick_buffer_annual / 12
    
    # 2. PENSION (12.8% - matches employment total contributions)  
    # Based on: Typical Dutch total pension contributions 12%-22% of gross
    # Your allocation: €400/month = 12.8% (conservative end of range)
    pension_monthly = 400.00
    pension_annual = pension_monthly * 12
    pension_rate = pension_annual / profit_after_business_costs
    
    # 3. TAX CALCULATIONS (Using simplified but accurate approach)
    # Entrepreneurial deductions
    self_employed_deduction = 2470.00
    starters_deduction = 2123.00
    total_deductions = self_employed_deduction + starters_deduction
    
    # Apply deductions
    profit_after_deductions = profit_after_business_costs - total_deductions
    
    # MKB profit exemption (12.70% in 2025)
    mkb_exemption = profit_after_deductions * 0.127
    
    # Taxable profit
    taxable_profit = profit_after_deductions - mkb_exemption
    
    # Simplified tax calculation (effective rate for this income level)
    effective_tax_rate = 0.37  # Approximate combined rate before credits
    gross_tax = taxable_profit * effective_tax_rate
    
    # Tax credits (major freelance advantage)
    general_tax_credit = 3068.00  # AHK
    labor_tax_credit = min(5414.23, profit_after_business_costs * 0.157)  # AK
    total_tax_credits = general_tax_credit + labor_tax_credit
    
    # Final tax liability
    income_tax_final = max(0, gross_tax - total_tax_credits)
    
    # ZVW healthcare premium
    zvw_premium = min(profit_after_deductions, 75864) * 0.0526
    
    total_taxes = income_tax_final + zvw_premium
    
    # === NET CALCULATIONS ===
    net_after_taxes = profit_after_business_costs - total_taxes
    net_after_all_allocations = net_after_taxes - vacation_sick_buffer_annual - pension_annual
    net_disposable_monthly = net_after_all_allocations / 12
    
    # === PER HOUR BREAKDOWN ===
    business_costs_per_hour = business_costs_monthly / hours_per_month
    taxes_per_hour = total_taxes / 12 / hours_per_month
    vacation_sick_per_hour = vacation_sick_buffer_monthly / hours_per_month
    pension_per_hour = pension_monthly / hours_per_month
    net_per_hour = net_disposable_monthly / hours_per_month
    
    return {
        # Input
        'hourly_rate': hourly_rate_ex_vat,
        'hours_per_month': hours_per_month,
        'monthly_revenue': monthly_revenue,
        'annual_revenue': annual_revenue,
        
        # Breakdown
        'business_costs_monthly': business_costs_monthly,
        'business_costs_per_hour': business_costs_per_hour,
        'business_costs_percentage': business_costs_annual / annual_revenue,
        
        'total_taxes_annual': total_taxes,
        'taxes_per_hour': taxes_per_hour,
        'taxes_percentage': total_taxes / annual_revenue,
        
        'vacation_sick_buffer_monthly': vacation_sick_buffer_monthly,
        'vacation_sick_per_hour': vacation_sick_per_hour,
        'vacation_sick_percentage': vacation_sick_buffer_rate,
        
        'pension_monthly': pension_monthly,
        'pension_per_hour': pension_per_hour,
        'pension_percentage': pension_rate,
        
        'net_disposable_monthly': net_disposable_monthly,
        'net_per_hour': net_per_hour,
        'net_percentage': net_after_all_allocations / annual_revenue,
        
        # Employment comparison data
        'profit_after_business_costs': profit_after_business_costs,
        'tax_credits': total_tax_credits,
        'entrepreneurial_deductions': total_deductions,
        'mkb_exemption': mkb_exemption,
    }

def print_employment_justified_breakdown(breakdown):
    """Print breakdown with employment-equivalent justifications."""
    
    b = breakdown
    rate = b['hourly_rate']
    
    print("="*70)
    print(f"   EMPLOYMENT-EQUIVALENT RATE BREAKDOWN: €{rate:.2f}/hour (excl. VAT)")
    print("="*70)
    
    print(f"\n📊 WHERE EACH €{rate:.2f} GOES (Employment-Justified):")
    print(f"   🏢 Business Costs:         €{b['business_costs_per_hour']:.2f}  ({b['business_costs_percentage']:.1%})")
    print(f"      ↳ What employees get free from employer")
    print(f"   🏛️  Taxes & Premiums:       €{b['taxes_per_hour']:.2f}  ({b['taxes_percentage']:.1%})")
    print(f"      ↳ After €{b['tax_credits']:,.0f} freelance tax advantages")
    print(f"   🏖️  Vacation & Sick Buffer: €{b['vacation_sick_per_hour']:.2f}  ({b['vacation_sick_percentage']:.1%})")
    print(f"      ↳ Equivalent to 25 vacation days + sick leave insurance")
    print(f"   🏦 Pension Contribution:   €{b['pension_per_hour']:.2f}  ({b['pension_percentage']:.1%})")
    print(f"      ↳ Conservative vs typical 12-22% employment pension")
    print(f"   💵 Net Available Income:   €{b['net_per_hour']:.2f}  ({b['net_percentage']:.1%})")
    print(f"      ↳ Your actual take-home pay")
    print(f"   ───────────────────────────────────────────────────")
    print(f"   🎯 TOTAL:                  €{rate:.2f}  (100.0%)")
    
    print(f"\n📈 ANNUAL FINANCIAL PICTURE:")
    print(f"   Gross Revenue:                €{b['annual_revenue']:,.0f}")
    print(f"   Business Costs:               €{b['business_costs_monthly']*12:,.0f}")
    print(f"   ═══════════════════════════════════════════════")
    print(f"   Business Profit:              €{b['profit_after_business_costs']:,.0f}")
    print(f"   ")
    print(f"   Employment-Equivalent Allocations:")
    print(f"   • Vacation/Sick Security:     €{b['vacation_sick_buffer_monthly']*12:,.0f}")
    print(f"   • Pension Contributions:      €{b['pension_monthly']*12:,.0f}")
    print(f"   • Taxes (after advantages):   €{b['total_taxes_annual']:,.0f}")
    print(f"   ───────────────────────────────────────────────")
    print(f"   NET AVAILABLE INCOME:         €{b['net_disposable_monthly']*12:,.0f}")
    
    print(f"\n💼 EMPLOYMENT REALITY CHECK:")
    
    # Calculate employee equivalent
    target_net_monthly = b['net_disposable_monthly']
    
    # Employee would need higher gross to get same net (due to limited deductions)
    employee_gross_needed = target_net_monthly / 0.68  # ~68% retention typical
    
    # Add back the benefits they get automatically
    employee_with_benefits = employee_gross_needed * 1.156  # Add 15.6% vacation/sick
    employee_with_pension = employee_with_benefits * 1.128   # Add 12.8% pension
    
    # Employer total cost
    employer_total_cost = employee_with_pension * 1.30  # Add employer costs (30%)
    equivalent_hourly = employer_total_cost / b['hours_per_month']
    
    print(f"   To get €{target_net_monthly:,.0f}/month net as employee:")
    print(f"   • Required gross salary:      €{employee_gross_needed:,.0f}/month")
    print(f"   • Plus vacation/sick value:   €{employee_with_benefits:,.0f}/month")
    print(f"   • Plus pension contributions: €{employee_with_pension:,.0f}/month")
    print(f"   • Total employer cost:        €{employer_total_cost:,.0f}/month")
    print(f"   • Equivalent hourly rate:     €{equivalent_hourly:.2f}/hour")
    print(f"   ➡️  CLIENT SAVES:              €{equivalent_hourly - rate:.2f}/hour")
    
    print(f"\n🎯 POWERFUL CLIENT ARGUMENTS:")
    print(f"   ✓ Only €{b['net_per_hour']:.2f}/hour is actual income ({b['net_percentage']:.1%})")
    print(f"   ✓ €{b['vacation_sick_per_hour'] + b['pension_per_hour']:.2f}/hour covers what employees get automatically")
    print(f"   ✓ Total rate saves €{equivalent_hourly - rate:.2f}/hour vs employee costs")
    print(f"   ✓ All percentages match employment equivalents")
    print(f"   ✓ Freelance tax advantages: €{b['tax_credits'] + b['entrepreneurial_deductions']:,.0f}/year")
    
    effective_tax_rate = (b['total_taxes_annual'] / b['profit_after_business_costs']) * 100
    print(f"\n📊 EFFECTIVE TAX RATE: {effective_tax_rate:.1f}%")
    print(f"    (Much lower than employees due to deductions & credits)")

def print_client_email_version(breakdown):
    """Ultra-clean version for email to clients."""
    
    b = breakdown
    rate = b['hourly_rate']
    
    print(f"\n" + "="*50)
    print(f"  €{rate:.2f}/HOUR BREAKDOWN FOR CLIENT")
    print("="*50)
    
    print(f"\nYour €{rate:.2f}/hour investment breaks down as:")
    print(f"")
    print(f"Business Operations:     €{b['business_costs_per_hour']:.2f}  ({b['business_costs_percentage']:.1%})")
    print(f"  Professional insurance, tools & supplies")
    print(f"")
    print(f"Vacation/Sick Coverage:  €{b['vacation_sick_per_hour']:.2f}  ({b['vacation_sick_percentage']:.1%})")
    print(f"  Equivalent to 25 vacation days + sick leave")
    print(f"")
    print(f"Pension Contributions:   €{b['pension_per_hour']:.2f}  ({b['pension_percentage']:.1%})")
    print(f"  Retirement planning (like employer contributions)")
    print(f"")
    print(f"Taxes & Premiums:        €{b['taxes_per_hour']:.2f}  ({b['taxes_percentage']:.1%})")
    print(f"  After €{b['tax_credits']:,.0f} in freelance tax advantages")
    print(f"")
    print(f"Net Take-Home Pay:       €{b['net_per_hour']:.2f}  ({b['net_percentage']:.1%})")
    print(f"  Actual income after all obligations")
    print(f"")
    print(f"TOTAL RATE:              €{rate:.2f}  (100%)")
    
    # Quick comparison
    employee_equivalent = (b['net_disposable_monthly'] / 0.68) * 1.30 / b['hours_per_month']
    savings = employee_equivalent - rate
    
    print(f"\nEmployee equivalent cost: €{employee_equivalent:.2f}/hour")
    print(f"Your savings with freelancer: €{savings:.2f}/hour")
    
    print(f"\nThis structure ensures professional service delivery")
    print(f"while providing significant savings vs employment costs.")


if __name__ == "__main__":
    # Calculate with employment-equivalent logic
    breakdown = calculate_employment_equivalent_rate_breakdown(
        hourly_rate_ex_vat=24.00,
        hours_per_month=130
    )
    
    # Print detailed breakdown
    print_employment_justified_breakdown(breakdown)
    
    # Print client-friendly version
    print_client_email_version(breakdown)
    
    print(f"\n🏆 CONCLUSION:")
    print(f"   Every percentage in this rate structure is justified")
    print(f"   by actual employment equivalent costs. You're not")
    print(f"   paying for luxury - you're getting professional")
    print(f"   service at below-employment costs.")