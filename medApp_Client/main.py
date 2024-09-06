import auth
import os

user_data = {
        "id": None,
        "name": None,
        "age": None,
        "weight": None,
        "height": None
    }
BASE_URL = 'http://127.0.0.1:5000'


def clrterm():
    os.system('cls')


if __name__ == '__main__':
    auth.auth_page()
