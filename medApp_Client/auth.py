import requests
import profile
import sys
from main import clrterm
from datetime import datetime
import main


def auth_page():
    clrterm()
    auth_select = input('1 - логин, 2 - регистрация, 3 - выход\n')
    match auth_select:
        case '1':
            auth_login()
        case '2':
            auth_register()
        case '3':
            sys.exit(0)
        case _:
            print('Некорректный ввод, попробуйте снова\n')
            auth_page()


def auth_login():
    clrterm()
    name = input('имя\n')
    password = input('пароль\n')
    auth_data = {
        "name": name,
        "password": password
    }
    resp_auth = requests.post(f'{main.BASE_URL}/login', json=auth_data)
    if resp_auth.status_code == 200:
        print("Login success\n")
        profile.profile_auth(name)
    else:
        print("Failed to login\n")
        auth_page()


def auth_register():
    clrterm()
    name = input('имя\n')
    password = input('пароль\n')
    age = input('возраст\n')
    weight = input('вес\n')
    height = input('рост\n')
    cur_date = datetime.now()
    auth_reg_data = {
        "name": name,
        "password": password,
        "age": age,
        "weight": weight,
        "height": height,
        "created_at": str(f'{cur_date.year}-{cur_date.month}-{cur_date.day}')
    }
    resp_register = requests.post(f'{main.BASE_URL}/register', json=auth_reg_data)
    if resp_register.status_code == 201:
        print("Register success\n")
        profile.profile_auth(name)
    else:
        print("Failed to register\n")
        auth_page()

