import pandas as pd

# --- CALCULATOR VERSIE 5.0 (Gedetailleerde Werkgeverslasten) ---
# --- CONFIGURATIE JAAR ---
CALCULATION_YEAR = 2025

# --- INPUTS ---
# Kies modus: "rate_based" of "target_net_based"
calculation_mode = "rate_based"

# --- FREELANCER INPUTS ---
freelance_hourly_rate_ex_vat_input = 17
hours_per_month_input = 130
non_declarable_overhead_percentage_input = 10
freelance_aov_monthly_input = 200
freelance_other_costs_monthly_input = 10
freelance_pension_monthly_input = 700.00 # Privé reservering
desired_freelance_buffer_percentage_input = 0.15
apply_entrepreneurial_deductions_input = True

# --- WERKNEMER INPUTS ---
# Doel netto inkomen (alleen voor 'target_net_based' modus)
target_net_disposable_monthly_income_input = 2000.00

# Componenten voor Werkgeverslasten (maakt de vergelijking realistischer)
# Deze vervangen de oude 'employer_total_cost_factor'
employee_pension_contribution_percentage_input = 0.05 # Werknemersdeel
employer_pension_contribution_percentage = 0.08 # Werkgeversdeel (% van bruto salaris)
employer_ww_premium_percentage = 0.0264 # Gemiddeld, lage premie voor vast contract
employer_wia_wao_premium_percentage = 0.075 # Schatting Aof + Whk
employer_zvw_percentage = 0.0657 # Werkgeversheffing ZVW 2024/2025
holiday_pay_rate_employee = 0.08
# Overige maandelijkse kosten per werknemer (lease, telefoon, reiskosten, etc.)
employee_other_monthly_costs_input = 200.00


# --- JAARSPECIFIEKE PARAMETERS ---
if CALCULATION_YEAR == 2025: # Waarden gebaseerd op 2024 en trends, officiële cijfers kunnen afwijken
    self_employed_deduction_annual = 3200.00
    starters_deduction_annual = 2123.00
    mkb_profit_exemption_rate = 0.1270
    zvw_rate_freelancer = 0.0526
    zvw_max_income = 75864.00
    box1_schijf1_grens = 75518.00
    box1_schijf1_tarief = 0.3697
    box1_schijf2_tarief = 0.4950
    ahk_max = 3362.00
    ahk_afbouw_grens_start = 24814.00
    ahk_afbouw_percentage = 0.0663
    ak_max = 5532.00
    ak_opbouw_grens1, ak_opbouw_perc1 = 11490, 0.08425
    ak_opbouw_grens2, ak_opbouw_perc2 = 23201, 0.31433
    ak_opbouw_grens3, ak_opbouw_perc3 = 37691, 0.02663
    ak_afbouw_start, ak_afbouw_perc = 37691.00, 0.06510
    ak_afbouw_eind = 124934.00
# (Hier zou de logica voor CALCULATION_YEAR == 2024 kunnen staan)
else:
    # Voor dit voorbeeld focussen we op 2025
    pass


# --- BELASTINGFUNCTIES ---
def calculate_ib_box1(taxable_income_annual, year):
    if taxable_income_annual <= 0: return 0
    if year == 2025:
        if taxable_income_annual <= box1_schijf1_grens:
            return taxable_income_annual * box1_schijf1_tarief
        else:
            return (box1_schijf1_grens * box1_schijf1_tarief) + ((taxable_income_annual - box1_schijf1_grens) * box1_schijf2_tarief)
    raise ValueError(f"Year {year} not supported")

def calculate_zvw(profit_for_zvw_annual):
    if profit_for_zvw_annual <= 0: return 0
    return min(profit_for_zvw_annual, zvw_max_income) * zvw_rate_freelancer

def calculate_general_tax_credit(income):
    afbouw_eind = ahk_afbouw_grens_start + (ahk_max / ahk_afbouw_percentage)
    credit = ahk_max if income <= ahk_afbouw_grens_start else (ahk_max - ahk_afbouw_percentage * (income - ahk_afbouw_grens_start) if income < afbouw_eind else 0)
    return max(0, credit)

def calculate_labor_tax_credit(income):
    if income <= 0: return 0
    if income <= ak_opbouw_grens1: credit = income * ak_opbouw_perc1
    elif income <= ak_opbouw_grens2: credit = (ak_opbouw_grens1 * ak_opbouw_perc1) + (income - ak_opbouw_grens1) * ak_opbouw_perc2
    elif income <= ak_opbouw_grens3: credit = (ak_opbouw_grens1 * ak_opbouw_perc1) + (ak_opbouw_grens2 - ak_opbouw_grens1) * ak_opbouw_perc2 + (income - ak_opbouw_grens2) * ak_opbouw_perc3
    elif income < ak_afbouw_start: credit = ak_max
    elif income <= ak_afbouw_eind: credit = ak_max - (income - ak_afbouw_start) * ak_afbouw_perc
    else: credit = 0
    return max(0, min(ak_max, credit))


# --- CORE CALCULATORS ---
def calculate_freelancer_finances(hourly_rate, total_hours, overhead_perc, aov_m, costs_m, pension_m, apply_deductions, buffer_perc, year):
    billable_hours_m = total_hours * (1 - overhead_perc / 100)
    gross_annual_revenue = hourly_rate * billable_hours_m * 12
    total_direct_costs_annual = (aov_m + costs_m) * 12
    profit_before_fiscal = gross_annual_revenue - total_direct_costs_annual
    
    deduction = self_employed_deduction_annual + starters_deduction_annual if apply_deductions else 0
    entrepreneurial_deduction = min(deduction, profit_before_fiscal) if profit_before_fiscal > 0 else 0
    profit_after_entrepreneurial = profit_before_fiscal - entrepreneurial_deduction
    mkb_exemption = profit_after_entrepreneurial * mkb_profit_exemption_rate
    taxable_profit_for_ib = profit_after_entrepreneurial - mkb_exemption
    
    total_ib_pvv = calculate_ib_box1(taxable_profit_for_ib, year)
    total_credits = calculate_general_tax_credit(taxable_profit_for_ib) + calculate_labor_tax_credit(profit_before_fiscal)
    payable_ib_pvv = max(0, total_ib_pvv - total_credits)
    zvw_payable = calculate_zvw(profit_after_entrepreneurial)
    total_tax = payable_ib_pvv + zvw_payable
    
    net_income_after_tax = profit_before_fiscal - total_tax
    buffer_amount = net_income_after_tax * buffer_perc
    pension_annual = pension_m * 12
    net_disposable_annual = net_income_after_tax - buffer_amount - pension_annual

    return {
        "hourly_rate": hourly_rate, "net_disposable_monthly": net_disposable_annual / 12,
        "gross_annual_revenue": gross_annual_revenue, "profit_before_fiscal_deductions_annual": profit_before_fiscal,
        "total_payable_tax_freelancer_annual": total_tax, "billable_hours_monthly": billable_hours_m,
        "net_disposable_income_freelancer_annual": net_disposable_annual,
    }

def calculate_employee_net_income(gross_monthly_excl_holiday, year):
    gross_annual_salary = gross_monthly_excl_holiday * 12
    pension_contribution_annual = gross_annual_salary * employee_pension_contribution_percentage_input
    taxable_income_annual = gross_annual_salary - pension_contribution_annual
    labor_income_annual = gross_annual_salary * (1 + holiday_pay_rate_employee) # Arbeidskorting over loon incl. vak.geld
    
    total_ib_pvv = calculate_ib_box1(taxable_income_annual, year)
    total_credits = calculate_general_tax_credit(taxable_income_annual) + calculate_labor_tax_credit(labor_income_annual)
    payable_tax_annual = max(0, total_ib_pvv - total_credits)
    
    total_net_annual = labor_income_annual - pension_contribution_annual - payable_tax_annual
    return {"net_monthly_income": total_net_annual / 12, "gross_monthly_salary": gross_monthly_excl_holiday}

def calculate_total_employer_cost(gross_monthly_excl_holiday):
    gross_annual_salary = gross_monthly_excl_holiday * 12
    holiday_pay = gross_annual_salary * holiday_pay_rate_employee
    gross_annual_incl_holiday = gross_annual_salary + holiday_pay
    
    cost_employer_pension = gross_annual_salary * employer_pension_contribution_percentage
    cost_ww = gross_annual_salary * employer_ww_premium_percentage
    cost_wia_wao = gross_annual_salary * employer_wia_wao_premium_percentage
    cost_zvw = min(gross_annual_salary, zvw_max_income) * employer_zvw_percentage
    other_costs = employee_other_monthly_costs_input * 12
    
    total_cost = gross_annual_incl_holiday + cost_employer_pension + cost_ww + cost_wia_wao + cost_zvw + other_costs
    
    return {
        "total_cost_annual": total_cost,
        "breakdown": {
            "Bruto jaarsalaris": gross_annual_salary, "Vakantiegeld": holiday_pay,
            "Werkgeversdeel Pensioen": cost_employer_pension, "Premies (WW, WIA, ZVW)": cost_ww + cost_wia_wao + cost_zvw,
            "Overige kosten (reis, etc.)": other_costs
        }
    }

# --- HOOFDLOGICA ---
if calculation_mode == "rate_based":
    freelancer_results = calculate_freelancer_finances(freelance_hourly_rate_ex_vat_input, hours_per_month_input, non_declarable_overhead_percentage_input, freelance_aov_monthly_input, freelance_other_costs_monthly_input, freelance_pension_monthly_input, apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR)
    target_net_for_employee_scenario = freelancer_results["net_disposable_monthly"]
else: # target_net_based
    target_net = target_net_disposable_monthly_income_input
    low_rate, high_rate = 10.0, 300.0
    for i in range(50): # Binary search for hourly rate
        rate_guess = (low_rate + high_rate) / 2
        res = calculate_freelancer_finances(rate_guess, hours_per_month_input, non_declarable_overhead_percentage_input, freelance_aov_monthly_input, freelance_other_costs_monthly_input, freelance_pension_monthly_input, apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR)
        if abs(res["net_disposable_monthly"] - target_net) < 0.50 or (high_rate - low_rate) < 0.01:
            freelancer_results = res
            break
        if res["net_disposable_monthly"] < target_net: low_rate = rate_guess
        else: high_rate = rate_guess
    target_net_for_employee_scenario = freelancer_results["net_disposable_monthly"]

# --- WERKNEMER SCENARIO'S ---
# Scenario 1: Gelijke werkgeverskosten
# We moeten iteratief zoeken naar het brutosalaris dat leidt tot de doelkosten
low_gross_s1, high_gross_s1 = 1000, 15000
s1_employee_gross_monthly = 0
for i in range(30):
    guess_gross = (low_gross_s1 + high_gross_s1) / 2
    cost = calculate_total_employer_cost(guess_gross)['total_cost_annual']
    if abs(cost - freelancer_results['gross_annual_revenue']) < 10:
        s1_employee_gross_monthly = guess_gross
        break
    if cost < freelancer_results['gross_annual_revenue']: low_gross_s1 = guess_gross
    else: high_gross_s1 = guess_gross
s1_employee_net_results = calculate_employee_net_income(s1_employee_gross_monthly, CALCULATION_YEAR)
s1_employer_cost_results = calculate_total_employer_cost(s1_employee_gross_monthly)

# Scenario 2: Gelijk netto inkomen
low_gross_s2, high_gross_s2 = 1000, 15000
s2_employee_gross_monthly = 0
for i in range(30):
    guess_gross = (low_gross_s2 + high_gross_s2) / 2
    net_income = calculate_employee_net_income(guess_gross, CALCULATION_YEAR)['net_monthly_income']
    if abs(net_income - target_net_for_employee_scenario) < 0.50:
        s2_employee_gross_monthly = guess_gross
        break
    if net_income < target_net_for_employee_scenario: low_gross_s2 = guess_gross
    else: high_gross_s2 = guess_gross
s2_employee_net_results = calculate_employee_net_income(s2_employee_gross_monthly, CALCULATION_YEAR)
s2_employer_cost_results = calculate_total_employer_cost(s2_employee_gross_monthly)
s2_equivalent_hourly_rate = (s2_employer_cost_results['total_cost_annual'] / 12) / freelancer_results['billable_hours_monthly']


# --- PRESENTATIE ---
pd.options.display.float_format = '{:.2f}'.format
print(f"\n--- CALCULATOR VERSIE 5.0 (Jaar: {CALCULATION_YEAR}) ---")

print("\n--- FREELANCER RESULTAAT ---")
fr = freelancer_results
print(f"{'Benodigd Uurtarief:':<40} € {fr['hourly_rate']:.2f}")
print(f"{'Netto Besteedbaar p/maand:':<40} € {fr['net_disposable_monthly']:.2f}")
print(f"{'Bruto Jaaromzet:':<40} € {fr['gross_annual_revenue']:.2f}")
print(f"{'Jaarlijkse Belasting & ZVW:':<40} € {fr['total_payable_tax_freelancer_annual']:.2f}")

print(f"\n--- WERKNEMER SCENARIO 1: O.b.v. Gelijke Werkgeverskosten (€ {fr['gross_annual_revenue']:.2f}/jaar) ---")
print(f"{'Resulterend Bruto Maandsalaris:':<40} € {s1_employee_net_results['gross_monthly_salary']:.2f}")
print(f"{'Resulterend Netto Maandinkomen:':<40} € {s1_employee_net_results['net_monthly_income']:.2f} (Let op: lager dan freelancer)")

print(f"\n--- WERKNEMER SCENARIO 2: O.b.v. Gelijk Netto Maandinkomen (€ {target_net_for_employee_scenario:.2f}) ---")
s2_cost = s2_employer_cost_results['total_cost_annual']
print(f"{'Benodigd Bruto Maandsalaris:':<40} € {s2_employee_net_results['gross_monthly_salary']:.2f}")
print(f"{'Totale Werkgeverskosten per jaar:':<40} € {s2_cost:.2f}")
print(f"{'Equivalent Freelance Uurtarief:':<40} € {s2_equivalent_hourly_rate:.2f}")

print("\n--- Specificatie Werkgeverskosten (Scenario 2) ---")
for item, value in s2_employer_cost_results['breakdown'].items():
    print(f"  {item:<38} € {value:.2f}")

print("\n--- SAMENVATTENDE VERGELIJKING ---")
summary_data = {
    "Indicator": ["Freelancer", "Werknemer (voor gelijk netto)"],
    "Netto Inkomen p/m": [f"€ {fr['net_disposable_monthly']:.2f}", f"€ {s2_employee_net_results['net_monthly_income']:.2f}"],
    "Uurtarief / Equiv. Uurtarief": [f"€ {fr['hourly_rate']:.2f}", f"€ {s2_equivalent_hourly_rate:.2f}"],
    "Totale Werkgeverskosten / Omzet (Jaar)": [f"€ {fr['gross_annual_revenue']:.2f}", f"€ {s2_cost:.2f}"]
}
print(pd.DataFrame(summary_data).to_string(index=False))
print("\nDisclaimer: Dit is een gedetailleerder model. Werkelijke premies en kosten kunnen per bedrijf afwijken.")
