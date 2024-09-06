import plotext as plt
import requests
import main


def show_2dgraph():
    tr_data = {
        "user_id": main.user_data.get("id")
    }
    response = requests.get(f"{main.BASE_URL}/training", params=tr_data)
    data = response.json()
    training_ids = [d['id'] for d in data]
    durations = [d['workout_time'] for d in data]
    calories = [d['calories'] for d in data]
    plt.clear_data()
    plt.plot(training_ids, durations, label="Duration")
    plt.plot(training_ids, calories, label="Calories")
    plt.xticks(ticks=training_ids, labels=[str(id) for id in training_ids])
    plt.title("Тренировки")
    plt.xlabel("ID тренировки")
    plt.ylabel("Значения")
    plt.theme('pro')
    plt.show()
