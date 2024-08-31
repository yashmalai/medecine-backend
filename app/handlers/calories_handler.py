

# TODO добавить значения из класса юзер(из профиля)
def calculate(MET, duration):
    man = [175, 75, 25] # рост, вес, возраст
    calories = man[1] * (duration/60) * MET
    return calories

def calc_calories(workout_type, workout_subtype, duration):
    match workout_type:
        case "running":
            match workout_subtype:
                case "distance_run": calories = calculate(MET=8, duration=duration)
                case "cross": calories = calculate(MET=12, duration=duration)
                case "sport_run": calories = calculate(MET=15, duration=duration)
        case "swimming":
            match workout_subtype:
                case "butterfly": calories = calculate(MET=9, duration=duration)
                case "brass": calories = calculate(MET=7, duration=duration)
                case "on_back": calories = calculate(MET=6, duration=duration)
        case "fighting":
            match workout_subtype:
                case "boxing": calories = calculate(MET=9, duration=duration)
                case "kikboxing": calories = calculate(MET=9, duration=duration)
                case "MMA": calories = calculate(MET=10, duration=duration)

    return calories