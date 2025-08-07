import pandas as pd

# --- CALCULATOR VERSIE 3.0 ---
# --- CONFIGURATIE JAAR ---
CALCULATION_YEAR = 2025 # Verander naar 2024 om oude cijfers te gebruiken

# --- INPUTS (Pas deze waarden aan zoals nodig) ---
# Scenario 1: Freelance uurtarief is de basis
freelance_hourly_rate_ex_vat_input = 35.00 # Voorbeeld als uurtarief de input is
hours_per_month_input = 130

# Scenario 2: Doel netto maandinkomen is de basis
target_net_disposable_monthly_income_input = 2500.00 # Voorbeeld als doel-netto de input is

# Kies welk scenario je wilt draaien:
# "rate_based" of "target_net_based"
calculation_mode = "target_net_based"
# calculation_mode = "rate_based"


# --- JAARSPECIFIEKE PARAMETERS ---
if CALCULATION_YEAR == 2025:
    # Zelfstandigenaftrek & Startersaftrek
    self_employed_deduction_annual = 2470.00
    starters_deduction_annual = 2123.00 # Voorlopig ongewijzigd aangenomen
    # MKB Winstvrijstelling
    mkb_profit_exemption_rate = 0.1270
    # ZVW parameters
    zvw_rate_freelancer = 0.0526
    zvw_max_income = 75864.00
    # Box 1 Schijven & Tarieven (niet-AOW)
    box1_schijf1_grens = 38441.00
    box1_schijf2_grens = 76817.00
    box1_tarief_ib_schijf1 = 0.0817 # IB deel (35,82% - 27,65% PVV) -> Dit moet 35.82% zijn voor gecombineerd.
                                      # De functie splitst het intern correct.
    box1_tarief_pvv_schijf1 = 0.2765 # PVV deel
    # Het gecombineerde tarief voor de eerste schijf is 35,82%
    # De functie calculate_ib_and_pvv_box1_... gebruikt deze logica
    box1_tarief_ib_schijf2_combined = 0.3748 # Gecombineerd tarief (is alleen IB, PVV is 0 in schijf 2)
    box1_tarief_ib_schijf3_combined = 0.4950
    # Algemene Heffingskorting (AHK) (niet-AOW)
    ahk_max = 3068.00
    ahk_afbouw_grens_start = 28406.00
    ahk_afbouw_grens_eind = 76817.00 # Uitgaande van afbouw tot 0 bij de start van de hoogste IB schijf.
                                     # Precieze eindgrens voor afbouw AHK is soms iets anders, maar dit is een goede benadering.
                                     # Formule: max - (inkomen - startgrens) * afbouwpercentage
    ahk_afbouw_percentage = 0.06337 # 6,337%
    # Arbeidskorting (AK) (niet-AOW) - Vereenvoudigde implementatie o.b.v. max en afbouwgrens
    # Exacte schijven AK 2025 zijn complex en kunnen variëren in presentatie.
    # We gebruiken het maximum en een afbouw. Voor precieze AK, externe tool aanbevolen.
    ak_max_2025 = 5599.00
    ak_opbouw_grens1_2025 = 11490 # Geschatte grenzen, kunnen licht afwijken van officiële publicaties
    ak_opbouw_perc1_2025 = 0.08425
    ak_opbouw_grens2_2025 = 24820 # Tot hier max opbouwdeel 1
    ak_opbouw_perc2_2025 = 0.31433
    ak_opbouw_grens3_2025 = 39957 # Tot hier max opbouwdeel 2
    ak_opbouw_perc3_2025 = 0.02663
    ak_afbouw_start_2025 = 43071.00 # Vanaf hier afbouw van AK
    ak_afbouw_perc_2025 = 0.06510
    ak_afbouw_eind_2025 = 129078.00 # Ong. grens waar AK nul wordt. (Max / afbouw_perc + afbouw_start)

elif CALCULATION_YEAR == 2024:
    # ... (vorige 2024 waarden hier) ...
    self_employed_deduction_annual = 3750.00
    starters_deduction_annual = 2123.00
    mkb_profit_exemption_rate = 0.1331
    zvw_rate_freelancer = 0.0532
    zvw_max_income = 71628.00
    box1_schijf1_grens = 75518.00 # In 2024 was er effectief 1 schijf met 36.97% tot deze grens
    box1_schijf2_grens = float('inf') # Geen tweede 'midden' schijf
    # De functie berekent voor 2024 intern met 36.97% en 49.50%
    ahk_max = 3362.00
    ahk_afbouw_grens_start = 24813.00
    ahk_afbouw_grens_eind = 75518.00
    ahk_afbouw_percentage = 0.06632
    ak_max_2025 = 5532.00 # Dit was AK max 2024
    ak_opbouw_grens1_2025 = 11490 # 2024 waarden
    ak_opbouw_perc1_2025 = 0.08425
    ak_opbouw_grens2_2025 = 23201 # (was 24820 in eerdere code, 23201 is correcter voor 2024 AK max opbouw)
    ak_opbouw_perc2_2025 = 0.31433
    ak_opbouw_grens3_2025 = 37691
    ak_opbouw_perc3_2025 = 0.02663
    ak_afbouw_start_2025 = 37691 # Vanaf AK max bereikt wordt, start afbouw
    ak_afbouw_perc_2025 = 0.06510
    ak_afbouw_eind_2025 = 124934 # Was 115295, gecorrigeerd
else:
    raise ValueError("Calculation year not supported")

# Overige parameters (minder jaargevoelig, of nog niet aangepast voor 2025)
apply_entrepreneurial_deductions_input = True
desired_freelance_buffer_percentage_input = 0.10
freelance_aov_monthly_input = 132.67
freelance_pension_monthly_input = 400.00
freelance_other_costs_monthly_input = 115.00

employer_total_cost_factor = 1.32
holiday_pay_rate_employee = 0.08
employee_pension_contribution_percentage_input = 0.05 # Expliciete werknemerspensioenbijdrage
# NIEUW: Netto retentiegraad voor werknemer NA pensioenbijdrage, maar VOOR vakantiegeld impact
# Dit percentage dekt alleen loonheffing.
employee_net_retention_after_pension_for_salary_only = {
    2500: 0.75, # Bij <= 2500 bruto (na pensioen), blijft 75% netto over van dat deel
    4000: 0.68, # Bij <= 4000 bruto (na pensioen), blijft 68% netto over van dat deel
    float('inf'): 0.62 # Daarboven 62%
}
# Netto retentie op vakantiegeld (vaak zwaarder belast door minder heffingskortingen)
employee_net_retention_on_holiday_pay = 0.50 # Aanname: 50% van bruto vakantiegeld blijft netto


# --- BELASTINGFUNCTIES ---
def calculate_ib_and_pvv_box1(taxable_income_annual, year):
    if taxable_income_annual <= 0: return 0, 0, 0
    ib_amount, pvv_amount = 0, 0

    if year == 2025:
        sch1_grens = box1_schijf1_grens
        sch2_grens = box1_schijf2_grens
        
        # Tarieven 2025
        tarief_gecombineerd_sch1 = 0.3582
        tarief_gecombineerd_sch2 = 0.3748
        tarief_gecombineerd_sch3 = 0.4950

        # Splitsing IB/PVV voor schijf 1 (PVV alleen in schijf 1 voor niet-AOW)
        pvv_deel_sch1 = 0.2765
        ib_deel_sch1 = tarief_gecombineerd_sch1 - pvv_deel_sch1

        if taxable_income_annual <= sch1_grens:
            ib_amount = taxable_income_annual * ib_deel_sch1
            pvv_amount = taxable_income_annual * pvv_deel_sch1
        elif taxable_income_annual <= sch2_grens:
            ib_amount = (sch1_grens * ib_deel_sch1) + \
                        ((taxable_income_annual - sch1_grens) * tarief_gecombineerd_sch2) # Schijf 2 is puur IB tarief
            pvv_amount = sch1_grens * pvv_deel_sch1
        else: # schijf 3
            ib_amount = (sch1_grens * ib_deel_sch1) + \
                        ((sch2_grens - sch1_grens) * tarief_gecombineerd_sch2) + \
                        ((taxable_income_annual - sch2_grens) * tarief_gecombineerd_sch3)
            pvv_amount = sch1_grens * pvv_deel_sch1
            
    elif year == 2024:
        sch1_grens_2024 = 75518.00
        tarief_gecombineerd_sch1_2024 = 0.3697
        tarief_gecombineerd_sch2_2024 = 0.4950
        pvv_deel_sch1_2024 = 0.2765 # Aanname pvv deel
        ib_deel_sch1_2024 = tarief_gecombineerd_sch1_2024 - pvv_deel_sch1_2024

        if taxable_income_annual <= sch1_grens_2024:
            ib_amount = taxable_income_annual * ib_deel_sch1_2024
            pvv_amount = taxable_income_annual * pvv_deel_sch1_2024
        else:
            ib_amount = (sch1_grens_2024 * ib_deel_sch1_2024) + \
                        ((taxable_income_annual - sch1_grens_2024) * tarief_gecombineerd_sch2_2024)
            pvv_amount = sch1_grens_2024 * pvv_deel_sch1_2024
    else:
        raise ValueError(f"Year {year} not supported in IB/PVV calculation")
        
    return ib_amount, pvv_amount, ib_amount + pvv_amount

def calculate_zvw(profit_for_zvw_annual, year_zvw_rate, year_zvw_max_income):
    if profit_for_zvw_annual <= 0: return 0
    taxable_for_zvw = min(profit_for_zvw_annual, year_zvw_max_income)
    return taxable_for_zvw * year_zvw_rate

def calculate_general_tax_credit(taxable_income_for_calc_annual, year_ahk_max, year_ahk_afbouw_start, year_ahk_afbouw_perc):
    ahk = 0
    if taxable_income_for_calc_annual <= year_ahk_afbouw_start:
        ahk = year_ahk_max
    # De afbouw stopt als AHK 0 is. De eindgrens is waar max_ahk - (Eindgrens - Startgrens) * perc = 0
    # Eindgrens = Startgrens + max_ahk / perc
    # Voor 2025: 28406 + 3068 / 0.06337 = 28406 + 48414 = 76820
    # Dit komt dichtbij de 76817 (start 3e schijf), dus de afbouw loopt tot ongeveer daar.
    elif taxable_income_for_calc_annual < (year_ahk_afbouw_start + year_ahk_max / year_ahk_afbouw_perc) :
        ahk = year_ahk_max - year_ahk_afbouw_perc * (taxable_income_for_calc_annual - year_ahk_afbouw_start)
    else:
        ahk = 0 # Volledig afgebouwd
    return max(0, ahk)

def calculate_labor_tax_credit(labor_income_annual, year):
    # Deze functie moet worden bijgewerkt met de volledige schijven voor 2025
    # Voor nu, een vereenvoudiging gebaseerd op 2024 structuur met 2025 max.
    # Dit is een PUNT VAN VERBETERING voor exacte 2025 AK.
    if labor_income_annual <= 0: return 0
    ak = 0
    if year == 2025:
        # Vereenvoudigde AK 2025 - dit moet gedetailleerder voor accurate cijfers!
        # Gebruik van 2024 structuur met 2025 max als placeholder.
        max_ak = ak_max_2025
        g1, p1 = ak_opbouw_grens1_2025, ak_opbouw_perc1_2025
        g2, p2 = ak_opbouw_grens2_2025, ak_opbouw_perc2_2025 # max na opbouw 1
        g3, p3 = ak_opbouw_grens3_2025, ak_opbouw_perc3_2025 # max na opbouw 2
        g4_start, p4 = ak_afbouw_start_2025, ak_afbouw_perc_2025
        g4_eind = ak_afbouw_eind_2025
        
        val_opbouw1 = g1 * p1
        
        if labor_income_annual <= g1:
            ak = labor_income_annual * p1
        elif labor_income_annual <= g2:
            ak = val_opbouw1 + (labor_income_annual - g1) * p2
        elif labor_income_annual <= g3:
            val_opbouw2 = val_opbouw1 + (g2 - g1) * p2
            ak = val_opbouw2 + (labor_income_annual - g2) * p3
            ak = min(ak, max_ak) # Zorgen dat het niet over het maximum gaat in de opbouwfase
        elif labor_income_annual < g4_start: # Plateau op maximum
             ak = max_ak
        elif labor_income_annual <= g4_eind : # Afbouwfase
            ak = max_ak - (labor_income_annual - g4_start) * p4
        else: # Na afbouw
            ak = 0
        
    elif year == 2024:
        # (2024 AK logica zoals in vorige versie)
        max_ak = 5532.00
        g1, p1 = 11490, 0.08425
        g2, p2 = 23201, 0.31433 # Grens waar opbouw 1 maximaal is.
        g3, p3 = 37691, 0.02663 # Grens waar opbouw 2 maximaal is (AK Max bereikt)
        g4_start, p4 = 37691, 0.06510 # Start afbouw = waar AK max is
        g4_eind = 124934 # Grens waar AK 0 is
        
        val_opbouw1 = g1*p1 # 967.93
        
        if labor_income_annual <= g1:
            ak = labor_income_annual * p1
        elif labor_income_annual <= g2:
            ak = val_opbouw1 + (labor_income_annual - g1) * p2
        elif labor_income_annual < g3: # Plateau op maximum voor afbouw begint
            ak_voor_max = val_opbouw1 + (g2-g1)*p2 + (labor_income_annual - g2)*p3
            ak = min(ak_voor_max, max_ak)
        elif labor_income_annual <= g4_eind: # afbouwfase
            ak = max_ak - (labor_income_annual - g4_start) * p4
        else:
            ak = 0
    else:
        raise ValueError(f"Year {year} not supported for AK calculation")
    return max(0, ak)


def calculate_freelancer_finances(hourly_rate, hours_per_month, aov_monthly, pension_monthly, other_costs_monthly,
                                  apply_deductions, buffer_percentage, year):
    # Gebruik jaarspecifieke parameters
    year_self_employed_deduction = self_employed_deduction_annual
    year_starters_deduction = starters_deduction_annual
    year_mkb_exemption_rate = mkb_profit_exemption_rate
    year_zvw_rate = zvw_rate_freelancer
    year_zvw_max_income_val = zvw_max_income
    year_ahk_max_val = ahk_max
    year_ahk_afbouw_start_val = ahk_afbouw_grens_start
    year_ahk_afbouw_perc_val = ahk_afbouw_percentage
    
    gross_annual_revenue = hourly_rate * hours_per_month * 12
    total_direct_costs = (aov_monthly + pension_monthly + other_costs_monthly) * 12
    profit_before_fiscal = gross_annual_revenue - total_direct_costs

    entrepreneurial_deduction = 0
    if apply_deductions:
        deduction = year_self_employed_deduction + year_starters_deduction
        entrepreneurial_deduction = min(deduction, profit_before_fiscal if profit_before_fiscal > 0 else 0)
    profit_after_entrepreneurial = profit_before_fiscal - entrepreneurial_deduction

    mkb_exemption = 0
    if profit_after_entrepreneurial > 0:
        mkb_exemption = profit_after_entrepreneurial * year_mkb_exemption_rate
    
    taxable_profit_for_ib_pvv = profit_after_entrepreneurial - mkb_exemption
    profit_for_zvw = profit_after_entrepreneurial

    ib_comp, pvv_comp, total_ib_pvv_berekend = calculate_ib_and_pvv_box1(taxable_profit_for_ib_pvv, year)
    
    labor_income = profit_before_fiscal
    ahk_credit = calculate_general_tax_credit(taxable_profit_for_ib_pvv, year_ahk_max_val, year_ahk_afbouw_start_val, year_ahk_afbouw_perc_val)
    ak_credit = calculate_labor_tax_credit(labor_income, year)
    total_credits = ahk_credit + ak_credit

    payable_ib_pvv = max(0, total_ib_pvv_berekend - total_credits)
    zvw_payable = calculate_zvw(profit_for_zvw, year_zvw_rate, year_zvw_max_income_val)
    total_tax = payable_ib_pvv + zvw_payable

    net_income_before_buffer = profit_before_fiscal - total_tax
    
    buffer_amount = (profit_before_fiscal * buffer_percentage) if profit_before_fiscal > 0 else 0
    net_disposable_annual = net_income_before_buffer - buffer_amount
    net_disposable_monthly = net_disposable_annual / 12
    
    results = {
        "hourly_rate": hourly_rate,
        "net_disposable_monthly": net_disposable_monthly,
        "profit_before_fiscal_deductions_annual": profit_before_fiscal,
        "entrepreneurial_deduction_amount": entrepreneurial_deduction,
        "profit_after_entrepreneurial_deductions": profit_after_entrepreneurial,
        "mkb_exemption_amount": mkb_exemption,
        "taxable_profit_for_ib_pvv_calc_annual": taxable_profit_for_ib_pvv,
        "profit_for_zvw_annual": profit_for_zvw,
        "ib_component_gross": ib_comp,
        "pvv_component_gross": pvv_comp,
        "total_ib_pvv_gross": total_ib_pvv_berekend,
        "general_tax_credit": ahk_credit,
        "labor_tax_credit": ak_credit,
        "total_tax_credits": total_credits,
        "payable_ib_pvv_annual": payable_ib_pvv,
        "zvw_freelancer_annual": zvw_payable,
        "total_payable_tax_freelancer_annual": total_tax,
        "net_income_before_buffer_annual": net_income_before_buffer,
        "buffer_amount_annual": buffer_amount,
        "net_disposable_income_freelancer_annual": net_disposable_annual,
        "total_direct_costs_annual": total_direct_costs_annual
    }
    return results

# Functie om werknemersnetto te schatten (verfijnd)
def get_employee_net_monthly(gross_monthly_excl_holiday, hours_per_month_emp, pension_contrib_perc):
    if gross_monthly_excl_holiday <=0: return 0,0,0

    # 1. Werknemersdeel pensioen
    pension_contribution_monthly = gross_monthly_excl_holiday * pension_contrib_perc
    taxable_gross_monthly_for_lh = gross_monthly_excl_holiday - pension_contribution_monthly

    # 2. Bepaal netto retentiegraad op basis van belastbaar bruto voor loonheffing
    current_retention_rate_lh_only = 0
    sorted_retention_bands = sorted(employee_net_retention_after_pension_for_salary_only.keys())
    for band_limit in sorted_retention_bands:
        if taxable_gross_monthly_for_lh <= band_limit:
            current_retention_rate_lh_only = employee_net_retention_after_pension_for_salary_only[band_limit]
            break
    
    # 3. Netto van regulier maandsalaris (na pensioen, na loonheffing)
    net_from_regular_salary_monthly = taxable_gross_monthly_for_lh * current_retention_rate_lh_only
    
    # 4. Vakantiegeld
    gross_holiday_pay_monthly_accrual = gross_monthly_excl_holiday * holiday_pay_rate_employee
    net_from_holiday_pay_monthly_accrual = gross_holiday_pay_monthly_accrual * employee_net_retention_on_holiday_pay
    
    # 5. Totaal gemiddeld netto maandinkomen (incl. netto vakantiegeld opbouw)
    avg_net_monthly_total = net_from_regular_salary_monthly + net_from_holiday_pay_monthly_accrual
    
    return avg_net_monthly_total, gross_monthly_excl_holiday, pension_contribution_monthly


# --- LOGICA VOOR VERSCHILLENDE MODI ---

if calculation_mode == "rate_based":
    freelancer_results = calculate_freelancer_finances(
        freelance_hourly_rate_ex_vat_input, hours_per_month_input,
        freelance_aov_monthly_input, freelance_pension_monthly_input, freelance_other_costs_monthly_input,
        apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR
    )
    target_net_for_employee_scenario = freelancer_results["net_disposable_monthly"]
    # Scenario 1 voor werknemer (gelijk aan FL omzet) blijft relevant
    fl_gross_annual_revenue = freelance_hourly_rate_ex_vat_input * hours_per_month_input * 12
    s1_emp_total_cost_annual = fl_gross_annual_revenue
    s1_emp_gross_annual_incl_holiday = s1_emp_total_cost_annual / employer_total_cost_factor
    s1_emp_gross_monthly_excl_holiday = (s1_emp_gross_annual_incl_holiday / (1 + holiday_pay_rate_employee)) / 12
    s1_avg_net_monthly_emp, _, _ = get_employee_net_monthly(s1_emp_gross_monthly_excl_holiday, hours_per_month_input, employee_pension_contribution_percentage_input)


elif calculation_mode == "target_net_based":
    # Iteratief zoeken naar freelance uurtarief
    print(f"Zoeken naar freelance uurtarief voor doel netto p/m: €{target_net_disposable_monthly_income_input:.2f}")
    target_net = target_net_disposable_monthly_income_input
    # Start met een ruime schatting voor uurtarief
    # Een ruwe schatting: als netto 50% is van bruto omzet (na kosten etc.)
    # Bruto omzet p/m = Netto * 2 + Kosten_p/m
    # Uurtarief = (Netto * 2 + Kosten_p/m) / uren
    estimated_costs_pm = freelance_aov_monthly_input + freelance_pension_monthly_input + freelance_other_costs_monthly_input
    low_rate = 10.0
    high_rate = (target_net * 3 + estimated_costs_pm) / hours_per_month_input if hours_per_month_input > 0 else 200 # Ruime bovengrens
    high_rate = max(low_rate +1, high_rate) # Zorg dat high_rate > low_rate

    found_rate = low_rate # Default als niets gevonden wordt
    freelancer_results = {}

    for i in range(50): # Max 50 iteraties (binary search like)
        current_rate_guess = (low_rate + high_rate) / 2
        if current_rate_guess <=0 : current_rate_guess = 0.01 # Voorkom 0 of negatief tarief

        res_guess = calculate_freelancer_finances(
            current_rate_guess, hours_per_month_input,
            freelance_aov_monthly_input, freelance_pension_monthly_input, freelance_other_costs_monthly_input,
            apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR
        )
        current_net = res_guess["net_disposable_monthly"]
        
        # print(f"Iter {i}: Rate={current_rate_guess:.2f}, Net={current_net:.2f}, Target={target_net:.2f}, Low={low_rate:.2f}, High={high_rate:.2f}")

        if abs(current_net - target_net) < 0.50: # Tolerantie van 50 cent
            found_rate = current_rate_guess
            freelancer_results = res_guess
            break
        
        if current_net < target_net:
            low_rate = current_rate_guess
        else:
            high_rate = current_rate_guess
        
        if (high_rate - low_rate) < 0.01 : # Convergentie
             # Neem de beste van de laatste twee
            res_low = calculate_freelancer_finances(low_rate, hours_per_month_input, freelance_aov_monthly_input, freelance_pension_monthly_input, freelance_other_costs_monthly_input, apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR)
            res_high = calculate_freelancer_finances(high_rate, hours_per_month_input, freelance_aov_monthly_input, freelance_pension_monthly_input, freelance_other_costs_monthly_input, apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR)
            if abs(res_low["net_disposable_monthly"] - target_net) < abs(res_high["net_disposable_monthly"] - target_net):
                found_rate = low_rate
                freelancer_results = res_low
            else:
                found_rate = high_rate
                freelancer_results = res_high
            break
    else: # Als loop eindigt zonder break (geen exacte match binnen tolerantie)
        # Gebruik de laatst berekende 'found_rate' (die het dichtstbij was of de laatste gok)
        # Als freelancer_results leeg is, bereken met de 'found_rate' die het dichtst bij was
        if not freelancer_results:
             freelancer_results = calculate_freelancer_finances(
                found_rate, hours_per_month_input,
                freelance_aov_monthly_input, freelance_pension_monthly_input, freelance_other_costs_monthly_input,
                apply_entrepreneurial_deductions_input, desired_freelance_buffer_percentage_input, CALCULATION_YEAR
            )
        print(f"Iteratieve zoektocht voltooid. Dichtstbijzijnde freelance uurtarief: €{found_rate:.2f} voor netto €{freelancer_results.get('net_disposable_monthly',0):.2f}")
    
    target_net_for_employee_scenario = target_net_disposable_monthly_income_input
    # Scenario 1 werknemer (gelijk aan FL omzet o.b.v. GEVONDEN tarief)
    if freelancer_results:
        fl_gross_annual_revenue = freelancer_results["hourly_rate"] * hours_per_month_input * 12
        s1_emp_total_cost_annual = fl_gross_annual_revenue
        s1_emp_gross_annual_incl_holiday = s1_emp_total_cost_annual / employer_total_cost_factor
        s1_emp_gross_monthly_excl_holiday = (s1_emp_gross_annual_incl_holiday / (1 + holiday_pay_rate_employee)) / 12
        s1_avg_net_monthly_emp, _, _ = get_employee_net_monthly(s1_emp_gross_monthly_excl_holiday, hours_per_month_input, employee_pension_contribution_percentage_input)
    else: # Fallback als freelancer_results niet gevuld is
        s1_avg_net_monthly_emp = 0 
        s1_emp_gross_monthly_excl_holiday = 0


else:
    raise ValueError("Invalid calculation_mode selected.")


# Werknemer Scenario 2: Bruto salaris voor DOEL netto inkomen
# Iteratief zoeken naar bruto maandsalaris werknemer
s2_target_net_monthly = target_net_for_employee_scenario
s2_low_gross = 1000.0
s2_high_gross = (s2_target_net_monthly / 0.4) if s2_target_net_monthly > 0 else 5000.0 # Ruime bovengrens
s2_high_gross = max(s2_low_gross +100, s2_high_gross)
s2_found_gross_monthly_excl_holiday = 0
s2_avg_net_monthly_emp_check = 0
s2_pension_contrib_monthly_val = 0

if s2_target_net_monthly > 0:
    for i in range(30): # Max 30 iteraties
        s2_current_gross_guess = (s2_low_gross + s2_high_gross) / 2
        if s2_current_gross_guess <=0 : s2_current_gross_guess = 100 # Voorkom 0 of negatief
        
        s2_current_net_emp, _, s2_pension_val_temp = get_employee_net_monthly(s2_current_gross_guess, hours_per_month_input, employee_pension_contribution_percentage_input)

        if abs(s2_current_net_emp - s2_target_net_monthly) < 0.50: # Tolerantie
            s2_found_gross_monthly_excl_holiday = s2_current_gross_guess
            s2_avg_net_monthly_emp_check = s2_current_net_emp
            s2_pension_contrib_monthly_val = s2_pension_val_temp
            break
        
        if s2_current_net_emp < s2_target_net_monthly:
            s2_low_gross = s2_current_gross_guess
        else:
            s2_high_gross = s2_current_gross_guess
        
        if (s2_high_gross - s2_low_gross) < 0.01:
            # Kies de beste van de twee
            net_low,_, pen_low = get_employee_net_monthly(s2_low_gross, hours_per_month_input, employee_pension_contribution_percentage_input)
            net_high,_, pen_high = get_employee_net_monthly(s2_high_gross, hours_per_month_input, employee_pension_contribution_percentage_input)
            if abs(net_low - s2_target_net_monthly) < abs(net_high - s2_target_net_monthly):
                s2_found_gross_monthly_excl_holiday = s2_low_gross
                s2_avg_net_monthly_emp_check = net_low
                s2_pension_contrib_monthly_val = pen_low
            else:
                s2_found_gross_monthly_excl_holiday = s2_high_gross
                s2_avg_net_monthly_emp_check = net_high
                s2_pension_contrib_monthly_val = pen_high
            break
    else: # Geen exacte match
        s2_found_gross_monthly_excl_holiday = (s2_low_gross + s2_high_gross) / 2 # Neem de laatste gok
        s2_avg_net_monthly_emp_check, _, s2_pension_contrib_monthly_val = get_employee_net_monthly(s2_found_gross_monthly_excl_holiday, hours_per_month_input, employee_pension_contribution_percentage_input)
        print(f"Iteratieve zoektocht werknemer bruto salaris voltooid. Dichtstbijzijnde: Bruto €{s2_found_gross_monthly_excl_holiday:.2f} voor netto €{s2_avg_net_monthly_emp_check:.2f}")

if s2_found_gross_monthly_excl_holiday <0: s2_found_gross_monthly_excl_holiday = 0


# Afgeleide waarden voor werknemer scenario 2
s2_gross_annual_salary_incl_holiday = s2_found_gross_monthly_excl_holiday * (1 + holiday_pay_rate_employee) * 12
s2_total_employer_cost_annual = s2_gross_annual_salary_incl_holiday * employer_total_cost_factor
s2_total_employer_cost_monthly = s2_total_employer_cost_annual / 12
s2_equivalent_freelance_hourly_rate = s2_total_employer_cost_monthly / hours_per_month_input if hours_per_month_input > 0 else 0


# --- PRESENTATIE ---
# (Presentatie code hier, vergelijkbaar met vorige versie, maar gebruikmakend van de berekende 'freelancer_results')
# Dit deel wordt lang, dus ik focus op de belangrijkste output variabelen voor nu.
# ... (volledige presentatiecode zoals in v2.0, maar aangepast aan de nieuwe variabelen)

print(f"--- CALCULATOR VERSIE 3.0 (Jaar: {CALCULATION_YEAR}) ---")
print(f"--- Gekozen Modus: {calculation_mode} ---")

print("\n--- INPUTS OVERZICHT (Effectief gebruikt) ---")
inputs_data = {
    "Freelance Uurtarief (excl. BTW)": f"€ {freelancer_results.get('hourly_rate', freelance_hourly_rate_ex_vat_input):.2f}" if freelancer_results else f"€ {freelance_hourly_rate_ex_vat_input:.2f} (initieel, mode: {calculation_mode})",
    "Uren per maand": hours_per_month_input,
    "Doel Netto Maandinkomen (indien van toepassing)": f"€ {target_net_disposable_monthly_income_input:.2f}" if calculation_mode == "target_net_based" else "N.v.t.",
    "Freelance AOV/mnd": f"€ {freelance_aov_monthly_input:.2f}",
    "Freelance Pensioen/mnd": f"€ {freelance_pension_monthly_input:.2f}",
    "Freelance Overige Kosten/mnd": f"€ {freelance_other_costs_monthly_input:.2f}",
    "Zelfstandigen/Startersaftrek Actief": "Ja" if apply_entrepreneurial_deductions_input else "Nee",
    "Freelance Buffer % (van Winst v. Fiscale Aftrek)": f"{desired_freelance_buffer_percentage_input*100:.0f}%",
}
for key, value in inputs_data.items(): print(f"{key:<55} {value}")

if freelancer_results:
    print("\n--- FREELANCER FINANCIËN (Details) ---")
    freelancer_finance_data_display = {
        "Bruto Jaaromzet": freelancer_results["profit_before_fiscal_deductions_annual"] + total_direct_costs_annual, # Reconstructie omzet
        "Totale Directe Jaarkosten": total_direct_costs_annual,
        "WINST VOOR FISCALE AFTREKPOSTEN (WvF)": freelancer_results["profit_before_fiscal_deductions_annual"],
        "  Ondernemersaftrek (Zelfst.+Starter)": -freelancer_results["entrepreneurial_deduction_amount"] if apply_entrepreneurial_deductions_input else "N.v.t.",
        "Winst na Ondernemersaftrek": freelancer_results["profit_after_entrepreneurial_deductions"],
        "  MKB Winstvrijstelling ({:.2f}%)".format(mkb_profit_exemption_rate*100) : -freelancer_results["mkb_exemption_amount"],
        "Belastbare Winst voor IB/PVV (Grondslag)": freelancer_results["taxable_profit_for_ib_pvv_calc_annual"],
        "Grondslag ZVW (Winst na Ondernemersaftrek)": freelancer_results["profit_for_zvw_annual"],
        "BEREKENDE BELASTING/PREMIES (vóór heffingskortingen):": "",
        "  Inkomstenbelasting component (Box 1)": freelancer_results["ib_component_gross"],
        "  Premie Volksverzekeringen component": freelancer_results["pvv_component_gross"],
        "  Totaal IB/PVV (bruto)": freelancer_results["total_ib_pvv_gross"],
        "HEFFINGSKORTINGEN:": "",
        "  Algemene Heffingskorting": -freelancer_results["general_tax_credit"],
        "  Arbeidskorting": -freelancer_results["labor_tax_credit"],
        "  Totaal Heffingskortingen": -freelancer_results["total_tax_credits"],
        "DEFINITIEVE JAARLIJKSE BELASTINGPLICHT:": "",
        "  Te Betalen IB/PVV (na kortingen)": freelancer_results["payable_ib_pvv_annual"],
        "  Te Betalen ZVW-bijdrage": freelancer_results["zvw_freelancer_annual"],
        "  TOTALE JAARLIJKSE BELASTING/ZVW": freelancer_results["total_payable_tax_freelancer_annual"],
        "NETTO RESULTAAT FREELANCER:": "",
        "  Netto Inkomen (WvF - Totale Belasting, vóór buffer)": freelancer_results["net_income_before_buffer_annual"],
        "  Gereserveerde Buffer": -freelancer_results["buffer_amount_annual"],
        "NETTO BESTEEDBAAR INKOMEN (Jaar)": freelancer_results["net_disposable_income_freelancer_annual"],
        "NETTO BESTEEDBAAR INKOMEN (Gem. Maand)": freelancer_results["net_disposable_monthly"],
        "Netto Effectief Uurtarief (Gem. Maand)": (freelancer_results["net_disposable_monthly"] / hours_per_month_input) if hours_per_month_input > 0 else 0
    }
    for key, value in freelancer_finance_data_display.items():
        display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) else str(value)
        if key.startswith("  "): print(f"  {key:<53} {display_value}")
        elif value == "": print(f"\n{key}")
        else: print(f"{key:<55} {display_value}")
    print("\n*Let op: Totale Jaarlijkse Belasting/ZVW is de totale schuld voor het jaar, vóór verrekening van eventuele voorlopige aanslagen.\n")
else:
    print("\n--- FREELANCER FINANCIËN: Kon niet berekend worden (check modus/inputs) ---")


print(f"--- WERKNEMER SCENARIO 1: O.B.V. GELIJKE WERKGEVERSKOSTEN ALS FREELANCER BRUTO OMZET (€ {s1_emp_total_cost_annual/12:.2f}/mnd) ---")
employee_s1_data_display = {
    "Bruto Maandsalaris (excl. vakantiegeld)": s1_emp_gross_monthly_excl_holiday,
    "  Werknemersdeel Pensioen (geschat, {:.0f}%)".format(employee_pension_contribution_percentage_input*100): s1_emp_gross_monthly_excl_holiday * employee_pension_contribution_percentage_input,
    "  Belastbaar voor Loonheffing (na pensioen)": s1_emp_gross_monthly_excl_holiday * (1-employee_pension_contribution_percentage_input),
    "NETTO GEMIDDELD MAANDINKOMEN (geschat, incl. vak.geld)": s1_avg_net_monthly_emp
}
for key, value in employee_s1_data_display.items():
    display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) else str(value)
    print(f"{key:<55} {display_value}")
print("*Bruto-netto werknemer is een schatting. Gebruik externe tool voor precisie.\n")


print(f"--- WERKNEMER SCENARIO 2: STREVEN NAAR GELIJK NETTO MAANDINKOMEN (€ {target_net_for_employee_scenario:.2f}) ---")
employee_s2_data_display = {
    "Doel Netto Maandinkomen Werknemer": target_net_for_employee_scenario,
    "GESCHAT Bruto Maandsalaris (excl. vakantiegeld)": s2_found_gross_monthly_excl_holiday,
    "  Werknemersdeel Pensioen (geschat, {:.0f}%)".format(employee_pension_contribution_percentage_input*100): s2_pension_contrib_monthly_val,
    "  Belastbaar voor Loonheffing (na pensioen)": s2_found_gross_monthly_excl_holiday - s2_pension_contrib_monthly_val,
    "  Netto Maandinkomen Werknemer (check, geschat)": s2_avg_net_monthly_emp_check,
    "Totale Maandelijkse Kosten Werkgever voor dit salaris": s2_total_employer_cost_monthly,
    "EQUIVALENT FREELANCE UURTARIEF NODIG (voor deze werkgeverskosten)": s2_equivalent_freelance_hourly_rate
}
for key, value in employee_s2_data_display.items():
    display_value = f"€ {value:.2f}" if isinstance(value, (int, float)) else str(value)
    print(f"{key:<55} {display_value}")
print("*Bruto-netto werknemer is een schatting. Gebruik externe tool voor precisie.\n")

print("--- SAMENVATTENDE VERGELIJKING FOCUS OP SCENARIO 2 (als doel netto is ingesteld) ---")
if calculation_mode == "target_net_based" and freelancer_results:
    summary_data = {
        "Indicator": ["Freelancer (voor doel netto)", "Werknemer (voor doel netto)"],
        "Netto Besteedbaar Maandinkomen (Doel)": [f"€ {freelancer_results['net_disposable_monthly']:.2f}", f"€ {s2_avg_net_monthly_emp_check:.2f}"],
        "Freelance Uurtarief / Equivalent": [f"€ {freelancer_results['hourly_rate']:.2f}", f"€ {s2_equivalent_freelance_hourly_rate:.2f} (equiv. WG kosten)"],
        "Bruto Maandsalaris WN (excl. vak) / FL Omzet p.m.": [f"€ {(freelancer_results['profit_before_fiscal_deductions_annual'] + total_direct_costs_annual)/12:.2f} (Omzet p.m.)", f"€ {s2_found_gross_monthly_excl_holiday:.2f}"]
    }
    df_summary = pd.DataFrame(summary_data)
    print(df_summary.to_string(index=False))
elif calculation_mode == "rate_based" and freelancer_results:
     summary_data = {
        "Indicator": ["Freelancer (op basis van uurtarief)", "Werknemer (equiv. netto als FL)"],
        "Netto Besteedbaar Maandinkomen": [f"€ {freelancer_results['net_disposable_monthly']:.2f}", f"€ {s2_avg_net_monthly_emp_check:.2f} (streeft naar FL netto)"],
        "Freelance Uurtarief / Equivalent": [f"€ {freelancer_results['hourly_rate']:.2f}", f"€ {s2_equivalent_freelance_hourly_rate:.2f} (equiv. WG kosten)"],
         "Bruto Maandsalaris WN (excl. vak) / FL Omzet p.m.": [f"€ {(freelancer_results['profit_before_fiscal_deductions_annual'] + total_direct_costs_annual)/12:.2f} (Omzet p.m.)", f"€ {s2_found_gross_monthly_excl_holiday:.2f}"]
    }
     df_summary = pd.DataFrame(summary_data)
     print(df_summary.to_string(index=False))

print("\nDisclaimer: Dit is een modelberekening. Werkelijke fiscale situaties en netto inkomens kunnen afwijken.")
print(f"Cijfers gebruikt voor jaar: {CALCULATION_YEAR}. Exacte AK 2025 schijven nog te verfijnen. Retentiegraad werknemer is schatting.")