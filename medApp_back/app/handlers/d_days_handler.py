
def calculate_drug_days(**kwargs):
    dose_raw = kwargs.get('dose')
    dose = int(dose_raw)
    schedule = kwargs.get('schedule')
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    days_total_raw = (end_date - start_date).days  # количество дней приема
    days_total = int(days_total_raw)
    doses_per_day = len(schedule.split(','))
    doses_per_day = dose * doses_per_day  # сколько таблеток в день

    total_doses = days_total * doses_per_day  # сколько надо пить таблеток всего
    return total_doses
