import pandas as pd

# --- CALCULATOR VERSIE 4.0 (Pension & Employee Calculation Corrected) ---
# --- CONFIGURATIE JAAR ---
CALCULATION_YEAR = 2025 # Verander naar 2024 om oude cijfers te gebruiken

# --- INPUTS (Pas deze waarden aan zoals nodig) ---
# Scenario 1: Freelance uurtarief is de basis
freelance_hourly_rate_ex_vat_input = 24 # Aangepast voor realistischer scenario na correcties
hours_per_month_input = 130

# Scenario 2: Doel netto maandinkomen is de basis
target_net_disposable_monthly_income_input = 2800.00

# Kies welk scenario je wilt draaien:
# "rate_based" of "target_net_based"
calculation_mode = "rate_based"
# calculation_mode = "target_net_based"

# --- NIEUWE REALISME INPUTS ---
# % van de gewerkte uren dat niet declarabel is (admin, acquisitie, etc.)
# Voorbeeld: 20% overhead betekent dat van 100 gewerkte uren, er 80 gefactureerd worden.
non_declarable_overhead_percentage_input = 0.0

# --- FREELANCER KOSTEN & RESERVERINGEN ---
apply_entrepreneurial_deductions_input = True
freelance_aov_monthly_input = 200.00 # Zakelijke kosten
freelance_other_costs_monthly_input = 50.00 # Zakelijke kosten
freelance_pension_monthly_input = 300.00 # PRIVÉ reservering, geen zakelijke kostenpost
desired_freelance_buffer_percentage_input = 0.15 # % van winst

# --- WERKNEMER PARAMETERS ---
employer_total_cost_factor = 1.30
holiday_pay_rate_employee = 0.08
employee_pension_contribution_percentage_input = 0.05


# --- JAARSPECIFIEKE PARAMETERS (2025) ---
if CALCULATION_YEAR == 2025:
    self_employed_deduction_annual = 3200.00  # Based on 2024 trend, official may vary
    starters_deduction_annual = 2123.00
    mkb_profit_exemption_rate = 0.1270
    zvw_rate_freelancer = 0.0526
    zvw_max_income = 75864.00
    box1_schijf1_grens = 75518.00 # For AOW-leeftijd
    box1_schijf1_tarief = 0.3697
    box1_schijf2_tarief = 0.4950
    ahk_max = 3362.00 # Based on 2024, official 2025 may vary
    ahk_afbouw_grens_start = 24814.00
    ahk_afbouw_percentage = 0.0663
    ak_max = 5532.00 # Based on 2024, official 2025 may vary
    ak_opbouw_grens1 = 11490
    ak_opbouw_perc1 = 0.08425
    ak_opbouw_grens2 = 23201
    ak_opbouw_perc2 = 0.31433
    ak_opbouw_grens3 = 37691
    ak_opbouw_perc3 = 0.02663
    ak_afbouw_start = 37691.00
    ak_afbouw_perc = 0.06510
    ak_afbouw_eind = 124934.00

elif CALCULATION_YEAR == 2024:
    self_employed_deduction_annual = 3750.00
    starters_deduction_annual = 2123.00
    mkb_profit_exemption_rate = 0.1331
    zvw_rate_freelancer = 0.0532
    zvw_max_income = 71628.00
    box1_schijf1_grens = 75518.00
    box1_schijf1_tarief = 0.3697
    box1_schijf2_tarief = 0.4950
    ahk_max = 3362.00
    ahk_afbouw_grens_start = 24813.00
    ahk_afbouw_percentage = 0.06632
    ak_max = 5532.00
    ak_opbouw_grens1 = 11490
    ak_opbouw_perc1 = 0.08425
    ak_opbouw_grens2 = 23201
    ak_opbouw_perc2 = 0.31433
    ak_opbouw_grens3 = 37691
    ak_opbouw_perc3 = 0.02663
    ak_afbouw_start = 37691.00
    ak_afbouw_perc = 0.06510
    ak_afbouw_eind = 124934.00
else:
    raise ValueError("Calculation year not supported")

# --- BELASTINGFUNCTIES (Generiek gemaakt voor Zowel Freelancer als Werknemer) ---
def calculate_ib_box1(taxable_income_annual, year):
    if taxable_income_annual <= 0: return 0
    if year in [2024, 2025]: # Using 2024 logic for both as 2025 is similar structure
        sch1_grens = box1_schijf1_grens
        tarief1 = box1_schijf1_tarief
        tarief2 = box1_schijf2_tarief
        if taxable_income_annual <= sch1_grens:
            return taxable_income_annual * tarief1
        else:
            return (sch1_grens * tarief1) + ((taxable_income_annual - sch1_grens) * tarief2)
    raise ValueError(f"Year {year} not supported in IB calculation")

def calculate_zvw(profit_for_zvw_annual):
    if profit_for_zvw_annual <= 0: return 0
    return min(profit_for_zvw_annual, zvw_max_income) * zvw_rate_freelancer

def calculate_general_tax_credit(taxable_income_for_calc_annual):
    afbouw_eind = ahk_afbouw_grens_start + (ahk_max / ahk_afbouw_percentage)
    if taxable_income_for_calc_annual <= ahk_afbouw_grens_start:
        credit = ahk_max
    elif taxable_income_for_calc_annual < afbouw_eind:
        credit = ahk_max - ahk_afbouw_percentage * (taxable_income_for_calc_annual - ahk_afbouw_grens_start)
    else:
        credit = 0
    return max(0, credit)

def calculate_labor_tax_credit(labor_income_annual):
    if labor_income_annual <= 0: return 0
    val_opbouw1 = ak_opbouw_grens1 * ak_opbouw_perc1
    val_opbouw2 = val_opbouw1 + (ak_opbouw_grens2 - ak_opbouw_grens1) * ak_opbouw_perc2
    if labor_income_annual <= ak_opbouw_grens1:
        credit = labor_income_annual * ak_opbouw_perc1
    elif labor_income_annual <= ak_opbouw_grens2:
        credit = val_opbouw1 + (labor_income_annual - ak_opbouw_grens1) * ak_opbouw_perc2
    elif labor_income_annual <= ak_opbouw_grens3:
        credit = val_opbouw2 + (labor_income_annual - ak_opbouw_grens2) * ak_opbouw_perc3
    elif labor_income_annual < ak_afbouw_start:
        credit = ak_max
    elif labor_income_annual <= ak_afbouw_eind:
        credit = ak_max - (labor_income_annual - ak_afbouw_start) * ak_afbouw_perc
    else:
        credit = 0
    return max(0, min(ak_max, credit))

# --- CORE CALCULATORS ---
def calculate_freelancer_finances(hourly_rate, total_hours_worked, overhead_perc, aov_monthly, other_costs_monthly, pension_monthly, apply_deductions, buffer_percentage, year):
    # Correctly calculate billable hours
    billable_hours_monthly = total_hours_worked / (1 + overhead_perc / 100)
    gross_annual_revenue = hourly_rate * billable_hours_monthly * 12
    
    # Pension is NOT a business cost. Only AOV and other costs are.
    total_direct_costs_annual = (aov_monthly + other_costs_monthly) * 12
    profit_before_fiscal = gross_annual_revenue - total_direct_costs_annual

    entrepreneurial_deduction = 0
    if apply_deductions and profit_before_fiscal > 0:
        deduction = self_employed_deduction_annual + starters_deduction_annual
        entrepreneurial_deduction = min(deduction, profit_before_fiscal)
    
    profit_after_entrepreneurial = profit_before_fiscal - entrepreneurial_deduction
    mkb_exemption = profit_after_entrepreneurial * mkb_profit_exemption_rate if profit_after_entrepreneurial > 0 else 0
    taxable_profit_for_ib = profit_after_entrepreneurial - mkb_exemption

    # Tax calculation
    total_ib_pvv_berekend = calculate_ib_box1(taxable_profit_for_ib, year)
    ahk_credit = calculate_general_tax_credit(taxable_profit_for_ib)
    ak_credit = calculate_labor_tax_credit(profit_before_fiscal) # Labor credit is based on profit before deductions
    total_credits = ahk_credit + ak_credit
    payable_ib_pvv = max(0, total_ib_pvv_berekend - total_credits)
    
    # ZVW calculation
    profit_for_zvw = profit_after_entrepreneurial
    zvw_payable = calculate_zvw(profit_for_zvw)
    total_tax = payable_ib_pvv + zvw_payable

    # Net income and private allocations
    net_income_after_tax = profit_before_fiscal - total_tax
    buffer_amount = net_income_after_tax * buffer_percentage # Buffer as % of post-tax income is more prudent
    pension_annual = pension_monthly * 12
    
    net_disposable_annual = net_income_after_tax - buffer_amount - pension_annual
    net_disposable_monthly = net_disposable_annual / 12

    return {
        "hourly_rate": hourly_rate, "net_disposable_monthly": net_disposable_monthly,
        "gross_annual_revenue": gross_annual_revenue, "total_direct_costs_annual": total_direct_costs_annual,
        "profit_before_fiscal_deductions_annual": profit_before_fiscal,
        "entrepreneurial_deduction_amount": entrepreneurial_deduction, "mkb_exemption_amount": mkb_exemption,
        "taxable_profit_for_ib_calc_annual": taxable_profit_for_ib,
        "total_ib_pvv_gross": total_ib_pvv_berekend, "general_tax_credit": ahk_credit, "labor_tax_credit": ak_credit,
        "total_tax_credits": total_credits, "payable_ib_pvv_annual": payable_ib_pvv,
        "zvw_freelancer_annual": zvw_payable, "total_payable_tax_freelancer_annual": total_tax,
        "net_income_after_tax_annual": net_income_after_tax, "buffer_amount_annual": buffer_amount,
        "pension_allocation_annual": pension_annual, "net_disposable_income_freelancer_annual": net_disposable_annual,
        "billable_hours_monthly": billable_hours_monthly
    }

def calculate_employee_finances(gross_monthly_excl_holiday, pension_contrib_perc, year):
    if gross_monthly_excl_holiday <= 0: return {"net_monthly_income": 0}
    
    gross_annual_salary = gross_monthly_excl_holiday * 12
    pension_contribution_annual = gross_annual_salary * pension_contrib_perc
    
    # Taxable income for Box 1 (loonheffing) is after pension contribution
    taxable_income_annual = gross_annual_salary - pension_contribution_annual
    
    # Labor income for arbeidskorting is the full gross salary including holiday pay
    labor_income_annual = gross_annual_salary * (1 + holiday_pay_rate_employee)

    # Calculate tax and credits using the same functions
    total_ib_pvv_gross = calculate_ib_box1(taxable_income_annual, year)
    ahk_credit = calculate_general_tax_credit(taxable_income_annual)
    ak_credit = calculate_labor_tax_credit(labor_income_annual)
    total_credits = ahk_credit + ak_credit
    
    payable_tax_annual = max(0, total_ib_pvv_gross - total_credits)
    
    # Net income calculation
    net_annual_income = taxable_income_annual - payable_tax_annual
    
    # Include net holiday pay
    holiday_pay_gross_annual = gross_monthly_excl_holiday * 12 * holiday_pay_rate_employee
    # Simplified tax on holiday pay (often special tariff, but this is a close estimate)
    tax_on_holiday_pay = calculate_ib_box1(labor_income_annual, year) - calculate_ib_box1(gross_annual_salary, year)
    net_holiday_pay_annual = max(0, holiday_pay_gross_annual - tax_on_holiday_pay)

    # Total net income is regular net + net holiday pay
    total_net_annual = net_annual_income + net_holiday_pay_annual
    
    # We want the average monthly net disposable income
    avg_net_monthly = (gross_annual_salary * (1 + holiday_pay_rate_employee) - pension_contribution_annual - payable_tax_annual) / 12


    return {
        "net_monthly_income": avg_net_monthly,
        "gross_monthly_salary": gross_monthly_excl_holiday,
        "pension_contribution_monthly": pension_contribution_annual / 12,
        "payable_tax_monthly": payable_tax_annual / 12,
        "labor_tax_credit": ak_credit,
        "general_tax_credit": ahk_credit
    }


# --- LOGICA VOOR VERSCHILLENDE MODI ---
freelancer_results = {}
if calculation_mode == "rate_based":
    freelancer_results = calculate_freelancer_finances(
        freelance_hourly_rate_ex_vat_input, hours_per_month_input, non_declarable_overhead_percentage_input,
        freelance_aov_monthly_input, freelance_other_costs_monthly_input, freelance_pension_monthly_input,
        apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR
    )
    target_net_for_employee_scenario = freelancer_results["net_disposable_monthly"]

elif calculation_mode == "target_net_based":
    target_net = target_net_disposable_monthly_income_input
    low_rate, high_rate = 10.0, 200.0
    for i in range(50):
        current_rate_guess = (low_rate + high_rate) / 2
        res_guess = calculate_freelancer_finances(
            current_rate_guess, hours_per_month_input, non_declarable_overhead_percentage_input,
            freelance_aov_monthly_input, freelance_other_costs_monthly_input, freelance_pension_monthly_input,
            apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR
        )
        if abs(res_guess["net_disposable_monthly"] - target_net) < 0.50:
            freelancer_results = res_guess
            break
        if res_guess["net_disposable_monthly"] < target_net: low_rate = current_rate_guess
        else: high_rate = current_rate_guess
        if (high_rate - low_rate) < 0.01:
            freelancer_results = res_guess
            break
    if not freelancer_results:
        freelancer_results = calculate_freelancer_finances(low_rate, hours_per_month_input, non_declarable_overhead_percentage_input, freelance_aov_monthly_input, freelance_other_costs_monthly_input, freelance_pension_monthly_input, apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR)
    target_net_for_employee_scenario = freelancer_results["net_disposable_monthly"]


# --- WERKNEMER BEREKENINGEN (Beide scenario's) ---
# Scenario 1: Gebaseerd op gelijke werkgeverskosten
s1_emp_total_cost_annual = freelancer_results.get("gross_annual_revenue", 0)
s1_emp_gross_annual_incl_holiday = s1_emp_total_cost_annual / employer_total_cost_factor
s1_emp_gross_monthly_excl_holiday = (s1_emp_gross_annual_incl_holiday / (1 + holiday_pay_rate_employee)) / 12
s1_employee_results = calculate_employee_finances(s1_emp_gross_monthly_excl_holiday, employee_pension_contribution_percentage_input, CALCULATION_YEAR)

# Scenario 2: Zoek naar bruto salaris voor gelijk netto inkomen
s2_employee_results = {}
low_gross, high_gross = 1000.0, 15000.0
for i in range(30):
    current_gross_guess = (low_gross + high_gross) / 2
    res_guess = calculate_employee_finances(current_gross_guess, employee_pension_contribution_percentage_input, CALCULATION_YEAR)
    if abs(res_guess["net_monthly_income"] - target_net_for_employee_scenario) < 0.50:
        s2_employee_results = res_guess
        break
    if res_guess["net_monthly_income"] < target_net_for_employee_scenario: low_gross = current_gross_guess
    else: high_gross = current_gross_guess
if not s2_employee_results:
    s2_employee_results = calculate_employee_finances(low_gross, employee_pension_contribution_percentage_input, CALCULATION_YEAR)

s2_gross_annual_salary_incl_holiday = s2_employee_results.get("gross_monthly_salary", 0) * (1 + holiday_pay_rate_employee) * 12
s2_total_employer_cost_annual = s2_gross_annual_salary_incl_holiday * employer_total_cost_factor
s2_equivalent_freelance_hourly_rate = (s2_total_employer_cost_annual / 12) / (freelancer_results.get("billable_hours_monthly") or hours_per_month_input)


# --- PRESENTATIE ---
pd.options.display.float_format = '{:.2f}'.format
print(f"\n--- CALCULATOR VERSIE 4.0 (Jaar: {CALCULATION_YEAR}) ---")
print(f"--- Gekozen Modus: {calculation_mode} ---")

# Inputs
print("\n--- INPUTS OVERZICHT ---")
inputs_data_display = {
    "Freelance Uurtarief (excl. BTW)": f"€ {freelancer_results.get('hourly_rate', 0):.2f}",
    "Totaal Werkuren per maand": f"{hours_per_month_input}",
    "Overhead percentage (niet-declarabel)": f"{non_declarable_overhead_percentage_input:.1f}%",
    "Effectieve Facturabele Uren per maand": f"{freelancer_results.get('billable_hours_monthly', 0):.1f}",
    "Freelance AOV/mnd (zakelijke kost)": f"€ {freelance_aov_monthly_input:.2f}",
    "Freelance Overige Kosten/mnd (zakelijke kost)": f"€ {freelance_other_costs_monthly_input:.2f}",
    "Freelance Pensioen/mnd (privé reservering)": f"€ {freelance_pension_monthly_input:.2f}",
    "Freelance Buffer % (van netto na belasting)": f"{desired_freelance_buffer_percentage_input*100:.0f}%",
}
for key, value in inputs_data_display.items(): print(f"{key:<55} {value}")

# Freelancer
if freelancer_results:
    print("\n--- FREELANCER FINANCIËN (Details) ---")
    fr = freelancer_results
    freelancer_finance_data_display = {
        "Bruto Jaaromzet (op basis van facturabele uren)": fr['gross_annual_revenue'],
        "Totale Directe Jaarkosten (AOV, etc.)": -fr['total_direct_costs_annual'],
        "WINST VOOR FISCALE AFTREKPOSTEN": fr['profit_before_fiscal_deductions_annual'],
        "  Ondernemersaftrek (Zelfst.+Starter)": -fr['entrepreneurial_deduction_amount'],
        "Winst na Ondernemersaftrek": fr['profit_before_fiscal_deductions_annual'] - fr['entrepreneurial_deduction_amount'],
        "  MKB Winstvrijstelling": -fr['mkb_exemption_amount'],
        "BELASTBARE WINST (Grondslag IB)": fr['taxable_profit_for_ib_calc_annual'],
        "BEREKENDE BELASTING (vóór kortingen)": fr['total_ib_pvv_gross'],
        "  Algemene Heffingskorting": -fr['general_tax_credit'],
        "  Arbeidskorting": -fr['labor_tax_credit'],
        "TE BETALEN IB/PVV": fr['payable_ib_pvv_annual'],
        "TE BETALEN ZVW-BIJDRAGE": fr['zvw_freelancer_annual'],
        "TOTALE JAARLIJKSE BELASTING & ZVW": fr['total_payable_tax_freelancer_annual'],
        "NETTO INKOMEN (Winst - Belasting)": fr['net_income_after_tax_annual'],
        "PRIVÉ RESERVERINGEN (van netto inkomen):": "",
        "  Gereserveerde Buffer": -fr['buffer_amount_annual'],
        "  Gereserveerd voor Pensioen": -fr['pension_allocation_annual'],
        "NETTO BESTEEDBAAR INKOMEN (Jaar)": fr['net_disposable_income_freelancer_annual'],
        "NETTO BESTEEDBAAR INKOMEN (Gem. Maand)": fr['net_disposable_monthly'],
    }
    for key, value in freelancer_finance_data_display.items():
        display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) else str(value)
        if key.startswith("  "): print(f"  {key:<53} {display_value}")
        elif value == "": print(f"\n{key}")
        else: print(f"{key:<55} {display_value}")

# Werknemer S1
print(f"\n--- WERKNEMER SCENARIO 1: O.B.V. GELIJKE WERKGEVERSKOSTEN ALS FREELANCER OMZET (€ {s1_emp_total_cost_annual/12:.2f}/mnd) ---")
s1r = s1_employee_results
employee_s1_data_display = {
    "Bruto Maandsalaris (excl. vakantiegeld)": s1r.get('gross_monthly_salary', 0),
    "NETTO GEMIDDELD MAANDINKOMEN (incl. vak.geld)": s1r.get('net_monthly_income', 0),
}
for key, value in employee_s1_data_display.items(): print(f"{key:<55} € {value:.2f}")

# Werknemer S2
print(f"\n--- WERKNEMER SCENARIO 2: STREVEN NAAR GELIJK NETTO MAANDINKOMEN (€ {target_net_for_employee_scenario:.2f}) ---")
s2r = s2_employee_results
employee_s2_data_display = {
    "Doel Netto Maandinkomen Werknemer": target_net_for_employee_scenario,
    "Benodigd Bruto Maandsalaris (excl. vak.geld)": s2r.get('gross_monthly_salary', 0),
    "Resulterend Netto Maandinkomen (check)": s2r.get('net_monthly_income', 0),
    "Totale Maandelijkse Kosten Werkgever": s2_total_employer_cost_annual / 12,
    "EQUIVALENT FREELANCE UURTARIEF NODIG": s2_equivalent_freelance_hourly_rate
}
for key, value in employee_s2_data_display.items(): print(f"{key:<55} € {value:.2f}")

# Samenvatting
print("\n--- SAMENVATTENDE VERGELIJKING ---")
summary_data = {
    "Indicator": ["Freelancer", "Werknemer (equivalent netto)"],
    "Netto Besteedbaar Maandinkomen": [f"€ {freelancer_results.get('net_disposable_monthly', 0):.2f}", f"€ {s2_employee_results.get('net_monthly_income', 0):.2f}"],
    "Nodig Uurtarief / Equivalent Uurtarief": [f"€ {freelancer_results.get('hourly_rate', 0):.2f}", f"€ {s2_equivalent_freelance_hourly_rate:.2f}"],
    "Bruto Maandinkomen Basis": [f"€ {freelancer_results.get('gross_annual_revenue', 0)/12:.2f} (FL Omzet)", f"€ {s2_employee_results.get('gross_monthly_salary', 0):.2f} (WN Salaris)"]
}
print(pd.DataFrame(summary_data).to_string(index=False))
print("\nDisclaimer: Dit is een modelberekening. Werkelijke fiscale situaties kunnen afwijken.")
