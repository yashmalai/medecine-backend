import profile
import sys
import time
import requests
from main import clrterm
from datetime import datetime
from beautifultable import BeautifulTable
from colorama import Fore
from handlers import wireframe, plotext_graph
import main


def trainings_main():
    clrterm()
    meds_select = input(
        Fore.CYAN + '1 - Добавить новую тренировку\n2 - Статистика тренировок\n'
                    '3 - На главную\n4 - Выход\n> ')
    match meds_select:
        case '1':
            trainings_create()
        case '2':
            statistics()
        case '3':
            profile.profile_main()
        case '4':
            sys.exit(0)
        case _:
            print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
            trainings_main()


def trainings_create():
    clrterm()
    training_name = input(Fore.CYAN + 'Введите название тренировки: ')
    meds_type_select = input('Выберите тип тренировки:\n1 - Бег\n2 - Плавание\n3 - Единоборства\n>')
    match meds_type_select:
        case '1':
            trainings_type = 'Бег'
            training_subtype_select = input(
                'Выберите подтип тренировки:\n1 - Бег на дистанцию\n2 - Кросс\n3 - Спортивный бег\n>')
            match training_subtype_select:
                case "1":
                    training_subtype = 'Бег на дистанцию'
                case "2":
                    training_subtype = 'Кросс'
                case "3":
                    training_subtype = 'Спортивный бег'
                case _:
                    print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
                    trainings_create()
        case '2':
            trainings_type = 'Плавание'
            training_subtype_select = input('Выберите подтип тренировки:\n1 - Батерфляй\n2 - Брасс\n3 - На спине\n>')
            match training_subtype_select:
                case "1":
                    training_subtype = 'Баттерфляй'
                case "2":
                    training_subtype = 'Брасс'
                case "3":
                    training_subtype = 'На спине'
                case _:
                    print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
                    trainings_create()
        case '3':
            trainings_type = 'Единоборства'
            training_subtype_select = input('Выберите подтип тренировки:\n1 - Бокс\n2 - Кикбоксинг\n3 - ММА\n>')
            match training_subtype_select:
                case "1":
                    training_subtype = 'Бокс'
                case "2":
                    training_subtype = 'Кикбоксинг'
                case "3":
                    training_subtype = 'ММА'
                case _:
                    print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
                    trainings_create()
        case _:
            print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
            trainings_create()
    duration = input('Введите длительность тренировки в минутах: ')
    animated_timer(int(duration))
    data = {
        'name': training_name,
        'user_id': main.user_data.get('id'),
        'workout_type': trainings_type,
        'workout_subtype': training_subtype,
        'workout_date': datetime.now().strftime('%Y-%m-%d'),
        'workout_time': duration,
        'weight': main.user_data.get('weight')
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        response = requests.post(f"{main.BASE_URL}/training", headers=headers, json=data)
        if response.status_code == 201:
            print(Fore.GREEN + "Тренировка проведена!")
            trainings_main()
    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + f"HTTP ошибка: {http_err}")
        trainings_main()
    except Exception as err:
        print(Fore.RED + f"Другая ошибка: {err}")
        trainings_main()


def statistics():
    try:
        trainings_data = {
            "user_id": main.user_data.get('id')
        }
        response = requests.get(f'{main.BASE_URL}/training', params=trainings_data)
        response.raise_for_status()
        training_resp = response.json()
        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
        table.columns.header = ["Название", "Тип", "Подтип", "Длительность", "Калории"]
        for training in training_resp:
            table.rows.append([
                training.get("name"),
                training.get("workout_type"),
                training.get("workout_subtype"),
                training.get("workout_time"),
                training.get("calories")
            ])
        trtemplist = []
        for n in range(len(training_resp)):
            trtemplist.append(f'{n + 1}')
        table.rows.header = trtemplist
        print(table)
        statistics_select = input('1 - График(2д), 2 - График(3д), 3 - Удалить тренировку, 4 - Назад\n')
        match statistics_select:
            case '1':
                plotext_graph.show_2dgraph()
                statistics()
            case '2':
                wireframe.show_wireframe()
                statistics()
            case '3':
                delete_tr_select = input('Введите номер тренировки для удаления\n')
                try:
                    delete_training(training_resp[int(delete_tr_select)-1].get('id'))
                except Exception as err:
                    print(f"Ошибка: {err}")
                    trainings_main()
            case '4':
                trainings_main()
            case _:
                print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
                statistics()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Другая ошибка: {err}")


def delete_training(training_id):
    try:
        response = requests.delete(f"{main.BASE_URL}/training/{int(training_id)}")
        if response.status_code == 204:
            print(Fore.GREEN + "Тренировка удалена!")
            trainings_main()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
        trainings_main()
    except Exception as err:
        print(f"Другая ошибка: {err}")
        trainings_main()


def timefuncdecor(func):
    def calctime(*ar):
        starttime = time.time()
        func(*ar)
        print(Fore.RED + f'Время выполнения: {time.time() - starttime}')
    return calctime


@timefuncdecor
def animated_timer(duration):
    duration *= 60
    start_time = time.time()
    end_time = start_time + duration
    animation_frames = ['—', '\\', '|', '/']
    frame_index = 0

    while time.time() < end_time:
        elapsed_time = int(time.time() - start_time)
        remaining_time = duration - elapsed_time
        hours = remaining_time // 3600
        minutes = remaining_time // 60
        seconds = remaining_time % 60

        sys.stdout.write(
            Fore.GREEN + f'\rТаймер: {hours:02d}:{minutes:02d}:{seconds:02d} {animation_frames[frame_index]}')
        sys.stdout.flush()

        time.sleep(0.25)
        frame_index = (frame_index + 1) % len(animation_frames)
