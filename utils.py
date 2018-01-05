# -*- coding: utf-8 -*-

import os
import tx
import os.path
from datetime import datetime
from datetime import timedelta
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def UpdateToS():

    try:
        f = open('./data/user.csv')
    except:
        return -1

    s = f.readline()
    email = s.split('\t')[-1]
    info = getCompletelist()
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
            tx.main(infoList)
        except:
            #print 'wrong'
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


def getList():
    f = open(r"data/root/0_time_routine_ls", 'r')
    lists = f.readlines()
    f.close()
    for i in range(lists.__len__()):
        lists[i] = lists[i].replace('\n', '')
    del lists[0]
    del lists[0]
    # print lists
    return lists


def listofTag(tag):
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


def getCompletelist():
    full_list = []
    lists = getList()
    for i in range(lists.__len__()):
        temp = lists[i].split(' ')
        temp_list = details(temp[0])
        full_list.append(temp_list)
    return full_list


def tranBoolList(aList):
    a = aList.replace('False', '0').replace('True', '1')
    a = a[1:-1].split(', ')
    return a


def saveSon(addWindow):
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
        return


def saveModify(IDs, new_list):
    detail = details(IDs)
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
    return


def getDayTitle(endDate, targetTag=None):
    TendDate = datetime.strptime(endDate, '%Y-%m-%d')
    endDate_list = endDate.split('-')
    IDlist = []
    Namelist = []
    _list = []
    lists = getList()
    for i in range(len(lists)):
        temp = lists[i].split(' ')
        temp_list = temp[2].split('-')

        temp_endDate = temp_list[0] + '-' + temp_list[1] + '-' + temp_list[2]
        temp_endDate2 = temp_list[0] + '-' + str(int(temp_list[1])) + '-' + str(int(temp_list[2]))

        # print temp_endDate, endDate
        temp_ID = temp[0]
        # listofTag(targetTag)
        # print a
        if targetTag != None:
            inThisTag = listofTag(targetTag)
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
            # print detail[13].replace('\n', '')
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


def getHourTitle(startDate, targetTag=None):
    endDate_list = startDate.split('-')
    endDate = endDate_list[0] + '-' + endDate_list[1] + '-' + endDate_list[2]
    TendDate = datetime.strptime(endDate, '%Y-%m-%d')
    IDlist = []
    Namelist = []
    _list = []
    lists = getList()
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

        # listofTag(targetTag)
        # print a

        if targetTag != None:
            inThisTag = listofTag(targetTag)
            idlist = []
            for item in inThisTag:
                idlist.append(item.split()[0])
            if temp_ID not in idlist:
                continue

        # >>>>>>> ee7dd62a3e4e07044937d59e1ac273ea592c74fe
        # print endDate_list[-1]
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


def initFolder():
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


def getLastNum():
    fname = "data/root/0_time_routine_ls"
    fname_sonIDlist = "data/list/sonIDlist"
    f_sonIDlist = open(fname_sonIDlist, 'w')
    with open(fname, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
        penult_line = lines[-2]
    list1 = last_line.split(' ')
    list2 = penult_line.split(' ')
    # print list1
    # print list2
    last_num = int(list1[0])
    if int(list2[0]) > int(list1[0]): last_num = int(list2[0])
    f.close()
    f_sonIDlist.write('0' + '\n')
    f_sonIDlist.write(str(last_num + 1) + ',')
    f_sonIDlist.close()
    return last_num, fname_sonIDlist


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
    #print date
    month = date[-3].replace('月', '')
    weekdays = {'周一': 1, '周二': 2, '周三': 3, '周四': 4, '周五': 5, '周六': 6, '周日': 7}
    weekday = weekdays[date[0]]
    date = date[-1] + '-' + month + '-' + date[-2]
    #date_weekday = date + '-' + str(weekday)
    # print date
    # print date_weekday
    return date
