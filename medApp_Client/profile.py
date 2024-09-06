import requests
import sys
import medicines
import trainings
import auth
from main import clrterm
from colorama import Fore
import main


def profile_auth(name):
    current_username = {"name": name}
    resp_profile = requests.get(f'{main.BASE_URL}/user', params=current_username)
    main.user_data = {
        "id": resp_profile.json().get('id'),
        "name": resp_profile.json().get('name'),
        "age": resp_profile.json().get('age'),
        "weight": resp_profile.json().get('weight'),
        "height": resp_profile.json().get('height'),
    }
    profile_main()


def profile_main():
    clrterm()
    profile_select = input(Fore.WHITE + '1 - Лекарства, 2 - Тренировки, 3 - Выход, 4 - Выйти из профиля, 5 - Удалить профиль\n')
    match profile_select:
        case '1':
            medicines.medicines_main()
        case '2':
            trainings.trainings_main()
        case '3':
            sys.exit(0)
        case '4':
            profile_logout()
        case '5':
            p_select_aware = input('Введите "я понимаю что делаю" чтобы удалить профиль \n')
            match p_select_aware:
                case 'я понимаю что делаю':
                    profile_delete()
                case _:
                    print('Некорректный ввод\n')
                    profile_main()
        case _:
            print('Некорректный ввод, попробуйте снова\n')
            profile_main()


def profile_delete():
    resp_delete = requests.delete(f'{main.BASE_URL}/delete_user/{main.user_data.get("id")}')
    if resp_delete.status_code == 200:
        print("User deleted successfully\n")
        user_data = main.user_data.fromkeys(main.user_data, None)
        print(user_data, '\n')
        auth.auth_page()
    else:
        print("Failed to delete user\n")
        profile_main()


def profile_logout():
    user_data = main.user_data.fromkeys(main.user_data, None)
    print(user_data, '\n')
    auth.auth_page()
