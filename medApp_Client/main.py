import npyscreen
import medicine
import training
import requests


BASE_URL = 'http://127.0.0.1:5000'


class IndexForm(npyscreen.FormWithMenus):
    def create(self):
        self.menu = self.new_menu(name="Main Menu", shortcut='^M')
        self.menu.addItem(text='Лекарства', onSelect=self.Med, shortcut='^X')
        self.menu.addItem(text='Тренировки', onSelect=self.Training, shortcut='^K')
        self.menu.addItem(text='Выход', onSelect=self.Exit, shortcut='^D')
        resp_get = requests.get(f"{BASE_URL}/log")
        resp_json = resp_get.json()
        for log in resp_json:
            self.logType = self.add(npyscreen.TitleFixedText, max_height=3, name='Тип', value=log['action_type'])
            self.logTime = self.add(npyscreen.TitleFixedText, max_height=3, name='Время создания', value=log['timestamp'])

    def Med(self):
        self.parentApp.addForm('Лекарства', medicine.MedicineMainForm, name='Лекарства')
        self.parentApp.switchForm(fmid='Лекарства')

    def Training(self):
        self.parentApp.addForm('Тренировки', training.TrainingMainForm, name='Тренировки')
        self.parentApp.switchForm(fmid='Тренировки')

    def Exit(self):
        self.parentApp.switchForm(None)


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addFormClass('MAIN', IndexForm, name='Главная страница')
        self.addFormClass('Лекарства', medicine.MedicineMainForm, name='Лекарства')
        self.addFormClass('Добавить лекарство', medicine.MedicineCreateForm, name='Добавить лекарство')
        self.addFormClass('Тренировки', training.TrainingMainForm, name='Тренировки')
        self.addFormClass('Добавить тренировку_бег', training.TrainingRunCreateForm, name='Добавить тренировку_бег')
        self.addFormClass('Добавить тренировку_плавание', training.TrainingSwimCreateForm, name='Добавить тренировку_плавание')
        self.addFormClass('Добавить тренировку_единоборства', training.TrainingFightCreateForm, name='Добавить тренировку_единоборства')
        npyscreen.setTheme(npyscreen.Themes.DefaultTheme)


if __name__ == '__main__':
    TestApp = MyApplication().run()
