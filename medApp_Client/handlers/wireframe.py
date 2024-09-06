import numpy as np
import matplotlib.pyplot as plt
import requests
import main


def show_wireframe():
    tr_data = {
        "user_id": main.user_data.get("id")
    }
    response = requests.get(f"{main.BASE_URL}/training", params=tr_data)
    data = response.json()
    workout_ids = np.array([entry['id'] for entry in data])
    durations = np.array([entry['workout_time'] for entry in data])
    calories = np.array([entry['calories'] for entry in data])
    workout_ids_grid, durations_grid = np.meshgrid(workout_ids, durations)
    calories_grid = np.interp(workout_ids_grid, workout_ids, calories)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(workout_ids_grid, durations_grid, calories_grid, color='blue')
    ax.set_xlabel('ID тренировки')
    ax.set_ylabel('Длительность (мин)')
    ax.set_zlabel('Калории')
    plt.show()
