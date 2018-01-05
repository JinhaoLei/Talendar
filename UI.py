# -*- coding: utf-8 -*-

import sys
#import sync
import client
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from utils import *
from time import time, localtime, strftime
from datetime import datetime
from datetime import timedelta
from calendar import monthrange
from functools import partial
import os
import chardet
import os.path
import time
import re
reload(sys)
sys.setdefaultencoding('utf8')

FONT_SIZE = 10
FONT_TYPE = "SimHei"
NEW_FONT_TYPE = "YouYuan"
NEW_FONT_SIZE = 10
ROW_HEIGHT = 90
COL_WIDTH = 100

def getFont():
    font = QFont()
    font.setFamily(NEW_FONT_TYPE)
    font.setBold(True)
    font.setPointSize(NEW_FONT_SIZE)
    return font


class RepeatWindow(QDialog):  # 勾选重复按钮后，弹出的重复设置
    def __init__(self, weekday):
        super(RepeatWindow, self).__init__()
        self.setWindowTitle(u"重复")
        self.setModal(True)
        self.initLayout()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(296, 197)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.flagB = 0
        self.background = QPixmap()
        self.weekday = weekday
        self.rejectFlag = 0
        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        if self.flagB == 0:
            self.setFixedSize(296, 197)
            self.background.load("./pic/repeat_small.png")
            p.drawPixmap(0, 0, 296, 197, self.background)
        elif self.flagB == 1:
            self.setFixedSize(374, 216)
            self.setContentsMargins(5,0,0,0)
            self.background.load("./pic/repeat_big.png")
            p.drawPixmap(0, 0, 374, 216, self.background)

    def diffUnit(self, index):

        if self.comboUnit.currentIndex() == 1:
            self.flagB = 1
            for i in range(7):
                self.checkBoxGroup[i].show()
                self.lblGroup[i].show()
                self.lblWeekRepeat.show()
                if i==self.weekday:
                    self.checkBoxGroup[i].setChecked(True)
        else:
            self.flagB = 0
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
        self.editTimes.setEnabled(False)
        self.editEnd.setEnabled(False)
        self.editTimes.clear()
        self.editEnd.clear()

    def initLayout(self):

        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()
        self.middleLayout = QGridLayout()

        lblUnit = QLabel(u'频率单位')
        lblUnit.setStyleSheet("color:white")
        lblUnit.setFont(getFont())
        lblUnit.setMaximumWidth(80)

        self.comboUnit = QComboBox()
        self.comboUnit.setMaximumWidth(50)

        lblFre = QLabel(u'频率')
        lblFre.setFont(getFont())
        lblFre.setStyleSheet("color:white")
        lblFre.setMaximumWidth(50)

        self.editFre = QLineEdit()
        self.editFre.setMaximumWidth(50)

        self.comboUnit.addItem(u"天")
        self.comboUnit.addItem(u"周")
        self.comboUnit.addItem(u"月")
        self.comboUnit.addItem(u"年")

        self.lblWeekRepeat = QLabel(u'重复时间')
        self.lblWeekRepeat.setFont(getFont())
        self.lblWeekRepeat.setStyleSheet("color:white")

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
        for lbl in self.lblGroup:
            lbl.setStyleSheet("color:white")
            lbl.setFont(getFont())

        lblEnd = QLabel(u'结束时间')
        lblEnd.setStyleSheet("color:white")
        lblEnd.setFont(getFont())

        lblNever = QLabel(u'永不')
        lblNever.setFont(getFont())
        lblNever.setStyleSheet("color:white")

        self.radioNever = QRadioButton()
        self.radioNever.setMaximumWidth(20)
        self.radioTimes = QRadioButton()

        lblRepeat = QLabel(u'重复')
        lblRepeat.setStyleSheet("color:white")
        lblRepeat.setFont(getFont())

        lblTimes = QLabel(u'次后')
        lblTimes.setFont(getFont())
        lblTimes.setStyleSheet("color:white")
        lblTimes.setMaximumWidth(50)

        self.editTimes = QLineEdit()
        self.editTimes.setMaximumWidth(30)
        self.editTimes.setEnabled(False)

        self.radioTimes.clicked.connect(self.setTimesEnable)
        self.radioNever.clicked.connect(self.setNeverEnable)
        self.radioEnd = QRadioButton()
        self.radioEnd.clicked.connect(self.setEndEnable)

        lblEndDate = QLabel(u'结束日期')
        lblEndDate.setFont(getFont())
        lblEndDate.setStyleSheet("color:white")

        self.editEnd = CalendarLineEdit(660, 410)
        self.editEnd.setEnabled(False)
        self.editEnd.setFixedWidth(110)
        self.editEnd.setMaximumWidth(50)

        self.topLayout.addWidget(lblUnit, 0, 0)
        self.topLayout.addWidget(self.comboUnit, 0, 1)
        self.topLayout.addWidget(lblFre, 1, 0)
        self.topLayout.addWidget(self.editFre, 1, 1)

        self.topHLayout = QHBoxLayout()
        self.topHLayout.addLayout(self.topLayout)
        self.topHLayout.addStretch()

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


        self.middleHLayout = QHBoxLayout()
        self.middleHLayout.addLayout(self.middleLayout)
        self.middleHLayout.addStretch()

        self.bottomLayout.addWidget(self.lblWeekRepeat, 0, 0)

        self.lblWeekRepeat.hide()

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

        self.btnClose = QPushButton()
        self.btnClose.setFixedSize(15, 15)

        self.btnClose.setStyleSheet("QPushButton{border-image:url(./pic/close.png)}""QPushButton:hover{border-image:url(./pic/close-hover.png)}")
        self.btnClose.clicked.connect(self.close)

        self.topBarLayout = QHBoxLayout()
        self.topBarLayout.addWidget(self.btnClose, 0, Qt.AlignRight | Qt.AlignTop)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(10, 5, 15, 15)
        self.mainLayout.addLayout(self.topBarLayout, 0, 0)
        self.mainLayout.addLayout(self.topHLayout, 1, 0)
        self.mainLayout.addLayout(self.middleHLayout, 2, 0)
        self.mainLayout.addLayout(self.bottomHLayout, 3, 0)
        self.mainLayout.addLayout(self.bottomCancelLayout, 4, 0)


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


class CalendarLineEdit(QLineEdit):  # 点击会出现日历选择的编辑条
    def __init__(self, x, y):
        super(CalendarLineEdit, self).__init__()
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


class Warn(QDialog):
    def __init__(self, s):
        super(Warn, self).__init__()
        self.btn = QPushButton()
        self.text = QLabel(unicode(s))
        self.text.setStyleSheet('color:white')

        font = QFont()
        font.setFamily(NEW_FONT_TYPE)
        font.setBold(True)
        font.setPointSize(NEW_FONT_SIZE)

        self.text.setFont(font)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.bLayout= QHBoxLayout()
        self.layout.addLayout(self.bLayout)
        self.bLayout.addStretch(1)
        self.bLayout.addWidget(self.btn)
        self.bLayout.addStretch(1)
        self.setModal(True)

        self.btn.clicked.connect(self.accept)
        self.btn.setFixedSize(75, 20)
        self.btn.setStyleSheet(
            "QPushButton{border-image:url(./pic/yes.png)}""QPushButton:hover{border-image:url(./pic/yes-hover.png)}")

        self.text.setAlignment(Qt.AlignCenter)
        self.layout.setAlignment(Qt.AlignHCenter)

        self.setFixedSize(240, 90)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.background = QPixmap()
        self.background.load("./pic/warn.png")

        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, 240, 90, self.background)


class Add(QDialog):  # 新建事项窗口
    def __init__(self):
        super(Add, self).__init__()
        
        self.setWindowTitle(u"新建")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        today = time.strftime('%Y-%m-%d-%w',time.localtime(time.time()))
        dates = today.split('-')
        table = {'0':u'周日', '1':u'周一', '2':u'周二', '3':u'周三', '4':u'周四', '5':u'周五','6':u'周六' }
        self.rTable = {u'周日':6, u'周一':0, u'周二':1, u'周三':2, u'周四':3, u'周五':4, u'周六':5}
        self.date = table[dates[-1]] + ' ' + dates[1] + u'月' + ' ' + dates[2] + ' ' + dates[0]
        
        self.weekday = int(dates[-1]) - 1
        
        if self.weekday == -1:
            self.weekday = 6
            
        self.setModal(True)
        self.initLayout()
        self.setFixedSize(540, 540)

        self.background = QPixmap()
        self.background.load("./pic/white.png")

        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, 540, 540, self.background)

    def repeat(self):  # 新建重复窗口
        date = unicode(self.editStartDate.text()).split()[0]
        self.weekday = self.rTable[date]
        repeatWindow = RepeatWindow(self.weekday)
        self.repeatParameters = []
        if repeatWindow.exec_():  # 用户在重复窗口里选择OK，在退出时获得所有重复窗口里设置的参数
            saveRepeat(repeatWindow, self)

    def diffUnit(self, index):
        if self.comboReminder.currentIndex() == 0:
            self.comboReminderUnit.setCurrentIndex(-1)
            self.editReminderTime.clear()
            self.editReminderTime.hide()
            self.editReminderTime.setText("30")
            self.comboReminderUnit.hide()
        else:
            self.editReminderTime.show()
            self.comboReminderUnit.show()
            self.comboReminderUnit.setCurrentIndex(0)

    def addTag(self):
        if self.numOfClicked == 5:
            pass
        else:
            self.numOfClicked += 1
            self.tagGroup[self.numOfClicked - 1].setEnabled(True)

    def newSubWindow(self):  # 新建事项窗口的接口,只用于创建子事件
        addWindow = Add()
        addWindow.buttonSon.setEnabled(False)
        addWindow.buttonSon.hide()
        if addWindow.exec_():  # 用户点击OK后，会获得所有设置的参数，包括在重复窗口里面获得的参数
            fname_sonIDlist = "data/list/sonIDlist"
            f_sonIDlist = open(fname_sonIDlist, 'r')
            lines = f_sonIDlist.readlines()
            first_line = lines[0]
            last_line = lines[-1]
            list1 = first_line.split(' ')
            list3 = last_line.split(',')
            num_son = int(list1[0])
            parents_number = int(list3[0])
            if num_son == 0:
                sonNum = parents_number + 1
            else:
                elder = int(list3[-2])
                sonNum = elder + 1
            f_sonIDlist.close()
            f_sonIDlist = open(fname_sonIDlist, 'w')
            f_sonIDlist.write(str(num_son + 1) + '\n')
            f_sonIDlist.write(str(parents_number) + ',')
            for i in range(parents_number + 1, sonNum + 1):
                f_sonIDlist.write(str(i) + ',')
            f_sonIDlist.close()
            name = addWindow.editTitle.text()
            if name == '': name = 'None'
            location = addWindow.editLoc.text()
            if location == '': location = 'None'
            startDate = addWindow.editStartDate.text()
            if startDate == '':
                startDate = '1000-1-1'
            else:
                startDate = filter(str(startDate))
            startHour = addWindow.editStartHour.text()
            if startHour == '': startHour = '25'
            startMinute = addWindow.editStartMinute.text()
            if startMinute == '': startMinute = '61'
            endDate = addWindow.editEndDate.text()
            if endDate == '':
                endDate = '1000-1-1'
            else:
                endDate = filter(str(endDate))
            endHour = addWindow.editEndHour.text()
            if endHour == '': endHour = '25'
            endMinute = addWindow.editEndMinute.text()
            if endMinute == '': endMinute = '61'
            note = addWindow.editNote.toPlainText()
            if note == '': note = 'None'
            reminder = addWindow.comboReminder.currentIndex()
            reminderUnit = addWindow.comboReminderUnit.currentIndex()
            reminderNumber = addWindow.editReminderTime.text()
            if reminderNumber == '': reminderNumber = '-1'
            tags = [unicode(addWindow.tagGroup[i].text()) for i in range(5)]
            f_tags = open(r"data/root/tags", 'r')
            tags_list = f_tags.readlines()
            f_tags.close()
            f_tags = open(r"data/root/tags", 'w')
            f_tags.writelines(tags_list)
            filename = str(sonNum) + '$$' + str(endDate) + '$$' + str(endHour)
            flag = False
            for i in range(5):
                if tags[i] != '':
                    for j in range(tags_list.__len__()):
                        if tags[i] == tags_list[j].replace('\n', ''):
                            flag = True
                    if not flag:
                        f_tags.write(str(tags[i]) + '\n')
                    tag_filename = 'data/root/' + tags[i]
                    f_special_tags = open(tag_filename.decode('utf-8'), 'a')
                    f_special_tags.write(str(sonNum) + ' ' + startDate + '-' + startHour + '-' + startMinute + ' '
                                         + endDate + '-' + endHour + '-' + endMinute + ' ' + name + '\n')
                    f_special_tags.close()
            f_tags.close()
            repeatInfo = addWindow.repeatParameters
            path = 'data/list/' + filename
            note_path = 'data/note/' + str(sonNum)
            f_notefile = open(note_path, 'w')
            f_notefile.write(note)
            f_notefile.close()
            f = open(path, 'w')
            f.write(str(sonNum) + '\n')
            f.write(name + '\n')
            f.write(location + '\n')
            f.write(startDate + ' ' + startHour + ' ' + startMinute + '\n')
            f.write(endDate + ' ' + endHour + ' ' + endMinute + '\n')
            f.write(str(reminder) + '\n')
            f.write(str(reminderUnit) + '\n')
            f.write(reminderNumber + '\n')
            for i in range(5):
                f.write(str(tags[i]) + ',')
            f.write('\n')
            if repeatInfo == []:
                f.write('-1' + '\n')
                f.write('-1' + '\n')
                f.write('[False, False, False]' + '\n')
                f.write('-1' + '\n')
                f.write('1000-1-1' + '\n')
                f.write('[False, False, False, False, False, False, False]' + '\n')
            else:
                for i in range(6):
                    f.write(str(repeatInfo[i]) + '\n')
            f.write(str(0) + '\n' + str(parents_number) + ',')
            f_time_routine = open(r"data/root/0_time_routine_ls", 'a')
            f_time_routine.write(str(sonNum) + ' ' + startDate + '-' + startHour + '-' + startMinute + ' '
                                 + endDate + '-' + endHour + '-' + endMinute + ' ' + name + '\n')
            # print name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, note, reminder, reminderUnit, reminderNumber, tags, repeatInfo
            # print repeatInfo
            return

    def deleteTag(self):
        if self.tagGroup[self.numOfClicked - 1].isEnabled():
            self.tagGroup[self.numOfClicked - 1].setEnabled(False)
            self.tagGroup[self.numOfClicked - 1].clear()
            self.numOfClicked -= 1

    def checkStartHour(self):
        try:
            value = int(self.editStartHour.text())
        except:
            value = -1
        if value < 0 or value > 23:
            warn = Warn('输入数值超出范围')
            if warn.exec_():
                return

    def checkEndHour(self):
        try:
            value = int(self.editEndHour.text())
        except:
            value = -1
        if value < 0 or value > 23:
            warn = Warn('输入数值超出范围')
            if warn.exec_():
                return

    def checkStartMinute(self):
        try:
            value = int(self.editStartMinute.text())
        except:
            value = -1
        if value < 0 or value > 59:
            warn = Warn('输入数值超出范围')
            if warn.exec_():
                return

    def checkEndMinute(self):
        try:
            value = int(self.editEndMinute.text())
        except:
            value = -1
        if value < 0 or value > 59:
            warn = Warn('输入数值超出范围')
            if warn.exec_():
                return

    def checkMinute(self):
        if int(self.editStartMinute.text()) < 0 or int(self.editStartMinute.text()) > 59:
            warn = Warn('输入数值超出范围')
            if warn.exec_():
                return
        elif int(self.editEndMinute.text()) < 0 or int(self.editEndMinute.text()) > 59:
            warn = Warn('输入数值超出范围')
            if warn.exec_():
                return

    def check(self):
        if self.editTitle.text() != '' and self.editStartDate.text() != '' and self.editEndDate.text() != '' \
                and self.editStartHour.text() != '' and self.editStartMinute.text() != '' and self.editEndMinute.text() != '' \
                and self.editEndHour.text() != '':
            if (int(self.editEndHour.text()) > int(self.editStartHour.text())) or (
                    int(self.editEndHour.text()) == int(self.editStartHour.text()) and int(
                    self.editEndMinute.text()) > int(self.editStartMinute.text())):
                self.accept()
            else:
                warn = Warn('时间信息填写有误')
                if warn.exec_():
                    return

        else:
            warn = Warn('时间信息填写有误')
            if warn.exec_():
                return

    def changeEditEndDate(self):
        self.editEndDate.setText(self.editStartDate.text())

    def initLayout(self):
        self.topLayout = QGridLayout()
        self.bottomLayout = QGridLayout()

        font = QFont()
        font.setFamily(NEW_FONT_TYPE)
        font.setBold(True)
        font.setPointSize(NEW_FONT_SIZE)

        lblTitle = QLabel(u'标题*')
        lblTitle.setFont(font)
        lblTitle.setStyleSheet("color:white")
        lblTitle.setMaximumWidth(100)
        self.editTitle = QLineEdit()

        lblStart = QLabel(u'开始时间*')
        lblStart.setFont(font)
        lblStart.setStyleSheet("color:white")

        self.editStartDate = CalendarLineEdit(510, 170)
        self.editStartDate.setMaximumWidth(110)
        self.editStartDate.setText(self.date)

        self.editStartHour = QLineEdit()
        self.editStartHour.setMaximumWidth(30)

        self.lblStartHour = QLabel(u'时*')
        self.lblStartHour.setFont(font)
        self.lblStartHour.setStyleSheet("color:white")

        self.editStartMinute = QLineEdit()
        self.editStartMinute.setMaximumWidth(30)

        self.lblStartMinute = QLabel(u'分*')
        self.lblStartMinute.setFont(font)
        self.lblStartMinute.setStyleSheet("color:white")

        lblEnd = QLabel(u'结束时间*')
        lblEnd.setStyleSheet("color:white")
        lblEnd.setFont(font)

        self.editEndDate = QLineEdit()
        self.editEndDate.setText(self.date)
        self.editEndDate.setMaximumWidth(110)
        self.editEndDate.setReadOnly(True)

        self.editStartDate.textChanged.connect(self.changeEditEndDate)

        self.editEndHour = QLineEdit()

        self.lblEndHour = QLabel(u'时*')
        self.lblEndHour.setStyleSheet("color:white")
        self.lblEndHour.setFont(font)
        self.lblEndHour.setMaximumWidth(30)

        self.editEndMinute = QLineEdit()
        self.editEndMinute.textChanged.connect(self.checkEndMinute)
        self.editStartMinute.textChanged.connect(self.checkStartMinute)
        self.editEndHour.textChanged.connect(self.checkEndHour)
        self.editStartHour.textChanged.connect(self.checkStartHour)
        self.editEndMinute.setMaximumWidth(30)
        self.editEndHour.setMaximumWidth(30)

        self.lblEndMinute = QLabel(u'分*')
        self.lblEndMinute.setStyleSheet("color:white")
        self.lblEndMinute.setFont(font)

        lblLoc = QLabel(u'地点')
        lblLoc.setStyleSheet("color:white")
        lblLoc.setFont(font)
        self.editLoc = QLineEdit()

        lblNote = QLabel(u'备注')
        lblNote.setStyleSheet("color:white")
        lblNote.setFont(font)
        self.editNote = QTextEdit()

        lblRepeat = QLabel(u'重复')
        lblRepeat.setStyleSheet("color:white")
        lblRepeat.setFont(getFont())
        self.buttonRepeat = QPushButton(u'...')
        self.buttonRepeat.setMaximumWidth(30)

        lblReminder = QLabel(u'提醒')
        lblReminder.setFont(font)
        lblReminder.setStyleSheet("color:white")
        lblReminder.setMaximumWidth(70)

        self.comboReminder = QComboBox()
        self.comboReminder.setMaximumWidth(70)
        self.comboReminder.addItem(u"无")
        self.comboReminder.addItem(u"提醒")
        self.comboReminder.addItem(u"电子邮件")

        self.editReminderTime = QLineEdit()
        self.editReminderTime.setMaximumWidth(30)
        self.editReminderTime.setText('30')

        self.comboReminderUnit = QComboBox()
        self.comboReminderUnit.addItem(u"分钟*")
        self.comboReminderUnit.addItem(u"小时*")
        self.comboReminderUnit.addItem(u"天*")
        self.comboReminderUnit.hide()
        self.comboReminder.currentIndexChanged.connect(self.diffUnit)

        self.topLayout.addWidget(self.editReminderTime, 6, 2)
        self.topLayout.addWidget(self.comboReminderUnit, 6, 3, 1, 2)

        self.editReminderTime.hide()

        self.buttonSon = QPushButton()
        self.buttonSon.clicked.connect(self.newSubWindow)
        self.buttonSon.setFixedSize(75, 20)
        self.buttonSon.setStyleSheet("QPushButton{border-image:url(./pic/createson.png)}""QPushButton:hover{border-image:url(./pic/createson-hover.png)}")
        self.sonIDList = []
        self.sonID = 0

        self.btnClose = QPushButton()
        self.btnClose.setFixedSize(15, 15)
        self.btnClose.setStyleSheet("QPushButton{border-image:url(./pic/close.png)}""QPushButton:hover{border-image:url(./pic/close-hover.png)}")
        self.btnClose.clicked.connect(self.close)

        self.topBarLayout = QHBoxLayout()
        self.topBarLayout.addWidget(self.btnClose, 0, Qt.AlignRight | Qt.AlignTop)
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
        self.buttonRepeat.clicked.connect(self.repeat)
        self.topLayout.addWidget(lblReminder, 6, 0)
        self.topLayout.addWidget(self.comboReminder, 6, 1)

        lblTag = QLabel(u'标签')
        lblTag.setFont(font)
        lblTag.setStyleSheet("color:white")
        lblTag.setFixedSize(70,20)

        btnAddTag = QPushButton()
        btnAddTag.setFixedSize(75, 20)
        btnAddTag.setStyleSheet("QPushButton{border-image:url(./pic/add.png)}""QPushButton:hover{border-image:url(./pic/add-hover.png)}")
        self.numOfClicked = 0

        tagA = QLineEdit()
        tagB = QLineEdit()
        tagC = QLineEdit()
        tagD = QLineEdit()
        tagE = QLineEdit()
        self.tagGroup = [tagA, tagB, tagC, tagD, tagE]
        btnAddTag.clicked.connect(self.addTag)
        for i in range(5):
            self.tagGroup[i].setEnabled(False)
            self.tagGroup[i].setMaximumWidth(90)
            self.bottomLayout.addWidget(self.tagGroup[i], 0, i + 1)

        btnDeleteTag = QPushButton()
        btnDeleteTag.setFixedSize(75, 20)
        btnDeleteTag.setStyleSheet("QPushButton{border-image:url(./pic/delete.png)}""QPushButton:hover{border-image:url(./pic/delete-hover.png)}")
        btnDeleteTag.clicked.connect(self.deleteTag)
        btnAddTag.setMaximumWidth(70)
        btnDeleteTag.setMaximumWidth(70)

        self.bottomLayout.addWidget(btnAddTag, 1, 1)
        self.bottomLayout.addWidget(btnDeleteTag, 1, 2)
        self.bottomLayout.addWidget(lblTag, 0, 0)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(17, 13, 22, 17)
        self.mainLayout.addLayout(self.topBarLayout, 0, 0)
        self.mainLayout.addLayout(self.topLayout, 1, 0)
        self.mainLayout.addLayout(self.bottomLayout, 2, 0)

        btnYes = QPushButton()
        btnYes.setFixedSize(75, 20)
        btnYes.setStyleSheet("QPushButton{border-image:url(./pic/yes.png)}""QPushButton:hover{border-image:url(./pic/yes-hover.png)}")
        btnYes.clicked.connect(self.check)

        btnNo = QPushButton()
        btnNo.setFixedSize(75, 20)
        btnNo.setStyleSheet("QPushButton{border-image:url(./pic/no.png)}""QPushButton:hover{border-image:url(./pic/no-hover.png)}")
        btnNo.clicked.connect(self.reject)

        self.boboLayout = QHBoxLayout()
        self.boboLayout.addWidget(self.buttonSon, 0)
        self.boboLayout.addStretch(1)
        self.boboLayout.addWidget(btnYes)
        self.boboLayout.addWidget(btnNo)
        self.mainLayout.addLayout(self.boboLayout, 3, 0)


class DeleteItem(QDialog):
    def __init__(self):
        super(DeleteItem, self).__init__()
        self.initLayout()
        self.setModal(True)
        self.setFixedSize(210, 100)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.background = QPixmap()
        self.background.load("./pic/othertag.png")

        self.flag = 0
        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, 210, 100, self.background)

    def initLayout(self):
        self.layout = QVBoxLayout(self)
        self.lblInfo = QLabel(u'  您确定要删除该事项吗？')
        self.lblInfo.setAlignment(Qt.AlignVCenter)
        self.lblInfo.setFont(getFont())
        self.setStyleSheet('color:white')

        self.layout.addWidget(self.lblInfo)

        btnYes = QPushButton()
        btnYes.setFixedSize(75, 20)
        btnYes.setStyleSheet(
            "QPushButton{border-image:url(./pic/yes.png)}""QPushButton:hover{border-image:url(./pic/yes-hover.png)}")
        btnYes.clicked.connect(self.accept)

        btnNo = QPushButton()
        btnNo.setFixedSize(75, 20)
        btnNo.setStyleSheet(
            "QPushButton{border-image:url(./pic/no.png)}""QPushButton:hover{border-image:url(./pic/no-hover.png)}")
        btnNo.clicked.connect(self.reject)

        self.boboLayout = QHBoxLayout()
        self.boboLayout.addWidget(btnYes)
        self.boboLayout.addWidget(btnNo)
        self.layout.addLayout(self.boboLayout)


class Show(Add):
    def __init__(self, id):
        super(Show, self).__init__()
        self.setWindowTitle(u"详细信息")
        self.id = str(id)
        self.flag = 0
        self.deleteFlag = 0
        self.btnDelete = QPushButton()
        self.btnDelete.clicked.connect(self.deleteItem)
        self.boboLayout.insertWidget(2, self.btnDelete)
        self.btnDelete.setFixedSize(75, 20)
        self.btnDelete.setStyleSheet(
            "QPushButton{border-image:url(./pic/delete.png)}""QPushButton:hover{border-image:url(./pic/delete-hover.png)}")

        self.showInfo(details(self.id))
        self.buttonSon.hide()

        self.btnSonNew = QPushButton()
        self.btnSonNew.clicked.connect(self.twinkle)
        self.btnSonNew.setFixedSize(75, 20)
        self.btnSonNew.setStyleSheet("QPushButton{border-image:url(./pic/showson.png)}""QPushButton:hover{border-image:url(./pic/showson-hover.png)}")

        self.boboLayout.insertWidget(0, self.btnSonNew)

        if len(self.sonIDList) == 1:
            self.btnSonNew.hide()
            self.btnSonNew.setEnabled(False)

    def twinkle(self):
        self.flag = 1
        self.accept()

    def newSubWindow(self):
        self.accept()

    def deleteItem(self):
        a = DeleteItem()
        if a.exec_():
            remove(self.id)
            self.deleteFlag = 1
            self.accept()
            return

    def showInfo(self, infoList):

        id, title, loc, startTime, endTime, reminder, reminderUnit, \
        reminderNumber, tags, comboUnit, frequency, radioSelected, endTimes, endDate, \
        checkBoxGroup, sonID, sonIDList, note = infoList

        self.sonIDList = sonIDList[:-1].split(",")
        self.id = id

        self.repeatInfo = []
        self.repeatInfo.extend([comboUnit, frequency, radioSelected, endTimes, \
                                endDate, checkBoxGroup])

        if title != 'None':
            self.editTitle.setText(unicode(title))
        if loc != 'None':
            self.editLoc.setText(unicode(loc))

        table = {'0': u'周日', '1': u'周一', '2': u'周二', '3': u'周三', '4': u'周四', '5': u'周五', '6': u'周六'}

        year, month, day = [int (startTime.split()[0].split('-')[i]) for i in range(3)]
        date = table[datetime(year, month, day).strftime("%w")] + ' ' + str(month) + u'月' + ' ' + str(day) + ' ' + str(year)

        self.editStartDate.setText(date)
        self.editStartHour.setText(startTime.split()[1])
        self.editStartMinute.setText(startTime.split()[2])
        self.editEndDate.setText(date)
        self.editEndHour.setText(endTime.split()[1])
        self.editEndMinute.setText(endTime.split()[2])

        if note != 'None':
            self.editNote.setText(unicode(note))
        self.comboReminder.setCurrentIndex(int(reminder))
        self.comboReminderUnit.setCurrentIndex(int(reminderUnit))

        if reminderNumber != 'None' or int(reminderNumber) > 0:
            self.editReminderTime.setText(reminderNumber)
        else:
            self.editReminderTime.setText('22')

        tags = tags.split(',')
        for i in range(5):
            if tags[i] != '':
                self.tagGroup[i].setText(unicode(tags[i]))
                self.tagGroup[i].setEnabled(True)
                self.numOfClicked+=1

        if '课程' in tags and '网络学堂' in tags:
            self.tagGroup[tags.index('课程')].setEnabled(False)
            self.tagGroup[tags.index('网络学堂')].setEnabled(False)

        if '作业' in tags and '网络学堂' in tags:
            self.tagGroup[tags.index('作业')].setEnabled(False)
            self.tagGroup[tags.index('网络学堂')].setEnabled(False)

    def repeat(self):  # 新建重复窗口

        repeatWindow = RepeatWindow(self.weekday)
        repeatWindow.comboUnit.setCurrentIndex(int(self.repeatInfo[0]))
        if self.repeatInfo[1] != '-1':
            repeatWindow.editFre.setText(self.repeatInfo[1])
        radioInfo = tranBoolList(self.repeatInfo[2])
        if radioInfo[0] == '1':
            repeatWindow.radioNever.setChecked(True)
        elif radioInfo[1] == '1':
            repeatWindow.radioTimes.setChecked(True)
        elif radioInfo[2] == '1':
            repeatWindow.radioEnd.setChecked(True)
        if self.repeatInfo[3] != '-1':
            repeatWindow.editTimes.setText(self.repeatInfo[3])
        if self.repeatInfo[4] != '1000-1-1':
            repeatWindow.editEnd.setText(self.repeatInfo[4])
        checkGroup = tranBoolList(self.repeatInfo[5])
        for i in range(7):
            if checkGroup[i] == '1':
                repeatWindow.checkBoxGroup[i].setChecked(True)

        if repeatWindow.exec_():  # 用户在重复窗口里选择OK，在退出时获得所有重复窗口里设置的参数
            saveRepeat(repeatWindow, self)
            return


class OtherTag(QDialog):
    def __init__(self):
        super(OtherTag, self).__init__()
        self.initLayout()
        self.setWindowTitle(u'其他标签')
        self.setFixedSize(210, 100)
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.background = QPixmap()
        self.background.load("./pic/othertag.png")
        
        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, 210, 100, self.background)

    def initLayout(self):
        self.layout = QVBoxLayout(self)
        self.lblInfo = QLabel(u'请输入希望查找的标签：')
        self.lblInfo.setFont(getFont())
        self.lblInfo.setStyleSheet('color:white')
        self.edit = QLineEdit()
        self.layout.addWidget(self.lblInfo)
        self.layout.addWidget(self.edit)
        btnYes = QPushButton()
        btnYes.setFixedSize(75, 20)
        btnYes.setStyleSheet(
            "QPushButton{border-image:url(./pic/yes.png)}""QPushButton:hover{border-image:url(./pic/yes-hover.png)}")
        btnYes.clicked.connect(self.check)

        btnNo = QPushButton()
        btnNo.setFixedSize(75, 20)
        btnNo.setStyleSheet(
            "QPushButton{border-image:url(./pic/no.png)}""QPushButton:hover{border-image:url(./pic/no-hover.png)}")
        btnNo.clicked.connect(self.reject)

        self.boboLayout = QHBoxLayout()
        self.boboLayout.addWidget(btnYes)
        self.boboLayout.addWidget(btnNo)
        self.layout.addLayout(self.boboLayout)

    def check(self):
        tag = self.edit.text()
        tagList = getTagList()
        if unicode(tag) in tagList or tag in tagList:
            self.accept()
            self.tag = tag
        else:
            warn = Warn('无含此标签的事项')
            if warn.exec_():
                return


class MultiItem(QDialog):
    def __init__(self, IDs, mainwindow):
        super(MultiItem, self).__init__()
        self.IDs = IDs
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initLayout()
        
        pal = QPalette()
        pal.setColor(self.backgroundRole(), QColor(55, 62, 150))
        self.setPalette(pal)
        self.show()
        self.mainwindow = mainwindow

    def showDetail(self, IDs):
        showWindow = Show(IDs)
        if showWindow.exec_():
            detail = details(IDs)
            self.close()

            if showWindow.flag == 1:
                self.mainwindow.twinkle(showWindow.sonIDList[1:])
                return

            if showWindow.deleteFlag == 1:
                self.mainwindow.refresh()
                return
            else:
                new_list = getInfo(showWindow)
                new_filename = IDs + '$$' + new_list[5] + '$$' + new_list[6]
                new_path = 'data/list/' + new_filename
                f = open(r"data/root/0_time_routine_ls", 'r')
                lists = f.readlines()
                f.close()
                f = open(r"data/root/0_time_routine_ls", 'w')
                for i in range(len(lists)):
                    lists[i] = lists[i].replace('\n', '')
                    temp_list = lists[i].split(' ')
                    if IDs == temp_list[0]:
                        filename_list = temp_list[2].split('-')
                        old_filename = temp_list[0] + '$$' + filename_list[0] + '-' + filename_list[1] + '-' + \
                                       filename_list[2] + '$$' + filename_list[3]
                        new_item = IDs + ' ' + new_list[2] + '-' + new_list[3] + '-' + new_list[4] + ' ' + new_list[
                            5] + '-' + new_list[6] + '-' + new_list[7] + ' ' + new_list[0]
                        lists[i] = new_item
                    f.write(lists[i] + '\n')
                f.close()
                old_path = 'data/list/' + old_filename
                os.remove(old_path)
                fnew = open(new_path, 'w')
                fnew.write(str(IDs) + '\n')
                fnew.write(new_list[0] + '\n')
                fnew.write(new_list[1] + '\n')
                fnew.write(new_list[2] + ' ' + new_list[3] + ' ' + new_list[4] + '\n')
                fnew.write(new_list[5] + ' ' + new_list[6] + ' ' + new_list[7] + '\n')
                fnew.write(str(new_list[8]) + '\n')
                fnew.write(str(new_list[9]) + '\n')
                fnew.write(new_list[10] + '\n')
                for i in range(5):
                    fnew.write(str(new_list[11][i]) + ',')
                fnew.write('\n')
                if new_list[13] == []:
                    fnew.write(detail[9] + '\n')
                    fnew.write(detail[10] + '\n')
                    fnew.write(detail[11] + '\n')
                    fnew.write(detail[12] + '\n')
                    fnew.write(detail[13] + '\n')
                    fnew.write(detail[14] + '\n')
                else:
                    for i in range(6):
                        fnew.write(str(new_list[13][i]) + '\n')
                fnew.write(detail[15] + '\n')
                fnew.write(detail[16] + '\n')
                fnew.close()
                note_path = 'data/note/' + IDs
                fnote = open(note_path, 'w')
                fnote.write(new_list[12])
                fnote.close()

                update = updateToS()
                if update == -1:
                    warn = Warn('未预留邮箱信息！')
                    self.mainwindow.refresh()
                    if warn.exec_():
                        return
                elif update == -2:
                    warn = Warn('网络异常，无法同步到服务器')
                    self.mainwindow.refresh()
                    if warn.exec_():
                        return
                else:

                    self.mainwindow.refresh()
                    return

    def initLayout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.btnClose = QPushButton()
        self.btnClose.setFixedSize(15, 15)
        self.btnClose.setStyleSheet("QPushButton{border-image:url(./pic/close.png)}""QPushButton:hover{border-image:url(./pic/close-hover.png)}")
        self.btnClose.clicked.connect(self.close)
        
        self.topBarLayout = QHBoxLayout()
        self.topBarLayout.addWidget(self.btnClose, 0, Qt.AlignRight | Qt.AlignTop)
        self.layout.addLayout(self.topBarLayout)

        currentItem = details(self.IDs[0])
        date = transDate(currentItem[3].split()[0])
        lblDate = QLabel(unicode(date))
        self.layout.addWidget(lblDate)
        lblDate.setFont(getFont())
        lblDate.setStyleSheet('color:white')
        
        btnNames = []
        for i in range(len(self.IDs)):
            btnNames.append('btnItem' + str(i))
        for i in range(len(self.IDs)):
            currentItem = details(str(self.IDs[i]))
            id = currentItem[0]
            name = currentItem[1]
            btnNames[i] = QPushButton(unicode(name))
            btnNames[i].setStyleSheet('background-color:white;color:rgb(55, 62, 150)')
            btnNames[i].setFont(getFont())
            btnNames[i].clicked.connect(partial(self.showDetail, id))
            self.layout.addWidget(btnNames[i])


class ProgressBar(QDialog):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(300, 40)
        self.initLayout()
        self.background = QPixmap()
        self.background.load("./pic/updatewindow.png")
        self.show()
        self.setModal(True)
        self.setStyleSheet("QProgressBar:chunk{background-color:rgb(131,189,232);}""QProgressBar{height:10px; text-align:center}")
        self.onStart()
        
    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, 300, 40, self.background)


    def initLayout(self):
        self.layout = QVBoxLayout(self)
        self.a = QProgressBar()
        self.layout.addWidget(self.a)
        self.timer = QBasicTimer()
        self.step = 0


    def timerEvent(self, event):
        if int(self.step) >= 100:
            self.timer.stop()
            self.accept()
            return
        self.step += 1
        self.a.setValue(int(self.step))

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)


class TimeThread(QThread):

    def __init__(self, username, password, email, window):
        super(TimeThread, self).__init__()
        self.username = username
        self.password = password
        self.email = email
        self.window = window

    def run(self):
        info, homework = sync.main(self.username, self.password)
        if info == '!!!':
            self.window.errorFlag = 1
        else:
            f = open('./data/user.csv', 'w')
            f.write(self.username + '\t' + self.password + '\t' + self.email)
            f.close()
            
            self.window.info = info
            self.window.info.extend(homework)

class UpdateWindow(QDialog):
    def __init__(self):
        super(UpdateWindow, self).__init__()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(230, 160)
        self.initLayout()
        self.background = QPixmap()
        self.background.load("./pic/updatewindow.png")
        self.errorFlag = 0
        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, 230, 160, self.background)

    def initLayout(self):
        self.layout = QGridLayout(self)
        self.lblUsername = QLabel(u'用户名*')
        self.lblUsername.setFont(getFont())
        self.lblUsername.setStyleSheet("color:white")
        self.lblEmail = QLabel(u'邮箱*')
        self.lblEmail.setStyleSheet("color:white")
        self.lblEmail.setFont(getFont())
        self.lblUsername.setFont(getFont())
        self.lblPassword = QLabel(u'密码*')
        self.lblPassword.setStyleSheet("color:white")
        self.lblPassword.setFont(getFont())
        self.editUsername = QLineEdit()
        self.editPassword = QLineEdit()
        self.editPassword.setEchoMode(QLineEdit.Password)
        self.editPassword.setMaxLength(30)
        self.editMail = QLineEdit()
      
        self.layout.addWidget(self.lblUsername, 1, 0)
        self.layout.addWidget(self.lblPassword, 2, 0)
        self.layout.addWidget(self.lblEmail, 3, 0)
        self.layout.addWidget(self.editUsername, 1, 1)
        self.layout.addWidget(self.editPassword, 2, 1)
        self.layout.addWidget(self.editMail, 3, 1)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addStretch(1)
        self.layout.addLayout(self.bottomLayout, 4, 1)

        btnYes = QPushButton()
        btnYes.setFixedSize(75, 20)
        btnYes.setStyleSheet(
            "QPushButton{border-image:url(./pic/yes.png)}""QPushButton:hover{border-image:url(./pic/yes-hover.png)}")
        btnYes.clicked.connect(self.Accept)

        btnNo = QPushButton()
        btnNo.setFixedSize(75, 20)
        btnNo.setStyleSheet(
            "QPushButton{border-image:url(./pic/no.png)}""QPushButton:hover{border-image:url(./pic/no-hover.png)}")
        btnNo.clicked.connect(self.reject)
        
        self.bottomLayout.addWidget(btnYes)
        self.bottomLayout.addWidget(btnNo)

        try:
            f = open('./data/user.csv', 'r')
            info = f.readline()
            username, password, mail = info.split('\t')
            self.editUsername.setText(username)
            self.editPassword.setText(password)
            self.editMail.setText(mail)
            f.close()
        except:
            pass

    def Accept(self):
        self.errorFlag = 0
        username = unicode(self.editUsername.text())
        password = unicode(self.editPassword.text())
        email = self.editMail.text()
        str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if not re.match(str, email):
            warn = Warn('请输入正确的邮箱')
            if warn.exec_():
                return
            self.acceptDrops()
        else:
            self.timer = TimeThread(username, password, email, self)
            self.timer.start()
            time.sleep(3)
            if self.errorFlag == 1:
                warn = Warn('用户名或密码错误')
                if warn.exec_():
                    return
            a = ProgressBar()
            if a.exec_():
                pass
        self.accept()

class TrayIcon(QSystemTrayIcon):
    def __init__(self,parent=None):
        super(TrayIcon, self).__init__(parent)
        self.initIcon()
        self.timer = QTimer(self)
        self.startCount()
        self.timer.timeout.connect(self.showMessage)



    def startCount(self):
        self.timer.start(60000)



    def initIcon(self):         #托盘初始化
        self.icon = QIcon("./pic/logo-square-15.png")
        self.show()
        self.setIcon(self.icon)  #设置系统托盘图标
        self.activated.connect(self.iconClied) #设置托盘点击事件处理函数
        self.tray_menu = QMenu(QApplication.desktop()) #创建菜单
        pw = self.parent()
        self.restoreAction = QAction(u'还原 ', self, triggered= pw.show) #添加一级菜单动作选项(还原主窗口)
        self.quitAction = QAction(u'退出 ', self, triggered=qApp.quit) #添加一级菜单动作选项(退出程序)
        self.tray_menu.addAction(self.restoreAction) #为菜单添加动作
        self.tray_menu.addAction(self.quitAction)
        self.setContextMenu(self.tray_menu) #设置系统托盘菜单

    def showMessage(self):

        titleList = []
        endDateList = []
        remindTimeList = []
        info = getcompletelist()
        for item in info:
            id, title, loc, startTime, endTime, reminder, reminderUnit, \
            reminderNumber, tags, comboUnit, frequency, radioSelected, endTimes, endDate, \
            checkBoxGroup, sonID, sonIDList, note = item
            #print reminder
            if reminder == '1':
                titleList.append(unicode(title))
                temp = startTime.split()
                startTime = temp[0] + ' ' + temp[1] + ':' + temp[2]
                temp = endTime.split()
                endTime = temp[0] + ' ' + temp[1] + ':' + temp[2]


                taggroup = tags.split(',')[:-1]
                if 'DDL' in taggroup:
                    endDateList.append(endTime)
                else:
                    endDateList.append(startTime)
                if reminderUnit == '0':
                    remindTimeList.append(int(reminderNumber))
                elif reminderUnit == '1':
                    remindTimeList.append(int(reminderNumber) * 60)
                elif reminderUnit == '2':
                    remindTimeList.append(int(reminderNumber) * 1440)


        self.timeNow = time.strftime('%Y-%m-%d %H:%M',time.localtime())

        self.timeArray = time.strptime(self.timeNow,'%Y-%m-%d %H:%M')
        self.timeStamp = int(time.mktime(self.timeArray))

        for i in range(len(titleList)):


            timeddl = time.strptime(endDateList[i],'%Y-%m-%d %H:%M')
            timeDDL = int(time.mktime(timeddl))
            timeLeftStampTemp = timeDDL-self.timeStamp
            if(timeLeftStampTemp/60==remindTimeList[i]):
                message=u"距离" + u'【 '+titleList[i]+u'】 ' + u"还有"+str(remindTimeList[i])+u"分钟！"
                self.showMessage(u"提醒", message)



    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()

            pw.show()

        if reason ==1 :
            self.tray_menu.show()
            #self.showMessage(u"测试", u"我是消息")

class Talendar(QWidget):  # 主界面

    def __init__(self):
        super(Talendar, self).__init__()
        self.initFolder()
        self.ddlFlag = False
        self.targetTag = None
        self.headerlabels = [u'星期一', u'星期二', u'星期三', u'星期四', u'星期五', u'星期六', u'星期日']
        self.setWindowTitle("Talendar")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.date = datetime.now()
        self.rowNum = 24
        self.starttime=1
        self.filterFlag = 0
        self.trayIcon = TrayIcon(self)
        self.trayIcon.show()
        self.resize(920, 620)
        self.center()
        # self.tableDict={u'一':0,u'二':1,u'三':2,u'四':3,u'五':4,u'六':5,u'日':6}
        self.tableDict = {u'Mon': 0, u'Tue': 1, u'Wed': 2, u'Thu': 3, u'Fri': 4, u'Sat': 5, u'Sun': 6}
        self.pageFlag = 'm'
        self.initGrid()

        self.timer = QTimer(self)
        self.count = 0

        self.timer.timeout.connect(self.updateDDL)
        self.startCount()

        self.background = QPixmap()
        self.background.load("./pic/mainwindow.png")

        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        if self.ddlFlag:
            p.drawPixmap(0, 0, 1156, 620, self.background)
        else:
            p.drawPixmap(0, 0, 920, 620, self.background)

    def startCount(self):
        self.timer.start(60000)

    def initFolder(self):
        root_directory = ''
        folder_data = 'data'
        folder_root = 'root'
        folder_note = 'note'
        folder_list = 'list'
        try:
            os.mkdir(root_directory + folder_data)
        except OSError:
            pass
        try:
            os.mkdir(root_directory + folder_data + '/' + folder_root)
        except OSError:
            pass
        try:
            os.mkdir(root_directory + folder_data + '/' + folder_list)
        except OSError:
            pass
        try:
            os.mkdir(root_directory + folder_data + '/' + folder_note)
        except OSError:
            pass
        if not os.path.isfile(r"data/root/0_time_routine_ls"):
            f = open(r"data/root/0_time_routine_ls", 'a')
            f.write('0 data/root/0_time_routine_ls' + '\n')
            f.write('0 data/root/0_time_routine_ls' + '\n')
            f.close()
        if not os.path.isfile(r"data/root/tags"):
            f = open(r"data/root/tags", 'a')
            f.write('0 data/root/tags' + '\n')
            f.close()

    def update(self):

        updateWindow = UpdateWindow()
        if updateWindow.exec_():
            while(1):
                try:
                    info = updateWindow.info
                    break
                except:
                    pass

            IDList = []

            oldInfo = getcompletelist()
            for item in oldInfo:
                id, title, loc, startTime, endTime, reminder, reminderUnit, \
                reminderNumber, tags, comboUnit, frequency, radioSelected, endTimes, endDate, \
                checkBoxGroup, sonID, sonIDList, note = item
                if '网络学堂' in tags.split(','):
                  remove(id)

            for item in info:
                fname = "data/root/0_time_routine_ls"
                fname_sonIDlist = "data/list/sonIDlist"
                f_sonIDlist = open(fname_sonIDlist, 'w')
                with open(fname, 'r') as f:
                    lines = f.readlines()
                    last_line = lines[-1]
                    penult_line = lines[-2]
                list1 = last_line.split(' ')
                list2 = penult_line.split(' ')
                last_num = int(list1[0])
                if int(list2[0]) > int(list1[0]): last_num = int(list2[0])
                f.close()
                f_sonIDlist.write('0' + '\n')
                f_sonIDlist.write(str(last_num + 1) + ',')
                f_sonIDlist.close()
                save(item, last_num, fname_sonIDlist)
                
            self.refresh()
            return

    def initGrid(self):

        self.initLeftGrid()  # 初始化左侧菜单栏
        self.initCalendarGrid()  # 初始化右侧日历表格界面
        self.initTopGrid()
        self.initMainGrid()  # 构建主布局

    def initTopGrid(self):  # updated
        self.topLayout = QHBoxLayout()

        self.year = QLabel(self.date.strftime("%Y"))

        upperPage = QPushButton()
        upperPage.setFixedSize(15, 25)
        upperPage.setStyleSheet(
            "QPushButton{border-image:url(./pic/forward.png)}""QPushButton:hover{border-image:url(./pic/forward-hover.png)}")
        self.topLayout.addWidget(upperPage)
        upperPage.clicked.connect(self.upPage)
        nextPage = QPushButton()
        self.topLayout.addWidget(nextPage)
        self.topLayout.addStretch(1)
        self.btnClose = QPushButton()
        self.btnClose.setFixedSize(25, 25)

        self.btnClose.setStyleSheet("QPushButton{border-image:url(./pic/close_big.png)}""QPushButton:hover{border-image:url(./pic/close-big-hover.png)}")
        self.btnClose.clicked.connect(self.hide)
        self.topLayout.addWidget(self.btnClose)
        self.topLayout.setSpacing(15)
        self.topLayout.setContentsMargins(0, 12, 10, 5)
        nextPage.setFixedSize(15, 25)
        nextPage.setStyleSheet(
            "QPushButton{border-image:url(./pic/next.png)}""QPushButton:hover{border-image:url(./pic/next-hover.png)}")
        nextPage.clicked.connect(self.nextPage)

    def initMainGrid(self):

        self.mainLayout = QGridLayout(self)
        self.leftLayout.setSpacing(20)
        self.leftLayout.setMargin(13)
        self.mainLayout.setRowStretch(0, 10)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowMinimumHeight(1, 0)
        self.mainLayout.addLayout(self.leftLayout, 0, 0)
        
        self.tempLayout = QVBoxLayout()
        self.tempLayout.addLayout(self.topLayout)
        self.tempLayout.addLayout(self.calendarLayout)
        
        self.mainLayout.addLayout(self.tempLayout, 0, 1)
        self.rightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightTopLayout.addStretch(1)
        self.rightBtnClose = QPushButton()
        self.rightBtnClose.setFixedSize(25, 25)
        self.rightBtnClose.setStyleSheet("QPushButton{border-image:url(./pic/close_big.png)}""QPushButton:hover{border-image:url(./pic/close-big-hover.png)}")
        self.rightBtnClose.clicked.connect(self.hide)
        self.rightBtnClose.hide()
        
        self.rightTopLayout.addWidget(self.rightBtnClose)
        self.rightLayout.addLayout(self.rightTopLayout)
        self.rightLayout.setSpacing(17)
        self.rightLayout.setContentsMargins(0, 7, 15, 0)
        self.mainLayout.addLayout(self.rightLayout, 0, 2)
        self.mainLayout.setColumnStretch(1, 2)

    def targetCourse(self):
        self.targetTag = '课程'
        self.refresh()

    def targetHomework(self):
        self.targetTag = '作业'
        self.refresh()

    def targetConf(self):
        self.targetTag = '活动'
        self.refresh()

    def targetOther(self):
        otherTagWindow = OtherTag()
        if otherTagWindow.exec_():
            self.targetTag = unicode(otherTagWindow.tag)
            self.refresh()
            return

    def showFilter(self):

        if self.filterFlag == 0:
            self.btnCourse.show()
            self.btnHomework.show()
            self.btnConf.show()
            self.btnOther.show()
        else:
            self.btnCourse.hide()
            self.btnHomework.hide()
            self.btnConf.hide()
            self.btnOther.hide()
            self.targetTag = None
            self.refresh()
        self.filterFlag = 1 - self.filterFlag

    def initLeftGrid(self):
        self.leftLayout = QVBoxLayout()
        topSpace1 = QSpacerItem(1, 40)
        self.leftLayout.addItem(topSpace1)

        btnLogo = QPushButton()
        btnLogo.setFixedSize(80, 12)
        btnLogo.setStyleSheet('border-image:url(./pic/onlylogo.png)')
        self.leftLayout.addWidget(btnLogo)

        topSpace = QSpacerItem(1, 10)
        self.leftLayout.addItem(topSpace)

        btnUpdate = QPushButton()
        btnUpdate.setFixedSize(75, 28)
        btnUpdate.setStyleSheet("QPushButton{border-image:url(./pic/update.png)}""QPushButton:hover{border-image:url(./pic/update-hover.png)}")
        btnUpdate.clicked.connect(self.update)



        btnNew = QPushButton()
        btnNew.setFixedSize(75, 28)
        btnNew.setStyleSheet("QPushButton{border-image:url(./pic/new.png)}""QPushButton:hover{border-image:url(./pic/new-hover.png)}")
        btnNew.clicked.connect(self.newWindow)
        self.leftLayout.addWidget(btnUpdate)
        self.leftLayout.addWidget(btnNew)

        self.btnFilter = QPushButton()
        self.leftLayout.addWidget(self.btnFilter)
        self.btnFilter.setFixedSize(75, 28)
        self.btnFilter.setStyleSheet("QPushButton{border-image:url(./pic/filter.png)}""QPushButton:hover{border-image:url(./pic/filter-hover.png)}")
        self.btnFilter.clicked.connect(self.showFilter)

        btnDDL = QPushButton()
        self.leftLayout.addWidget(btnDDL)
        btnDDL.setFixedSize(75, 28)
        btnDDL.setStyleSheet("QPushButton{border-image:url(./pic/ddl.png)}""QPushButton:hover{border-image:url(./pic/ddl-hover.png)}")

        change = QPushButton()
        change.clicked.connect(self.transform)
        change.setFixedSize(75, 28)
        change.setStyleSheet("QPushButton{border-image:url(./pic/screen.png)}""QPushButton:hover{border-image:url(./pic/screen-hover.png)}")
        self.leftLayout.addWidget(change)

        btnDDL.clicked.connect(self.showDDL)

        self.btnCourse = QPushButton()
        self.btnCourse.setFixedSize(75, 20)
        self.btnCourse.setStyleSheet("QPushButton{border-image:url(./pic/sub-course.png)}""QPushButton:hover{border-image:url(./pic/sub-course-hover.png)}")
        self.btnHomework = QPushButton()
        self.btnHomework.setFixedSize(75, 20)
        self.btnHomework.setStyleSheet("QPushButton{border-image:url(./pic/sub-homework.png)}""QPushButton:hover{border-image:url(./pic/sub-homework-hover.png)}")
        self.btnConf = QPushButton()
        self.btnConf.setFixedSize(75, 20)
        self.btnConf.setStyleSheet("QPushButton{border-image:url(./pic/sub-conf.png)}""QPushButton:hover{border-image:url(./pic/sub-conf-hover.png)}")
        self.btnOther = QPushButton()
        self.btnOther.setFixedSize(75, 20)
        self.btnOther.setStyleSheet("QPushButton{border-image:url(./pic/sub-other.png)}""QPushButton:hover{border-image:url(./pic/sub-other-hover.png)}")

        self.btnCourse.clicked.connect(self.targetCourse)
        self.btnHomework.clicked.connect(self.targetHomework)
        self.btnConf.clicked.connect(self.targetConf)
        self.btnOther.clicked.connect(self.targetOther)

        self.leftLayout.insertWidget(6, self.btnOther)
        self.leftLayout.insertWidget(6, self.btnConf)
        self.leftLayout.insertWidget(6, self.btnHomework)
        self.leftLayout.insertWidget(6, self.btnCourse)

        self.btnHomework.hide()
        self.btnConf.hide()
        self.btnOther.hide()
        self.btnCourse.hide()

        self.leftLayout.addStretch(1)

    def initDDL(self):

        titleList = []
        endDateList = []
        info = getcompletelist()
        for item in info:
            id, title, loc, startTime, endTime, reminder, reminderUnit, \
            reminderNumber, tags, comboUnit, frequency, radioSelected, endTimes, endDate, \
            checkBoxGroup, sonID, sonIDList, note = item
            if 'DDL' in tags.split(','):
                titleList.append(unicode(title))
                temp = endTime.split()
                endTime = temp[0] + ' ' + temp[1] + ':' + temp[2]
                endDateList.append(endTime)

        row = len(endDateList)
        self.newDDL = QTableWidget(row, 1)
        try:
            self.rightLayout.removeWidget(self.DDL)  # self.DDL.setRowCount(6)
        except:
            pass
        self.DDL = self.newDDL
        self.rightLayout.addWidget(self.DDL)


        self.DDL.setColumnWidth(0, 220)
        for i in range(row):
            self.DDL.setRowHeight(i, 100)
        self.DDL.setFrameShadow(QFrame.Plain)
        self.DDL.setHorizontalHeaderLabels([u'DDL列表'])
        self.timenow = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        self.timeArray = time.strptime(self.timenow, '%Y-%m-%d %H:%M')
        self.timeStamp = int(time.mktime(self.timeArray))

        flag = [i for i in range(len(titleList))]
        flag.append(0)
        # flag =[0,1,2,0,0,0]#最后一位是为了移动方便，其实不用这个
        timeStampMax = 15778116610
        timeLeftStamp = [timeStampMax for i in range(row+1)]
        for i in range(len(titleList)):
            timeddl = time.strptime(endDateList[i], '%Y-%m-%d %H:%M')
            timeDDL = int(time.mktime(timeddl))
            timeLeftStampTemp = timeDDL - self.timeStamp
            for j in range(0, len(flag) - 1):
                if (timeLeftStampTemp < timeLeftStamp[j]):
                    for k in range(j, len(flag) - 1):
                        kk = j + len(flag) - 1 - k - 1
                        flag[kk + 1] = flag[kk]
                        timeLeftStamp[kk + 1] = timeLeftStamp[kk]

                    timeLeftStamp[j] = timeLeftStampTemp
                    flag[j] = i
                    break

        for m in range(0, len(flag) - 1):
            self.initDDLItem(titleList[flag[m]], endDateList[flag[m]])
            self.DDL.setCellWidget(m, 0, self.DDLItem)

    def initDDLItem(self, item, deadLine):
        self.DDLItem = QTableWidget(3, 1)
        self.DDLItem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.DDLItem.setColumnWidth(0, 150)

        self.DDLItem.setRowHeight(1, 30)
        self.DDLItem.setRowHeight(2, 30)
        self.DDLItem.setRowHeight(0, 30)
        self.DDLItem.setVerticalHeaderLabels([u'内容', u'截止时间', u'剩余时间'])
        self.DDLItem.setShowGrid(False)
        self.DDLItem.horizontalHeader().hide()

        timeddl = time.strptime(deadLine, '%Y-%m-%d %H:%M')
        timeDDL = int(time.mktime(timeddl))
        timeLeftStampTemp = timeDDL - self.timeStamp


        timeLeftDay = timeLeftStampTemp / 86400
        timeLeftHour = (timeLeftStampTemp - timeLeftDay * 86400) / 3600
        timeLeftMin = (timeLeftStampTemp - timeLeftDay * 86400 - timeLeftHour * 3600) / 60
        

        LeftTime = str(timeLeftDay) + u'天' + str(timeLeftHour) + u'小时' + str(timeLeftMin) + u'分钟'

        newitem = QTableWidgetItem(item)

        self.DDLItem.setItem(0, 0, newitem)
        newitem = QTableWidgetItem(deadLine)
        self.DDLItem.setItem(1, 0, newitem)
        newitem = QTableWidgetItem(LeftTime)

        if (timeLeftStampTemp > 7 * 86400):
            newitem.setBackgroundColor(QColor(0, 255, 0, 125))
        else:
            if (timeLeftStampTemp > 3 * 86400):
                newitem.setBackgroundColor(QColor(255, 255, 0, 125))
            else:
                newitem.setBackgroundColor(QColor(255, 0, 0, 125))

        self.DDLItem.setItem(2, 0, newitem)

    def reverseDDLFlag(self):
        if self.ddlFlag:
            self.ddlFlag = False
        else:
            self.ddlFlag = True

    def updateDDL(self):
        if self.ddlFlag:
            self.resize(1162, 620)
            self.initDDL()
            self.DDL.show()
            self.rightBtnClose.show()
            self.btnClose.hide()
            self.center()
            self.background.load("./pic/bigwindow.png")

        else:
            self.resize(920, 620)
            try:
                self.DDL.hide()
            except:
                pass
            self.rightBtnClose.hide()
            self.btnClose.show()
            self.center()
            self.background.load("./pic/mainwindow.png")

    def showDDL(self):
        self.reverseDDLFlag()
        self.updateDDL()

    def fillBlank(self, flag, start, end):  # column 1 row 0
        for i in range(start, end):
            self.leftLayout.addWidget(QLabel(''), 0, 0)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        self.c.closeApp.connect(self.close)
        self.setWindowTitle('Emit signal')
        self.show()

    def newWindow(self):  # 新建事项窗口的接口
        fname = "data/root/0_time_routine_ls"
        fname_sonIDlist = "data/list/sonIDlist"
        f_sonIDlist = open(fname_sonIDlist, 'w')
        with open(fname, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            penult_line = lines[-2]
        list1 = last_line.split(' ')
        list2 = penult_line.split(' ')
        last_num = int(list1[0])
        if int(list2[0]) > int(list1[0]): last_num = int(list2[0])
        f.close()
        f_sonIDlist.write('0' + '\n')
        f_sonIDlist.write(str(last_num + 1) + ',')
        f_sonIDlist.close()

        addWindow = Add()
        if addWindow.exec_():  # 用户点击OK后，会获得所有设置的参数，包括在重复窗口里面获得的参数
            save(getInfo(addWindow), last_num, fname_sonIDlist)
            update = updateToS()
            if update == -1:
                warn = Warn('未预留邮箱信息！')
                self.refresh()
                if warn.exec_():
                    return
            elif update == -2:
                warn = Warn('网络异常，邮件提醒不工作')
                self.refresh()
                if warn.exec_():
                    return
            else:
                print 'add'
                self.refresh()
                pass


            return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def initCalendarGrid(self):

        self.grid = self.WeekGrid(self.starttime)
        self.date = datetime.now()
        self.grid.close()
        self.grid = self.MonthGrid()

        self.calendarLayout = QGridLayout()
        self.calendarLayout.setContentsMargins(0, 0, 13, 0)

        self.calendarLayout.addWidget(self.grid)

    def transFlag(self):
        if self.pageFlag == 'w':
            self.pageFlag = 'm'
        elif self.pageFlag == 'm':
            self.pageFlag = 'w'

    def refresh(self):
        if self.pageFlag == 'w':
            self.date = datetime.now()
            self.grid.close()
            self.grid = self.WeekGrid(self.starttime)
            self.calendarLayout.addWidget(self.grid)
        else:
            self.date = datetime.now()
            self.grid.close()
            self.grid = self.MonthGrid()
            self.calendarLayout.addWidget(self.grid)
        self.updateDDL()

    def transform(self):
        self.transFlag()
        self.ddlFlag = False
        self.refresh()

    def twinkle_b(self):
        import time
        nolist = self.nolist
        #print nolist
        colnum = 7
        rownum = self.rowNum
        templist = []
        colorlist = []
        # <<<<<<< HEAD
        # =======
        # print "nolist",nolist
        # >>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe



        for i in range(colnum):
            for j in range(rownum):
                tempWidget = self.grid.cellWidget(j, i)
                try:
                    n = tempWidget.count()
                except:
                    continue
                if self.pageFlag == 'w':
                    n = n - 1
                for w in range(n):
                    if self.pageFlag == 'w':
                        w = w + 1
                    # print w
                    items = tempWidget.item(w)
                    numlist = items.statusTip()
                    # print numlist
                    numlist = numlist.split('-')
                    # print numlist
                    for w, item in enumerate(numlist):
                        # print item
                        if not item == '' and str(item) in nolist:
                            items.setBackground(QColor(Qt.yellow))
                            templist.append(items)
                            colorlist.append(item)
        self.templist = templist
        self.colorlist = colorlist
        # print templist
        return templist, colorlist

    def twinkle_d(self, templist, colorlist):
        # <<<<<<< HEAD
        # =======
        # print "test",templist, colorlist
        # >>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe
        for i, item in enumerate(templist):
            item.setBackground(self.getColor(colorlist[i]))

    def twinkle(self,nolist):  # 闪烁调用接口，需要传入id的list，id为字符串格式。利用了self.nolist, self.templist和self.colorlist来传参，可以调整闪烁时间和闪烁次数
        self.nolist = nolist
        # <<<<<<< HEAD
        # =======

        # >>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe
        self.templist = []
        self.colorlist = []
        self.times = QTimer(self)
        self.ww = 0
        self.times.timeout.connect(self.twinkle__)
        # <<<<<<< HEAD
        self.times.start(100)  # 闪烁时间
        # =======
        # self.times.start(50)#闪烁时间
        # self.twinkle__()
        # >>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe

    def twinkle__(self):
        if self.ww > 16:  # 闪烁次数
            self.times.stop()
        if self.ww % 2 == 0:
            self.templist, self.colorlist = self.twinkle_b()
        else:
            self.twinkle_d(self.templist, self.colorlist)
        self.ww += 1

    def getColor(self, no):
        if no==-1:
            return QColor(125,234,234,125)
        colortable=[QColor(234,123,123,125),QColor(200,125,234,125),QColor(125,200,123,125),QColor(120,130,210,125),QColor(125,150,160,125),QColor(12,200,56,125),QColor(36,136,159,125),QColor(225,157,189,125),QColor(173,230,145,125)]
        return colortable[int(no)%len(colortable)]

    def WeekGrid(self, starttime=1, endtime=24):
        self.rowNum=endtime-starttime+1
        #self.starttime_=starttime
        rowNum = self.rowNum       
        grid = QTableWidget()
        #print rowNum
        grid.setSelectionMode(QAbstractItemView.SingleSelection)
        grid.setColumnCount(7)
        grid.setRowCount(self.rowNum)
        column_width = [COL_WIDTH for i in range(7)]
        year=self.date.strftime("%Y")
        month=self.date.strftime("%m")
        todayCol=self.tableDict[self.date.strftime("%a").decode('utf-8')]
        #print todayCol
        for column in range(7):
            grid.setColumnWidth(column, column_width[column])
        for row in range(rowNum):
            grid.setRowHeight(row, 90)
        tempheaderlabels=[]
        beginDate=self.date-timedelta(todayCol)
        for item in self.headerlabels:
            tempheaderlabels.append(item+'\n'+beginDate.strftime("%Y-%m-%d"))
            beginDate=beginDate+timedelta(1)
        grid.setHorizontalHeaderLabels(tempheaderlabels)
        grid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        rowlabels = []

        for i in range(rowNum):
            rowlabels.append(str(i+starttime)+':00')

        grid.setVerticalHeaderLabels(rowlabels)
        ##############################################
       
        beginDate=self.date-timedelta(todayCol)
        flag_=0
        if self.date.strftime("%Y%m%d")==strftime("%Y%m%d"):
            flag_=1
            tableWidgetItem=grid.horizontalHeaderItem(todayCol)
            tableWidgetItem.setForeground(QBrush(QColor(Qt.red)))#DsetBackgroundColor(QColor(Qt.yellow))
            grid.setHorizontalHeaderItem(todayCol, tableWidgetItem)
        for col in range(7):
            if not col==todayCol:
                flag=0
            elif flag_==1:
                flag=1
            for row in range(rowNum):
                #<<<<<<< HEAD
                scheduleid,scheduletitle=self.getHourScheduleTitle(beginDate.strftime("%Y-%m-%d")+'-'+str(row+starttime))
                #print col,row
                #=======
                scheduleid,scheduletitle=self.getHourScheduleTitle(beginDate.strftime("%Y-%m-%d")+'-'+str(row+starttime), self.targetTag)
                #>>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe
                comBox=QListWidget()
                newItem=QListWidgetItem('')
                newItem.setFont(QFont(FONT_TYPE,FONT_SIZE))
                newItem.setFlags(Qt.NoItemFlags)
                
                comBox.addItem(newItem)
                otherschedule=[]
                for i,title in enumerate(scheduletitle):
                    if i<3:
                        title = title.decode('utf-8')
                        if len(title)>6:

                            title=title[:6]+u'...'
                        newItem=QListWidgetItem(unicode(title))
                        newItem.setFont(QFont(FONT_TYPE,FONT_SIZE))
                        newItem.setStatusTip(str(scheduleid[i]))
                        newItem.setBackground(self.getColor(scheduleid[i]))
                        
                        comBox.addItem(newItem)
                    else:
                        otherschedule.append(scheduleid[i])

                if len(otherschedule)>0:
                    newItem=QListWidgetItem(u"还有%d项..."%len(otherschedule))
                    newItem.setFont(QFont(FONT_TYPE,FONT_SIZE))
                    status=''
                    for item in otherschedule:
                        status=status+str(item)+'-'
                    newItem.setStatusTip(status)
                    newItem.setBackground(self.getColor(-1))#QColor(Qt.yellow)))
                    comBox.addItem(newItem)
                comBox.itemDoubleClicked.connect(self.mouseDoubleClicked)
                
                comBox.setStyleSheet("QListWidget::item:selected:!active{background:none;color:#19649F;border-width:2px;}"
                "QListWidget::Item:hover{background:skyblue;}"
                "QListWidget::item:selected:active{background:none;color:#19649F;border-width:-1;}")
                grid.setCellWidget(row,col,comBox)
            beginDate=beginDate+timedelta(1)

        return grid

    def getDayScheduleTitle(self, endDate, targetTag=None):
        TendDate = datetime.strptime(endDate, '%Y-%m-%d')
        endDate_list = endDate.split('-')
        IDlist = []
        Namelist = []
        _list = []
        lists = getlist()
        for i in range(len(lists)):
            temp = lists[i].split(' ')
            temp_list = temp[2].split('-')

            temp_endDate = temp_list[0] + '-' + temp_list[1] + '-' + temp_list[2]
            temp_endDate2 = temp_list[0] + '-' + str(int(temp_list[1])) + '-' + str(int(temp_list[2]))

            # print temp_endDate, endDate
            temp_ID = temp[0]
            # get_tag_list(targetTag)
            # print a
            if targetTag != None:
                inThisTag = get_tag_list(targetTag)
                idlist = []
                for item in inThisTag:
                    idlist.append(item.split()[0])
                if temp_ID not in idlist:
                    continue

            if temp_endDate2 == endDate:
                IDlist.append(temp[0])
                Namelist.append(temp[3])
            else:
                filename = temp_ID + '$$' + temp_endDate + '$$' + temp_list[3]
                path = 'data/list/' + filename
                f = open(path, 'r')
                detail = f.readlines()
                __list = detail[3].split(' ')  #####
                startlist = __list[0].split('-')
                startDate = startlist[0] + '-' + startlist[1] + '-' + startlist[2]
                TstartDate = datetime.strptime(startDate, '%Y-%m-%d')
                repeattype = detail[9].replace('\n', '')
                # 0:天 1:周 2:月 3:年
                repeatfren = int(detail[10].replace('\n', ''))
                endtypelist = detail[11].replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').split(',')
                endtype = -1  #######
                for j in range(len(endtypelist)):
                    if endtypelist[j] == 'True':
                        endtype = j
                        # 0:永不 1;重复次数 2：结束日期
                repeattimes = int(detail[12].replace('\n', ''))
                #print detail[13].replace('\n', '')
                enddate = datetime.strptime(detail[13].replace('\n', ''), '%Y-%m-%d')
                repeatweekdays = detail[14].replace('\n', '').replace('[', '').replace(']', '').split(',')
                if TendDate >= TstartDate:
                    if repeattype == '0':
                        if endtype == 0:  # 按日重复，永不停止
                            delta = TendDate - TstartDate
                            if delta.days % repeatfren == 0:
                                IDlist.append(temp[0])
                                Namelist.append(temp[3])
                        elif endtype == 1:  # 按照日重复，间隔一定的天数
                            due_date = TstartDate + timedelta(days=(repeattimes * repeatfren))
                            delta = TendDate - TstartDate
                            if due_date > TendDate:
                                if delta.days % repeatfren == 0:
                                    IDlist.append(temp[0])
                                    Namelist.append(temp[3])
                        elif endtype == 2:  # 按天重复到某个日期
                            delta = TendDate - TstartDate
                            if enddate >= TendDate:
                                if delta.days % repeatfren == 0:
                                    IDlist.append(temp[0])
                                    Namelist.append(temp[3])
                    elif repeattype == '1':
                        if endtype == 0:  # 按周重复，永不停止
                            weekday = TendDate.weekday()
                            if repeatweekdays[(weekday + 1) % 7 - 1] == ' True':
                                delta = TendDate - TstartDate
                                if delta.days % (7 * repeatfren) < 7:
                                    IDlist.append(temp[0])
                                    Namelist.append(temp[3])
                        elif endtype == 1:  # 按照周重复一定的次数
                            due_date = TstartDate + timedelta(days=(repeattimes * (7 * repeatfren)))
                            if due_date > TendDate:
                                weekday = TendDate.weekday()
                                if repeatweekdays[(weekday + 1) % 7 - 1] == ' True':
                                    delta = TendDate - TstartDate
                                    if delta.days % (7 * repeatfren) < 7:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                        elif endtype == 2:  # 按周重复到某个日期
                            if enddate >= TendDate:
                                weekday = TendDate.weekday()
                                if repeatweekdays[(weekday + 1) % 7 - 1] == ' True':
                                    delta = TendDate - TstartDate
                                    if delta.days % (7 * repeatfren) < 7:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                    elif repeattype == '2':
                        if endtype == 0:  # 按月重复，永不停止
                            delta = (int(endDate_list[0]) - int(startlist[0])) * 12 + int(endDate_list[1]) - int(
                                startlist[1])
                            if delta % repeatfren == 0:
                                if endDate_list[2] == startlist[2]:
                                    IDlist.append(temp[0])
                                    Namelist.append(temp[3])
                        elif endtype == 1:  # 按照月重复一定的次数
                            if endDate_list[2] == startlist[2]:
                                delta = (int(endDate_list[0]) - int(startlist[0])) * 12 + int(endDate_list[1]) - int(
                                    startlist[1])
                                if delta % repeatfren == 0:
                                    if delta / repeatfren < repeattimes:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                        elif endtype == 2:  # 按月重复到某个日期
                            if enddate >= TendDate:
                                if endDate_list[2] == startlist[2]:
                                    delta = (int(endDate_list[0]) - int(startlist[0])) * 12 + int(
                                        endDate_list[1]) - int(
                                        startlist[1])
                                    if delta % repeatfren == 0:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                    elif repeattype == '3':
                        if endtype == 0:  # 按年重复，永不停止
                            delta = (int(endDate_list[0]) - int(startlist[0]))
                            if delta % repeatfren:
                                if endDate_list[2] == startlist[2]:
                                    if endDate_list[1] == startlist[1]:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                        elif endtype == 1:  # 按照年重复一定的次数
                            if endDate_list[2] == startlist[2]:
                                if endDate_list[1] == startlist[1]:
                                    delta = (int(endDate_list[0]) - int(startlist[0]))
                                    if delta % repeatfren == 0:
                                        if delta / repeatfren < repeattimes:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
                        elif endtype == 2:  # 按月重复到某个日期
                            if enddate >= TendDate:
                                delta = (int(endDate_list[0]) - int(startlist[0]))
                                if delta % repeatfren:
                                    if endDate_list[2] == startlist[2]:
                                        if endDate_list[1] == startlist[1]:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
        _list.append(IDlist)
        _list.append(Namelist)
        # print _list
        return _list

    def getHourScheduleTitle(self, startDate, targetTag=None):
        #print startDate
        endDate_list = startDate.split('-')
        endDate = endDate_list[0] + '-' + endDate_list[1] + '-' + endDate_list[2]
        TendDate = datetime.strptime(endDate, '%Y-%m-%d')
        IDlist = []
        Namelist = []
        _list = []
        lists = getlist()
        # print endDate
        for i in range(len(lists)):
            temp = lists[i].split(' ')
            # print temp
            temp_list = temp[1].split('-')  # 开始时间
            temp_list1 = temp[2].split('-')  # 结束时间
            temp_endDate1 = temp_list[0] + '-' + temp_list[1] + '-' + temp_list[2]
            if len(temp_list[2]) == 1:  # 如果只有一个字符加0
                temp_list[2] = '0' + temp_list[2]
            if len(temp_list1[2]) == 1:
                temp_list1[2] = '0' + temp_list1[2]
            temp_endDate = temp_list[0] + '-' + temp_list[1] + '-' + temp_list[2]
            endhour = int(temp_list[3])
            # temp_beginDate = temp_list1[0] + '-' + temp_list1[1] + '-' + temp_list1[2]
            beginhour = int(temp_list1[3])
            # print temp_endDate
            # print endDate
            # <<<<<<< HEAD
            # print endhour, beginhour
            # =======
            # print endhour,beginhour
            temp_ID = temp[0]

            # get_tag_list(targetTag)
            # print a

            if targetTag != None:
                inThisTag = get_tag_list(targetTag)
                idlist = []
                for item in inThisTag:
                    idlist.append(item.split()[0])
                if temp_ID not in idlist:
                    continue

            # >>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe
            #print endDate_list[-1]
            if endhour <= int(endDate_list[-1]) and beginhour >= int(endDate_list[-1]):

                if temp_endDate == endDate:
                    IDlist.append(temp[0])
                    Namelist.append(temp[3])
                else:
                    filename = temp_ID + '$$' + temp_endDate1 + '$$' + temp_list1[3]
                    path = 'data/list/' + filename
                    f = open(path, 'r')
                    detail = f.readlines()
                    startlist = detail[3].split('-')
                    __list = detail[3].split(' ')  #####
                    startlist = __list[0].split('-')
                    _startDate = startlist[0] + '-' + startlist[1] + '-' + startlist[2]
                    TstartDate = datetime.strptime(_startDate, '%Y-%m-%d')
                    repeattype = detail[9].replace('\n', '')
                    # 0:天 1:周 2:月 3:年
                    repeatfren = int(detail[10].replace('\n', ''))
                    endtypelist = detail[11].replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').split(
                        ',')
                    endtype = -1
                    for j in range(len(endtypelist)):
                        if endtypelist[j] == 'True':
                            endtype = j
                            # 0:永不 1;重复次数 2：结束日期
                    repeattimes = int(detail[12].replace('\n', ''))
                    enddate = datetime.strptime(detail[13].replace('\n', ''), '%Y-%m-%d')
                    repeatweekdays = detail[14].replace('\n', '').replace('[', '').replace(']', '').split(',')
                    if TendDate >= TstartDate:
                        if repeattype == '0':
                            if endtype == 0:  # 按日重复，永不停止
                                delta = TendDate - TstartDate
                                if delta.days % repeatfren == 0:
                                    IDlist.append(temp[0])
                                    Namelist.append(temp[3])
                            elif endtype == 1:  # 按照日重复，间隔一定的天数
                                due_date = TstartDate + timedelta(days=(repeattimes * repeatfren))
                                delta = TendDate - TstartDate
                                if due_date > TendDate:
                                    if delta.days % repeatfren == 0:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                            elif endtype == 2:  # 按天重复到某个日期
                                delta = TendDate - TstartDate
                                if enddate >= TendDate:
                                    if delta.days % repeatfren == 0:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                        elif repeattype == '1':
                            if endtype == 0:  # 按周重复，永不停止
                                weekday = TendDate.weekday()
                                if repeatweekdays[(weekday + 1) % 7 - 1] == ' True':
                                    delta = TendDate - TstartDate
                                    if delta.days % (7 * repeatfren) < 7:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                            elif endtype == 1:  # 按照周重复一定的次数
                                due_date = TstartDate + timedelta(days=(repeattimes * (7 * repeatfren)))
                                if due_date > TendDate:
                                    weekday = TendDate.weekday()
                                    if repeatweekdays[(weekday + 1) % 7 - 1] == ' True':
                                        delta = TendDate - TstartDate
                                        if delta.days % (7 * repeatfren) < 7:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
                            elif endtype == 2:  # 按周重复到某个日期
                                if enddate >= TendDate:
                                    weekday = TendDate.weekday()
                                    if repeatweekdays[(weekday + 1) % 7 - 1] == ' True':
                                        delta = TendDate - TstartDate
                                        if delta.days % (7 * repeatfren) < 7:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
                        elif repeattype == '2':
                            if endtype == 0:  # 按月重复，永不停止
                                delta = (int(endDate_list[0]) - int(startlist[0])) * 12 + int(endDate_list[1]) - int(
                                    startlist[1])
                                if delta % repeatfren == 0:
                                    if endDate_list[2] == startlist[2]:
                                        IDlist.append(temp[0])
                                        Namelist.append(temp[3])
                            elif endtype == 1:  # 按照月重复一定的次数
                                if endDate_list[2] == startlist[2]:
                                    delta = (int(endDate_list[0]) - int(startlist[0])) * 12 + int(
                                        endDate_list[1]) - int(
                                        startlist[1])
                                    if delta % repeatfren == 0:
                                        if delta / repeatfren < repeattimes:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
                            elif endtype == 2:  # 按月重复到某个日期
                                if enddate >= TendDate:
                                    if endDate_list[2] == startlist[2]:
                                        delta = (int(endDate_list[0]) - int(startlist[0])) * 12 + int(
                                            endDate_list[1]) - int(
                                            startlist[1])
                                        if delta % repeatfren == 0:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
                        elif repeattype == '3':
                            if endtype == 0:  # 按年重复，永不停止
                                delta = (int(endDate_list[0]) - int(startlist[0]))
                                if delta % repeatfren:
                                    if endDate_list[2] == startlist[2]:
                                        if endDate_list[1] == startlist[1]:
                                            IDlist.append(temp[0])
                                            Namelist.append(temp[3])
                            elif endtype == 1:  # 按照年重复一定的次数
                                if endDate_list[2] == startlist[2]:
                                    if endDate_list[1] == startlist[1]:
                                        delta = (int(endDate_list[0]) - int(startlist[0]))
                                        if delta % repeatfren == 0:
                                            if delta / repeatfren < repeattimes:
                                                IDlist.append(temp[0])
                                                Namelist.append(temp[3])
                            elif endtype == 2:  # 按月重复到某个日期
                                if enddate >= TendDate:
                                    delta = (int(endDate_list[0]) - int(startlist[0]))
                                    if delta % repeatfren:
                                        if endDate_list[2] == startlist[2]:
                                            if endDate_list[1] == startlist[1]:
                                                IDlist.append(temp[0])
                                                Namelist.append(temp[3])
        _list.append(IDlist)
        _list.append(Namelist)
        return _list

    def mouseDoubleClicked(self, eve):
        self.mouseClicked(eve.statusTip())

    def mouseClicked(self, ID):  # 鼠标响应接口，需要对ID类型进行判断，如果为空，则直接返回，不为空，分为单个时间和多个事件，多个事件一定以‘-’结尾
        # print ID

        IDs = unicode(ID).split('-')

        if len(IDs) > 1:
            IDs = IDs[:-1]
            multiWindow = MultiItem(IDs, self)
            if multiWindow.exec_():
                self.refresh()
                return
        else:
            IDs = IDs[0]
            showWindow = Show(IDs)
            detail = details(IDs)
            #d_endtime_list = detail[4].split()
            if showWindow.exec_():

                if showWindow.flag == 1:
                    #print 'twinkle'
                    self.twinkle(showWindow.sonIDList[1:])
                    #self.refresh()
                    return
                    # self.twinkle(showWindow.sonIDList)
                if showWindow.deleteFlag == 1:
                    self.refresh()
                    pass
                else:

                    new_list = getInfo(showWindow)
                    new_filename = IDs + '$$' + new_list[5] + '$$' + new_list[6]
                    new_path = 'data/list/' + new_filename
                    f = open(r"data/root/0_time_routine_ls", 'r')
                    lists = f.readlines()
                    f.close()
                    f = open(r"data/root/0_time_routine_ls", 'w')
                    for i in range(len(lists)):
                        lists[i] = lists[i].replace('\n', '')
                        temp_list = lists[i].split(' ')
                        if IDs == temp_list[0]:
                            filename_list = temp_list[2].split('-')
                            old_filename = temp_list[0] + '$$' + filename_list[0] + '-' + filename_list[1] + '-' + \
                                           filename_list[2] + '$$' + filename_list[3]
                            new_item = IDs + ' ' + new_list[2] + '-' + new_list[3] + '-' + new_list[4] + ' ' + new_list[
                                5] + '-' + new_list[6] + '-' + new_list[7] + ' ' + new_list[0]
                            lists[i] = new_item
                        f.write(lists[i] + '\n')
                    f.close()
                    old_path = 'data/list/' + old_filename
                    os.remove(old_path)
                    fnew = open(new_path, 'w')
                    fnew.write(str(IDs) + '\n')
                    fnew.write(new_list[0] + '\n')
                    fnew.write(new_list[1] + '\n')
                    fnew.write(new_list[2] + ' ' + new_list[3] + ' ' + new_list[4] + '\n')
                    fnew.write(new_list[5] + ' ' + new_list[6] + ' ' + new_list[7] + '\n')
                    fnew.write(str(new_list[8]) + '\n')
                    fnew.write(str(new_list[9]) + '\n')
                    fnew.write(new_list[10] + '\n')
                    for i in range(5):
                        fnew.write(str(new_list[11][i]) + ',')
                    fnew.write('\n')
                    if new_list[13] == []:
                        fnew.write(detail[9] + '\n')
                        fnew.write(detail[10] + '\n')
                        fnew.write(detail[11] + '\n')
                        fnew.write(detail[12] + '\n')
                        fnew.write(detail[13] + '\n')
                        fnew.write(detail[14] + '\n')
                    else:
                        for i in range(6):
                            fnew.write(str(new_list[13][i]) + '\n')
                    fnew.write(detail[15] + '\n')
                    fnew.write(detail[16] + '\n')
                    fnew.close()
                    note_path = 'data/note/' + IDs
                    fnote = open(note_path, 'w')
                    fnote.write(new_list[12])
                    fnote.close()

                    #remove(IDs)

                    #save(getinfo(addWindow), last_num, fname_sonIDlist)
                    update = updateToS()
                    if update == -1:
                        warn = Warn('未预留邮箱信息！')
                        self.refresh()
                        if warn.exec_():
                            return
                    elif update == -2:
                        warn = Warn('网络异常，无法同步到服务器')
                        self.refresh()
                        if warn.exec_():
                            return
                    else:
                        print 'show'
                        self.refresh()
                        pass


                return

    def addNewEvent(self, row, col, ID, title):  # 仅更改显示，数据未存
        comBox = self.grid.cellWidget(row, col)
        if comBox is None:
            comBox = QListWidget()
            self.grid.setCellWidget(row, col, comBox)
        if comBox.count() > 0:
            item_C = comBox.item(comBox.count() - 1)
            if item_C.statusTip()[-1] == '-':
                string_c = item_C.statusTip()
                num = string_c.count('-')
                string_c = string_c + str(ID) + '-'
                item_C.setStatusTip(string_c)
                item_C.setText(u"还有%d项..." % (num + 1))
                return
            elif comBox.count() > 2:
                item_C = QListWidgetItem(u"还有1项...")
                item_C.setFont(QFont(FONT_TYPE, FONT_SIZE))
                item_C.setStatusTip(str(ID) + '-')
                comBox.addItem(item_C)
                return
        title = title.decode('utf-8')
        if len(title) > 6:

            title = title[:6] + u'...'
        newItem = QListWidgetItem(unicode(title))
        newItem.setFont(QFont(FONT_TYPE, FONT_SIZE))
        newItem.setStatusTip(str(ID))
        comBox.addItem(newItem)
        comBox.itemDoubleClicked.connect(self.mouseDoubleClicked)

    def MonthGrid(self):
        beginDay = datetime(int(self.date.strftime("%Y")), int(self.date.strftime("%m")), 1)
        year = int(self.date.strftime("%Y"))
        month = int(self.date.strftime("%m"))
        beginRow = 0
        beginCol = self.tableDict[beginDay.strftime("%a").decode('utf-8')]
        monthTime = monthrange(int(self.date.strftime("%Y")), int(self.date.strftime("%m")))[1]
        todayCol = self.tableDict[self.date.strftime("%a").decode('utf-8')]
        todayRow = (int(self.date.strftime("%d")) + beginCol - 1) / 7
        mrowNum = (beginCol + monthTime + 6) / 7
        self.rowNum = mrowNum
        grid = QTableWidget()
        grid.setColumnCount(7)
        grid.setRowCount(mrowNum)
        column_width = [COL_WIDTH for i in range(7)]
        for column in range(7):
            grid.setColumnWidth(column, column_width[column])
        for row in range(mrowNum):
            grid.setRowHeight(row, ROW_HEIGHT)

        grid.setHorizontalHeaderLabels(self.headerlabels)
        grid.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for day in range(monthTime):
            text = beginDay.strftime("%m-%d")
            scheduleid, scheduletitle = self.getDayScheduleTitle(str(year) + '-' + str(month) + '-' + str(day + 1),
                                                                 self.targetTag)
            # print scheduleid, scheduletitle
            comBox = QListWidget()
            newItem = QListWidgetItem(unicode(text))

            if self.date.strftime("%Y-%m-%d") == strftime("%Y-%m-%d") and day == int(self.date.strftime("%d")) - 1:
                newItem.setBackground(QBrush(QColor(255, 217, 42)))
                #newItem.setBackground(QBrush(QColor(Qt.yellow)))
            newItem.setFlags(Qt.NoItemFlags)
            comBox.addItem(newItem)
            otherschedule = []

            for i, title in enumerate(scheduletitle):
                if i < 3:
                    title = title.decode('utf-8')
                    if len(title) > 6:

                        title = title[:6] + '...'
                    #print title
                    newItem = QListWidgetItem(unicode(title))
                    newItem.setFont(QFont(FONT_TYPE, FONT_SIZE))
                    newItem.setStatusTip(str(scheduleid[i]))
                    newItem.setBackground(self.getColor(scheduleid[i]))
                    comBox.addItem(newItem)
                else:
                    otherschedule.append(scheduleid[i])
            if len(otherschedule) > 0:
                newItem = QListWidgetItem(u"还有%d项..." % len(otherschedule))
                newItem.setFont(QFont(FONT_TYPE, FONT_SIZE))
                status = ''

                for item in otherschedule:
                    status = status + str(item) + '-'
                newItem.setStatusTip(status)
                newItem.setBackground(self.getColor(-1))
                comBox.addItem(newItem)
            comBox.itemDoubleClicked.connect(self.mouseDoubleClicked)

            comBox.setStyleSheet("QListWidget::item:selected:!active{background:none;color:#19649F;border-width:2px;}"
                                 "QListWidget::Item:hover{background:skyblue;}"
                                 "QListWidget::item:selected:active{background:none;color:#19649F;border-width:-1;}")
            # grid.setCellWidget(0,3,comBox)
            # tempDay=QTableWidgetItem(text)
            tempCol = beginCol
            tempRow = beginRow
            # tempDay.setTextAlignment(Qt.AlignCenter)

            grid.setCellWidget(tempRow, tempCol, comBox)

            beginCol += 1
            beginRow = beginRow + beginCol / 7
            beginCol = beginCol % 7
            beginDay = beginDay + timedelta(1)

        return grid

    def upPage(self):
        if self.pageFlag == 'w':
            self.grid.close()
            self.grid = self.wupPage()
            self.calendarLayout.addWidget(self.grid)
        else:
            self.grid.close()
            self.grid = self.mupPage()
            self.calendarLayout.addWidget(self.grid)

    def nextPage(self):
        if self.pageFlag == 'w':
            self.grid.close()
            self.grid = self.wnextPage()
            self.calendarLayout.addWidget(self.grid)

        else:
            self.grid.close()
            self.grid = self.mnextPage()
            self.calendarLayout.addWidget(self.grid)

    def mupPage(self):
        month = int(self.date.strftime('%m'))
        year = int(self.date.strftime('%Y'))
        if month == 1:
            year = year - 1
            month = 12
        else:
            month = month - 1
        self.date = self.date - timedelta(monthrange(year, month)[1])
        return self.MonthGrid()

    def mnextPage(self):
        month = int(self.date.strftime('%m'))
        year = int(self.date.strftime('%Y'))
        self.date = self.date + timedelta(monthrange(year, month)[1])
        return self.MonthGrid()

    def wupPage(self):
        self.date = self.date - timedelta(days=7)
        return self.WeekGrid()

    def wnextPage(self):

        self.date = self.date + timedelta(days=7)
        return self.WeekGrid()


def main():

    app = QApplication(sys.argv)
    talendar = Talendar()
    talendar.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()









