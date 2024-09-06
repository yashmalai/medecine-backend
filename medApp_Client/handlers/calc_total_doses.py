def calc_total(dose, day, total):
    day_num = len(day.split(','))
    total_num = len(total.split(','))
    total_doses = int(dose)*day_num*total_num
    return total_doses
