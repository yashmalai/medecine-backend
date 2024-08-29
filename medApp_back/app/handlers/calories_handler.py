def calculate(MET, workout_time):
    man = [175, 75, 25] # рост, вес, возраст
    calories = man[1] * (workout_time/60) * MET
    return calories


def calc_calories(workout_type, workout_subtype, workout_time):
    match workout_type:
        case "Бег":
            match workout_subtype:
                case "Бег на дистанцию": calories = calculate(MET=8, workout_time=workout_time)
                case "Кросс": calories = calculate(MET=12, workout_time=workout_time)
                case "Спортивный бег": calories = calculate(MET=15, workout_time=workout_time)
        case "Плавание":
            match workout_subtype:
                case "Баттерфляй": calories = calculate(MET=9, workout_time=workout_time)
                case "Брасс": calories = calculate(MET=7, workout_time=workout_time)
                case "На спине": calories = calculate(MET=6, workout_time=workout_time)
        case "Единоборства":
            match workout_subtype:
                case "Бокс": calories = calculate(MET=9, workout_time=workout_time)
                case "Кик-бокс": calories = calculate(MET=9, workout_time=workout_time)
                case "ММА": calories = calculate(MET=10, workout_time=workout_time)

    return calories