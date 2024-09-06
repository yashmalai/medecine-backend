def calculate(MET, workout_time, weight):
    calories = int(weight) * (int(workout_time)/60) * MET
    return calories


def calc_calories(workout_type, workout_subtype, workout_time, weight):
    match workout_type:
        case "Бег":
            match workout_subtype:
                case "Бег на дистанцию": calories = calculate(MET=8, workout_time=workout_time, weight=weight)
                case "Кросс": calories = calculate(MET=12, workout_time=workout_time, weight=weight)
                case "Спортивный бег": calories = calculate(MET=15, workout_time=workout_time, weight=weight)
        case "Плавание":
            match workout_subtype:
                case "Баттерфляй": calories = calculate(MET=9, workout_time=workout_time, weight=weight)
                case "Брасс": calories = calculate(MET=7, workout_time=workout_time, weight=weight)
                case "На спине": calories = calculate(MET=6, workout_time=workout_time, weight=weight)
        case "Единоборства":
            match workout_subtype:
                case "Бокс": calories = calculate(MET=9, workout_time=workout_time, weight=weight)
                case "Кикбоксинг": calories = calculate(MET=9, workout_time=workout_time, weight=weight)
                case "ММА": calories = calculate(MET=10, workout_time=workout_time, weight=weight)

    return calories