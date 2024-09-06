from datetime import timedelta
from main import clrterm


def calc_delta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta


def calc_schedule(startdate, enddate, sch_type):
    sch_arr = []
    match sch_type:
        case 'everyday':
            for result in calc_delta(startdate, enddate, timedelta(days=1)):
                sch_arr.append(result.strftime('%Y-%m-%d'))
            return sch_arr
        case 'skip_day':
            for result in calc_delta(startdate, enddate, timedelta(days=2)):
                sch_arr.append(result.strftime('%Y-%m-%d'))
            return sch_arr
        case 'other':
            sch_arr_select = []
            for result in calc_delta(startdate, enddate, timedelta(days=1)):
                sch_arr_select.append(result)
            while len(sch_arr_select) != 0:
                clrterm()
                for n in range(len(sch_arr_select)):
                    print(f'{n+1} -', sch_arr_select[n])
                sch_choice = input('Введите номер даты, "стоп" чтобы закончить выбор')
                match sch_choice:
                    case 'стоп':
                        break
                    case _:
                        try:
                            sch_arr.append(sch_arr_select[int(sch_choice)-1].strftime('%Y-%m-%d'))
                            sch_arr_select.pop(int(sch_choice)-1)
                        except (TypeError, ValueError, IndexError):
                            continue
            return sch_arr



