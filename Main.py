import sys
import sqlite3
import datetime

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, \
    QTableWidgetItem, QTableWidget, QAbstractItemView, QMessageBox, QComboBox


# Стартовое окно
class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        # Выводим стартовое окно, устанавливаем css
        uic.loadUi('Start.ui', self)
        self.window_Pupil = None
        self.window_Teacher = None
        self.person = None
        self.ButtonStart.setStyleSheet('background: #f9cc02; border: none; '
                                       'color: #ff2a00; border-radius: 13px;')
        self.Entry.setStyleSheet('color: #fff;')
        self.Text1.setStyleSheet('color: #fff;')
        self.Text2.setStyleSheet('color: #fff;')
        self.lineLogin.setStyleSheet('background-color: #ffeb99; border: none;')
        self.linePassword.setStyleSheet('background-color: #ffeb99; border: none; type="password"')
        self.setStyleSheet("background-color: #6fc238;")
        self.check.setStyleSheet('color: #fff;')

        # Активация функции по нажатию кнопки
        self.ButtonStart.clicked.connect(self.PressEntry)

    def PressEntry(self):
        # Проверка наличия в базе данных такого логина с паролем
        login = self.lineLogin.text()
        password = self.linePassword.text()
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        pupils = cur.execute(f"SELECT * FROM Ученики WHERE "
                             f"Логин='{login}' AND Пароль='{password}'").fetchall()
        teachers = cur.execute(f"SELECT * FROM Учителя WHERE "
                               f"Логин='{login}' AND Пароль='{password}'").fetchall()
        con.close()
        # проверяем кто имеет такой пароль с логином, и если никто, то выводим надпись об ошибке
        if pupils:
            # Если пользователь захотел, запоминаем его в текстовом файле
            if self.check.isChecked():
                File = open("Пользователь.txt", encoding="utf-8", mode="w")
                File.write(str(pupils[0][0]) + " Ученики")
                File.close()
            # Новое окно и закрытие старого
            self.window_Pupil = PupilsWindow(pupils[0][0])
            self.window_Pupil.show()
            self.hide()
        elif teachers:
            # Если пользователь захотел, запоминаем его в текстовом файле
            if self.check.isChecked():
                File = open("Пользователь.txt", encoding="utf-8", mode="w")
                File.write(str(teachers[0][0]) + " Учителя")
                File.close()
            # Новое окно и закрытие старого
            self.window_Teacher = TeacherWindow(teachers[0][0])
            self.window_Teacher.show()
            self.hide()
        else:
            self.labelNot.setText('Введён неправильный пароль или логин')
            self.labelNot.setStyleSheet("color: #ff2a00")


# Меню ученика
class PupilsWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Устанавливаем имя человека в приветствии и оформление
        self.ex = Start()
        uic.loadUi('Pupil.ui', self)
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        name = list(cur.execute(f"SELECT * FROM Ученики WHERE id='{int(name)}'").fetchone())
        self.information = name
        self.Name.setText(f"Добро пожаловать, {name[1]} {name[2]}")
        self.Name.setStyleSheet("color: #6fc238;")
        self.setStyleSheet("background-color: #eff7e5;")
        self.ButtonTabel.setStyleSheet('background: #71c438; border: none; '
                                       'color: #fff; border-radius: 13px;')
        self.ButtonWeek.setStyleSheet('background: #71c438; border: none; '
                                      'color: #fff; border-radius: 13px;')
        self.ButtonPupils.setStyleSheet('background: #71c438; border: none; '
                                        'color: #fff; border-radius: 13px;')
        self.ButtonAccount.setStyleSheet('background: #71c438; border: none; '
                                         'color: #fff; border-radius: 13px;')
        self.Diary.setStyleSheet('background: #71c438; border: none; '
                                 'color: #fff; border-radius: 13px;')
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 5px;')
        # Действия по нажатию кнопок
        self.ButtonAccount.clicked.connect(self.OpenCabinet)
        self.Exit.clicked.connect(self.PressExit)
        self.ButtonPupils.clicked.connect(self.SeeClassmates)
        self.ButtonWeek.clicked.connect(self.SeeTuple)
        self.ButtonTabel.clicked.connect(self.SeeTable)
        self.Diary.clicked.connect(self.SeeDiary)

    # выход на главный экран
    def PressExit(self):
        open("Пользователь.txt", 'w').close()
        self.ex.show()
        self.hide()

    # Открытие личного кабинета
    def OpenCabinet(self):
        self.ex = Cabinet(self.information[0], 'ученик')
        self.ex.show()
        self.hide()

    # открытие списка учеников в твоём классе
    def SeeClassmates(self):
        self.ex = ClassmatesSee(self.information)
        self.ex.show()
        self.hide()

    # Просмотреть расписание
    def SeeTuple(self):
        self.ex = TimeTable(self.information)
        self.ex.show()
        self.hide()

    # Посмотреть табель успеваемости
    def SeeTable(self):
        self.ex = TableWindow(self.information)
        self.ex.show()
        self.hide()

    # Посмтреть дневник
    def SeeDiary(self):
        self.ex = Diary(self.information)
        self.ex.show()
        self.hide()


# Дневник
class Diary(QMainWindow):
    def __init__(self, name):
        # Стили
        super().__init__()
        self.ex = Start()
        uic.loadUi('Diary.ui', self)
        # Приложение для возвращения назад
        self.ex = PupilsWindow(name[0])
        self.inf = name
        self.Title.setStyleSheet("color: #6fc238;")
        for child in self.findChildren(QTableWidget):
            child.setStyleSheet("background-color: #eff7e5;")
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        # Стили для особых кнопок
        list_Nad = [self.MondayBut, self.TuesdayBut, self.WednesdayBut, self.ThursdayBut,
                    self.FridayBut, self.SaturdayBut]
        for But in list_Nad:
            But.setStyleSheet('background: #71c438; border: none; '
                              'color: #fff; border-top-left-radius: 10px; border-top-right-radius: 10px')
        # Смотрим первое и последнее время выставления оценок, по жтому будем регулировать размеры дневника
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = list(map(lambda x: x[0], cur.execute(f"SELECT Дата FROM Оценки WHERE Ученик='{name[0]}' "
                                                      f"ORDER BY Дата").fetchall()))
        self.start = datetime.datetime.strptime(result[0], '%Y-%m-%d')
        self.end = datetime.datetime.strptime(result[-1], '%Y-%m-%d')
        # От этой переменной будем отталкиваться при заполении дневника
        self.seeingStart = self.end - datetime.timedelta(days=self.end.weekday())
        self.SetDiary()

        self.Prev.clicked.connect(self.MinTime)
        self.Next.clicked.connect(self.MaxTime)
        self.Exit.clicked.connect(self.Exiting)

    # Увеличиваем переменную, дневник переходит на следующую неделю
    def MaxTime(self):
        self.seeingStart += datetime.timedelta(days=7)
        self.SetDiary()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.Exiting()

    # Уменьшаем переменную, дневник переходит на прошлую неделю
    def MinTime(self):
        self.seeingStart -= datetime.timedelta(days=7)
        self.SetDiary()

    # Выход
    def Exiting(self):
        self.ex.show()
        self.hide()

    def SetDiary(self):
        # Находим расписание на неделю
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM РасписанияНаНеделю WHERE Класс='{self.inf[5]}'").fetchall()
        if result:
            result = result[0]
        list_days = [self.Monday, self.Tuesday, self.Wednesday, self.Thursday, self.Friday, self.Saturday]
        kol = 1
        TimeStart = self.seeingStart
        # Заполняем каждую таблицу для каждого дня недели
        for day in list_days:
            if result[kol]:
                mon = cur.execute(f"SELECT * FROM Расписания WHERE id='{result[kol]}'").fetchall()[0]
                # Очистка
                day.setRowCount(0)
                # Это на случай если за день будет только 1 урок
                if ',' in str(mon[2]):
                    day.setRowCount(len(mon[2].split(',')))
                    list_1 = mon[2].split(',')
                    list_2 = mon[3].split(',')
                else:
                    day.setRowCount(1)
                    list_1 = [mon[2]]
                    list_2 = [mon[3]]
                # Настройка и заполнение таблицы
                day.setColumnCount(4)
                day.setHorizontalHeaderItem(0, QTableWidgetItem("Урок"))
                day.setHorizontalHeaderItem(1, QTableWidgetItem("Кабинет"))
                day.setHorizontalHeaderItem(2, QTableWidgetItem("Домашнее задание"))
                day.setHorizontalHeaderItem(3, QTableWidgetItem("Оценка"))
                day.horizontalHeader().setSectionResizeMode(True)
                for i, elem in enumerate(list_1):
                    name = cur.execute(f"SELECT Название FROM Предметы WHERE id='{elem}'").fetchone()[0]
                    day.setItem(i, 0, QTableWidgetItem(name))
                for i, elem in enumerate(list_2):
                    name = cur.execute(f"SELECT * FROM Кабинеты WHERE id='{elem}'").fetchone()
                    # Некоторые кабинеты называютя по-особенному, по типу Лабораторной
                    if name[0] not in range(17, 19):
                        day.setItem(i, 1, QTableWidgetItem('к.' + str(name[0])))
                    else:
                        day.setItem(i, 1, QTableWidgetItem(name[1]))
                for i, elem in enumerate(list_1):
                    # Если есть оценка за этот предмет, за эту дату, ставим
                    mark = cur.execute(f"SELECT * FROM Оценки WHERE Ученик='{self.inf[0]}' AND Предмет='{elem}'"
                                       f" AND Дата='{str(TimeStart).split()[0]}'").fetchone()
                    if mark:
                        day.setItem(i, 3, QTableWidgetItem(str(mark[3])))
                for i, elem in enumerate(list_1):
                    dz = cur.execute(f"SELECT * FROM ДомашнееЗадание WHERE Класс='{self.inf[5]}' AND Предмет='{elem}'"
                                     f" AND Дата='{str(TimeStart).split()[0]}'").fetchone()
                    if dz:
                        day.setItem(i, 2, QTableWidgetItem(str(dz[4])))
                kol += 1
                TimeStart += datetime.timedelta(days=1)
        # Тут указываем в названиях дату
        list_Nad = [self.MondayBut, self.TuesdayBut, self.WednesdayBut, self.ThursdayBut,
                    self.FridayBut, self.SaturdayBut]
        TimeStart = self.seeingStart
        for i in list_Nad:
            i.setText(i.text().split()[0] + ' (' + str(TimeStart).split()[0] + ')')
            TimeStart += datetime.timedelta(days=1)
        # Проверяем возможность перейти на следующую и предыдущую недели
        if self.seeingStart + datetime.timedelta(days=7) > self.end:
            self.Next.setEnabled(False)
            self.Next.setStyleSheet('background: #F0E68C; border: none; '
                                    'color: #FF4500; border-radius: 10px;')
        else:
            self.Next.setEnabled(True)
            self.Next.setStyleSheet('background: #f9cc02; border: none; '
                                    'color: #ff2a00; border-radius: 10px;')

        if self.seeingStart - datetime.timedelta(days=7) < self.start - datetime.timedelta(days=self.start.weekday()):
            self.Prev.setEnabled(False)
            self.Prev.setStyleSheet('background: #F0E68C; border: none; '
                                    'color: #FF4500; border-radius: 10px;')
        else:
            self.Prev.setEnabled(True)
            self.Prev.setStyleSheet('background: #f9cc02; border: none; '
                                    'color: #ff2a00; border-radius: 10px;')


# Экран Учителя
class TeacherWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Устанавливаем имя человека в приветствии и оформление
        self.ex = Start()
        uic.loadUi('Teacher.ui', self)
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        name = list(cur.execute(f"SELECT * FROM Учителя WHERE id='{name}'").fetchone())
        self.information = name
        self.Name.setText(f"Добро пожаловать, {name[1]} {name[2]}")
        self.Name.setStyleSheet("color: #6fc238;")
        self.setStyleSheet("background-color: #eff7e5;")
        self.ButtonMarks.setStyleSheet('background: #71c438; border: none; '
                                       'color: #fff; border-radius: 13px;')
        self.ButtonPupils.setStyleSheet('background: #71c438; border: none; '
                                        'color: #fff; border-radius: 13px;')
        self.ButtonTimetable.setStyleSheet('background: #71c438; border: none; '
                                           'color: #fff; border-radius: 13px;')
        self.ButtonAccount.setStyleSheet('background: #71c438; border: none; '
                                         'color: #fff; border-radius: 13px;')
        self.ButtonDz.setStyleSheet('background: #71c438; border: none; '
                                    'color: #fff; border-radius: 13px;')
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 5px;')

        self.ButtonAccount.clicked.connect(self.OpenCabinet)
        self.ButtonMarks.clicked.connect(self.OpenMarks)
        self.Exit.clicked.connect(self.PressExit)
        self.ButtonPupils.clicked.connect(self.SeeClasses)
        self.ButtonTimetable.clicked.connect(self.SeeTimeTable)
        self.ButtonDz.clicked.connect(self.OpenDz)

    # Функция выхода и возврашения на прошлый экран
    def PressExit(self):
        open("Пользователь.txt", 'w').close()
        self.ex.show()
        self.hide()

    # Открытие личного кабинета
    def OpenCabinet(self):
        self.ex = Cabinet(self.information[0], 'учитель')
        self.ex.show()
        self.hide()

    # Поставить оценку
    def OpenMarks(self):
        self.ex = MakeMark(self.information)
        self.ex.show()
        self.hide()

    # Список классов
    def SeeClasses(self):
        self.ex = Classes(self.information)
        self.ex.show()
        self.hide()

    # Расписание вашего класса
    def SeeTimeTable(self):
        self.ex = TimeTableTeacher(self.information)
        self.ex.show()
        self.hide()

    # Задать домашку
    def OpenDz(self):
        self.ex = MakeDz(self.information)
        self.ex.show()
        self.hide()


class Cabinet(QMainWindow):
    def __init__(self, name, acc):
        super().__init__()
        uic.loadUi('Cabinet.ui', self)
        # В зависимости от того, кто зашёл: учитель или ученик, делаем перефирию
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        if acc == 'ученик':
            name = list(cur.execute(f"SELECT * FROM Ученики WHERE id='{int(name)}'").fetchone())
        else:
            name = list(cur.execute(f"SELECT * FROM Учителя WHERE id='{int(name)}'").fetchone())
        self.Name.setText(name[1])
        self.Surname.setText(name[2])
        self.Birthday.setText(name[3])
        self.Age.setText(str(name[4]))
        # В зависимости от типа пользователя делаем настройку
        if acc == 'ученик':
            self.LabelChange.setText("Класс")
            result = cur.execute(f"SELECT Название FROM Классы WHERE id='{name[5]}'").fetchall()
            self.Changed.setText(result[0][0])
            self.ex = PupilsWindow(name[0])
        elif acc == 'учитель':
            self.LabelChange.setText("Предмет")
            result = cur.execute(f"SELECT Название FROM Предметы WHERE id='{name[5]}'").fetchall()
            self.Changed.setText(result[0][0])
            self.ex = TeacherWindow(name[0])
        self.Login.setText(name[6])
        self.Password.setText(name[7])

        # Сохраняем временные данные
        self.information = name
        self.acc = acc

        # стили
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Change.setStyleSheet('background: #f9cc02; border: none; '
                                  'color: #ff2a00; border-radius: 10px;')
        self.setStyleSheet("background-color: #6fc238;")
        for child in self.findChildren(QLabel):
            child.setStyleSheet("QLabel {color: #fff}")

        # кнопки
        self.Exit.clicked.connect(self.PressExit)
        self.Change.clicked.connect(self.ChangeInformation)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()

    # открытия окна для изменения информации
    def ChangeInformation(self):
        self.ex = ChangeCabinet(self.information[0], self.acc)
        self.ex.show()
        self.hide()

    # выход из кабинета
    def PressExit(self):
        self.ex.show()
        self.hide()


class ChangeCabinet(QMainWindow):
    def __init__(self, name, acc):
        super().__init__()
        uic.loadUi('ChangeCabinet.ui', self)
        # В зависимости от того, ученик или учитель, делаем оформление и выбор
        self.params = {}
        self.acc = acc
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        if acc == "ученик":
            name = list(cur.execute(f"SELECT * FROM Ученики WHERE id='{name}'").fetchone())
        else:
            name = list(cur.execute(f"SELECT * FROM Учителя WHERE id='{name}'").fetchone())
            self.LabelChange.setText('Класс')
        for child in self.findChildren(QLabel):
            child.setStyleSheet("color: #fff")
        self.setStyleSheet("background-color: #6fc238;")
        for child in self.findChildren(QLineEdit):
            child.setStyleSheet('background-color: #ffeb99; border: none;')
        self.comboBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Save.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')

        # Устанавливаем изначальные данные
        self.Name.setText(name[1])
        self.Surname.setText(name[2])
        self.Birthday.setText(name[3])
        self.Age.setText(str(name[4]))
        self.con = sqlite3.connect("PyQt5 Project.db")
        cur = self.con.cursor()
        if self.acc == "ученик":
            result = cur.execute("SELECT * FROM Классы").fetchall()
            for i in result:
                self.params[i[2]] = i[0]
            self.comboBox.addItems(list(self.params.keys()))
            self.comboBox.setCurrentIndex(name[5] - 1)
        else:
            self.LabelChange.setText("Предмет")
            result = cur.execute("SELECT * FROM Предметы").fetchall()
            for i in result:
                self.params[i[1]] = i[0]
            self.comboBox.addItems(list(self.params.keys()))
            self.comboBox.setCurrentIndex(name[5] - 1)
        self.Login.setText(name[6])
        self.Password.setText(name[7])
        self.information = name
        self.ex = None

        self.Save.clicked.connect(self.ChangeCabinet)
        self.Exit.clicked.connect(self.Exiting)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.ChangeCabinet()
        if event.key() == Qt.Key_Backspace:
            self.Exiting()

    def ChangeCabinet(self):
        # Если пользователь заполнил правильно меняем данные в зависимости от того ученик это или учитель
        try:
            if self.acc == 'ученик':
                date = datetime.datetime.strptime(self.Birthday.text(), '%Y-%m-%d')
                con = sqlite3.connect("PyQt5 Project.db")
                cur = con.cursor()
                Class = cur.execute(f"SELECT id FROM Классы WHERE Название='{self.comboBox.currentText()}'").fetchone()
                cur.execute(f"""UPDATE Ученики 
                                SET Имя='{self.Name.text()}', Фамилия='{self.Surname.text()}', 
                                Рождение='{str(date).split()[0]}',
                                Возраст='{int(self.Age.text())}', Класс='{int(Class[0])}', 
                                Логин='{self.Login.text()}', Пароль='{self.Password.text()}'
                                WHERE id = '{int(self.information[0])}'""")
                con.commit()
            else:
                date = datetime.datetime.strptime(self.Birthday.text(), '%Y-%m-%d')
                con = sqlite3.connect("PyQt5 Project.db")
                cur = con.cursor()
                Work = cur.execute(f"SELECT id FROM Предметы WHERE Название='{self.comboBox.currentText()}'").fetchone()
                cur.execute(f"""UPDATE Учителя
                                            SET Имя='{self.Name.text()}', Фамилия='{self.Surname.text()}', 
                                            Рождение='{str(date).split()[0]}',
                                            Возраст='{int(self.Age.text())}', Предмет='{Work[0]}', 
                                            Логин='{self.Login.text()}', Пароль='{self.Password.text()}'
                                            WHERE id = '{int(self.information[0])}'""")
                con.commit()
            self.ex = Cabinet(self.information[0], self.acc)
            self.ex.show()
            self.hide()
        # иначе говорим ему об ошибке
        except:
            self.Error.setText("Ошибка в заполнении")
            self.Error.setStyleSheet("color: #ff2a00")

    def Exiting(self):
        self.ex = Cabinet(self.information[0], self.acc)
        self.ex.show()
        self.hide()


# Просмотр списка одноклассников
class ClassmatesSee(QMainWindow):
    def __init__(self, name):
        # Стили...
        super().__init__()
        uic.loadUi('ListClassmates.ui', self)
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Title.setStyleSheet("color: #6fc238;")
        self.table.setStyleSheet("background-color: #eff7e5;")
        self.comboBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Sort.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.comboBox.addItems(["id", "Имя", "Фамилия", "Дата рождения", "Возраст"])
        self.inf = name
        # создаем сортированный список с начальными настройками
        self.Sorting('start')
        self.ex = PupilsWindow(name[0])

        self.Exit.clicked.connect(self.PressExit)
        self.Sort.clicked.connect(self.Sorting)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.Sorting()

    def PressExit(self):
        self.ex.show()
        self.hide()

    def Sorting(self, name=None):
        sortWord = 'id'
        if not name:
            sortWord = self.comboBox.currentText()
            if sortWord == "Дата рождения":
                sortWord = "Рождение"
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Ученики WHERE Класс='{self.inf[5]}' AND 
                             NOT id='{self.inf[0]}' ORDER BY {sortWord};""").fetchall()
        # Если одноклассники есть, заполняем таблицу
        if result:
            self.table.setRowCount(len(result))
            self.table.setColumnCount(len(result[0]) - 4)
            self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Имя"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Фамилия"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Дата рождения"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Возраст"))
            self.table.horizontalHeader().setSectionResizeMode(True)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem[1:]):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
        # Иначе пишем о проблеме
        else:
            self.label.setText("Странно, но никто не найден.")
            self.label.setStyleSheet("color: #6fc238;")


# Расписание для ученика
class TimeTable(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Стили
        uic.loadUi('Timetable.ui', self)
        self.ex = PupilsWindow(name[0])
        self.Title.setStyleSheet("color: #6fc238;")
        for child in self.findChildren(QTableWidget):
            child.setStyleSheet("background-color: #eff7e5;")
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        # Ищем расписание для нужного класса
        result = cur.execute(f"SELECT * FROM РасписанияНаНеделю WHERE Класс='{name[5]}'").fetchall()
        if result:
            result = result[0]
        list_days = [self.Monday, self.Tuesday, self.Wednesday, self.Thursday, self.Friday, self.Saturday]
        list_Nad = [self.MondayBut, self.TuesdayBut, self.WednesdayBut, self.ThursdayBut,
                    self.FridayBut, self.SaturdayBut]
        kol = 1
        # Заполняем
        for day in list_days:
            if result[kol]:
                mon = cur.execute(f"SELECT * FROM Расписания WHERE id='{result[kol]}'").fetchall()[0]
                # Нужно на случай, если за день только один урок
                if ',' in str(mon[2]):
                    day.setRowCount(len(mon[2].split(',')))
                    list_1 = mon[2].split(',')
                    list_2 = mon[3].split(',')
                else:
                    day.setRowCount(1)
                    list_1 = [mon[2]]
                    list_2 = [mon[3]]
                day.setColumnCount(2)
                day.setHorizontalHeaderItem(0, QTableWidgetItem("Урок"))
                day.setHorizontalHeaderItem(1, QTableWidgetItem("Кабинет"))
                day.horizontalHeader().setSectionResizeMode(True)
                day.setEditTriggers(QAbstractItemView.NoEditTriggers)
                for i, elem in enumerate(list_1):
                    name = cur.execute(f"SELECT Название FROM Предметы WHERE id='{elem}'").fetchone()[0]
                    day.setItem(i, 0, QTableWidgetItem(name))
                for i, elem in enumerate(list_2):
                    name = cur.execute(f"SELECT * FROM Кабинеты WHERE id='{elem}'").fetchone()
                    # Нужно для названий то типу Лабораторная
                    if name[0] not in range(17, 19):
                        day.setItem(i, 1, QTableWidgetItem('к.' + str(name[0]) + ' - Кабинет ' + name[1].lower()))
                    else:
                        day.setItem(i, 1, QTableWidgetItem(name[1]))
                kol += 1

            self.Exit.clicked.connect(self.PressExit)
        for But in list_Nad:
            But.setStyleSheet('background: #71c438; border: none; '
                              'color: #fff; border-top-left-radius: 10px; border-top-right-radius: 10px')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()

    def PressExit(self):
        self.ex.show()
        self.hide()


# Табель успеваемости
class TableWindow(QMainWindow):
    def __init__(self, name):
        # Стили
        super().__init__()
        uic.loadUi('Table.ui', self)
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Title.setStyleSheet("color: #6fc238;")
        self.table.setStyleSheet("background-color: #eff7e5;")
        self.comboBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Sort.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.inf = name
        self.ex = PupilsWindow(self.inf[0])
        # Добавляем в список comboBox все предметы, которые есть у ученика в расписании
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM РасписанияНаНеделю WHERE id='{name[5]}'").fetchall()[0]
        list_ = []
        for i in result[1:-1]:
            if i:
                list_.extend(cur.execute(f"SELECT Предметы FROM Расписания WHERE id='{i}'").fetchone()[0].split(','))
        list_ = tuple(set(map(int, list_)))
        result = list(map(lambda x: x[0], cur.execute(f"SELECT Название FROM Предметы WHERE id IN {list_}").fetchall()))
        result.insert(0, 'Все')
        self.comboBox.addItems(result)
        # Вывод всех оценок, сортированных по дате ставления
        self.Sorting()

        self.Sort.clicked.connect(self.Sorting)
        self.Exit.clicked.connect(self.PressExit)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.Sorting()

    def Sorting(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        # Находим все оценки для нужного ученика по нужному преджмету
        Id = cur.execute(f"""SELECT id FROM Предметы WHERE Название='{self.comboBox.currentText()}'""").fetchone()
        result = cur.execute(f"""SELECT * FROM Оценки WHERE Ученик='{self.inf[5]}' ORDER BY Дата;""").fetchall()
        if Id:
            result = cur.execute(f"""SELECT * FROM Оценки WHERE Ученик='{self.inf[5]}' AND Предмет='{Id[0]}' 
            ORDER BY Дата;""").fetchall()
        # Заполение
        self.table.setRowCount(len(result))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Предмет"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Оценка"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Дата"))
        self.table.horizontalHeader().setSectionResizeMode(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        if result:
            for i, elem in enumerate(result):
                for j, val in enumerate(elem[2:]):
                    # Если мы заполняем название предмета, мы должны его сначала получить
                    if j == 0:
                        self.table.setItem(i, j, QTableWidgetItem(
                            cur.execute(f"SELECT Название FROM Предметы WHERE id='{val}'").fetchone()[0]))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(str(val)))
        # Если мы вывели оценки по одному предмету, выводим среднюю оценку
        if Id:
            kol = 0
            for i in result:
                kol += i[3]
            if result:
                self.Mark.setText('Средняя оценка: ' + str(kol / len(result)))
            else:
                self.Mark.setText('Нет данных')
            self.Mark.setStyleSheet("color: #6fc238;")
        else:
            self.Mark.setText('')

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()


# Задать Д/з
class MakeDz(QMainWindow):
    def __init__(self, name):
        # Стили
        super().__init__()
        uic.loadUi('MakeDz.ui', self)
        self.setStyleSheet("background-color: #6fc238;")
        for child in self.findChildren(QLabel):
            child.setStyleSheet("QLabel {color: #fff}")
        self.Ok.setStyleSheet('background: #f9cc02; border: none; '
                              'color: #ff2a00; border-radius: 15px;')
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 15px;')
        self.Dz.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Class.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Date.setStyleSheet('background-color: #ffeb99; border: none;')
        self.ex = TeacherWindow(name[0])

        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = list(map(lambda x: x[0], cur.execute(f"SELECT Название FROM Классы").fetchall()))
        self.Class.addItems(result)
        self.Item.setText(cur.execute(f"SELECT Название FROM Предметы WHERE id='{name[5]}'").fetchone()[0])
        self.Ok.clicked.connect(self.AddMark)
        self.Exit.clicked.connect(self.PressExit)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.AddMark()

    def AddMark(self):
        # Считываем все данные и сохраняем домашнее задание
        try:
            con = sqlite3.connect("PyQt5 Project.db")
            cur = con.cursor()
            idClass = cur.execute(f"SELECT id FROM Классы WHERE Название='{self.Class.currentText()}'").fetchone()[0]
            idItem = cur.execute(f"SELECT id FROM Предметы WHERE Название='{self.Item.text()}'").fetchone()[0]
            date = datetime.datetime.strptime(self.Date.text(), '%Y-%m-%d')
            cur.execute(f"INSERT INTO ДомашнееЗадание(Класс, Предмет, Дата, Домашка) VALUES('{idClass}', '{idItem}', "
                        f"'{str(date).split()[0]}', '{self.Dz.text()}')")
            con.commit()
            self.ex.show()
            self.hide()
        # иначе выводим предупреждение
        except:
            self.labelNot.setText('Введены неправильные данные')
            self.labelNot.setStyleSheet("color: #ff2a00")

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()


# Поставить оценку
class MakeMark(QMainWindow):
    def __init__(self, name):
        # Стили
        super().__init__()
        uic.loadUi('MakeMark.ui', self)
        self.setStyleSheet("background-color: #6fc238;")
        for child in self.findChildren(QLabel):
            child.setStyleSheet("QLabel {color: #fff}")
        self.Ok.setStyleSheet('background: #f9cc02; border: none; '
                              'color: #ff2a00; border-radius: 15px;')
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 15px;')
        self.line.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Date.setStyleSheet('background-color: #ffeb99; border: none;')
        self.ClassBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.PupilBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.ex = TeacherWindow(name[0])

        # ЗАполняем комбо боксы
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = list(map(lambda x: x[0], cur.execute(f"SELECT Название FROM Классы").fetchall()))
        self.ClassBox.addItems(result)
        self.choosePupils()
        self.ClassBox.currentIndexChanged.connect(self.choosePupils)
        self.Item.setText(cur.execute(f"SELECT Название FROM Предметы WHERE id='{name[5]}'").fetchone()[0])
        self.Ok.clicked.connect(self.AddMark)
        self.Exit.clicked.connect(self.PressExit)

    # При изменении значения класса в комбо боксе меняем учеников на соответствующих новому классу
    def choosePupils(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        idClass = cur.execute(f"SELECT id FROM Классы WHERE Название='{self.ClassBox.currentText()}'").fetchall()[0]
        result = list(map(lambda x: x[0] + ' ' + x[1], cur.execute(f"SELECT Имя, Фамилия FROM Ученики "
                                                                   f"WHERE Класс='{idClass[0]}'").fetchall()))
        self.PupilBox.clear()
        self.PupilBox.addItems(result)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.AddMark()

    # Добавить оценку
    def AddMark(self):
        # Считываем всю информацию и сохраняяем
        try:
            con = sqlite3.connect("PyQt5 Project.db")
            cur = con.cursor()
            idPupil = cur.execute(f"SELECT id FROM Ученики WHERE "
                                  f"Имя='{self.PupilBox.currentText().split()[0]}'").fetchone()[0]
            idItem = cur.execute(f"SELECT id FROM Предметы WHERE Название='{self.Item.text()}'").fetchone()[0]
            data = str(datetime.datetime.strptime(self.Date.text(), '%Y-%m-%d')).split()[0]
            cur.execute(f"INSERT INTO Оценки(Ученик, Предмет, Оценка, Дата) VALUES({idPupil}, {idItem}, "
                        f"{self.line.text()}, '{data}')")
            con.commit()
            self.ex.show()
            self.hide()
        except:
            self.labelNot.setText('Введены неправильные данные')
            self.labelNot.setStyleSheet("color: #ff2a00")

    def PressExit(self):
        self.ex.show()
        self.hide()


# Списки всех классов
class Classes(QMainWindow):
    def __init__(self, name):
        # Стили
        super().__init__()
        uic.loadUi('ListClasses.ui', self)
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Title.setStyleSheet("color: #6fc238;")
        self.table.setStyleSheet("background-color: #eff7e5;")
        self.comboBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.classBox.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Sort.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.AddClass.setStyleSheet('background: #f9cc02; border: none; '
                                    'color: #ff2a00; border-radius: 10px;')
        self.AddPupil.setStyleSheet('background: #f9cc02; border: none; '
                                    'color: #ff2a00; border-radius: 10px;')
        self.DeletePupil.setStyleSheet('background: #f9cc02; border: none; '
                                       'color: #ff2a00; border-radius: 10px;')
        self.DeleteClass.setStyleSheet('background: #f9cc02; border: none; '
                                       'color: #ff2a00; border-radius: 10px;')
        self.setStyleSheet("background-color: #eff7e5;")
        self.comboBox.addItems(["id", "Имя", "Фамилия", "Дата рождения", "Возраст"])

        # Добавить все классы
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = list(map(lambda x: x[0], cur.execute(f"""SELECT Название FROM Классы""").fetchall()))
        self.classBox.addItems(result)
        # Запомнить временные данные
        self.inf = name
        self.ex = TeacherWindow(name[0])

        # Св-ва кнопок
        self.Exit.clicked.connect(self.PressExit)
        self.Sort.clicked.connect(self.Sorting)
        self.AddClass.clicked.connect(self.NewClass)
        self.AddPupil.clicked.connect(self.NewPupil)
        self.DeletePupil.clicked.connect(self.NonePupil)
        self.DeleteClass.clicked.connect(self.NoneClass)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.Sorting()

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()

    # Заполняем таблицу и сортируем информацию об учениках
    def Sorting(self):
        sortWord = self.comboBox.currentText()
        # Находим всех нужных учеников
        if sortWord == "Дата рождения":
            sortWord = "Рождение"
        Class = self.classBox.currentText()
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        Class = cur.execute(f"""SELECT id FROM Классы WHERE Название='{Class}'""").fetchone()[0]
        result = cur.execute(f"""SELECT * FROM Ученики WHERE Класс='{Class}' ORDER BY {sortWord};""").fetchall()
        # Заполняем таблицу
        if result:
            self.table.setRowCount(len(result))
            self.table.setColumnCount(len(result[0]) - 2)
            self.table.setColumnCount(len(result[0]) - 2)
            self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Имя"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Фамилия"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Дата рождения"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Возраст"))
            self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Логин"))
            self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Пароль"))
            self.table.horizontalHeader().setSectionResizeMode(True)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem[1:]):
                    # Костыль т.к. приходится перепрыгивать пару ненужных значений в базе данных
                    if 6 > j >= 4:
                        self.table.setItem(i, j, QTableWidgetItem(str(elem[j + 2])))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.label.setText("Странно, но никто не найден.")
            self.label.setStyleSheet("color: #6fc238;")

    # Создать новый класс
    def NewClass(self):
        self.ex = CreateClass(self.inf)
        self.ex.show()
        self.hide()

    # Создать нового ученика
    def NewPupil(self):
        self.ex = CreatePupil(self.inf)
        self.ex.show()
        self.hide()

    # Удалить ученика
    def NonePupil(self):
        self.ex = DeletePupil(self.inf)
        self.ex.show()
        self.hide()

    # Удалить класс
    def NoneClass(self):
        self.ex = DeleteClass(self.inf)
        self.ex.show()
        self.hide()


# Расписание, которое учитель может редактировать
class TimeTableTeacher(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Стили
        uic.loadUi('TimetableTeacher.ui', self)
        self.ex = TeacherWindow(name[0])
        self.Title.setStyleSheet("color: #6fc238;")
        for child in self.findChildren(QTableWidget):
            child.setStyleSheet("background-color: #eff7e5;")
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Save.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        # Ищем класс учителя, если он есть, продолжаем
        Class = cur.execute(f"SELECT id FROM Классы WHERE КлассРук='{name[0]}'").fetchone()
        list_Nad = [self.MondayBut, self.TuesdayBut, self.WednesdayBut, self.ThursdayBut,
                    self.FridayBut, self.SaturdayBut]
        if Class:
            Class = Class[0]
            result = cur.execute(f"SELECT * FROM РасписанияНаНеделю WHERE Класс='{Class}'").fetchall()
            if result:
                result = result[0]
            list_days = [self.Monday, self.Tuesday, self.Wednesday, self.Thursday, self.Friday, self.Saturday]
            self.inf = name
            kol = 1
            # Заполняем все таблицы в соответствии с расписанием
            for day in list_days:
                day.setRowCount(8)
                day.setColumnCount(2)
                day.setHorizontalHeaderItem(0, QTableWidgetItem("Урок"))
                day.setHorizontalHeaderItem(1, QTableWidgetItem("Кабинет"))
                day.horizontalHeader().setSectionResizeMode(True)
                if result[kol]:
                    mon = cur.execute(f"SELECT * FROM Расписания WHERE id='{result[kol]}'").fetchall()[0]
                    # Нужно на случай, если за день только один урок
                    if ',' in str(mon[2]):
                        list_1 = mon[2].split(',')
                        list_2 = mon[3].split(',')
                    else:
                        list_1 = [mon[2]]
                        list_2 = [mon[3]]
                    for i, elem in enumerate(list_1):
                        name = cur.execute(f"SELECT Название FROM Предметы WHERE id='{elem}'").fetchone()[0]
                        day.setItem(i, 0, QTableWidgetItem(name))
                    for i, elem in enumerate(list_2):
                        name = cur.execute(f"SELECT * FROM Кабинеты WHERE id='{elem}'").fetchone()
                        # Нужно для названий то типу Лабораторная
                        if name[0] not in range(17, 19):
                            day.setItem(i, 1, QTableWidgetItem('к.' + str(name[0]) + ' - Кабинет ' + name[1].lower()))
                        else:
                            day.setItem(i, 1, QTableWidgetItem(name[1]))
                    kol += 1
            self.Save.clicked.connect(self.SaveAll)
        # Кнопочки
        self.Exit.clicked.connect(self.PressExit)
        for But in list_Nad:
            But.setStyleSheet('background: #71c438; border: none; '
                              'color: #fff; border-top-left-radius: 10px; border-top-right-radius: 10px')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.SaveAll()

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()

    # Сохранить изменения
    def SaveAll(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        Class = cur.execute(f"SELECT id FROM Классы WHERE КлассРук='{self.inf[0]}'").fetchone()
        Class = Class[0]
        result = cur.execute(f"SELECT * FROM РасписанияНаНеделю WHERE Класс='{Class}'").fetchall()
        if result:
            result = result[0]
        list_days = [self.Monday, self.Tuesday, self.Wednesday, self.Thursday, self.Friday, self.Saturday]
        list_strings = ['Понедельник', "Вторник", 'Среда', 'Четверг', 'Пятница', 'Суббота']
        kol = 0
        try:
            # Считываем всё и вся и сохраняем это
            for num, i in enumerate(result[1:-1]):
                # Сохраняем новые предметы
                new_items = []
                for j in range(list_days[kol].rowCount()):
                    if list_days[kol].item(j, 0):
                        if list_days[kol].item(j, 0).text() != '':
                            new_items.append(cur.execute(f"SELECT id FROM Предметы "
                                                         f"WHERE "
                                                         f"Название='{list_days[kol].item(j, 0).text()}'").fetchone()[
                                                 0])
                # Сохраняем новые кабинеты
                new_cabinets = []
                for j in range(list_days[kol].rowCount()):
                    if list_days[kol].item(j, 1):
                        if list_days[kol].item(j, 1).text() != '':
                            if list(list_days[kol].item(j, 1).text())[0] == "к":
                                Cab = int(''.join(list(list_days[kol].item(j, 1).text().split()[0])[2:]))
                            else:
                                Cab = cur.execute(f"SELECT id FROM Кабинеты "
                                                  f"WHERE Название='{list_days[kol].item(j, 1).text()}'").fetchone()[0]
                            new_cabinets.append(Cab)
                kol += 1
                new_items = list(map(str, new_items))
                new_cabinets = list(map(str, new_cabinets))
                # Записываем изменения
                if i and new_items and new_cabinets:
                    cur.execute(f"UPDATE Расписания "
                                f"SET Предметы='{','.join(new_items)}', Кабинеты='{','.join(new_cabinets)}'"
                                f"WHERE id='{i}'")
                elif new_items and new_cabinets:
                    cur.execute(f"INSERT INTO Расписания(Класс, Предметы, Кабинеты) VALUES('{result[-1]}', "
                                f"'{','.join(new_items)}', "
                                f"'{','.join(new_cabinets)}')")
                    Id = cur.execute(f"SELECT id FROM Расписания WHERE Предметы='{','.join(new_items)}'"
                                     f" AND Кабинеты='{','.join(new_cabinets)}'"
                                     f" AND Класс='{result[-1]}'").fetchone()[0]
                    cur.execute(f"UPDATE РасписанияНаНеделю "
                                f"SET {list_strings[num]}='{Id}'"
                                f"WHERE id='{result[0]}'")
                else:
                    cur.execute(f"UPDATE РасписанияНаНеделю "
                                f"SET {list_strings[num]}=''"
                                f"WHERE id='{result[0]}'")
                    cur.execute(f"DELETE FROM Расписания WHERE id='{i}'")
            con.commit()
            self.Error.setText('')
        # Подстраховка
        except:
            self.Error.setText("Возникла ошибка. Проверьте правильность заполениния расписания")
            self.Error.setStyleSheet("color: #ff2a00")


# Создание класса
class CreateClass(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Стили
        uic.loadUi('NewClass.ui', self)
        self.ex = Classes(name)
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Create.setStyleSheet('background: #f9cc02; border: none; '
                                  'color: #ff2a00; border-radius: 10px;')
        self.Teacher.setStyleSheet('background-color: #ffeb99; border: none;')
        self.Name.setStyleSheet('background-color: #ffeb99; border: none;')
        self.setStyleSheet("background-color: #6fc238;")
        for child in self.findChildren(QLabel):
            child.setStyleSheet("color: #fff")

        # Заполение инфобоксов
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        ids = tuple(map(lambda x: x[0], cur.execute(f"SELECT КлассРук From Классы").fetchall()))
        ids = ids + (0,)
        result = list(map(lambda x: x[0] + ' ' + x[1], cur.execute(f"SELECT Имя, Фамилия FROM Учителя "
                                                                   f"WHERE id NOT IN {ids}").fetchall()))
        if result:
            self.Teacher.addItems(result)
        else:
            self.Teacher.addItems(['Нет свободных учителей'])

        self.Exit.clicked.connect(self.PressExit)
        self.Create.clicked.connect(self.CreateNew)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.CreateNew()

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()

    # Считывание информации и запись
    def CreateNew(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        if not self.Name.text() or self.Name.text() == '' or self.Teacher.currentText() == 'Нет свободных учителей':
            if self.Teacher.currentText() == 'Нет свободных учителей':
                self.Error.setText("Нет доступных учителей")
            else:
                self.Error.setText("Введите название")
            self.Error.setStyleSheet("color: #ff2a00")
        else:
            idTeacher = cur.execute(f"SELECT id FROM Учителя "
                                    f"WHERE Имя='{self.Teacher.currentText().split()[0]}'").fetchone()[0]
            cur.execute(f"INSERT INTO Классы(Количество,Название,КлассРук) VALUES (0,"
                        f"'{self.Name.text()}','{idTeacher}')")
            con.commit()
            self.PressExit()


# Создание ученика
class CreatePupil(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Стили
        uic.loadUi('NewPupil.ui', self)
        self.ex = Classes(name)
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Create.setStyleSheet('background: #f9cc02; border: none; '
                                  'color: #ff2a00; border-radius: 10px;')
        self.setStyleSheet("background-color: #6fc238;")
        self.Klass.setStyleSheet('background-color: #ffeb99; border: none;')
        for child in self.findChildren(QLabel):
            child.setStyleSheet("color: #fff")
        for child in self.findChildren(QLineEdit):
            child.setStyleSheet('background-color: #ffeb99; border: none;')
        # Заполнение инфобоксов
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Классы").fetchall()
        self.params = {}
        for i in result:
            self.params[i[2]] = i[0]
        self.Klass.addItems(list(self.params.keys()))

        self.Exit.clicked.connect(self.PressExit)
        self.Create.clicked.connect(self.CreateNew)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.CreateNew()

    # Считывание и запись информации
    def CreateNew(self):
        try:
            date = datetime.datetime.strptime(self.Birthday.text(), '%Y-%m-%d')
            con = sqlite3.connect("PyQt5 Project.db")
            cur = con.cursor()
            Class = cur.execute(f"SELECT id FROM Классы WHERE Название='{self.Klass.currentText()}'").fetchone()
            cur.execute(f"""INSERT INTO Ученики(Имя,Фамилия,Рождение,Возраст,Класс,Логин,Пароль) VALUES (
                                            '{self.Name.text()}','{self.Surname.text()}', '{str(date).split()[0]}',
                                            '{int(self.Age.text())}','{int(Class[0])}','{self.Login.text()}',
                                            '{self.Password.text()}')""")
            old_num = cur.execute(f"SELECT Количество FROM Классы "
                                  f"WHERE Название='{self.Klass.currentText()}'").fetchone()[0]
            cur.execute(f"UPDATE Классы SET Количество='{old_num + 1}' WHERE Название='{self.Klass.currentText()}'")
            con.commit()
            self.PressExit()
        # иначе говорим ему об ошибке
        except:
            self.Error.setText("Ошибка в заполнении")
            self.Error.setStyleSheet("color: #ff2a00")

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()


# Удалить ученика
class DeletePupil(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('DeletePupil.ui', self)
        # Стили
        self.ex = Classes(name)
        self.setStyleSheet("background-color: #6fc238;")
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Delete.setStyleSheet('background: #f9cc02; border: none; '
                                  'color: #ff2a00; border-radius: 10px;')
        for child in self.findChildren(QLabel):
            child.setStyleSheet("color: #fff")
        for child in self.findChildren(QComboBox):
            child.setStyleSheet('background-color: #ffeb99; border: none;')
        # Заполнение инфобоксов
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM Классы").fetchall()
        self.params = {}
        for i in result:
            self.params[i[2]] = i[0]
        self.Class.addItems(list(self.params.keys()))
        self.check_change()
        # Кнопочки
        self.Exit.clicked.connect(self.PressExit)
        self.Delete.clicked.connect(self.NoPupil)
        self.Class.currentIndexChanged.connect(self.check_change)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.NoPupil()

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()

    # Обновляет учеников если поменялся класс
    def check_change(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        idClass = cur.execute(f"SELECT id FROM Классы WHERE Название='{self.Class.currentText()}'").fetchone()[0]
        pupils = list(map(lambda x: x[0] + ' ' + x[1], cur.execute(f"SELECT Имя, Фамилия FROM Ученики "
                                                                   f"WHERE Класс='{idClass}'").fetchall()))
        self.Pupil.clear()
        self.Pupil.addItems(pupils)
        if not pupils:
            self.Pupil.addItems(['Учеников нет'])

    # Удаление ученика
    def NoPupil(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        valid = QMessageBox.question(self, '', "Вы действительно хотите удалить ученика?", QMessageBox.Yes,
                                     QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur.execute(f"DELETE FROM Ученики WHERE Имя='{self.Pupil.currentText().split()[0]}' AND "
                        f"Фамилия='{self.Pupil.currentText().split()[1]}'")
        con.commit()
        self.check_change()


# Удаление класса
class DeleteClass(QMainWindow):
    def __init__(self, name):
        super().__init__()
        # Стили
        self.params = {}
        uic.loadUi('DeleteClass.ui', self)
        self.ex = Classes(name)
        self.setStyleSheet("background-color: #6fc238;")
        self.Exit.setStyleSheet('background: #f9cc02; border: none; '
                                'color: #ff2a00; border-radius: 10px;')
        self.Delete.setStyleSheet('background: #f9cc02; border: none; '
                                  'color: #ff2a00; border-radius: 10px;')
        for child in self.findChildren(QLabel):
            child.setStyleSheet("color: #fff")
        for child in self.findChildren(QComboBox):
            child.setStyleSheet('background-color: #ffeb99; border: none;')

        self.Update_Class()
        # Кнопочки
        self.Exit.clicked.connect(self.PressExit)
        self.Delete.clicked.connect(self.NoClass)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.PressExit()
        if event.key() == Qt.Key_Enter:
            self.NoClass()

    # Выход
    def PressExit(self):
        self.ex.show()
        self.hide()

    # Удаление класса и всех учеников в этом классе, с предупреждением
    def NoClass(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        valid = QMessageBox.question(self, '', "Вы действительно хотите удалить класс? "
                                               "Это удалит всех учеников в классе", QMessageBox.Yes,
                                     QMessageBox.No)
        if valid == QMessageBox.Yes:
            idClass = cur.execute(f"SELECT id FROM Классы WHERE Название='{self.Class.currentText()}'").fetchone()[0]
            cur.execute(f"DELETE FROM Ученики WHERE Класс='{idClass}'")
            cur.execute(f"DELETE FROM Классы WHERE id='{idClass}'")
        con.commit()
        self.Update_Class()

    # Работает при запуске окна и при удалении класса, обновляет список существующих классов
    def Update_Class(self):
        con = sqlite3.connect("PyQt5 Project.db")
        cur = con.cursor()
        self.params = {}
        result = cur.execute("SELECT * FROM Классы").fetchall()
        for i in result:
            self.params[i[2]] = i[0]
        self.Class.addItems(list(self.params.keys()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Смотрим, есть ли в файле сохранённый пользователь и если есть, открываем второе окно сразу
    file = open("Пользователь.txt", encoding="utf-8", mode="r")
    person = file.readline().split()
    if person:
        if person[1] == "Учителя":
            window_Teacher = TeacherWindow(person[0])
            window_Teacher.show()
        elif person[1] == "Ученики":
            window_Pupil = PupilsWindow(person[0])
            window_Pupil.show()
    # иначе открываем вход
    else:
        ex = Start()
        ex.show()
    sys.exit(app.exec())
