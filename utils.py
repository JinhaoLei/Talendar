# -*- coding: utf-8 -*-

import os
import os.path
import re
import sys
import client
reload(sys)
sys.setdefaultencoding('utf8')

def updateToS():

    try:
        f = open('./data/user.csv')
    except:
        return -1

    s = f.readline()
    email = s.split('\t')[-1]
    info = getcompletelist()
    infoList = ''
    for item in info:
        id, title, loc, startTime, endTime, reminder, reminderUnit, \
        reminderNumber, tags, comboUnit, frequency, radioSelected, endTimes, endDate, \
        checkBoxGroup, sonID, sonIDList, note = item
        if reminder == '2':
            print 'here'
            tag = tags.split(',')
            if 'DDL' in tag:
                ddlFlag = '1'
            else:
                ddlFlag = '0'
            infoList += title + '\t' + loc + '\t' + startTime + '\t' + endTime \
                        + '\t' + tags + '\t' + reminderUnit + '\t' + reminderNumber + '\t' + ddlFlag + '\t' + email + '\t' + note + '$$'
            #print infoList
    if len(infoList) > 1:
        try:
            client.main(infoList)
        except:
            return -2
    else:
        pass
    return 0

def transDate(date):
    [year, month, day] = date.split('-')
    s = month + u'月' + day + u'日 ' + year
    return s

def details(ID):
    f = open(r"data/root/0_time_routine_ls", 'r')
    lists = f.readlines()
    f.close()
    flag = False
    _list = []
    for i in range(len(lists)):
        lists[i] = lists[i].replace('\n', '')
        temp_list = lists[i].split(' ')
        # print temp_list, ID
        # print temp_list[0], ID
        if ID == temp_list[0]:
            filename_list = temp_list[2].split('-')
            filename = temp_list[0] + '$$' + filename_list[0] + '-' + filename_list[1] + '-' + filename_list[2] + '$$' + \
                       filename_list[3]
            flag = True
    if flag:
        path = 'data/list/' + filename
        notepath = 'data/note/' + ID
        if os.path.isfile(path):
            f = open(path, 'r')
            f_notepath = open(notepath, 'r')
            note = f_notepath.read()
            _list = f.readlines()
            for i in range(len(_list)):
                _list[i] = _list[i].replace('\n', '')
            _list.append(note)
        return _list
    else:
        return _list

def getlist():
    f = open(r"data/root/0_time_routine_ls", 'r')
    lists = f.readlines()
    f.close()
    for i in range(lists.__len__()):
        lists[i] = lists[i].replace('\n', '')
    del lists[0]
    del lists[0]
    # print lists
    return lists


def get_tag_list(tag):
    path = u'data/root/'.encode('utf-8') + tag
    try:
        f = open(path.decode('utf8'), 'r')
    except:
        return []
    lists = f.readlines()
    for i in range(lists.__len__()):
        lists[i] = lists[i].replace('\n', '')
    return lists


def getTagList():
    f = open(r"data/root/tags", 'r')
    tags = []
    for n, line in enumerate(f):
        if n == 0:
            pass
        else:
            tags.append(line.strip())
    return tags


def getcompletelist():
    full_list = []
    lists = getlist()
    for i in range(lists.__len__()):
        temp = lists[i].split(' ')
        temp_list = details(temp[0])
        full_list.append(temp_list)
    return full_list


def tranBoolList(aList):
    a = aList.replace('False', '0').replace('True', '1')
    a = a[1:-1].split(', ')
    return a


def remove(ID):
    detail = details(ID)
    tags = detail[8].split(',')
    for i in range(5):
        tags[i] = tags[i].decode('utf-8')
    k = -1
    _tag_list = []
    for i in range(5):
        if not tags[i] == '':
            tag_path = u'data/root/'.encode('utf-8') + tags[i].encode('utf-8')
            f = open(tag_path.decode('utf-8').encode('gbk'), 'r')
            tag_list = f.readlines()
            f.close()
            for j in range(len(tag_list)):
                _tag_list.append(tag_list[j].replace('\n', ''))
                tag_temp = _tag_list[j].split(' ')
                if ID == tag_temp[0]:
                    del tag_list[j]
                    break
            if len(tag_list):
                f = open(tag_path.decode('utf-8').encode('gbk'), 'w')
                #print tag_list
                f.writelines(tag_list)
                f.close()
            else:
                f = open(r"data/root/tags", 'r')
                os.remove(tag_path.decode('utf-8').encode('gbk'))
                tag_lists = f.readlines()
                f.close()
                for h in range(len(tag_lists)):
                    if tags[i] == tag_lists[h].replace('\n', '').decode('utf-8'):
                        del tag_lists[h]
                        break
                f = open(r"data/root/tags", 'w')
                f.writelines(tag_lists)
                f.close()
    time_list = detail[4].split(' ')
    filename = ID + '$$' + time_list[0] + '$$' + time_list[1]
    f = open(r"data/root/0_time_routine_ls", 'r')
    lists = f.readlines()
    f.close()
    _lists = []
    lenth = len(lists)
    for i in range(0, len(lists))[::-1]:
        _lists.append(lists[i].replace('\n', ''))
        temp_list = _lists[lenth - 1 - i].split(' ')
        if ID == temp_list[0]:
            path = 'data/list/' + filename
            os.remove(path)
            del lists[i]
    notepath = 'data/note/' + ID
    os.remove(notepath)

    f = open(r"data/root/0_time_routine_ls", 'w')
    f.writelines(lists)
    f.close()

    if detail[15] == '0':
        sonlist = detail[16].split(',')
        if sonlist[0] != ID:
            parent_list = details(sonlist[0])
            if not parent_list == []:
                del parent_list[-1]
                pa_sonlist = parent_list[-1].split(',')
                del parent_list[-1]
                for i in range(0, len(pa_sonlist))[::-1]:
                    if pa_sonlist[i] == ID:
                        del pa_sonlist[i]
                        pa_numson = int(parent_list[-1]) - 1
                        parent_list[-1] = str(pa_numson)
                pa_time = parent_list[4].split(' ')
                pa_fil_name = parent_list[0] + '$$' + pa_time[0] + '$$' + pa_time[1]
                pa_fil_name = 'data/list/' + pa_fil_name
                parent_f = open(pa_fil_name, 'w')
                for i in range(len(parent_list)):
                    parent_f.write(parent_list[i] + '\n')
                for i in range(len(pa_sonlist) - 1):
                    parent_f.write(pa_sonlist[i] + ',')
                parent_f.close()
    else:
        son_list = detail[16].split(',')
        del son_list[-1]
        del son_list[0]
        for i in range(len(son_list)):
            remove(son_list[i])
    # print lists
    # print _lists
    # del lists[k]
    return

def getInfo(addWindow):
    name = addWindow.editTitle.text()
    location = addWindow.editLoc.text()
    startDate = addWindow.editStartDate.text()
    startDate = filter(str(startDate))
    startHour = addWindow.editStartHour.text()
    startMinute = addWindow.editStartMinute.text()
    endDate = addWindow.editEndDate.text()
    startDate = filter(str(startDate))
    endHour = addWindow.editEndHour.text()
    endMinute = addWindow.editEndMinute.text()
    reminder = addWindow.comboReminder.currentIndex()
    reminderUnit = addWindow.comboReminderUnit.currentIndex()
    reminderNumber = addWindow.editReminderTime.text()
    tags = [unicode(addWindow.tagGroup[i].text()) for i in range(5)]
    note = addWindow.editNote.toPlainText()
    repeatInfo = addWindow.repeatParameters

    if name == '':
        name = 'None'

    if location == '':
        location = 'None'

    if startDate == '':
        startDate = '1000-1-1'
    else:
        startDate = filter(str(startDate))

    if startHour == '':
        startHour = '25'

    if startMinute == '':
        startMinute = '61'

    if endDate == '':
        endDate = '1000-1-1'
    else:
        endDate = filter(str(endDate))

    if endHour == '':
        endHour = '25'

    if endMinute == '':
        endMinute = '61'

    if note == '': note = 'None'

    if reminderNumber == '':
        reminderNumber = '-1'

    return [name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, reminder, reminderUnit, reminderNumber, tags, note, repeatInfo]

def save(info_list, last_num, fname_sonIDlist):
    #print info_list
    #print len(info_list)
    name, location, startDate, startHour, startMinute, endDate, endHour, endMinute, reminder, reminderUnit, reminderNumber, tags, note, repeatInfo = info_list

    f_tags = open(r"data/root/tags", 'r')
    tags_list = f_tags.readlines()
    f_tags.close()
    f_tags = open(r"data/root/tags", 'w')
    f_tags.writelines(tags_list)
    filename = str(last_num + 1) + '$$' + str(endDate) + '$$' + str(endHour)
    flag = False
    #print tags
    for i in range(5):
        flag = False
        if tags[i] != '':
            for j in range(tags_list.__len__()):
                if str(tags[i]) == tags_list[j].replace('\n', ''):
                    flag = True
            if not flag:
                #print tags[]
                f_tags.write(str(tags[i]) + '\n')
            tag_filename = 'data/root/' + tags[i]
            f_special_tags = open(tag_filename.decode('utf-8'), 'a')
            f_special_tags.write(str(last_num + 1) + ' ' + startDate + '-' + startHour + '-' + startMinute + ' '
                                 + endDate + '-' + endHour + '-' + endMinute + ' ' + name + '\n')
            f_special_tags.close()
    f_tags.close()

    #print repeatInfo
    # sonIDList = addWindow.sonIDList
    # 给父级事件赋子事件
    note_path = 'data/note/' + str(last_num + 1)
    path = 'data/list/' + filename
    f_notefile = open(note_path, 'w')
    f_notefile.write(note)
    f_notefile.close()
    f = open(path, 'w')
    f.write(str(last_num + 1) + '\n')
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
    # f_repeat = open(r'data/list/new', 'r')
    # repeat_list = f_repeat.readlines()
    # f_repeat.close()
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
    f_sonIDlist = open(fname_sonIDlist, 'r')
    son_list = f_sonIDlist.readlines()
    # print son_list
    f.writelines(son_list)
    f_sonIDlist.close()
    os.remove(fname_sonIDlist)
    # os.remove(r'data/list/new')
    f.close()

    f_time_routine = open(r"data/root/0_time_routine_ls", 'a')
    f_time_routine.write(str(last_num + 1) + ' ' + startDate + '-' + startHour + '-' + startMinute + ' '
                         + endDate + '-' + endHour + '-' + endMinute + ' ' + name + '\n')
    f_time_routine.close()

def saveRepeat(repeatWindow, addWindow):
    comboUnit = repeatWindow.comboUnit.currentIndex()
    frequency = repeatWindow.editFre.text()
    if frequency == '': frequency = '-1'
    radioSelected = [repeatWindow.radioNever.isChecked(), repeatWindow.radioTimes.isChecked(),
                     repeatWindow.radioEnd.isChecked()]
    endTimes = repeatWindow.editTimes.text()
    if endTimes == '': endTimes = '-1'
    endDate = repeatWindow.editEnd.text()
    if endDate == '':
        endDate = '1000-1-1'
    else:
        endDate = filter(str(endDate))
    checkBoxGroup = [repeatWindow.checkBoxGroup[i].isChecked() for i in range(7)]
    addWindow.repeatParameters = [comboUnit, unicode(frequency), radioSelected, unicode(endTimes), unicode(endDate),
                             checkBoxGroup]  # 所有重复窗口里面设置的参数
def filter(s):
    if re.match(r"(\d{4}-\d{1,2}-\d{1,2})", s):
        return s
    date = s.split()
    month = date[-3].replace('月', '')
    weekdays = {'周一': 1, '周二': 2, '周三': 3, '周四': 4, '周五': 5, '周六': 6, '周日': 7}
    weekday = weekdays[date[0]]
    date = date[-1] + '-' + month + '-' + date[-2]

    return date
