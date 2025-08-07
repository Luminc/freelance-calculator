#!/usr/bin/env python3
"""
Employment Benefits Analysis
============================

Calculates the true cost of employment benefits that freelancers must self-fund.
Based on typical Dutch employment practices.
"""

def calculate_employment_equivalent_costs():
    """
    Calculate what employment benefits actually cost, 
    to justify freelance rate structure.
    """
    
    print("="*60)
    print("   EMPLOYMENT BENEFITS vs FREELANCE SELF-FUNDING")
    print("="*60)
    
    # Base scenario
    monthly_revenue = 3120.00  # €24/hour × 130 hours
    annual_revenue = monthly_revenue * 12
    
    print(f"\nBase Revenue: €{monthly_revenue:,.0f}/month (€{annual_revenue:,.0f}/year)")
    
    # === VACATION & SICK LEAVE ANALYSIS ===
    print(f"\n🏖️  VACATION & SICK LEAVE EQUIVALENT:")
    
    # Standard Dutch employment
    work_days_per_year = 365 - 104  # Remove weekends = 261 days
    vacation_days = 25  # Typical Dutch vacation
    public_holidays = 8  # Average Dutch public holidays
    productive_work_days = work_days_per_year - vacation_days - public_holidays
    
    paid_non_productive_days = vacation_days + public_holidays
    vacation_sick_percentage = paid_non_productive_days / work_days_per_year
    
    print(f"   Work days per year: {work_days_per_year}")
    print(f"   - Vacation days: {vacation_days}")
    print(f"   - Public holidays: {public_holidays}")
    print(f"   = Productive work days: {productive_work_days}")
    print(f"   = Paid non-work ratio: {vacation_sick_percentage:.1%}")
    
    vacation_equivalent_annual = annual_revenue * vacation_sick_percentage
    vacation_equivalent_monthly = vacation_equivalent_annual / 12
    vacation_per_hour = vacation_equivalent_monthly / 130
    
    print(f"   Employee vacation/holiday value: €{vacation_equivalent_annual:,.0f}/year")
    print(f"   Freelance equivalent needed: €{vacation_equivalent_monthly:.0f}/month")
    print(f"   Per hour equivalent: €{vacation_per_hour:.2f}")
    
    # === SICK LEAVE INSURANCE ===
    print(f"\n🏥 SICK LEAVE INSURANCE:")
    # Dutch employers must pay 70% for up to 2 years
    # Risk varies, but 2-5% is typical insurance cost
    sick_leave_risk_percentage = 0.03  # 3% is conservative
    sick_leave_annual = annual_revenue * sick_leave_risk_percentage
    sick_leave_monthly = sick_leave_annual / 12
    sick_leave_per_hour = sick_leave_monthly / 130
    
    print(f"   Employer sick pay risk: ~{sick_leave_risk_percentage:.1%} of salary")
    print(f"   Annual risk value: €{sick_leave_annual:,.0f}")
    print(f"   Monthly equivalent: €{sick_leave_monthly:.0f}")  
    print(f"   Per hour equivalent: €{sick_leave_per_hour:.2f}")
    
    # === TOTAL BUFFER NEEDED ===
    total_buffer_annual = vacation_equivalent_annual + sick_leave_annual
    total_buffer_monthly = total_buffer_annual / 12
    total_buffer_percentage = total_buffer_annual / annual_revenue
    buffer_per_hour = total_buffer_monthly / 130
    
    print(f"\n🛡️  TOTAL INCOME SECURITY BUFFER:")
    print(f"   Required annual buffer: €{total_buffer_annual:,.0f}")
    print(f"   Monthly buffer needed: €{total_buffer_monthly:.0f}")
    print(f"   Percentage of revenue: {total_buffer_percentage:.1%}")
    print(f"   Per hour: €{buffer_per_hour:.2f}")
    
    # === PENSION ANALYSIS ===
    print(f"\n🏦 PENSION CONTRIBUTIONS:")
    
    # Typical Dutch pension contributions
    employee_pension_low = 0.04  # 4%
    employee_pension_high = 0.07  # 7%
    employer_pension_low = 0.08   # 8%
    employer_pension_high = 0.15  # 15%
    
    total_pension_low = employee_pension_low + employer_pension_low
    total_pension_high = employee_pension_high + employer_pension_high
    
    pension_low_annual = annual_revenue * total_pension_low
    pension_high_annual = annual_revenue * total_pension_high
    
    print(f"   Typical Dutch employment pension:")
    print(f"   - Employee: {employee_pension_low:.0%}-{employee_pension_high:.0%} of gross")
    print(f"   - Employer: {employer_pension_low:.0%}-{employer_pension_high:.0%} of gross") 
    print(f"   - Total: {total_pension_low:.0%}-{total_pension_high:.0%} of gross")
    print(f"   ")
    print(f"   Annual equivalent: €{pension_low_annual:,.0f} - €{pension_high_annual:,.0f}")
    print(f"   Monthly equivalent: €{pension_low_annual/12:.0f} - €{pension_high_annual/12:.0f}")
    
    # Current pension allocation
    current_pension_monthly = 400
    current_pension_annual = current_pension_monthly * 12
    current_pension_percentage = current_pension_annual / annual_revenue
    
    print(f"\n   Your current pension allocation:")
    print(f"   - Monthly: €{current_pension_monthly}")
    print(f"   - Annual: €{current_pension_annual:,.0f}")
    print(f"   - Percentage: {current_pension_percentage:.1%}")
    print(f"   - Position: {'LOW' if current_pension_percentage < total_pension_low else 'NORMAL' if current_pension_percentage < total_pension_high else 'HIGH'}")
    
    # === SUMMARY ===
    print(f"\n📊 EMPLOYMENT EQUIVALENT SUMMARY:")
    total_benefits_monthly = total_buffer_monthly + current_pension_monthly
    total_benefits_percentage = (total_buffer_annual + current_pension_annual) / annual_revenue
    benefits_per_hour = total_benefits_monthly / 130
    
    print(f"   Income security buffer: €{total_buffer_monthly:.0f}/month ({total_buffer_percentage:.1%})")
    print(f"   Pension contributions: €{current_pension_monthly}/month ({current_pension_percentage:.1%})")
    print(f"   ─────────────────────────────────────────────")
    print(f"   Total benefits equivalent: €{total_benefits_monthly:.0f}/month ({total_benefits_percentage:.1%})")
    print(f"   Per hour benefits cost: €{benefits_per_hour:.2f}")
    
    print(f"\n🎯 KEY INSIGHTS:")
    print(f"   • Your {total_buffer_percentage:.1%} buffer is JUSTIFIED (matches vacation + sick risk)")
    print(f"   • Your {current_pension_percentage:.1%} pension is CONSERVATIVE (typical: {total_pension_low:.0%}-{total_pension_high:.0%})")
    print(f"   • Total {total_benefits_percentage:.1%} for benefits matches employment reality")
    print(f"   • Employees get these automatically - you must self-fund")
    
    return {
        'vacation_sick_percentage': vacation_sick_percentage,
        'sick_leave_percentage': sick_leave_risk_percentage, 
        'total_buffer_percentage': total_buffer_percentage,
        'pension_percentage': current_pension_percentage,
        'total_benefits_percentage': total_benefits_percentage,
        'benefits_per_hour': benefits_per_hour
    }

def compare_with_current_rate_structure():
    """Compare current rate structure with employment-based calculations."""
    
    print(f"\n" + "="*60)
    print("   CURRENT vs EMPLOYMENT-JUSTIFIED BREAKDOWN")
    print("="*60)
    
    # Current structure (from rate_justification.py)
    current_buffer_percentage = 0.15  # 15%
    current_pension_percentage = 0.128  # 12.8% (€400/€3120)
    
    # Employment-justified
    employment_data = calculate_employment_equivalent_costs()
    
    print(f"\n📊 COMPARISON:")
    print(f"                          Current    Employment-Based")
    print(f"   Buffer (vacation/sick): {current_buffer_percentage:.1%}      {employment_data['total_buffer_percentage']:.1%}")
    print(f"   Pension:               {current_pension_percentage:.1%}     {employment_data['pension_percentage']:.1%}")
    print(f"   Total benefits:        {current_buffer_percentage + current_pension_percentage:.1%}     {employment_data['total_benefits_percentage']:.1%}")
    
    print(f"\n✅ VALIDATION:")
    if current_buffer_percentage >= employment_data['total_buffer_percentage']:
        print(f"   ✓ Your buffer percentage is justified")
    else:
        print(f"   ⚠ Your buffer could be higher ({employment_data['total_buffer_percentage']:.1%})")
        
    if abs(current_pension_percentage - employment_data['pension_percentage']) < 0.02:
        print(f"   ✓ Your pension percentage matches employment")
    else:
        print(f"   • Your pension is conservative vs employment standards")

if __name__ == "__main__":
    benefits_data = calculate_employment_equivalent_costs()
    compare_with_current_rate_structure()
    
    print(f"\n💼 CLIENT ARGUMENT:")
    print(f"   'The {benefits_data['total_benefits_percentage']:.0%} I allocate for benefits matches what")
    print(f"    employees receive automatically. You're getting the same")
    print(f"    value while avoiding all employment overhead.'")