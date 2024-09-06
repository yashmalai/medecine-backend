import datetime
import profile
import sys
import requests
import re
import math
from main import clrterm
from handlers import calc_schedule
from handlers import calc_total_doses
from beautifultable import BeautifulTable
from colorama import Fore
import main


def medicines_check():
    userid = main.user_data.get('id')
    medcheck_data = {
        "user_id": userid,
        "med_status": 'active'
    }
    resp_get_meds = requests.get(f'{main.BASE_URL}/medicine', params=medcheck_data)
    resp_get_meds_json = resp_get_meds.json()
    medchecklist = []
    for med in resp_get_meds_json:
        if datetime.date.today().strftime("%Y-%m-%d") in list(med.get('schedule_times').split(",")):
            medcheckdict = {
                "name": med.get('name'),
                "drug_type": med.get('drug_type'),
                "intake_time": med.get('intake_time'),
                "intake_rule": med.get('intake_rule'),
                "dose": med.get('dose')
            }
            medchecklist.append(medcheckdict)
    return medchecklist


def medicines_main():
    clrterm()
    med_check_list = medicines_check()
    if len(med_check_list) != 0:
        for med in med_check_list:
            print(Fore.YELLOW + f"Не забудьте принять лекарство - {med.get('name')}({med.get('drug_type')})"
                  f" - Сегодня в {med.get('intake_time')} - {med.get('dose')}шт/мл/мг/мин {med.get('intake_rule')}\n")
    meds_select = input(Fore.WHITE + '1 - Добавить новое лекарство, 2 - Активные лекарства, '
                        '3 - Предстоящие лекарства, 4 - Архив, 5 - На главную, 6 - Выход\n')
    match meds_select:
        case '1':
            medicines_create()
        case '2':
            medicines_show_meds(med_stat='active')
        case '3':
            medicines_show_meds(med_stat='ongoing')
        case '4':
            medicines_show_meds(med_stat='completed')
        case '5':
            profile.profile_main()
        case '6':
            sys.exit(0)
        case _:
            print('Некорректный ввод, попробуйте снова\n')
            medicines_main()


def medicines_create():
    clrterm()
    meds_type_select = input(Fore.WHITE + 'Выберите тип лекарства: 1 - Таблетки, 2 - Капсулы,'
                                          ' 3 - Капли, 4 - Уколы, 5 - Процедуры\n')
    match meds_type_select:
        case '1':
            meds_type = 'Таблетки'
        case '2':
            meds_type = 'Капсулы'
        case '3':
            meds_type = 'Капли'
        case '4':
            meds_type = 'Уколы'
        case '5':
            meds_type = 'Процедуры'
        case _:
            print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
            medicines_create()
    meds_name = input('Название:\n')
    meds_dose = input('Дозировка(шт/мл/мг/мин):\n')
    if not re.match("^[0-9]*$", meds_dose):
        print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
        medicines_create()
    meds_intaketime_num = input('Кол-во приемов в день:\n')
    if not re.match("^[0-9]*$", meds_intaketime_num):
        print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
        medicines_create()
    meds_intaketime_arr = []
    for n in range(int(meds_intaketime_num)):
        meds_sometime = input(f'Время приема №{n + 1}:\n')
        meds_intaketime_arr.insert(n, meds_sometime)
    meds_intake_time = ','.join([str(rule) for rule in meds_intaketime_arr])
    meds_intake_rule_select = input('Введите правило приема(1 - До еды, 2 - После еды, 3 - Во время еды)\n')
    match meds_intake_rule_select:
        case '1':
            meds_intake_rule = 'До еды'
        case '2':
            meds_intake_rule = 'После еды'
        case '3':
            meds_intake_rule = 'Во время еды'
        case _:
            print(Fore.RED + 'Некорректный ввод, попробуйте снова \n')
            medicines_create()
    meds_start_date_str = input('Дата начала приема(дд/мм/гггг):\n')
    meds_end_date_str = input('Дата окончания приема(дд/мм/гггг):\n')
    try:
        meds_start_date = datetime.datetime.strptime(meds_start_date_str, '%d/%m/%Y').date()
        meds_end_date = datetime.datetime.strptime(meds_end_date_str, '%d/%m/%Y').date()
    except(TypeError, ValueError, IndexError):
        print(Fore.RED + 'Некорректный ввод, попробуйте снова \n')
        medicines_create()
    if meds_start_date > meds_end_date:
        print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
        medicines_create()
    meds_schedule_times_select = input('1 - Каждый день, 2 - Через день, 3 - Другое\n')
    match meds_schedule_times_select:
        case '1':
            sch_type = 'everyday'
            meds_schedule_times_arr = calc_schedule.calc_schedule(meds_start_date, meds_end_date, sch_type)
        case '2':
            sch_type = 'skip_day'
            meds_schedule_times_arr = calc_schedule.calc_schedule(meds_start_date, meds_end_date, sch_type)
        case '3':
            sch_type = 'other'
            meds_schedule_times_arr = calc_schedule.calc_schedule(meds_start_date, meds_end_date, sch_type)
        case _:
            print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
            medicines_create()
    meds_schedule_times = ','.join([str(sch) for sch in meds_schedule_times_arr])
    meds_comment = input('Комментарий(необязательно):\n')
    meds_total_doses = calc_total_doses.calc_total(meds_dose, meds_intake_time, meds_schedule_times)
    if meds_start_date > datetime.date.today():
        meds_status = 'ongoing'
    elif meds_start_date == datetime.date.today():
        meds_status = 'active'
    else:
        print(Fore.RED + 'Некорректный ввод даты начала/окончания курса(прием лекарств уже начался)\n')
        medicines_create()
    meds_data = {
        "user_id": main.user_data.get('id'),
        "name": meds_name,
        "drug_type": meds_type,
        "dose": meds_dose,
        "intake_rule": meds_intake_rule,
        "intake_time": meds_intake_time,
        "start_date": meds_start_date_str,
        "end_date": meds_end_date_str,
        "schedule_times": meds_schedule_times,
        "comment": meds_comment,
        "total_doses": meds_total_doses,
        "med_status": meds_status
    }
    resp_med_create = requests.post(f'{main.BASE_URL}/medicine', json=meds_data)
    if resp_med_create.status_code == 201:
        print(Fore.GREEN + "Лекарство успешно добавлено\n")
        medicines_main()
    else:
        print(Fore.RED + "Ошибка при добавлении лекарства\n")
        medicines_main()


def medicines_take_meds(medid, doses, total):
    clrterm()
    takemeds_select = input('Введите кол-во принятых лекарств:\n')
    if not re.match("^[0-9]*$", takemeds_select):
        print(Fore.RED + 'Некорректный ввод, попробуйте снова\n')
        medicines_take_meds(medid, doses, total)
    takemeds_fin = int(takemeds_select) + doses
    if takemeds_fin > total:
        print(Fore.RED + 'Некорректный ввод (принято > общего кол-ва)\n')
        medicines_take_meds(medid, doses, total)
    takemeds_data = {
        "id": medid,
        "doses_taken": takemeds_fin
    }
    resp_takemeds = requests.post(f'{main.BASE_URL}/medicine/takemeds', params=takemeds_data)
    if resp_takemeds.status_code == 201:
        print(Fore.GREEN + "Лекарство успешно принято\n")
        medicines_main()
    else:
        print(Fore.RED + "Ошибка при изменении лекарства\n")
        medicines_main()


def medicines_show_meds(med_stat):
    clrterm()
    meds_table = BeautifulTable()
    get_meds_data = {
        "user_id": main.user_data.get('id'),
        "med_status": med_stat
    }
    resp_get_meds = requests.get(f'{main.BASE_URL}/medicine', params=get_meds_data)
    resp_get_meds_json = resp_get_meds.json()
    for med in resp_get_meds_json:
        meds_table.rows.append([med.get('name'), med.get('start_date'), med.get('end_date'),
                                f"{med.get('doses_taken')} из {med.get('total_doses')}"])
    medtemplist = []
    for n in range(len(resp_get_meds_json)):
        medtemplist.append(Fore.GREEN + f'{n + 1}')
    meds_table.rows.header = medtemplist
    meds_table.columns.header = [Fore.YELLOW + "Название", Fore.YELLOW + "Дата начала", Fore.YELLOW + "Дата окончания",
                                 Fore.YELLOW + "Лекарств принято/осталось"]
    print(meds_table, "\n")
    show_meds_select = input(Fore.WHITE + 'Выберите лекарство(по номеру в таблице), "назад" для выхода:\n')
    match show_meds_select:
        case 'назад':
            medicines_main()
        case _:
            try:
                clrterm()
                print(f"{resp_get_meds_json[int(show_meds_select)-1].get('name')}"
                      f"({resp_get_meds_json[int(show_meds_select)-1].get('drug_type')})\n")
                print(f"Правило приема: {resp_get_meds_json[int(show_meds_select)-1].get('dose')}"
                      f" шт/мл/мг/мин {resp_get_meds_json[int(show_meds_select)-1].get('intake_rule')}"
                      f" в {resp_get_meds_json[int(show_meds_select)-1].get('intake_time')}\n")
                med_progress_bar = []
                current_med_int = int(resp_get_meds_json[int(show_meds_select)-1].get('doses_taken'))
                total_med_int = int(resp_get_meds_json[int(show_meds_select)-1].get('total_doses'))
                if current_med_int == 0:
                    current_len_raw = 0
                else:
                    current_len_raw = math.ceil(50/(total_med_int/current_med_int))
                for n in range(current_len_raw):
                    med_progress_bar.append(Fore.GREEN + '█')
                for i in range(50 - current_len_raw):
                    med_progress_bar.append(Fore.WHITE + '-')
                m_p_bar_str = ''.join(med_progress_bar)
                print(f"| {m_p_bar_str} ", Fore.WHITE + f"| {current_med_int} из {total_med_int} принято\n")
                print(f"Дата начала - окончания приема:{resp_get_meds_json[int(show_meds_select)-1].get('start_date')}"
                      f" - {resp_get_meds_json[int(show_meds_select)-1].get('end_date')}\n")
                print(f"Комментарии к приему:{resp_get_meds_json[int(show_meds_select)-1].get('comment')}\n")
                match med_stat:
                    case 'active':
                        show_actions_select = input('1 - Принять лекарство, 2 - Назад, 3 - В главное меню\n')
                        match show_actions_select:
                            case '1':
                                medicines_take_meds(resp_get_meds_json[int(show_meds_select)-1].get('id'),
                                                    resp_get_meds_json[int(show_meds_select)-1].get('doses_taken'),
                                                    resp_get_meds_json[int(show_meds_select)-1].get('total_doses'))
                            case '2':
                                meds_stat = med_stat
                                medicines_show_meds(meds_stat)
                            case '3':
                                medicines_main()
                            case _:
                                print('Некорректный ввод\n')
                                meds_stat = med_stat
                                medicines_show_meds(meds_stat)
                    case 'ongoing' | 'completed':
                        show_actions_select = input('1 - Назад, 2 - В главное меню\n')
                        match show_actions_select:
                            case '1':
                                meds_stat = med_stat
                                medicines_show_meds(meds_stat)
                            case '2':
                                medicines_main()
                            case _:
                                print('Некорректный ввод\n')
                                meds_stat = med_stat
                                medicines_show_meds(meds_stat)

            except(TypeError, ValueError, IndexError):
                print('Ошибка ввода, попробуйте снова')
                meds_stat = med_stat
                medicines_show_meds(meds_stat)


