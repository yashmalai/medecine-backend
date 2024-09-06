
def calculate_drug_days(doses):
    dose_raw = doses.get('dose')
    dose = int(dose_raw)
    intake_time = doses.get('intake_time')
    start_date = doses.get('start_date')
    end_date = doses.get('end_date')

    days_total_raw = (end_date - start_date).days  # количество дней приема
    days_total = int(days_total_raw)
    doses_per_day = len(intake_time.split(','))
    doses_per_day = dose * doses_per_day  # сколько таблеток в день

    total_doses = days_total * doses_per_day  # сколько надо пить таблеток всего
    return total_doses
