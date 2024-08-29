import npyscreen
import requests
import json
import main
import tr_plot


BASE_URL = 'http://127.0.0.1:5000'


class TrainingMainForm(npyscreen.FormWithMenus):
    def create(self):
        self.menu = self.new_menu(name="Меню(Тренировки)", shortcut='^M')
        self.menu.addItem(text='Добавить тренировку(бег)', onSelect=self.CreateTrRun, shortcut='^X')
        self.menu.addItem(text='Добавить тренировку(плавание)', onSelect=self.CreateTrSwim, shortcut='^S')
        self.menu.addItem(text='Добавить тренировку(единоборства)', onSelect=self.CreateTrFight, shortcut='^A')
        self.menu.addItem(text='График калорий', onSelect=self.ShowTrPlt, shortcut='^B')
        self.menu.addItem(text='На главную', onSelect=self.Main_menu, shortcut='^K')
        self.menu.addItem(text='Выход', onSelect=self.Exit, shortcut='^D')
        resp_get = requests.get(f"{BASE_URL}/training")
        resp_json = resp_get.json()
        for trn in resp_json:
            self.trName = self.add(npyscreen.TitleFixedText, max_height=3, name='Название', value=trn['name'])
            trdt = trn['workout_date']
            self.trDate = self.add(npyscreen.TitleFixedText, max_height=3, name='Дата', value=f'{trdt}')
            trtp = trn['workout_type']
            trsbtp = trn['workout_subtype']
            self.trType = self.add(npyscreen.TitleFixedText, max_height=3, name='Вид тренировки', value=f'{trtp} - {trsbtp}')
            self.Cals = self.add(npyscreen.TitleFixedText, max_height=3, name='Потраченные калории', value=trn['calories'])

    def CreateTrRun(self):
        self.parentApp.addForm('Добавить тренировку_бег', TrainingRunCreateForm, name='Добавить тренировку_бег')
        self.parentApp.switchForm(fmid='Добавить тренировку_бег')

    def ShowTrPlt(self):
        resp_get = requests.get(f"{BASE_URL}/training")
        resp_json = resp_get.json()
        cals_list = []
        for trn in resp_json:
            trcals = trn['calories']
            cals_list.append(trcals)
        tr_plot.ShowPlot(*cals_list)

    def CreateTrSwim(self):
        self.parentApp.addForm('Добавить тренировку_плавание', TrainingSwimCreateForm,
                               name='Добавить тренировку_плавание')
        self.parentApp.switchForm(fmid='Добавить тренировку_плавание')

    def CreateTrFight(self):
        self.parentApp.addForm('Добавить тренировку_единоборства', TrainingFightCreateForm,
                               name='Добавить тренировку_единоборства')
        self.parentApp.switchForm(fmid='Добавить тренировку_единоборства')

    def Main_menu(self):
        self.parentApp.addForm('MAIN', main.IndexForm, name='Главная страница')
        self.parentApp.switchForm(fmid='MAIN')

    def Exit(self):
        self.parentApp.switchForm(None)


class TrainingRunCreateForm(npyscreen.ActionForm):
    def create(self):
        self.trName = self.add(npyscreen.TitleText, name='Название')
        self.trType = self.add(npyscreen.TitleFixedText, name='Вид тренировки', value='Бег')
        self.trSubType = self.add(npyscreen.TitleSelectOne, name='Вид бега', max_height=3,
                                  values=["Бег на дистанцию", "Кросс", "Спортивный бег"])
        self.trDate = self.add(npyscreen.TitleDateCombo, name='Дата тренировки')
        self.trTime = self.add(npyscreen.TitleText, name='Длительность(мин)')

    def on_ok(self):
        tr_date_ser = json.dumps(self.trDate.value, indent=4, sort_keys=True, default=str)
        tr_date_ser_fin = tr_date_ser.strip('"')
        tr_time_raw = self.trTime.value
        tr_time_int = int(tr_time_raw)
        training_data = {
            "name": self.trName.value,
            "workout_type": self.trType.value,
            "workout_subtype": self.trSubType.get_selected_objects()[0],
            "workout_date": tr_date_ser_fin,
            "workout_time": tr_time_int,
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(f"{BASE_URL}/training", headers=headers, json=training_data)
        if response.status_code == 201:
            print("Medicine added successfully")
        else:
            print("Failed to add medicine")
        self.parentApp.addForm('Тренировки', TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')

    def on_cancel(self):
        self.parentApp.addForm('Тренировки', TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')


class TrainingSwimCreateForm(npyscreen.ActionForm):
    def create(self):
        self.trName = self.add(npyscreen.TitleText, name='Название')
        self.trType = self.add(npyscreen.TitleFixedText, name='Вид тренировки', value='Плавание')
        self.trSubType = self.add(npyscreen.TitleSelectOne, name='Вид плавания', max_height=3,
                                  values=["Баттерфляй", "Брасс", "На спине"])
        self.trDate = self.add(npyscreen.TitleDateCombo, name='Дата тренировки')
        self.trTime = self.add(npyscreen.TitleText, name='Длительность(мин)')

    def on_ok(self):
        tr_date_ser = json.dumps(self.trDate.value, indent=4, sort_keys=True, default=str)
        tr_date_ser_fin = tr_date_ser.strip('"')
        tr_time_raw = self.trTime.value
        tr_time_int = int(tr_time_raw)
        training_data = {
            "name": self.trName.value,
            "workout_type": self.trType.value,
            "workout_subtype": self.trSubType.get_selected_objects()[0],
            "workout_date": tr_date_ser_fin,
            "workout_time": tr_time_int,
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(f"{BASE_URL}/training", headers=headers, json=training_data)
        if response.status_code == 201:
            print("Training added successfully")
        else:
            print("Failed to add training")
        self.parentApp.addForm('Тренировки', TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')

    def on_cancel(self):
        self.parentApp.addForm('Тренировки', TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')


class TrainingFightCreateForm(npyscreen.ActionForm):
    def create(self):
        self.trName = self.add(npyscreen.TitleText, name='Название')
        self.trType = self.add(npyscreen.TitleFixedText, name='Вид тренировки', value='Единоборства')
        self.trSubType = self.add(npyscreen.TitleSelectOne, name='Вид единоборств', max_height=3,
                                  values=["Бокс", "Кик-бокс", "ММА"])
        self.trDate = self.add(npyscreen.TitleDateCombo, name='Дата тренировки')
        self.trTime = self.add(npyscreen.TitleText, name='Длительность(мин)')

    def on_ok(self):
        tr_date_ser = json.dumps(self.trDate.value, indent=4, sort_keys=True, default=str)
        tr_date_ser_fin = tr_date_ser.strip('"')
        tr_time_raw = self.trTime.value
        tr_time_int = int(tr_time_raw)
        training_data = {
            "name": self.trName.value,
            "workout_type": self.trType.value,
            "workout_subtype": self.trSubType.get_selected_objects()[0],
            "workout_date": tr_date_ser_fin,
            "workout_time": tr_time_int,
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(f"{BASE_URL}/training", headers=headers, json=training_data)
        if response.status_code == 201:
            print("Medicine added successfully")
        else:
            print("Failed to add medicine")
        self.parentApp.addForm('Тренировки', TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')

    def on_cancel(self):
        self.parentApp.addForm('Тренировки', TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')

