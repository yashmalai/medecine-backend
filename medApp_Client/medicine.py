import npyscreen
import requests
import json
import main


BASE_URL = 'http://127.0.0.1:5000'


class MedicineMainForm(npyscreen.FormWithMenus):
    def create(self):
        self.menu = self.new_menu(name="Меню(Лекарства)", shortcut='^M')
        self.menu.addItem(text='Добавить лекарство', onSelect=self.CreateMed, shortcut='^X')
        self.menu.addItem(text='На главную', onSelect=self.Main_menu, shortcut='^K')
        self.menu.addItem(text='Выход', onSelect=self.Exit, shortcut='^D')
        resp_get = requests.get(f"{BASE_URL}/medicine")
        resp_json = resp_get.json()
        for med in resp_json:
            self.medName = self.add(npyscreen.TitleFixedText, max_height=3, name='Название', value=med['name'])
            strtdt = med['start_date']
            enddt = med['end_date']
            self.medDate = self.add(npyscreen.TitleFixedText, max_height=3, name='Даты приема', value=f'{strtdt} - {enddt}')
            drgtp = med['drug_type']
            ds = med['dose']
            drgsch = med['schedule_times']
            self.medDose = self.add(npyscreen.TitleFixedText, max_height=3, name='Правило приема', value=f'{drgtp} - {ds} шт/мл - {drgsch}')
            ttlds = int(med['total_doses'])
            dstkn = int(med['doses_taken'])
            self.medTaken = self.add(npyscreen.TitleSlider, max_height=3, max_width=100, name='Лекарств принято', out_of=ttlds, step=1, value=dstkn, color='GREEN_BLACK', label=True)

    def CreateMed(self):
        self.parentApp.addForm('Добавить лекарство', MedicineCreateForm, name='Добавить лекарство')
        self.parentApp.switchForm(fmid='Добавить лекарство')

    def Main_menu(self):
        self.parentApp.addForm('MAIN', main.IndexForm, name='Главная страница')
        self.parentApp.switchForm(fmid='MAIN')

    def Exit(self):
        self.parentApp.switchForm(None)


class MedicineCreateForm(npyscreen.ActionForm):
    def on_ok(self):
        start_date_ser = json.dumps(self.medStartDate.value, indent=4, sort_keys=True, default=str)
        start_date_ser_fin = start_date_ser.strip('"')
        end_date_ser = json.dumps(self.medEndDate.value, indent=4, sort_keys=True, default=str)
        end_date_ser_fin = end_date_ser.strip('"')
        medicine_data = {
            "name": self.medName.value,
            "dose": self.medDose.value,
            "drug_type": self.medType.get_selected_objects()[0],
            "intake_rule": self.medIntakeRule.get_selected_objects()[0],
            "comment": self.medComment.value,
            "schedule_times": self.medSchTime.value,
            "days_of_week": self.medDays.get_selected_objects()[0],
            "start_date": start_date_ser_fin,
            "end_date": end_date_ser_fin
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(f"{BASE_URL}/medicine", headers=headers, json=medicine_data)
        if response.status_code == 201:
            print("Medicine added successfully")
        else:
            print("Failed to add medicine")
        self.parentApp.addForm('Лекарства', MedicineMainForm, name='Лекарства')
        self.parentApp.switchForm(fmid='Лекарства')

    def on_cancel(self):
        self.parentApp.addForm('Лекарства', MedicineMainForm, name='Лекарства')
        self.parentApp.switchForm(fmid='Лекарства')

    def create(self):
        self.medName = self.add(npyscreen.TitleText, name='Название')
        self.medType = self.add(npyscreen.TitleSelectOne, name='Тип', max_height=3,
                                values=["Таблетки", "Капсулы", "Уколы", "Капли", "Процедуры"])
        self.medDose = self.add(npyscreen.TitleText, name='Дозировка')
        self.medIntakeRule = self.add(npyscreen.TitleSelectOne, name='Правило приема',
                                      max_height=3, values=["До еды", "После еды", "Без правил"])
        self.medComment = self.add(npyscreen.TitleText, name='Комментарий')
        self.medSchTime = self.add(npyscreen.TitleText, name='Время приема')
        self.medDays = self.add(npyscreen.TitleMultiSelect, name='Дни приема', max_height=3,
                                values=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])
        self.medStartDate = self.add(npyscreen.TitleDateCombo, name='Дата начала приема')
        self.medEndDate = self.add(npyscreen.TitleDateCombo, name='Дата окончания приема')
