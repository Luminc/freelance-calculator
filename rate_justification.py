#!/usr/bin/env python3
"""
Client-Friendly Rate Justification Tool
========================================

A simple, clear breakdown of where each euro of your hourly rate goes.
Perfect for client discussions and rate justifications.
"""

def calculate_rate_breakdown(hourly_rate_ex_vat=24.00, hours_per_month=130, include_pension_savings=400):
    """
    Calculate a clear, client-friendly breakdown of freelance hourly rate.
    
    Args:
        hourly_rate_ex_vat: Your hourly rate excluding VAT
        hours_per_month: Billable hours per month  
        include_pension_savings: Monthly personal savings/pension (not tax deductible)
    """
    
    # === BASIC CALCULATIONS ===
    monthly_revenue = hourly_rate_ex_vat * hours_per_month
    annual_revenue = monthly_revenue * 12
    
    # === BUSINESS COSTS (Tax Deductible) ===
    aov_monthly = 200.00  # Disability insurance / professional insurance
    other_costs_monthly = 50.00  # Office supplies, software, etc.
    business_costs_monthly = aov_monthly + other_costs_monthly
    business_costs_annual = business_costs_monthly * 12
    
    # Profit before personal allocations and taxes
    profit_before_personal_tax = annual_revenue - business_costs_annual
    
    # === TAX CALCULATIONS ===
    # Entrepreneurial deductions (2025)
    self_employed_deduction = 2470.00
    starters_deduction = 2123.00
    total_deductions = self_employed_deduction + starters_deduction
    
    # Profit after deductions
    profit_after_deductions = profit_before_personal_tax - total_deductions
    
    # MKB profit exemption (12.70% in 2025)
    mkb_exemption = profit_after_deductions * 0.127
    
    # Taxable profit
    taxable_profit = profit_after_deductions - mkb_exemption
    
    # Income tax + social premiums (simplified calculation)
    # Using effective rates based on income level
    if taxable_profit <= 38441:
        gross_tax_rate = 0.3582  # First bracket
    else:
        # Mixed bracket calculation (simplified for clarity)
        gross_tax_rate = 0.38  # Approximate for this income level
    
    gross_tax = taxable_profit * gross_tax_rate
    
    # Tax credits (heffingskortingen) - major benefit for freelancers!
    general_tax_credit = 3068.00  # AHK
    labor_tax_credit = min(5414.23, profit_before_personal_tax * 0.157)  # AK (simplified)
    total_tax_credits = general_tax_credit + labor_tax_credit
    
    # Final tax liability
    income_tax_final = max(0, gross_tax - total_tax_credits)
    
    # ZVW healthcare premium (5.26% over profit after deductions)
    zvw_premium = min(profit_after_deductions, 75864) * 0.0526
    
    total_taxes = income_tax_final + zvw_premium
    
    # === PERSONAL ALLOCATIONS ===
    net_after_tax = profit_before_personal_tax - total_taxes
    
    # Buffer for irregular income (15% of net income)
    buffer_amount = net_after_tax * 0.15
    
    # Pension/savings (personal choice, not tax deductible)
    pension_savings_annual = include_pension_savings * 12
    
    # Final disposable income
    net_disposable_annual = net_after_tax - buffer_amount - pension_savings_annual
    net_disposable_monthly = net_disposable_annual / 12
    
    # === RESULTS ===
    return {
        # Input
        'hourly_rate': hourly_rate_ex_vat,
        'hours_per_month': hours_per_month,
        'monthly_revenue': monthly_revenue,
        'annual_revenue': annual_revenue,
        
        # Costs & Deductions
        'business_costs_monthly': business_costs_monthly,
        'business_costs_annual': business_costs_annual,
        'profit_before_personal_tax': profit_before_personal_tax,
        'entrepreneurial_deductions': total_deductions,
        'mkb_exemption': mkb_exemption,
        'taxable_profit': taxable_profit,
        
        # Taxes
        'gross_tax': gross_tax,
        'tax_credits': total_tax_credits,
        'income_tax_final': income_tax_final,
        'zvw_premium': zvw_premium,
        'total_taxes': total_taxes,
        
        # Personal allocations
        'net_after_tax': net_after_tax,
        'buffer_amount': buffer_amount,
        'pension_savings_annual': pension_savings_annual,
        'net_disposable_annual': net_disposable_annual,
        'net_disposable_monthly': net_disposable_monthly,
    }

def print_client_friendly_breakdown(breakdown):
    """Print a clear, professional breakdown suitable for client presentations."""
    
    b = breakdown
    rate = b['hourly_rate']
    
    print("="*60)
    print(f"   HOURLY RATE BREAKDOWN: €{rate:.2f}/hour (excl. VAT)")
    print("="*60)
    
    print(f"\n📊 MONTHLY OVERVIEW ({b['hours_per_month']} hours/month)")
    print(f"   Gross Revenue: €{b['monthly_revenue']:.2f}")
    
    # Break down each euro
    business_cost_per_hour = b['business_costs_monthly'] / b['hours_per_month']
    tax_per_hour = b['total_taxes'] / 12 / b['hours_per_month']
    buffer_per_hour = b['buffer_amount'] / 12 / b['hours_per_month']
    pension_per_hour = b['pension_savings_annual'] / 12 / b['hours_per_month']
    net_per_hour = b['net_disposable_monthly'] / b['hours_per_month']
    
    print(f"\n💰 WHERE EACH €{rate:.2f} GOES:")
    print(f"   📋 Business Costs:        €{business_cost_per_hour:.2f}  ({business_cost_per_hour/rate*100:.1f}%)")
    print(f"   🏛️  Taxes & Premiums:     €{tax_per_hour:.2f}  ({tax_per_hour/rate*100:.1f}%)")
    print(f"   🛡️  Income Buffer:        €{buffer_per_hour:.2f}  ({buffer_per_hour/rate*100:.1f}%)")
    print(f"   🏦 Pension/Savings:       €{pension_per_hour:.2f}  ({pension_per_hour/rate*100:.1f}%)")
    print(f"   💵 Net Available Income:  €{net_per_hour:.2f}  ({net_per_hour/rate*100:.1f}%)")
    print(f"   ────────────────────────────────────────")
    print(f"   🎯 Total:                 €{rate:.2f}  (100.0%)")
    
    print(f"\n📈 ANNUAL PERSPECTIVE:")
    print(f"   Gross Revenue:           €{b['annual_revenue']:,.2f}")
    print(f"   Business Costs:          €{b['business_costs_annual']:,.2f}")
    print(f"   Taxes (after €{b['tax_credits']:,.0f} credits): €{b['total_taxes']:,.2f}")
    print(f"   Buffer (15% of net):     €{b['buffer_amount']:,.2f}")
    print(f"   Pension/Savings:         €{b['pension_savings_annual']:,.2f}")
    print(f"   ────────────────────────────────────────")
    print(f"   Net Available:           €{b['net_disposable_annual']:,.2f}")
    
    print(f"\n💼 EMPLOYEE EQUIVALENT:")
    # To get same net income as employee, they'd need higher gross
    employee_equivalent_gross = b['net_disposable_monthly'] / 0.68  # ~68% net retention
    employer_total_cost = employee_equivalent_gross * 1.32  # Employer costs
    equivalent_hourly = employer_total_cost / b['hours_per_month']
    
    print(f"   Employee gross needed:   €{employee_equivalent_gross:.2f}/month")
    print(f"   Employer total cost:     €{employer_total_cost:.2f}/month")
    print(f"   Equivalent hourly rate:  €{equivalent_hourly:.2f}/hour")
    
    print(f"\n🎯 KEY BENEFITS OF FREELANCE RATE:")
    print(f"   • Tax deductions save    €{b['entrepreneurial_deductions']:,.0f}/year")
    print(f"   • Tax credits provide    €{b['tax_credits']:,.0f}/year benefit")
    print(f"   • MKB exemption saves    €{b['mkb_exemption']:,.0f}/year")
    print(f"   • Total tax advantages:  €{b['entrepreneurial_deductions'] + b['tax_credits'] + b['mkb_exemption']:,.0f}/year")
    
    print(f"\n⚖️  FREELANCE RESPONSIBILITIES:")
    print(f"   • No paid holidays/sick leave")
    print(f"   • Own insurance & pension planning")
    print(f"   • Business risk & irregular income")
    print(f"   • Administrative overhead")
    
    effective_tax_rate = (b['total_taxes'] / b['profit_before_personal_tax']) * 100
    print(f"\n📊 EFFECTIVE TAX RATE: {effective_tax_rate:.1f}%")
    print(f"   (Much lower than employee due to deductions & credits)")

def print_simple_summary(breakdown):
    """Ultra-simple one-page summary for quick client reference."""
    
    b = breakdown
    rate = b['hourly_rate']
    
    print("\n" + "="*50)
    print(f"  €{rate:.2f}/HOUR RATE JUSTIFICATION")
    print("="*50)
    
    # Per hour breakdown
    hours = b['hours_per_month']
    costs_per_hour = b['business_costs_monthly'] / hours
    tax_per_hour = b['total_taxes'] / 12 / hours
    buffer_per_hour = b['buffer_amount'] / 12 / hours
    pension_per_hour = b['pension_savings_annual'] / 12 / hours
    net_per_hour = b['net_disposable_monthly'] / hours
    
    print(f"\nPer Hour Breakdown:")
    print(f"Business costs:     €{costs_per_hour:.2f}")
    print(f"Taxes & premiums:   €{tax_per_hour:.2f}")
    print(f"Income buffer:      €{buffer_per_hour:.2f}")
    print(f"Pension/savings:    €{pension_per_hour:.2f}")
    print(f"Net income:         €{net_per_hour:.2f}")
    print(f"TOTAL:              €{rate:.2f}")
    
    print(f"\nKey Facts:")
    print(f"• Net monthly income: €{b['net_disposable_monthly']:,.0f}")
    print(f"• Effective tax rate: {(b['total_taxes']/b['profit_before_personal_tax']*100):.1f}%")
    print(f"• Annual tax benefits: €{b['entrepreneurial_deductions'] + b['tax_credits']:,.0f}")


if __name__ == "__main__":
    # Calculate with your current settings
    breakdown = calculate_rate_breakdown(
        hourly_rate_ex_vat=24.00,
        hours_per_month=130,
        include_pension_savings=400  # Your monthly pension/savings goal
    )
    
    # Print detailed breakdown
    print_client_friendly_breakdown(breakdown)
    
    # Also print simple summary
    print_simple_summary(breakdown)
    
    print(f"\n📧 For questions about this rate structure:")
    print(f"   This breakdown reflects Dutch tax law 2025 and")
    print(f"   standard freelance business practices.")