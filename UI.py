# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import time,localtime,strftime
from datetime import datetime
from datetime import timedelta
from calendar import monthrange

reload(sys)
sys.setdefaultencoding('utf8')


class RepeatWindow(QDialog):  # 勾选重复按钮后，弹出的重复设置
    def __init__(self):
        super(RepeatWindow, self).__init__()
        self.setWindowTitle(u"重复")
        self.setModal(True)
        self.initLayout()
        self.resize(300, 100)
        self.rejectFlag = 0
        self.show()

    def diffUnit(self, index):


        if self.comboUnit.currentIndex() == 1:
            for i in range(7):
                self.checkBoxGroup[i].show()
                self.lblGroup[i].show()
                self.lblWeekRepeat.show()
        else:
            for i in range(7):
                self.checkBoxGroup[i].hide()
                self.lblGroup[i].hide()
                self.lblWeekRepeat.hide()
                self.checkBoxGroup[i].setChecked(False)

    def setTimesEnable(self):
        self.editTimes.setEnabled(True)
        self.editEnd.setEnabled(False)
        self.editEnd.clear()

    def setEndEnable(self):
        self.editEnd.setEnabled(True)
        self.editTimes.setEnabled(False)
        self.editTimes.clear()

    def setNeverEnable(self):
        #self.editNever.setEnabled(True)
        self.editTimes.setEnabled(False)
        self.editEnd.setEnabled(False)
        self.editTimes.clear()
        self.editEnd.clear()

    def initLayout(self):
        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()
        self.middleLayout = QGridLayout()


        lblUnit = QLabel(u'频率单位')
        lblUnit.setMaximumWidth(50)
        self.comboUnit = QComboBox()
        self.comboUnit.setMaximumWidth(50)
        lblFre = QLabel(u'频率')
        lblFre.setMaximumWidth(50)
        self.editFre = QLineEdit()
        self.editFre.setMaximumWidth(50)


        self.comboUnit.addItem(u"天")
        self.comboUnit.addItem(u"周")
        self.comboUnit.addItem(u"月")
        self.comboUnit.addItem(u"年")

        self.lblWeekRepeat = QLabel(u'重复时间')
        #self.lblWeekRepeat.setMaximumWidth(50)

        self.Mon = QCheckBox()
        self.Tue = QCheckBox()
        self.Wedn = QCheckBox()
        self.Thu = QCheckBox()
        self.Fri = QCheckBox()
        self.Sat = QCheckBox()
        self.Sun = QCheckBox()

        self.lblMon = QLabel(u'一')
        self.lblTue = QLabel(u'二')
        self.lblWedn = QLabel(u'三')
        self.lblThu = QLabel(u'四')
        self.lblFri = QLabel(u'五')
        self.lblSat = QLabel(u'六')
        self.lblSun = QLabel(u'日')
        self.checkBoxGroup = [self.Mon, self.Tue, self.Wedn, self.Thu, self.Fri, self.Sat, self.Sun]
        self.lblGroup = [self.lblMon, self.lblTue, self.lblWedn, self.lblThu, self.lblFri, self.lblSat, self.lblSun]
        self.comboUnit.currentIndexChanged.connect(self.diffUnit)



        lblEnd = QLabel(u'结束时间')
        lblNever = QLabel(u'永不')
        self.radioNever = QRadioButton()
        self.radioNever.setMaximumWidth(20)
        self.radioTimes = QRadioButton()
        lblRepeat = QLabel(u'重复')
        lblTimes = QLabel(u'次后')
        lblTimes.setMaximumWidth(50)
        self.editTimes = QLineEdit()
        self.editTimes.setMaximumWidth(30)
        self.editTimes.setEnabled(False)
        self.radioTimes.clicked.connect(self.setTimesEnable)
        self.radioNever.clicked.connect(self.setNeverEnable)
        self.radioEnd = QRadioButton()
        lblEndDate = QLabel(u'结束日期')
        self.editEnd = calendarLineEdit(660, 410)
        self.editEnd.setEnabled(False)
        #self.editEnd.setMaximumWidth(170)
        self.editEnd.setFixedWidth(110)
        self.radioEnd.clicked.connect(self.setEndEnable)



        self.topLayout.addWidget(lblUnit, 0, 0)
        self.topLayout.addWidget(self.comboUnit, 0, 1)
        self.topLayout.addWidget(lblFre, 1, 0)
        self.topLayout.addWidget(self.editFre, 1, 1)
        self.topHLayout = QHBoxLayout()
        self.topHLayout.addLayout(self.topLayout)
        self.topHLayout.addStretch()
        #topSpace = QSpacerItem(200, 1)
        #self.topLayout.addItem(topSpace, 0, 2)
        #self.topLayout.setColumnStretch(0, 5)
        #self.topLayout.setColumnStretch(1, 1)
        #self.topLayout.setColumnStretch(2, 5)
        #self.topLayout.setColumnStretch(0, 1)
        #self.topLayout.setColumnStretch(1, 3)

        self.middleLayout.addWidget(lblEnd, 0, 0)
        self.middleLayout.addWidget(self.radioNever, 0, 1)
        self.middleLayout.addWidget(lblNever, 0, 2)
        self.middleLayout.addWidget(self.radioTimes, 1, 1)
        self.middleLayout.addWidget(lblRepeat, 1, 2)
        self.middleLayout.addWidget(self.editTimes, 1, 3)
        self.middleLayout.addWidget(lblTimes, 1, 4)
        self.middleLayout.addWidget(self.radioEnd, 2, 1)
        self.middleLayout.addWidget(lblEndDate, 2, 2)
        self.middleLayout.addWidget(self.editEnd, 2, 3, 1, 2)
        self.editEnd.setMaximumWidth(50)
        self.middleHLayout = QHBoxLayout()
        self.middleHLayout.addLayout(self.middleLayout)
        self.middleHLayout.addStretch()


        self.bottomLayout.addWidget(self.lblWeekRepeat, 0, 0)
        self.lblWeekRepeat.hide()
        # weekday = [u'一', u'二', u'三', u'四', u'五', u'六', u'日']
        for i in range(7):
            self.bottomLayout.addWidget(self.lblGroup[i], 0, 2 * i + 1)
            self.bottomLayout.addWidget(self.checkBoxGroup[i], 0, 2 * i + 1 + 1)
            self.checkBoxGroup[i].hide()
            self.lblGroup[i].hide()
        self.bottomHLayout = QHBoxLayout()
        self.bottomHLayout.addLayout(self.bottomLayout)
        self.bottomHLayout.addStretch()

        buttonsOkCancel = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttonsOkCancel.accepted.connect(self.accept)
        buttonsOkCancel.rejected.connect(self.reject)

        self.bottomCancelLayout = QHBoxLayout()
        self.bottomCancelLayout.addStretch()
        self.bottomCancelLayout.addWidget(buttonsOkCancel)

        #self.bottomLayout.addWidget(buttonsOkCancel, 1, 2)

        self.mainLayout = QGridLayout(self)

        self.mainLayout.addLayout(self.topHLayout, 0, 0)
        #self.mainLayout.addLayout(self.spaceLayout, 1, 0)
        self.mainLayout.addLayout(self.middleHLayout, 1, 0)
        self.mainLayout.addLayout(self.bottomHLayout, 2, 0)
        self.mainLayout.addLayout(self.bottomCancelLayout, 3, 0)


class CalendarWindow(QDialog):  # 日历选择控件
    def __init__(self, x, y, printDate):
        super(CalendarWindow, self).__init__()
        self.printDate = printDate
        self.setModal(True)
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


class calendarLineEdit(QLineEdit):  # 点击会出现日历选择的编辑条
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


class Add(QDialog):  # 新建事项窗口
    def __init__(self):
        super(Add, self).__init__()
        self.setWindowTitle(u"新建")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setModal(True)
        self.initLayout()
        self.setFixedSize(500, 500)
        # self.setFixedSize(self.width(), self.height())
        self.show()

    def Repeat(self):  # 新建重复窗口

        repeatWindow = RepeatWindow()
        self.repeatParameters = []
        if repeatWindow.exec_():  # 用户在重复窗口里选择OK，在退出时获得所有重复窗口里设置的参数

            comboUnit = repeatWindow.comboUnit.currentIndex()
            frequency = repeatWindow.editFre.text()
            radioSelected = [repeatWindow.radioNever.isChecked(), repeatWindow.radioTimes.isChecked(),
                                     repeatWindow.radioEnd.isChecked()]
            endTimes = repeatWindow.editTimes.text()
            endDate = repeatWindow.editEnd.text()
            checkBoxGroup = [repeatWindow.checkBoxGroup[i].isChecked() for i in range(7)]
            self.repeatParameters = [comboUnit, frequency, radioSelected, endTimes, endDate,
                                             checkBoxGroup]  # 所有重复窗口里面设置的参数
            print checkBoxGroup


    def diffUnit(self, index):
        if self.comboReminder.currentIndex() == 0:
            self.editReminderTime.setText("-1")
            self.comboReminderUnit.setCurrentIndex(-1)
            self.editReminderTime.clear()
            self.editReminderTime.hide()
            self.comboReminderUnit.hide()
        else:
            self.editReminderTime.show()
            self.comboReminderUnit.show()
            self.comboReminderUnit.setCurrentIndex(0)

    def AddTag(self):
        self.numOfClicked += 1
        self.tagGroup[self.numOfClicked - 1].setEnabled(True)

    def newSubWindow(self):  # 新建事项窗口的接口,只用于创建子事件
        addWindow = Add()
        #addWindow.buttonSon.hide()
        addWindow.buttonSon.setEnabled(False)
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
            #ifCheckRepeat = addWindow.checkRepeat.isChecked()
            reminder = addWindow.comboReminder.currentIndex()
            reminderUnit = addWindow.comboReminderUnit.currentIndex()
            reminderNumber = addWindow.editReminderTime.text()
            tags = [unicode(addWindow.tagGroup[i].text()) for i in range(5)]
            repeatInfo = addWindow.repeatParameters
            #sonID = self.sonID  # 子事件没有子事件
            #self.sonID += 1
            #self.sonIDList.append(self.sonID)  # 给父级事件赋子事件
            sonIDList = []
            self.sonIDList.append(self.sonID)
            self.sonID += 1
            print name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, note, reminder, reminderUnit, reminderNumber, tags, repeatInfo, sonIDList
            # print repeatInfo
            return

    def DeleteTag(self):
        self.tagGroup[self.numOfClicked - 1].setEnabled(False)
        self.tagGroup[self.numOfClicked - 1].clear()
        self.numOfClicked -= 1

    def initLayout(self):
        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()
        lblTitle = QLabel(u'标题')
        lblTitle.setMaximumWidth(100)
        self.editTitle = QLineEdit()

        lblStart = QLabel(u'开始时间')
        # lblStart.setMaximumWidth(50)
        self.editStartDate = calendarLineEdit(510, 170)
        self.editStartDate.setMaximumWidth(110)
        self.editStartHour = QLineEdit()
        self.editStartHour.setMaximumWidth(30)
        self.lblStartHour = QLabel(u'时')
        self.editStartMinute = QLineEdit()
        self.editStartMinute.setMaximumWidth(30)
        self.lblStartMinute = QLabel(u'分')
        lblEnd = QLabel(u'结束时间')

        self.editEndDate = calendarLineEdit(510, 200)
        self.editEndDate.setMaximumWidth(110)
        self.editEndHour = QLineEdit()
        self.lblEndHour = QLabel(u'时')
        self.lblEndHour.setMaximumWidth(30)
        self.editEndMinute = QLineEdit()
        self.editEndMinute.setMaximumWidth(30)
        self.editEndHour.setMaximumWidth(30)
        self.lblEndMinute = QLabel(u'分')
        # self.lblEndMinute.setMaximumWidth(110)


        lblLoc = QLabel(u'地点')
        self.editLoc = QLineEdit()

        lblNote = QLabel(u'备注')
        self.editNote = QTextEdit()

        lblRepeat = QLabel(u'重复')
        self.buttonRepeat = QPushButton(u'...')
        self.buttonRepeat.setMaximumWidth(30)

        lblReminder = QLabel(u'提醒')
        self.comboReminder = QComboBox()
        lblReminder.setMaximumWidth(70)
        self.comboReminder.setMaximumWidth(70)

        self.comboReminder.addItem(u"无")
        self.comboReminder.addItem(u"提醒")
        self.comboReminder.addItem(u"电子邮件")
        self.editReminderTime = QLineEdit()
        self.editReminderTime.setMaximumWidth(30)
        self.comboReminderUnit = QComboBox()
        #self.comboReminderUnit.setMaximumWidth(30)

        self.comboReminderUnit.addItem(u"分钟")
        self.comboReminderUnit.addItem(u"小时")
        self.comboReminderUnit.addItem(u"天")
        self.topLayout.addWidget(self.editReminderTime, 6, 2)
        self.topLayout.addWidget(self.comboReminderUnit, 6, 3, 1, 2)
        self.editReminderTime.hide()
        self.comboReminderUnit.hide()
        self.comboReminder.currentIndexChanged.connect(self.diffUnit)

        self.buttonSon = QPushButton(u'创建子事件')
        self.buttonSon.clicked.connect(self.newSubWindow)
        self.buttonSon.setMaximumWidth(70)
        self.sonIDList = []  # 请改掉这一句
        self.sonID = 0

        self.topLayout.addWidget(lblTitle, 0, 0)
        self.topLayout.addWidget(self.editTitle, 0, 1, 1, 5)
        self.topLayout.addWidget(lblStart, 1, 0)
        self.topLayout.addWidget(self.editStartDate, 1, 1)
        self.topLayout.addWidget(self.editStartHour, 1, 2)
        self.topLayout.addWidget(self.lblStartHour, 1, 3)
        self.topLayout.addWidget(self.editStartMinute, 1, 4)
        self.topLayout.addWidget(self.lblStartMinute, 1, 5)
        self.topLayout.addWidget(lblEnd, 2, 0)
        self.topLayout.addWidget(self.editEndDate, 2, 1)
        self.topLayout.addWidget(self.editEndHour, 2, 2)
        self.topLayout.addWidget(self.lblEndHour, 2, 3)
        self.topLayout.addWidget(self.editEndMinute, 2, 4)
        self.topLayout.addWidget(self.lblEndMinute, 2, 5)
        self.topLayout.addWidget(lblLoc, 3, 0)
        self.topLayout.addWidget(self.editLoc, 3, 1, 1, 5)
        self.topLayout.addWidget(lblNote, 4, 0)
        self.topLayout.addWidget(self.editNote, 4, 1, 1, 5)
        self.topLayout.addWidget(lblRepeat, 5, 0)
        self.topLayout.addWidget(self.buttonRepeat, 5, 1)
        self.repeatParameters = []
        self.buttonRepeat.clicked.connect(self.Repeat)
        self.topLayout.addWidget(lblReminder, 6, 0)
        self.topLayout.addWidget(self.comboReminder, 6, 1)

        lblTag = QLabel(u'标签')
        #lblTag.setMaximumWidth(1000)
        buttonAddTag = QPushButton(u'添加')
        # buttonAddTag.setMaximumWidth(150)
        self.numOfClicked = 0

        tagA = QLineEdit()
        tagB = QLineEdit()
        tagC = QLineEdit()
        tagD = QLineEdit()
        tagE = QLineEdit()
        self.tagGroup = [tagA, tagB, tagC, tagD, tagE]
        buttonAddTag.clicked.connect(self.AddTag)
        for i in range(5):
            self.tagGroup[i].setEnabled(False)
            self.tagGroup[i].setMaximumWidth(90)
            self.bottomLayout.addWidget(self.tagGroup[i], 0, i + 1)
        buttonDeleteTag = QPushButton(u'删除')
        # buttonDeleteTag.setMaximumWidth(91)

        buttonDeleteTag.clicked.connect(self.DeleteTag)
        self.bottomLayout.addWidget(buttonAddTag, 1, 1)
        self.bottomLayout.addWidget(buttonDeleteTag, 1, 2)
        buttonAddTag.setMaximumWidth(70)
        buttonDeleteTag.setMaximumWidth(70)
        self.bottomLayout.addWidget(lblTag, 0, 0)
        # lblTag.setMaximumWidth(90)



        self.mainLayout = QGridLayout(self)
        # self.mainLayout.setMargin(150)
        # self.bottomLayout.setMargin(50)
        # self.mainLayout.setColumnStretch(1, 20)
        self.mainLayout.addLayout(self.topLayout, 0, 0)
        self.mainLayout.addLayout(self.bottomLayout, 1, 0)

        buttonsOkCancel = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttonsOkCancel.accepted.connect(self.accept)
        buttonsOkCancel.rejected.connect(self.reject)
        # buttonsOkCancel.setMaximumWidth(50)
        # self.bottomLayout.addWidget(QSpacerItem, 2, 0)
        self.bottomLayout.addWidget(buttonsOkCancel, 3, 4, 1, 2)
        self.bottomLayout.addWidget(self.buttonSon, 3, 0)
        # self.bottomLayout.addWidget(buttonsOkCancel, 10, 2)

        '''self.mainLayout = QGridLayout(self)
        self.mainLayout.setMargin(15)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setColumnStretch(1, 20)
        self.mainLayout.addLayout(self.topLayout, 0, 0)'''


def newWindow(self):  # 新建事项窗口的接口
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
        reminder = addWindow.comboReminder.currentIndex()
        reminderUnit = addWindow.comboReminderUnit.currentIndex()
        reminderNumber = addWindow.editReminderTime.text()
        tags = [unicode(addWindow.tagGroup[i].text()) for i in range(5)]
        repeatInfo = addWindow.repeatParameters
        sonIDList = addWindow.sonIDList
          # 给父级事件赋子事件
        print name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, note, reminder, reminderUnit, reminderNumber, tags, repeatInfo, sonIDList
        #print repeatInfo
        return


class DDL(QWidget):  # DDL列表界面
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
        self.mainLayout.addLayout(self.toolbar, 0, 0)
        self.mainLayout.addLayout(self.right, 0, 1)

        # self.toolbar = QVBoxLayout()
        ##self.toolbar.addWidget(btnNew)

        # self.toolbar.addStretch(1)


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
        self.right = QVBoxLayout()
        issue = QPushButton(U'DDL1')
        self.right.addWidget(issue)
        self.right.addStretch(1)


def newDDL(self):
    addWindow = DDL()
    if addWindow.exec_():
        return


class Talendar(QWidget):  # 主界面

    def __init__(self):
        super(Talendar, self).__init__()
        self.headerlabels = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五', u'星期六', u'星期日']
        self.setWindowTitle("Talendar")
        self.date=datetime.now()
        self.rowNum=24 

        self.resize(695, 500)
        #self.tableDict={u'一':0,u'二':1,u'三':2,u'四':3,u'五':4,u'六':5,u'日':6}
        self.tableDict = {u'Mon': 0, u'Tue': 1, u'Wed': 2, u'Thu': 3, u'Fri': 4, u'Sat': 5, u'Sun': 6}
        self.pageFlag='w'
        self.initGrid()

        pal = QPalette()

        pal.setColor(self.backgroundRole(), QColor(55, 62, 150))
        self.setPalette(pal)
        # self.center()
        # self.current_row = 0
        # self.setGeometry(300, 300, 1000, 400)
        # elf.setWindowTitle('Talendar')
        # self.setWindowIcon(QtGui.QIcon('icon.png'))

    def initDB(self):
        pass

    def initGrid(self):
        self.initLeftGrid()  # 初始化左侧菜单栏
        self.initCalendarGrid()  # 初始化右侧日历表格界面
        self.initTopGrid()
        self.initMainGrid()  # 构建主布局
	

    def initTopGrid(self):#updated
        self.topLayout=QHBoxLayout()
        
        self.year=QLabel(self.date.strftime("%Y"))
	    #self.topLayout.addWidget(self.year)
        upperPage = QPushButton(u'上一页')
        self.topLayout.addWidget(upperPage)
        upperPage.clicked.connect(self.upPage)
        nextPage = QPushButton(u'下一页')
        self.topLayout.addWidget(nextPage)


        nextPage.clicked.connect(self.nextPage)

    def initMainGrid(self):
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setRowStretch(0,10)
        self.mainLayout.setRowStretch(1,1)
        self.mainLayout.setRowMinimumHeight(1,0)
        


        self.mainLayout.addLayout(self.leftLayout, 0, 0)
        self.tempLayout=QVBoxLayout()
        self.tempLayout.addLayout(self.topLayout)
        self.tempLayout.addLayout(self.calendarLayout)
        #self.mainLayout.addLayout(self.calendarLayout, 1, 1 )
        #self.mainLayout.addLayout(self.topLayout,0,1)
        #self.topLayout.setMaximumWidth(20)
        self.mainLayout.addLayout(self.tempLayout,0,1)




    def initLeftGrid(self):
        self.leftLayout = QVBoxLayout()
        # self.leftLayout.setMargin(10)

        btnUpdate = QPushButton(u'同步')
        self.leftLayout.addWidget(btnUpdate)
        btnNew = QPushButton()
        self.leftLayout.addWidget(btnNew)
        btnNew.setFixedSize(70, 70)
        btnNew.setStyleSheet("border-image:url(new.png)")

        btnNew.clicked.connect(newWindow)
        btnDDL = QPushButton(u'DDL列表')
        self.leftLayout.addWidget(btnDDL)
        btnSetting = QPushButton(u'设置')
        self.leftLayout.addWidget(btnSetting)

        self.leftLayout.addStretch(1)
        btnDDL.clicked.connect(newDDL)
        ##############updated###################
        change=QPushButton(u'视图转换')
        change.clicked.connect(self.Transform)
        self.leftLayout.addWidget(change)

        # self.leftLayout.setRowStretch(0, 1)
        # self.leftLayout.setRowStretch(1, 1)
        # self.leftLayout.setColumnStretch(0, 1)

    def fillBlank(self, flag, start, end):  # column 1 row 0
        for i in range(start, end):
            self.leftLayout.addWidget(QLabel(''), 0, 0)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        # self.c = Communicate()
        self.c.closeApp.connect(self.close)

        # self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, event):
        self.c.closeApp.emit()

    ########################### updated part#################
    def initCalendarGrid(self):



        self.grid=self.WeekGrid()
        self.calendarLayout = QGridLayout()
        
        self.calendarLayout.addWidget(self.grid)

    def Transform(self):
        if self.pageFlag=='w':
            self.date=datetime.now()
            self.grid.close()
            self.grid=self.MonthGrid()
            self.calendarLayout.addWidget(self.grid)
            self.pageFlag='m'
        else:
            self.date=datetime.now()
            self.grid.close()
            self.grid=self.WeekGrid()
            self.calendarLayout.addWidget(self.grid)
            self.pageFlag='w'


    def WeekGrid(self):
        rowNum = self.rowNum       
        grid = QTableWidget()
        grid.setColumnCount(7)
        grid.setRowCount(self.rowNum)
        column_width = [75 for i in range(7)]
        for column in range(7):
            grid.setColumnWidth(column, column_width[column])
        for row in range(rowNum):
            grid.setRowHeight(row, 55)


        grid.setHorizontalHeaderLabels(self.headerlabels)
        grid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        grid.setSelectionBehavior(QAbstractItemView.SelectRows)



        rowlabels = []

        for i in range(self.rowNum):

            rowlabels.append(str(i+1))


        grid.setVerticalHeaderLabels(rowlabels)
        if self.date.strftime("%Y%m%d")==strftime("%Y%m%d"):
            for i in range(self.rowNum):
                today=QTableWidgetItem('')
                todayCol=self.tableDict[self.date.strftime("%a").decode('utf-8')]
       
                today.setBackground(QBrush(QColor(Qt.yellow)))
                grid.setItem(i,todayCol,today)
        return grid

    def MonthGrid(self):
        beginDay=datetime(int(self.date.strftime("%Y")),int(self.date.strftime("%m")),1)
        beginRow=0
        beginCol=self.tableDict[beginDay.strftime("%a").decode('utf-8')]
        monthTime=monthrange(int(self.date.strftime("%Y")),int(self.date.strftime("%m")))[1]
        todayCol=self.tableDict[self.date.strftime("%a").decode('utf-8')]
        todayRow=(int(self.date.strftime("%d"))+beginCol-1)/7
        mrowNum=(beginCol+monthTime+6)/7
        grid=QTableWidget()
        grid.setColumnCount(7)
        grid.setRowCount(mrowNum)
        column_width=[75 for i in range(7)]
        for column in range(7):
            grid.setColumnWidth(column,column_width[column])
        for row in range(mrowNum):
            grid.setRowHeight(row,85)

        grid.setHorizontalHeaderLabels(self.headerlabels)
        grid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        grid.setSelectionBehavior(QAbstractItemView.SelectRows)
        today=QTableWidgetItem(self.date.strftime("%m-%d"))
        if self.date.strftime("%Y%m%d")==strftime("%Y%m%d"):   
            today.setBackground(QBrush(QColor(Qt.yellow)))
        today.setTextAlignment(Qt.AlignCenter)
        grid.setItem(todayRow,todayCol,today)
        for day in range(monthTime):
            if not day==int(self.date.strftime("%d"))-1:
                tempDay=QTableWidgetItem(beginDay.strftime("%m-%d"))
                tempCol=beginCol
                tempRow=beginRow
                tempDay.setTextAlignment(Qt.AlignCenter)
                grid.setItem(tempRow,tempCol,tempDay)
            beginCol+=1
            beginRow=beginRow+beginCol/7
            beginCol=beginCol%7
            beginDay=beginDay+timedelta(1)

        return grid

    def upPage(self):
        if self.pageFlag=='w':
            self.grid.close()
            self.grid=self.wupPage()
            self.calendarLayout.addWidget(self.grid)
        else:
            self.grid.close()
            self.grid=self.mupPage()
            self.calendarLayout.addWidget(self.grid)

    def nextPage(self):
        if self.pageFlag=='w':
            self.grid.close()
            self.grid=self.wnextPage()
            self.calendarLayout.addWidget(self.grid)

        else:
            self.grid.close()
            self.grid=self.mnextPage()
            self.calendarLayout.addWidget(self.grid)
            

    def mupPage(self):
        month=int(self.date.strftime('%m'))
        year=int(self.date.strftime('%Y'))
        if month==1:
            year=year-1
            month=12
        else:
            month=month-1
        self.date=self.date-timedelta(monthrange(year,month)[1])
        return self.MonthGrid()

    def mnextPage(self):
        month=int(self.date.strftime('%m'))
        year=int(self.date.strftime('%Y'))
        self.date=self.date+timedelta(monthrange(year,month)[1])
        return self.MonthGrid()



    def wupPage(self):
        self.date = self.date - timedelta(days= 7)
        return self.WeekGrid()

    def wnextPage(self):

        self.date = self.date + timedelta(days= 7)
        return self.WeekGrid()

def main():
    app = QApplication(sys.argv)
    #mainPage = MainPage()
    talendar = Talendar()
    talendar.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


