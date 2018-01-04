# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, Comment
import re
import os
import logging
import json
import time
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO)

def filter(s):
	date = '-'.join([str(int(s.split()[0].split('-')[i])) for i in range(3)])
	hour = str(int(s.split()[1].split(':')[0]))
	minute = str(int(s.split()[1].split(':')[1]))
	return date, hour, minute


class GetTimetable(object):
	def __init__(self, username, password):
		self.session = requests.Session()
		self.urlLogin = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
		self.loginData = {'i_user': username, 'i_pass': password}
		self.cookies = self.session.post(self.urlLogin, data=self.loginData, verify=False).cookies
		self.semester = self.getCurrentSemester()
		self.currentCourse = self.getCourseInfo()
	
	def getCurrentSemester(self):
		currentSemesterUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/getCurrentTeachingWeek'
		res = self.session.get(currentSemesterUrl, cookies=self.cookies).json()
		logging.info("current semester is " + res['currentSemester']['semesterName'])
		
		return (res['currentSemester'])

	def getCourseInfo(self):
		courseListUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester['id']
		res = self.session.get(courseListUrl, cookies=self.cookies).json()
		return (res['resultList'])


	def getCourseTime(self):
		classList = []
		startTime = {
		'1':28800,
		'2':35400,
		'3':48600,
		'4':55200,
		'5':61500,
		'6':69600,
		}
		endTime ={
		'1':34500,
		'2':41100,
		'3':54300,
		'4':60900,
		'5':67200,
		'6':75300,
		}
		semesterStartDay = self.semester['startDate']
		stamp = time.mktime(time.strptime(semesterStartDay,"%Y-%m-%d"))
		for i in self.currentCourse:
			currentCourseName = i['course_name']
			currentCourseTeacherName = i['teacherInfo']['name']
			currentCourseTeacherEmail = i['teacherInfo']['email']
			if currentCourseTeacherEmail == None:
				currentCourseTeacherEmail = 'None'

			timeplaceListUrl = 'http://learn.cic.tsinghua.edu.cn/b/course/info/timePlace/' + i['courseId']
			res = self.session.get(timeplaceListUrl, cookies=self.cookies).json()
			for records in res['resultList']:
				coursePlace = records['skdd']
				if records['skjc'].encode("utf-8") == '0':
					logging.info('unfixed course time ' + currentCourseName)
				else:
					repeatGap = '1'
					if records['skzc'] =="前8周":
						repeatTimes = '8'
						timeFlag = stamp + (int(records['skxq']) - 1) * 86400.0
					elif records['skzc'] =="后8周":
						repeatTimes = '8'
						timeFlag = stamp + (int(records['skxq']) - 1 + 56) * 86400.0
					elif records['skzc'] =="全周":
						repeatTimes = '16'
						timeFlag = stamp + (int(records['skxq']) - 1) * 86400.0
					elif records['skzc'] =="双周":
						repeatTimes = '8'
						repeatGap = '2'
						timeFlag = stamp + (int(records['skxq']) - 1 + 7) * 86400.0
					elif records['skzc'] =="单周":
						repeatTimes = '8'
						repeatGap = '2'
						timeFlag = stamp + (int(records['skxq']) - 1) * 86400.0
					else:
						logging.info(currentCourseName + "未识别的上课类型：" + records['skzc'])
					courseTimeStart = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeFlag + startTime[records['skjc'].encode("utf-8")]))
					startDate, startHour, startMinute = filter(courseTimeStart)
					courseTimeEnd = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeFlag + endTime[records['skjc'].encode("utf-8")]))
					endDate, endHour, endMinute = filter(courseTimeEnd)
					repeatFlag = [False, False, False, False, False, False]
					repeatFlag.insert(int(records['skxq'])-1,True)
					courseInfoList = [currentCourseName, coursePlace, \
					startDate, startHour, startMinute, endDate, endHour, endMinute, '0', '0', '30', [u'课程', u'网络学堂', u'', u'', u''],\
					"教师姓名："+currentCourseTeacherName + "\r教师邮箱：" + currentCourseTeacherEmail + "\r课程类型：" + records['skzc'] ,\
					 [1, unicode(repeatGap), [False, True, False], unicode(repeatTimes), '1000-1-1', repeatFlag]]
					classList.append(courseInfoList)
		return classList



class WebLearningScraper(object):
	def __init__(self, username, password):
		self.oldLogin(username, password)
		self.newLogin(username, password)
		self.semester = self.getCurrentSemester()
		self.currentCourse = self.getCourseInfo()

	def oldLogin(self,username, password):
		self.sessionOld = requests.Session()
		self.oldUrlLogin = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
		self.loginDataOld = {'userid':username, 'userpass':password}
		r = self.sessionOld.post(self.oldUrlLogin,self.loginDataOld )
	def newLogin(self,username, password):
		self.sessionNew = requests.Session()
		self.newUrlLogin = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
		self.loginDataNew = {'i_user': username, 'i_pass': password}
		self.cookies = self.sessionNew.post(self.newUrlLogin, data=self.loginDataNew, verify=False).cookies
	def getCurrentSemester(self):
		currentSemesterUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/getCurrentTeachingWeek'
		res = self.sessionNew.get(currentSemesterUrl, cookies=self.cookies).json()
		logging.info("current semester is " + res['currentSemester']['semesterName'])
		return (res['currentSemester']['id'])

	def getCourseInfo(self):
		courseListUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester
		res = self.sessionNew.get(courseListUrl, cookies=self.cookies).json()
		return (res['resultList'])

	def getCourseinfoDict(self):
		courseListUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester
		res = self.sessionNew.get(courseListUrl, cookies=self.cookies).json()
		infoDict = {}
		for item in res['resultList']:
			infoDict[item['courseId']] = item
		return (infoDict)

	def makeSoup(self,url):
		r = self.sessionOld.get(url)
		r.encoding = 'bgk'
		soup = BeautifulSoup(r.content, "html.parser")
		return soup
	def courses(self):
		soup = self.makeSoup('http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?typepage=1')
		homeworkList = []
		newWebLearningList = []
		for j in soup.find_all('tr', class_=['info_tr', 'info_tr2']):
			i = j.find('a')
			url = i['href']
			if url.startswith('/Mult'):
				url = 'https://learn.tsinghua.edu.cn' + url
				name = i.contents[0]
				name = re.sub(r'[\n\r\t ]', '', name)
				name = re.sub(r'\([^\(\)]+\)$', '', name)
				name = re.sub(r'\([^\(\)]+\)$', '', name)
				id = url[-6:]
				
				url = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/hom_wk_brw.jsp?course_id=' + id
				soup = self.makeSoup(url)
				for i in soup.find_all('tr', class_=['tr1', 'tr2']):
					tds = i.find_all('td')
					if (( '已经提交' in tds[3].contents[0]) == 1):
						continue
					else:
						detailUrl = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/' + i.find('a')['href']
						id = re.search(r'(\d+)', url).group(0)
						title = i.find('a').contents[0]
						logging.info('course homework for course ' + name + ':' + title)
						startTime = tds[1].contents[0] + " 0:00:00"
						
						endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.strptime(tds[2].contents[0],"%Y-%m-%d")) + 86399))
						endDate, endHour, endMinute = filter(endTime)
						endtime = datetime.datetime(int(endDate.split('-')[0]), int(endDate.split('-')[1]), int(endDate.split('-')[2]))
						now = datetime.datetime.now()
						if (now-endtime).days>=3:
							continue
						startDate, startHour, startMinute = endDate, endHour, str(int(endMinute) - 1)
						#submitted = ( '已经提交' in tds[3].contents[0])
						soup = self.makeSoup(detailUrl)
						try:
							details = soup.find_all('td', class_='tr_2')[1].textarea.contents[0]
						except:
							details = ""
						#print name
						homeworkList.append([ name  + '：' + title, '', startDate, startHour, startMinute, endDate, endHour, endMinute,\
						'0', '0', '30', [u'作业', u'网络学堂', u'DDL', u'', u''], details, [-1, u'-1', [False, False, False], u'-1', '1000-1-1',\
						 [False, False, False, False, False, False, False]]])
			else:
				continue
		for i in self.currentCourse:
			logging.info('course homework for course ' + i['course_name'] + ':')
			homeworkCourseName = i['course_name']
			newHomeworkUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/homework/list4Student/' + i['courseId'] +'/0'
			res = self.sessionNew.get(newHomeworkUrl, cookies=self.cookies).json()
			for records in res['resultList']:
				#0，尚未提交；1，已经提交；3，已经批改
				if (records['courseHomeworkRecord']['status'] =='0'):
					homeworkTitle = records['courseHomeworkInfo']['title']
					homeworkDetail = records['courseHomeworkInfo']['detail']
					homeworkStartTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(records['courseHomeworkInfo']['beginDate']/1000))
					homeworkEndTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(records['courseHomeworkInfo']['endDate']/1000))
					
					endDate, endHour, endMinute = filter(homeworkEndTime)
					startDate, startHour, startMinute = endDate, endHour, str(int(endMinute) - 1)
					endtime = datetime.datetime(int(endDate.split('-')[0]), int(endDate.split('-')[1]), int(endDate.split('-')[2]))
					now = datetime.datetime.now()
					if (now-endtime).days>=3:
						continue
					homeworkList.append([homeworkCourseName + '：' + homeworkTitle, '', startDate, startHour, startMinute, endDate, endHour, endMinute,\
						'0', '0', '30', [u'作业', u'网络学堂', u'DDL', u'', u''], homeworkDetail, [-1, u'-1', [False, False, False], u'-1', '1000-1-1',\
						 [False, False, False, False, False, False, False]]])
		return homeworkList
	
def main(username, password):
	try:
		info = GetTimetable(username, password).getCourseTime()
		homework = WebLearningScraper(username, password).courses()
		return info, homework
	except:
		return '!!!', '!!!'
