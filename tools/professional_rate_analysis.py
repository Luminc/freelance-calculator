#!/usr/bin/env python3
"""
Professional Rate Analysis Based on Skill Set
=============================================

Calculate market-based rates for your actual professional responsibilities:
- Content Management & Strategy
- Professional Photography  
- Marketing & Campaign Development
- Data Entry & Database Management
- Marketing Automation (AI/Claude integration)
"""

def analyze_professional_rate_structure():
    """
    Calculate fair rates based on professional skill set and market rates.
    """
    
    print("="*70)
    print("   PROFESSIONAL RATE ANALYSIS - MULTI-DISCIPLINARY EXPERT")
    print("="*70)
    
    # Market rates for individual skills (Netherlands, 2025)
    skill_rates = {
        "Content Manager/Strategist": {"low": 35, "high": 50, "weight": 0.30},
        "Professional Photography": {"low": 40, "high": 75, "weight": 0.25}, 
        "Marketing Specialist": {"low": 30, "high": 45, "weight": 0.20},
        "Data/Database Management": {"low": 25, "high": 40, "weight": 0.15},
        "Marketing Automation (AI)": {"low": 50, "high": 80, "weight": 0.10}
    }
    
    print("\n📊 INDIVIDUAL SKILL MARKET RATES (€/hour):")
    
    weighted_low_rate = 0
    weighted_high_rate = 0
    
    for skill, data in skill_rates.items():
        low_rate = data["low"]
        high_rate = data["high"] 
        weight = data["weight"]
        
        weighted_low_rate += low_rate * weight
        weighted_high_rate += high_rate * weight
        
        print(f"   {skill:<35} €{low_rate:2d}-{high_rate:2d}  ({weight:.0%} of work)")
    
    print(f"   {'─' * 65}")
    print(f"   {'WEIGHTED AVERAGE MARKET RATE:':<35} €{weighted_low_rate:.0f}-{weighted_high_rate:.0f}")
    
    # Your current and historical rates
    historical_rate_incl_vat = 20.00
    historical_rate_excl_vat = 16.53
    current_rate_excl_vat = 24.00
    current_rate_incl_vat = 29.04
    
    print(f"\n📈 YOUR RATE PROGRESSION:")
    print(f"   Historical rate (incl. VAT):     €{historical_rate_incl_vat:.2f}")
    print(f"   Historical rate (excl. VAT):     €{historical_rate_excl_vat:.2f}")
    print(f"   Current rate (excl. VAT):        €{current_rate_excl_vat:.2f}")
    print(f"   Current rate (incl. VAT):        €{current_rate_incl_vat:.2f}")
    
    print(f"\n🎯 MARKET COMPARISON:")
    market_position_low = (current_rate_excl_vat / weighted_low_rate) * 100
    market_position_high = (current_rate_excl_vat / weighted_high_rate) * 100
    
    print(f"   Market range:                    €{weighted_low_rate:.0f}-{weighted_high_rate:.0f}/hour")
    print(f"   Your current rate:               €{current_rate_excl_vat:.0f}/hour")
    print(f"   Position in market:              {market_position_low:.0f}% of low end")
    print(f"   Position in market:              {market_position_high:.0f}% of high end")
    
    if current_rate_excl_vat < weighted_low_rate:
        print(f"   📊 VERDICT: SIGNIFICANTLY UNDERPRICED")
        underpriced_amount = weighted_low_rate - current_rate_excl_vat
        print(f"   💰 Could charge €{underpriced_amount:.0f}/hour MORE")
    elif current_rate_excl_vat < weighted_high_rate:
        print(f"   📊 VERDICT: FAIRLY PRICED (conservative)")
        room_for_growth = weighted_high_rate - current_rate_excl_vat  
        print(f"   💰 Room for growth: €{room_for_growth:.0f}/hour")
    else:
        print(f"   📊 VERDICT: PREMIUM PRICING")
    
    # Payroll offer analysis
    payroll_offer_rate = 16.45
    
    print(f"\n💸 PAYROLL OFFER ANALYSIS:")
    print(f"   Offered rate (incl. vacation):   €{payroll_offer_rate:.2f}/hour")
    print(f"   Market value range:              €{weighted_low_rate:.0f}-{weighted_high_rate:.0f}/hour")
    
    payroll_vs_low = (payroll_offer_rate / weighted_low_rate) * 100
    payroll_vs_high = (payroll_offer_rate / weighted_high_rate) * 100
    
    print(f"   Offer as % of market low:        {payroll_vs_low:.0f}%")
    print(f"   Offer as % of market high:       {payroll_vs_high:.0f}%") 
    
    market_low_gap = weighted_low_rate - payroll_offer_rate
    market_high_gap = weighted_high_rate - payroll_offer_rate
    
    print(f"   Below market low by:             €{market_low_gap:.0f}/hour")
    print(f"   Below market high by:            €{market_high_gap:.0f}/hour")
    print(f"   📉 VERDICT: SEVERELY UNDERVALUED")
    
    # Client value analysis
    print(f"\n🏢 CLIENT VALUE ANALYSIS:")
    
    # Calculate what client saves with your current rate
    avg_market_rate = (weighted_low_rate + weighted_high_rate) / 2
    client_savings_per_hour = avg_market_rate - current_rate_excl_vat
    client_savings_monthly = client_savings_per_hour * 130  # 130 hours/month
    client_savings_annual = client_savings_monthly * 12
    
    print(f"   Average market rate:             €{avg_market_rate:.0f}/hour")
    print(f"   Your current rate:               €{current_rate_excl_vat:.0f}/hour") 
    print(f"   Client saves per hour:           €{client_savings_per_hour:.0f}")
    print(f"   Client saves per month:          €{client_savings_monthly:,.0f}")
    print(f"   Client saves per year:           €{client_savings_annual:,.0f}")
    
    # Employee cost comparison
    print(f"\n👥 EMPLOYEE COST COMPARISON:")
    
    # To match your professional output, they'd need someone at market rate
    employee_gross_for_market_value = avg_market_rate / 0.68  # ~68% net retention
    employer_total_cost = employee_gross_for_market_value * 1.32  # +32% employer costs
    
    print(f"   Market-equivalent employee gross: €{employee_gross_for_market_value:.0f}/hour")
    print(f"   Total employer cost:             €{employer_total_cost:.0f}/hour")
    print(f"   Your rate vs employer cost:      €{current_rate_excl_vat:.0f} vs €{employer_total_cost:.0f}")
    
    total_savings_vs_employee = employer_total_cost - current_rate_excl_vat
    print(f"   Total savings with freelancer:   €{total_savings_vs_employee:.0f}/hour")
    
    return {
        "market_low": weighted_low_rate,
        "market_high": weighted_high_rate, 
        "market_avg": avg_market_rate,
        "current_rate": current_rate_excl_vat,
        "payroll_offer": payroll_offer_rate,
        "client_savings_annual": client_savings_annual,
        "employer_equivalent_cost": employer_total_cost
    }

def generate_rate_justification_arguments(analysis):
    """Generate strong arguments for rate justification based on analysis."""
    
    print(f"\n" + "="*70)
    print("   RATE JUSTIFICATION ARGUMENTS")
    print("="*70)
    
    print(f"\n🎯 KEY ARGUMENTS FOR €{analysis['current_rate']:.0f}/HOUR RATE:")
    
    print(f"\n1. **SIGNIFICANTLY BELOW MARKET**")
    print(f"   • Market range: €{analysis['market_low']:.0f}-{analysis['market_high']:.0f}/hour")
    print(f"   • Your rate: €{analysis['current_rate']:.0f}/hour")
    print(f"   • You could charge €{analysis['market_low'] - analysis['current_rate']:.0f}-{analysis['market_high'] - analysis['current_rate']:.0f} MORE")
    
    print(f"\n2. **PAYROLL OFFER WAS INSULTING**")
    print(f"   • Offered: €{analysis['payroll_offer']:.2f}/hour")
    print(f"   • Market value: €{analysis['market_avg']:.0f}/hour")
    print(f"   • Offer was {(analysis['payroll_offer']/analysis['market_avg']*100):.0f}% of market value")
    print(f"   • Below market by €{analysis['market_avg'] - analysis['payroll_offer']:.0f}/hour")
    
    print(f"\n3. **MASSIVE CLIENT SAVINGS**")
    print(f"   • Market rate average: €{analysis['market_avg']:.0f}/hour")
    print(f"   • Your rate: €{analysis['current_rate']:.0f}/hour")
    print(f"   • Annual savings: €{analysis['client_savings_annual']:,.0f}")
    
    print(f"\n4. **HUGE SAVINGS VS EMPLOYEE**")
    print(f"   • Equivalent employee cost: €{analysis['employer_equivalent_cost']:.0f}/hour")
    print(f"   • Your freelance rate: €{analysis['current_rate']:.0f}/hour")
    print(f"   • Saves €{analysis['employer_equivalent_cost'] - analysis['current_rate']:.0f}/hour")
    
    print(f"\n5. **MULTI-DISCIPLINARY EXPERTISE**")
    print(f"   • Content strategy & management")
    print(f"   • Professional photography")
    print(f"   • Marketing campaign development") 
    print(f"   • Database management")
    print(f"   • AI/automation integration")
    print(f"   • Replacing you requires multiple specialists")
    
    print(f"\n🔥 POWER STATEMENTS FOR CLIENT DISCUSSIONS:")
    
    print(f"\n💼 **Professional Positioning:**")
    print(f'   "My €{analysis["current_rate"]:.0f}/hour rate reflects {(analysis["current_rate"]/analysis["market_avg"]*100):.0f}% of market value')
    print(f'    for multi-disciplinary content management and marketing expertise."')
    
    print(f"\n💰 **Value Proposition:**")
    print(f'   "This rate saves you €{analysis["client_savings_annual"]:,.0f} annually compared to')
    print(f'    market rates, while delivering professional results across multiple specialties."')
    
    print(f"\n⚖️ **Comparison Argument:**")
    print(f'   "An equivalent employee would cost €{analysis["employer_equivalent_cost"]:.0f}/hour total.')
    print(f'    My freelance rate provides €{analysis["employer_equivalent_cost"] - analysis["current_rate"]:.0f}/hour savings with greater flexibility."')
    
    print(f"\n🚫 **Payroll Rejection:**")
    print(f'   "The €{analysis["payroll_offer"]:.2f} payroll offer represented a {((analysis["current_rate"] - analysis["payroll_offer"])/analysis["current_rate"]*100):.0f}% pay cut')
    print(f'    for the same professional work - well below industry standards for')
    print(f'    content management and marketing expertise."')


if __name__ == "__main__":
    analysis = analyze_professional_rate_structure()
    generate_rate_justification_arguments(analysis)
    
    print(f"\n🏆 CONCLUSION:")
    print(f"   Your €{analysis['current_rate']:.0f}/hour rate is professionally justified,")
    print(f"   competitively priced, and provides excellent client value.")
    print(f"   The payroll offer was unacceptable and unprofessional.")
    print(f"   \n   Stand firm - you have the stronger position.")