import pandas as pd

# --- INPUTS (Pas deze waarden aan zoals nodig) ---
freelance_hourly_rate_ex_vat = 24.00
hours_per_month = 130

# Freelance kosten per maand
freelance_aov_monthly = 200
freelance_pension_monthly = 200.00
freelance_other_costs_monthly = 0

# NIEUW: Toggle voor zelfstandigen/startersaftrek
apply_entrepreneurial_deductions = False # Zet op True om mee te nemen
self_employed_deduction_annual_2024 = 3750.00
starters_deduction_annual_2024 = 2123.00 # Alleen relevant als apply_entrepreneurial_deductions = True

# MKB Winstvrijstelling
mkb_profit_exemption_rate_freelancer = 0.1331 # 13.31% voor 2024

# NIEUW: Buffer voor freelancer
desired_freelance_buffer_percentage = 0.10 # 10% van winst voor belasting wordt gereserveerd

# ZVW parameters 2024
zvw_rate_freelancer_2024 = 0.0532 # 5.32%
zvw_max_income_2024 = 71628.00

# Werkgeverslasten en vakantiegeld werknemer
employer_total_cost_factor = 1.32
holiday_pay_rate_employee = 0.08

# NIEUW: Aanname voor netto retentie op vakantiegeld werknemer
employee_net_retention_on_holiday_pay = 0.55 # Geschat 55% van bruto vakantiegeld blijft netto over

# Optioneel: Gemiddelde werknemersbijdrage aan pensioen (als percentage van bruto maandsalaris)
employee_pension_contribution_percentage = 0.05

# --- BELASTINGFUNCTIES FREELANCER (2024 tarieven) ---
def calculate_income_tax_box1_2024(taxable_income_annual):
    """Berekent Inkomstenbelasting Box 1 voor 2024. Exclusief heffingskortingen."""
    if taxable_income_annual <= 0:
        return 0
    
    schijf1_grens = 75518.00
    tarief_schijf1 = 0.3697 # Tarief voor inkomen tot AOW-leeftijd
    tarief_schijf2 = 0.4950

    if taxable_income_annual <= schijf1_grens:
        tax = taxable_income_annual * tarief_schijf1
    else:
        tax = (schijf1_grens * tarief_schijf1) + \
              ((taxable_income_annual - schijf1_grens) * tarief_schijf2)
    return tax

def calculate_zvw_2024(profit_before_tax_annual):
    """Berekent Inkomensafhankelijke bijdrage ZVW voor 2024."""
    if profit_before_tax_annual <= 0:
        return 0
    
    taxable_for_zvw = min(profit_before_tax_annual, zvw_max_income_2024)
    zvw_contribution = taxable_for_zvw * zvw_rate_freelancer_2024
    return zvw_contribution

# --- DYNAMISCHE NETTO RETENTIEGRAAD WERKNEMER ---
def get_employee_net_retention_rate(gross_monthly_salary_excl_holiday):
    """Geeft een geschat netto retentiepercentage o.b.v. bruto maandsalaris."""
    if gross_monthly_salary_excl_holiday <= 2500:
        return 0.70 # Hogere retentie bij lagere salarissen
    elif gross_monthly_salary_excl_holiday <= 4000:
        return 0.63 # Gemiddelde retentie
    else:
        return 0.58 # Lagere retentie bij hogere salarissen
    # Deze staffel is een benadering. Echte bruto/netto is complexer.

# --- BEREKENINGEN FREELANCER (JAARBASIS VOOR BELASTING) ---
# 1. Bruto Jaaromzet Freelancer
gross_annual_revenue_freelancer = freelance_hourly_rate_ex_vat * hours_per_month * 12

# 2. Totale Jaarlijkse Freelance Kosten (excl. buffer)
total_freelance_costs_annual = (freelance_aov_monthly + freelance_pension_monthly + freelance_other_costs_monthly) * 12

# 3. Winst vóór Ondernemersaftrek en MKB-vrijstelling
profit_before_deductions_annual = gross_annual_revenue_freelancer - total_freelance_costs_annual

# 4. Ondernemersaftrek (indien van toepassing)
entrepreneurial_deduction_total_annual = 0
if apply_entrepreneurial_deductions:
    entrepreneurial_deduction_total_annual = self_employed_deduction_annual_2024 + starters_deduction_annual_2024
    # Check: Zelfstandigenaftrek kan niet hoger zijn dan de winst
    entrepreneurial_deduction_total_annual = min(entrepreneurial_deduction_total_annual, profit_before_deductions_annual if profit_before_deductions_annual > 0 else 0)

profit_after_entrepreneurial_deductions_annual = profit_before_deductions_annual - entrepreneurial_deduction_total_annual

# 5. MKB-winstvrijstelling
if profit_after_entrepreneurial_deductions_annual > 0:
    mkb_exemption_amount_annual = profit_after_entrepreneurial_deductions_annual * mkb_profit_exemption_rate_freelancer
else:
    mkb_exemption_amount_annual = 0

# 6. Belastbare Winst voor IB (na MKB-vrijstelling)
taxable_profit_for_ib_annual = profit_after_entrepreneurial_deductions_annual - mkb_exemption_amount_annual

# 7. Winst voor ZVW (na ondernemersaftrek, vóór MKB-vrijstelling)
# De grondslag voor ZVW is winst vóór MKB-vrijstelling, maar na ondernemersaftrek
profit_for_zvw_annual = profit_after_entrepreneurial_deductions_annual

# 8. Inkomstenbelasting Box 1
income_tax_freelancer_annual = calculate_income_tax_box1_2024(taxable_profit_for_ib_annual)

# 9. ZVW-bijdrage
zvw_freelancer_annual = calculate_zvw_2024(profit_for_zvw_annual)

# 10. Totale Belasting Freelancer
total_tax_freelancer_annual = income_tax_freelancer_annual + zvw_freelancer_annual

# 11. Winst na Belasting, vóór Buffer
profit_after_tax_before_buffer_annual = profit_after_entrepreneurial_deductions_annual - total_tax_freelancer_annual # Let op: MKB is al in mindering gebracht op IB grondslag

# 12. Buffer Reservering
# Buffer berekend over winst na kosten & ondernemersaftrek, maar vóór MKB, IB en ZVW.
# Of, alternatief, over winst na alle kosten en aftrekposten, maar voor belastingen.
# Hier kiezen we voor: Winst na kosten, voor ondernemersaftrek, voor MKB en belastingen.
# profit_base_for_buffer_annual = profit_before_deductions_annual # Een andere optie
# Gekozen: buffer over de winst die anders belastbaar zou zijn (na kosten en aftrekposten, voor MKB-vrijstelling)
profit_base_for_buffer_annual = profit_after_entrepreneurial_deductions_annual
buffer_amount_annual = profit_base_for_buffer_annual * desired_freelance_buffer_percentage if profit_base_for_buffer_annual > 0 else 0

# 13. Netto Besteedbaar Inkomen Freelancer (Jaar en Maand)
net_disposable_income_freelancer_annual = profit_after_tax_before_buffer_annual - buffer_amount_annual
net_disposable_income_freelancer_monthly = net_disposable_income_freelancer_annual / 12
if hours_per_month > 0:
    net_effective_hourly_rate_freelancer = net_disposable_income_freelancer_monthly / hours_per_month
else:
    net_effective_hourly_rate_freelancer = 0


# --- BEREKENINGEN WERKNEMER - SCENARIO 1: O.B.V. GELIJKE WERKGEVERSKOSTEN ALS FREELANCER BRUTO OMZET ---
total_employer_cost_annual_scenario1 = gross_annual_revenue_freelancer
gross_annual_salary_employee_incl_holiday_scenario1 = total_employer_cost_annual_scenario1 / employer_total_cost_factor
gross_monthly_salary_employee_excl_holiday_scenario1 = (gross_annual_salary_employee_incl_holiday_scenario1 / (1 + holiday_pay_rate_employee)) / 12

# Jaarlijkse netto berekening werknemer Scenario 1
employee_net_retention_rate_s1 = get_employee_net_retention_rate(gross_monthly_salary_employee_excl_holiday_scenario1)
#   Netto van regulier salaris (12 maanden)
net_from_regular_salary_annual_s1 = (gross_monthly_salary_employee_excl_holiday_scenario1 * employee_net_retention_rate_s1) * 12
#   Bruto vakantiegeld
gross_holiday_pay_annual_s1 = gross_monthly_salary_employee_excl_holiday_scenario1 * holiday_pay_rate_employee * 12
#   Netto van vakantiegeld
net_from_holiday_pay_annual_s1 = gross_holiday_pay_annual_s1 * employee_net_retention_on_holiday_pay
#   Totaal netto jaarinkomen werknemer
total_net_annual_income_employee_scenario1 = net_from_regular_salary_annual_s1 + net_from_holiday_pay_annual_s1
#   Effectief gemiddeld netto maandinkomen werknemer
avg_net_monthly_income_employee_scenario1 = total_net_annual_income_employee_scenario1 / 12


# --- BEREKENINGEN WERKNEMER - SCENARIO 2: GELIJK NETTO BESTEEDBAAR INKOMEN ALS FREELANCER ---
target_net_disposable_monthly_income_employee_scenario2 = net_disposable_income_freelancer_monthly

# Iteratieve benadering om bruto salaris te vinden dat leidt tot doel-netto (vereenvoudigd)
# We moeten rekening houden met vakantiegeld en de dynamische retentiegraad.
# Stel: Netto_Doel = (Bruto_Maand_excl_Vak * Retentie_Regulier * 12 + Bruto_Maand_excl_Vak * VakRate * Retentie_Vak * 12) / 12
# Netto_Doel = Bruto_Maand_excl_Vak * (Retentie_Regulier + VakRate * Retentie_Vak)
# Bruto_Maand_excl_Vak = Netto_Doel / (Retentie_Regulier + VakRate * Retentie_Vak)

# Eerste schatting voor bruto maandsalaris
temp_retention_rate_for_estimation = get_employee_net_retention_rate(3000) # Gemiddelde gok
denominator = temp_retention_rate_for_estimation + (holiday_pay_rate_employee * employee_net_retention_on_holiday_pay)
estimated_gross_monthly_salary_excl_holiday_scenario2 = target_net_disposable_monthly_income_employee_scenario2 / denominator if denominator > 0 else 3000

# Verfijn met een paar iteraties (eenvoudige iteratie, niet perfect)
for _ in range(5): # 5 iteraties zouden moeten helpen convergeren
    current_retention_rate = get_employee_net_retention_rate(estimated_gross_monthly_salary_excl_holiday_scenario2)
    denominator = current_retention_rate + (holiday_pay_rate_employee * employee_net_retention_on_holiday_pay)
    if denominator == 0 : break # voorkom delen door 0
    new_gross = target_net_disposable_monthly_income_employee_scenario2 / denominator
    if abs(new_gross - estimated_gross_monthly_salary_excl_holiday_scenario2) < 1: # Convergentie
        estimated_gross_monthly_salary_excl_holiday_scenario2 = new_gross
        break
    estimated_gross_monthly_salary_excl_holiday_scenario2 = new_gross


# Werknemer cijfers voor Scenario 2
gross_annual_salary_incl_holiday_scenario2 = estimated_gross_monthly_salary_excl_holiday_scenario2 * (1 + holiday_pay_rate_employee) * 12
total_employer_cost_annual_scenario2 = gross_annual_salary_incl_holiday_scenario2 * employer_total_cost_factor
total_employer_cost_monthly_scenario2 = total_employer_cost_annual_scenario2 / 12

if hours_per_month > 0:
    equivalent_freelance_hourly_rate_scenario2 = total_employer_cost_monthly_scenario2 / hours_per_month
else:
    equivalent_freelance_hourly_rate_scenario2 = 0

# Jaarlijkse netto berekening werknemer Scenario 2 (check)
employee_net_retention_rate_s2 = get_employee_net_retention_rate(estimated_gross_monthly_salary_excl_holiday_scenario2)
net_from_regular_salary_annual_s2 = (estimated_gross_monthly_salary_excl_holiday_scenario2 * employee_net_retention_rate_s2) * 12
gross_holiday_pay_annual_s2 = estimated_gross_monthly_salary_excl_holiday_scenario2 * holiday_pay_rate_employee * 12
net_from_holiday_pay_annual_s2 = gross_holiday_pay_annual_s2 * employee_net_retention_on_holiday_pay
total_net_annual_income_employee_scenario2_check = net_from_regular_salary_annual_s2 + net_from_holiday_pay_annual_s2
avg_net_monthly_income_employee_scenario2_check = total_net_annual_income_employee_scenario2_check / 12

# --- PRESENTATIE ---
pd.options.display.float_format = '{:.2f}'.format

print("--- INPUTS OVERZICHT ---")
inputs_data = {
    "Freelance Uurtarief (excl. BTW)": f"€ {freelance_hourly_rate_ex_vat:.2f}",
    "Uren per maand": hours_per_month,
    "Freelance AOV/mnd": f"€ {freelance_aov_monthly:.2f}",
    "Freelance Pensioen/mnd": f"€ {freelance_pension_monthly:.2f}",
    "Freelance Overige Kosten/mnd": f"€ {freelance_other_costs_monthly:.2f}",
    "Zelfstandigen/Startersaftrek Actief": "Ja" if apply_entrepreneurial_deductions else "Nee",
    "Freelance Buffer % (van winst v. belasting)": f"{desired_freelance_buffer_percentage*100:.0f}%",
    "Werkgeverslasten Factor": employer_total_cost_factor,
    "Werknemer Pensioenbijdrage % (van bruto)": f"{employee_pension_contribution_percentage*100:.0f}%",
    "Netto Retentie Vakantiegeld WN %": f"{employee_net_retention_on_holiday_pay*100:.0f}%"
}
for key, value in inputs_data.items(): print(f"{key:<45} {value}")
print("\n--- FREELANCER FINANCIËN (JAARBASIS & GEM. MAAND) ---")
freelancer_finance_data = {
    "Bruto Jaaromzet": gross_annual_revenue_freelancer,
    "Totale Jaarkosten (excl. buffer)": total_freelance_costs_annual,
    "Winst voor Ondernemersaftrek & MKB": profit_before_deductions_annual,
    "  Ondernemersaftrek (Zelfst.+Starter)": -entrepreneurial_deduction_total_annual if apply_entrepreneurial_deductions else "N.v.t.",
    "Winst na Ondernemersaftrek": profit_after_entrepreneurial_deductions_annual,
    "  MKB Winstvrijstelling (13.31%)": -mkb_exemption_amount_annual,
    "Belastbare Winst voor IB": taxable_profit_for_ib_annual,
    "Grondslag ZVW": profit_for_zvw_annual,
    "  Inkomstenbelasting Box 1 (geschat)": -income_tax_freelancer_annual,
    "  ZVW-bijdrage (geschat)": -zvw_freelancer_annual,
    "Winst na Belasting (voor buffer)": profit_after_tax_before_buffer_annual,
    "  Gereserveerde Buffer": -buffer_amount_annual,
    "NETTO BESTEEDBAAR INKOMEN (Jaar)": net_disposable_income_freelancer_annual,
    "NETTO BESTEEDBAAR INKOMEN (Gem. Maand)": net_disposable_income_freelancer_monthly,
    "Netto Effectief Uurtarief (Gem. Maand)": net_effective_hourly_rate_freelancer
}
for key, value in freelancer_finance_data.items():
    display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) else value
    print(f"{key:<45} {display_value}")
print("*IB berekening is excl. heffingskortingen. Werkelijke IB kan lager zijn.\n")

print(f"--- WERKNEMER SCENARIO 1: O.B.V. GELIJKE WERKGEVERSKOSTEN ALS FREELANCER BRUTO OMZET (€ {total_employer_cost_annual_scenario1/12:.2f}/mnd) ---")
employee_s1_data = {
    "Bruto Maandsalaris (excl. vakantiegeld)": gross_monthly_salary_employee_excl_holiday_scenario1,
    "  Geschatte Netto Retentiegraad (regulier sal.)": f"{employee_net_retention_rate_s1*100:.0f}%",
    "Bruto Jaarsalaris (incl. 8% vakantiegeld)": gross_annual_salary_employee_incl_holiday_scenario1,
    "  Netto Jaarinkomen (geschat, incl. netto vak.geld)": total_net_annual_income_employee_scenario1,
    "NETTO GEMIDDELD MAANDINKOMEN (geschat)": avg_net_monthly_income_employee_scenario1
}
for key, value in employee_s1_data.items():
    display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) and not "%" in key else value
    print(f"{key:<55} {display_value}")
print("*Gebruik een externe bruto-netto calculator voor een precieze berekening.\n")

print(f"--- SCENARIO 2: STREVEN NAAR GELIJK NETTO MAANDINKOMEN (€ {target_net_disposable_monthly_income_employee_scenario2:.2f}) ---")
employee_s2_data = {
    "Doel Netto Maandinkomen Werknemer": target_net_disposable_monthly_income_employee_scenario2,
    "GESCHAT Bruto Maandsalaris Werknemer (excl. vakantiegeld)": estimated_gross_monthly_salary_excl_holiday_scenario2,
    "  Geschatte Netto Retentiegraad (regulier sal.)": f"{employee_net_retention_rate_s2*100:.0f}%",
    "  Netto Jaarinkomen Werknemer (check, geschat)": total_net_annual_income_employee_scenario2_check,
    "  Netto Maandinkomen Werknemer (check, geschat)": avg_net_monthly_income_employee_scenario2_check,
    "Totale Maandelijkse Kosten Werkgever voor dit salaris": total_employer_cost_monthly_scenario2,
    "EQUIVALENT FREELANCE UURTARIEF NODIG": equivalent_freelance_hourly_rate_scenario2
}
for key, value in employee_s2_data.items():
    display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) and not "%" in key else value
    print(f"{key:<55} {display_value}")
print("*Dit geschatte bruto salaris is een benadering. Gebruik externe 'netto-naar-bruto' tool voor precisie.\n")

print("--- SAMENVATTENDE VERGELIJKING FOCUS OP SCENARIO 2 ---")
summary_data = {
    "Indicator": ["Freelancer (huidige input)", "Werknemer (doel gelijk netto)"],
    "Netto Besteedbaar Maandinkomen (Doel)": [f"€ {net_disposable_income_freelancer_monthly:.2f}", f"€ {avg_net_monthly_income_employee_scenario2_check:.2f} (check)"],
    "Freelance Uurtarief / Equivalent": [f"€ {freelance_hourly_rate_ex_vat:.2f}", f"€ {equivalent_freelance_hourly_rate_scenario2:.2f} (nodig)"],
    "Totale Werkgeverskosten per maand": ["N.v.t.", f"€ {total_employer_cost_monthly_scenario2:.2f}"]
}
df_summary = pd.DataFrame(summary_data)
print(df_summary.to_string(index=False))

print("\nDisclaimer: Dit is een modelberekening. Werkelijke fiscale situaties en netto inkomens kunnen afwijken.")
print("Heffingskortingen zijn niet meegenomen voor freelancer IB. Gebruik externe tools voor precieze bruto/netto berekeningen.")
print("De dynamische netto retentiegraad voor werknemers is een schatting.")

