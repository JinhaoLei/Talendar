# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
reload(sys)
sys.setdefaultencoding('utf8')

class RepeatWindow(QDialog):    #勾选重复按钮后，弹出的重复设置
    def __init__(self):
        super(RepeatWindow, self).__init__()
        self.setWindowTitle(u"重复")
        self.initLayout()
        self.resize(300, 100)
        self.show()

    def diffUnit(self, index):
        weekday = [u'一', u'二', u'三', u'四', u'五', u'六', u'日']

        if self.comboUnit.currentIndex() == 1:
            self.leftLayout.addWidget(self.lblWeekRepeat, 5, 0)
            for i in range(7):
                self.leftLayout.addWidget(QLabel(weekday[i]), 5, 2*i + 1)
                self.leftLayout.addWidget(self.checkBoxGroup[i], 5, 2* i + 1 + 1)
        else:
            self.leftLayout.removeWidget(self.Mon)
            self.leftLayout.removeWidget(self.Tue)
            self.leftLayout.removeWidget(self.Wedn)
            self.leftLayout.removeWidget(self.Thu)
            self.leftLayout.removeWidget(self.Fri)
            self.leftLayout.removeWidget(self.Sat)
            self.leftLayout.removeWidget(self.Sun)



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

        self.lblWeekRepeat = QLabel(u'重复时间')

        self.Mon = QCheckBox()
        self.Tue = QCheckBox()
        self.Wedn = QCheckBox()
        self.Thu = QCheckBox()
        self.Fri = QCheckBox()
        self.Sat = QCheckBox()
        self.Sun = QCheckBox()
        self.checkBoxGroup = [self.Mon, self.Tue, self.Wedn, self.Thu, self.Fri, self.Sat, self.Sun]
        self.comboUnit.currentIndexChanged.connect(self.diffUnit)


        lblFre = QLabel(u'频率')
        self.editFre = QLineEdit()
        self.editFre.setFixedWidth(50)

        lblEnd = QLabel(u'结束时间')


        lblNever = QLabel(u'永不')
        self.radioNever = QRadioButton()

        self.radioTimes = QRadioButton()
        lblRepeat = QLabel(u'重复')

        lblTimes = QLabel(u'次后')
        self.editTimes = QLineEdit()
        self.editTimes.setFixedWidth(50)
        self.editTimes.setEnabled(False)
        self.radioTimes.clicked.connect(self.setTimesEnable)

        self.radioEnd = QRadioButton()
        lblEndDate = QLabel(u'结束日期')
        self.editEnd = calendarLineEdit(590, 370)
        self.editEnd.setEnabled(False)
        #self.editEnd.setFixedWidth(50)
        self.radioEnd.clicked.connect(self.setEndEnable)



        self.leftLayout.addWidget(lblUnit, 0, 0)
        self.leftLayout.addWidget(self.comboUnit, 0, 1)

        self.leftLayout.addWidget(lblFre, 1, 0)
        self.leftLayout.addWidget(self.editFre, 1, 1)

        self.leftLayout.addWidget(lblEnd, 2, 0)
        #self.leftLayout.addWidget(editEnd, 2, 1)

        self.leftLayout.addWidget(lblNever, 2, 2)
        self.leftLayout.addWidget(self.radioNever, 2, 1)

        self.leftLayout.addWidget(self.radioTimes, 3, 1)
        self.leftLayout.addWidget(lblRepeat, 3, 2)
        self.leftLayout.addWidget(self.editTimes, 3, 3)
        self.leftLayout.addWidget(lblTimes, 3, 4)

        self.leftLayout.addWidget(self.radioEnd, 4, 1)
        self.leftLayout.addWidget(lblEndDate, 4, 2)
        self.leftLayout.addWidget(self.editEnd, 4, 3)

        buttonsOkCancel = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttonsOkCancel.accepted.connect(self.accept)
        buttonsOkCancel.rejected.connect(self.reject)
        self.leftLayout.addWidget(buttonsOkCancel, 6, 1)
        self.leftLayout.addWidget(buttonsOkCancel, 6, 2)

class CalendarWindow(QDialog):   #日历选择控件
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

class calendarLineEdit(QLineEdit):   #点击会出现日历选择的编辑条
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

class Add(QDialog):               #新建事项窗口
    def __init__(self):
        super(Add, self).__init__()
        self.setWindowTitle(u"新建")
        self.initLayout()
        self.resize(300, 100)
        self.show()

    def Repeat(self):   #新建重复窗口
        repeatWindow = RepeatWindow()
        if repeatWindow.exec_():   #用户在重复窗口里选择OK，在退出时获得所有重复窗口里设置的参数
            comboUnit = repeatWindow.comboUnit.currentIndex()
            frequency = repeatWindow.editFre.text()
            radioSelected = [repeatWindow.radioNever.isChecked(), repeatWindow.radioTimes.isChecked(), repeatWindow.radioEnd.isChecked()]
            endTimes = repeatWindow.editTimes.text()
            endDate = repeatWindow.editEnd.text()
            checkBoxGroup = [repeatWindow.checkBoxGroup[i].isChecked() for i in range(7)]
            self.repeatParameters = [comboUnit, frequency, radioSelected, endTimes, endDate, checkBoxGroup]   #所有重复窗口里面设置的参数

    def diffUnit(self, index):
        if self.comboReminder.currentIndex() == 0:
            self.editReminderTime.setText("-1")
            self.comboReminderUnit.setCurrentIndex(-1)
        else:
            self.leftLayout.addWidget(self.editReminderTime, 6, 2)
            self.leftLayout.addWidget(self.comboReminderUnit, 6, 3)

    def AddTag(self):
        self.numOfClicked += 1
        self.tagGroup[self.numOfClicked - 1].show()

    def newSubWindow(self):  # 新建事项窗口的接口,只用于创建子事件
        addWindow = Add()
        if addWindow.exec_():  # 用户点击OK后，会获得所有设置的参数，包括在重复窗口里面获得的参数
            name = addWindow.editTitle.text()
            location = addWindow.editLoc.text()
            startDate = addWindow.editStartDate.text()
            startHour = addWindow.editStartHour.text()
            startMinute = addWindow.editStartMinute.text()
            endDate = addWindow.editEndDate.text()
            endHour = addWindow.editEndHour.text()
            endMinute = addWindow.editEndMinute.text()
            note = addWindow.editNote.toPlainText()
            ifCheckRepeat = addWindow.checkRepeat.isChecked()
            reminder = addWindow.comboReminder.currentIndex()
            reminderUnit = addWindow.comboReminderUnit.currentIndex()
            reminderNumber = addWindow.editReminderTime.text()
            tags = [unicode(addWindow.tagGroup[i].text()) for i in range(5)]
            repeatInfo = addWindow.repeatParameters
            sonID = -1  # 子事件没有子事件
            self.sonID = 999  # 给父级事件赋子事件

            print name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, note, ifCheckRepeat, reminder, reminderUnit, reminderNumber, tags, repeatInfo, sonID
            return

    def DeleteTag(self):
        self.tagGroup[self.numOfClicked - 1].hide()
        self.tagGroup[self.numOfClicked - 1].clear()
        self.numOfClicked -= 1

    def initLayout(self):
        self.leftLayout = QGridLayout(self)

        lblTitle = QLabel(u'标题')
        self.editTitle = QLineEdit()

        lblStart = QLabel(u'开始时间')
        self.editStartDate = calendarLineEdit(590, 370)

        self.editStartHour = QLineEdit()
        self.lblStartHour = QLabel(u'时')
        self.editStartMinute = QLineEdit()
        self.lblStartMinute = QLabel(u'分')
        lblEnd = QLabel(u'结束时间')
        self.editEndDate = calendarLineEdit(590, 390)

        self.editEndHour = QLineEdit()
        self.lblEndHour = QLabel(u'时')
        self.editEndMinute = QLineEdit()
        self.lblEndMinute = QLabel(u'分')

        lblLoc = QLabel(u'地点')
        self.editLoc = QLineEdit()

        lblTag = QLabel(u'标签')
        buttonAddTag = QPushButton(u'添加')
        self.numOfClicked = 0

        tagA = QLineEdit()
        tagB = QLineEdit()
        tagC = QLineEdit()
        tagD = QLineEdit()
        tagE = QLineEdit()
        self.tagGroup = [tagA, tagB, tagC, tagD, tagE]
        buttonAddTag.clicked.connect(self.AddTag)
        self.leftLayout.addWidget(buttonAddTag, 9, 1)
        self.leftLayout.addWidget(lblTag, 8, 0)

        for i in range(5):
            self.tagGroup[i].hide()
            self.leftLayout.addWidget(self.tagGroup[i], 8, i+1)
        buttonDeleteTag = QPushButton(u'删除')
        self.leftLayout.addWidget(buttonDeleteTag, 9, 2)
        buttonDeleteTag.clicked.connect(self.DeleteTag)

        lblNote = QLabel(u'备注')
        self.editNote = QTextEdit()


        lblRepeat = QLabel(u'重复')
        self.checkRepeat = QCheckBox()

        lblReminder = QLabel(u'提醒')
        self.comboReminder = QComboBox()

        self.comboReminder.addItem(u"无")
        self.comboReminder.addItem(u"提醒")
        self.comboReminder.addItem(u"电子邮件")
        self.editReminderTime = QLineEdit()
        self.comboReminderUnit = QComboBox()

        self.comboReminderUnit.addItem(u"分钟")
        self.comboReminderUnit.addItem(u"小时")
        self.comboReminderUnit.addItem(u"天")
        self.comboReminder.currentIndexChanged.connect(self.diffUnit)

        self.buttonSon = QPushButton(u'创建子事件')
        self.buttonSon.clicked.connect(self.newSubWindow)
        self.sonID = 999  #请改掉这一句

        self.leftLayout.addWidget(lblTitle, 0, 0)
        self.leftLayout.addWidget(self.editTitle, 0, 1)

        self.leftLayout.addWidget(lblStart, 1, 0)
        self.leftLayout.addWidget(self.editStartDate, 1, 1)
        self.leftLayout.addWidget(self.editStartHour, 1,2)
        self.leftLayout.addWidget(self.lblStartHour, 1, 3)
        self.leftLayout.addWidget(self.editStartMinute, 1, 4)
        self.leftLayout.addWidget(self.lblStartMinute, 1, 5)


        self.leftLayout.addWidget(lblEnd, 2, 0)
        self.leftLayout.addWidget(self.editEndDate, 2, 1)
        self.leftLayout.addWidget(self.editEndHour, 2, 2)
        self.leftLayout.addWidget(self.lblEndHour, 2, 3)
        self.leftLayout.addWidget(self.editEndMinute, 2, 4)
        self.leftLayout.addWidget(self.lblEndMinute, 2, 5)

        self.leftLayout.addWidget(lblLoc, 3, 0)
        self.leftLayout.addWidget(self.editLoc, 3, 1)

        self.leftLayout.addWidget(lblNote, 4, 0)
        self.leftLayout.addWidget(self.editNote, 4, 1)

        self.leftLayout.addWidget(lblRepeat, 5, 0)
        self.leftLayout.addWidget(self.checkRepeat, 5, 1)
        self.repeatParameters = []
        self.checkRepeat.stateChanged.connect(self.Repeat)

        self.leftLayout.addWidget(lblReminder, 6, 0)
        self.leftLayout.addWidget(self.comboReminder, 6, 1)
        self.leftLayout.addWidget(self.buttonSon, 7, 0)

        buttonsOkCancel = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttonsOkCancel.accepted.connect(self.accept)
        buttonsOkCancel.rejected.connect(self.reject)
        self.leftLayout.addWidget(buttonsOkCancel, 10, 1)
        self.leftLayout.addWidget(buttonsOkCancel, 10, 2)

        '''self.mainLayout = QGridLayout(self)
        self.mainLayout.setMargin(15)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setColumnStretch(1, 20)
        self.mainLayout.addLayout(self.leftLayout, 0, 0)'''



def newWindow(self):     #新建事项窗口的接口
    addWindow = Add()
    if addWindow.exec_():   #用户点击OK后，会获得所有设置的参数，包括在重复窗口里面获得的参数
        name = addWindow.editTitle.text()
        location = addWindow.editLoc.text()
        startDate = addWindow.editStartDate.text()
        startHour = addWindow.editStartHour.text()
        startMinute = addWindow.editStartMinute.text()
        endDate = addWindow.editEndDate.text()
        endHour = addWindow.editEndHour.text()
        endMinute = addWindow.editEndMinute.text()
        note = addWindow.editNote.toPlainText()
        ifCheckRepeat =  addWindow.checkRepeat.isChecked()
        reminder = addWindow.comboReminder.currentIndex()
        reminderUnit = addWindow.comboReminderUnit.currentIndex()
        reminderNumber = addWindow.editReminderTime.text()
        tags = [unicode(addWindow.tagGroup[i].text()) for i in range(5)]
        repeatInfo = addWindow.repeatParameters
        sonID = addWindow.sonID
        print name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, note, ifCheckRepeat, reminder, reminderUnit, reminderNumber, tags, repeatInfo, sonID
        return

class DDL(QWidget): #DDL列表界面
    def __init__(self):
        super(DDL, self).__init__()
        self.initUI()

    def Repeat(self):
        repeatWindow = RepeatWindow()
        if repeatWindow.exec_():
            return

    def initUI(self):

        self.mainLayout = QGridLayout(self)
        self.initToolBar()
        self.initRight()
        self.mainLayout.addLayout(self.toolbar,0,0)
        self.mainLayout.addLayout(self.right,0,1)

       # self.toolbar = QVBoxLayout()
        ##self.toolbar.addWidget(btnNew)

        #self.toolbar.addStretch(1)


        self.move(300, 150)
       # self.setWindowTitle('Calculator')
       # self.show()
        self.setWindowTitle(u"Deadline")





        self.resize(300, 300)
        self.show()


    def initToolBar(self):
        self.toolbar = QVBoxLayout()
        btnNew = QPushButton(u'新建')
        self.toolbar.addWidget(btnNew)
        btnDelete = QPushButton(u'删除')
        self.toolbar.addWidget(btnDelete)

        self.toolbar.addStretch(1)

    def initRight(self):
        self.right =QVBoxLayout()
        issue = QPushButton(U'DDL1')
        self.right.addWidget(issue)
        self.right.addStretch(1)

def newDDL(self):
    addWindow = DDL()
    if addWindow.exec_():
        return

class Talendar(QWidget):#主界面

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


        self.initLeftGrid()   #初始化左侧菜单栏
        self.initCalendarGrid()   #初始化右侧日历表格界面
        self.initMainGrid()    #构建主布局


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
        btnDDL.clicked.connect(newDDL)
        #self.leftLayout.setRowStretch(0, 1)
        #self.leftLayout.setRowStretch(1, 1)
        #self.leftLayout.setColumnStretch(0, 1)

    def fillBlank(self, flag, start, end):     #column 1 row 0
        for i in range(start, end):
            self.leftLayout.addWidget(QLabel(''),0, 0)

    def initCalendarGrid(self):
        self.calendarLayout = QGridLayout()
        self.grid = QTableWidget()
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