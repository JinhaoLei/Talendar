# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RepeatWindow(QDialog):
    def __init__(self):
        super(RepeatWindow, self).__init__()
        self.setWindowTitle(u"重复")
        self.initLayout()
        self.resize(300, 100)
        self.show()

    def diffUnit(self, index):
        if self.comboUnit.currentIndex() == 1:
            self.lblWeekRepeat = QLabel(u'重复时间')
            weekday = [u'一', u'二', u'三', u'四', u'五', u'六', u'日']


            self.leftLayout.addWidget(self.lblWeekRepeat, 5, 0)
            Mon = QCheckBox()
            Tue = QCheckBox()
            Wedn = QCheckBox()
            Thu = QCheckBox()
            Fri = QCheckBox()
            Sat = QCheckBox()
            Sun = QCheckBox()
            checkBoxGroup = [Mon, Tue, Wedn, Thu, Fri, Sat, Sun]

            for i in range(7):
                self.leftLayout.addWidget(QLabel(weekday[i]), 5, 2*i + 1)
                self.leftLayout.addWidget(checkBoxGroup[i], 5, 2* i + 1 + 1)

    def setTimesEnable(self):
        self.editTimes.setEnabled(True)

    def setEndEnable(self):
        self.editEnd.setEnabled(True)


    def initLayout(self):
        self.leftLayout = QGridLayout(self)

        lblUnit = QLabel(u'频率单位')
        self.comboUnit = QComboBox()



        self.comboUnit.addItem(u"天")
        self.comboUnit.addItem(u"周")
        self.comboUnit.addItem(u"月")
        self.comboUnit.addItem(u"年")
        self.comboUnit.currentIndexChanged.connect(self.diffUnit)


        lblFre = QLabel(u'频率')
        editFre = QLineEdit()
        editFre.setFixedWidth(50)

        lblEnd = QLabel(u'结束时间')


        lblNever = QLabel(u'永不')
        radioNever = QRadioButton()

        radioTimes = QRadioButton()
        lblRepeat = QLabel(u'重复')

        lblTimes = QLabel(u'次后')
        self.editTimes = QLineEdit()
        self.editTimes.setFixedWidth(50)
        self.editTimes.setEnabled(False)
        radioTimes.clicked.connect(self.setTimesEnable)

        radioEnd = QRadioButton()
        lblEndDate = QLabel(u'结束日期')
        self.editEnd = calendarLineEdit(590, 370)
        self.editEnd.setEnabled(False)
        #self.editEnd.setFixedWidth(50)
        radioEnd.clicked.connect(self.setEndEnable)



        self.leftLayout.addWidget(lblUnit, 0, 0)
        self.leftLayout.addWidget(self.comboUnit, 0, 1)

        self.leftLayout.addWidget(lblEnd, 2, 0)
        #self.leftLayout.addWidget(editEnd, 2, 1)

        self.leftLayout.addWidget(lblNever, 2, 2)
        self.leftLayout.addWidget(radioNever, 2, 1)

        self.leftLayout.addWidget(radioTimes, 3, 1)
        self.leftLayout.addWidget(lblRepeat, 3, 2)
        self.leftLayout.addWidget(self.editTimes, 3, 3)
        self.leftLayout.addWidget(lblTimes, 3, 4)

        self.leftLayout.addWidget(radioEnd, 4, 1)
        self.leftLayout.addWidget(lblEndDate, 4, 2)
        self.leftLayout.addWidget(self.editEnd, 4, 3)



class CalendarWindow(QDialog):
    def __init__(self, x, y, printDate):
        super(CalendarWindow, self).__init__()
        self.printDate = printDate
        self.layout = QGridLayout(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showCalendar()
        self.layout.addWidget(self.cal, 0, 0)
        self.move(x, y)
        self.date = ""
        self.show()

    def showCalendar(self):
        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.click)


    def click(self):
        self.date = self.cal.selectedDate()
        self.printDate(self.date)
        self.close()




class calendarLineEdit(QLineEdit):
    def __init__(self, x, y):
        super(calendarLineEdit, self).__init__()
        self.setWindowTitle("Talendar")
        self.x = x
        self.y = y
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.calendar = CalendarWindow(self.x, self.y, self.printDate)
            if self.calendar.exec_():
                return
    def printDate(self, date):
        self.date = date
        self.setText(self.date.toString())

class Add(QDialog):
    def __init__(self):
        super(Add, self).__init__()
        self.setWindowTitle(u"新建")
        self.initLayout()
        self.resize(300, 100)
        self.show()

    def Repeat(self):
        repeatWindow = RepeatWindow()
        if repeatWindow.exec_():
            return


    def diffUnit(self, index):
        if self.comboReminder.currentIndex() == 0:
            pass
        else:
            self.editReminderTime = QLineEdit()
            self.comboReminderUnit = QComboBox()

            self.comboReminderUnit.addItem(u"分钟")
            self.comboReminderUnit.addItem(u"小时")
            self.comboReminderUnit.addItem(u"天")

            self.leftLayout.addWidget(self.editReminderTime, 6, 2)
            self.leftLayout.addWidget(self.comboReminderUnit, 6, 3)



    def initLayout(self):
        self.leftLayout = QGridLayout(self)

        lblTitle = QLabel(u'标题')
        editTitle = QLineEdit()

        lblStart = QLabel(u'开始时间')
        editStart = calendarLineEdit(590, 370)



        lblEnd = QLabel(u'结束时间')
        editEnd = calendarLineEdit(590, 390)

        lblLoc = QLabel(u'地点')
        editLoc = QLineEdit()

        lblNote = QLabel(u'备注')
        editNote = QTextEdit()

        lblRepeat = QLabel(u'重复')
        checkRepeat = QCheckBox()

        lblReminder = QLabel(u'提醒')
        self.comboReminder = QComboBox()

        self.comboReminder.addItem(u"无")
        self.comboReminder.addItem(u"提醒")
        self.comboReminder.addItem(u"电子邮件")
        self.comboReminder.currentIndexChanged.connect(self.diffUnit)

        self.buttonSon = QPushButton(u'创建子事件')
        self.buttonSon.clicked.connect(newWindow)

        self.leftLayout.addWidget(lblTitle, 0, 0)
        self.leftLayout.addWidget(editTitle, 0, 1)

        self.leftLayout.addWidget(lblStart, 1, 0)
        self.leftLayout.addWidget(editStart, 1, 1)

        self.leftLayout.addWidget(lblEnd, 2, 0)
        self.leftLayout.addWidget(editEnd, 2, 1)

        self.leftLayout.addWidget(lblLoc, 3, 0)
        self.leftLayout.addWidget(editLoc, 3, 1)

        self.leftLayout.addWidget(lblNote, 4, 0)
        self.leftLayout.addWidget(editNote, 4, 1)

        self.leftLayout.addWidget(lblRepeat, 5, 0)
        self.leftLayout.addWidget(checkRepeat, 5, 1)
        checkRepeat.stateChanged.connect(self.Repeat)

        self.leftLayout.addWidget(lblReminder, 6, 0)
        self.leftLayout.addWidget(self.comboReminder, 6, 1)
        self.leftLayout.addWidget(self.buttonSon, 7, 0)
        '''self.mainLayout = QGridLayout(self)
        self.mainLayout.setMargin(15)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setColumnStretch(1, 20)
        self.mainLayout.addLayout(self.leftLayout, 0, 0)'''


def newWindow(self):
    addWindow = Add()
    if addWindow.exec_():
        return


class Talendar(QWidget):

    def __init__(self):
        super(Talendar, self).__init__()
        self.setWindowTitle("Talendar")

        self.initGrid()
        self.resize(650, 500)
        #self.center()
        #self.current_row = 0
        #self.setGeometry(300, 300, 1000, 400)
        #elf.setWindowTitle('Talendar')
        #self.setWindowIcon(QtGui.QIcon('icon.png'))

    def initDB(self):
        pass



    def initGrid(self):


        self.initLeftGrid()
        self.initCalendarGrid()
        self.initMainGrid()


    def initMainGrid(self):
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setMargin(15)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setColumnStretch(1,20)
        self.mainLayout.addLayout(self.leftLayout, 0, 0)
        self.mainLayout.addLayout(self.calendarLayout, 0, 1)
        #self.mainLayout.addLayout(bottomLayout, 1, 0, 1, 2)
        #self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)


    def initLeftGrid(self):
        self.leftLayout = QVBoxLayout()
        #self.leftLayout.setMargin(10)

        btnUpdate = QPushButton(u'同步')
        self.leftLayout.addWidget(btnUpdate)
        btnNew = QPushButton(u'新建')
        self.leftLayout.addWidget(btnNew)

        btnNew.clicked.connect(newWindow)
        btnDDL = QPushButton(u'DDL列表')
        self.leftLayout.addWidget(btnDDL)
        btnSetting = QPushButton(u'设置')
        self.leftLayout.addWidget(btnSetting)

        self.leftLayout.addStretch(1)
        #self.leftLayout.setRowStretch(0, 1)
        #self.leftLayout.setRowStretch(1, 1)
        #self.leftLayout.setColumnStretch(0, 1)

    def fillBlank(self, flag, start, end):     #column 1 row 0
        for i in range(start, end):
            self.leftLayout.addWidget(QLabel(''),0, 0)

    def initCalendarGrid(self):
        self.calendarLayout = QGridLayout()
        self.grid = QTableWidget()


        #self.setCentralWidget(self.grid)

        self.grid.setColumnCount(7)
        self.grid.setRowCount(0)
        column_width = [75 for i in range(7)]
        for column in range(7):
            self.grid.setColumnWidth(column, column_width[column])
        headerlabels = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五', u'星期六', u'星期日']
        self.grid.setHorizontalHeaderLabels(headerlabels)
        self.grid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.grid.setSelectionBehavior(QAbstractItemView.SelectRows)


        self.calendarLayout.addWidget(self.grid)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def initUI(self):

        #self.c = Communicate()
        self.c.closeApp.connect(self.close)

        #self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()


    def mousePressEvent(self, event):

        self.c.closeApp.emit()


def main():

    app = QApplication(sys.argv)
    talendar = Talendar()
    talendar.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()