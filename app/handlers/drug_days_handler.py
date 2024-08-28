from datetime import datetime

def calculate_drug_days(**kwargs):
    dose = kwargs.get('dose')
    schedule = kwargs.get('schedule')
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    days_total = (end_date - start_date).days + 1 # количество дней приема
    
    doses_per_day = len(schedule.split(',')) 
    doses_per_day = dose * doses_per_day # сколько таблеток в день
    
    total_doses = days_total * doses_per_day # сколько надо пить таблеток всего
    return total_doses
        
