# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO)

class NewWebLearningScraper(object):
	def __init__(self, username, password):
		self.session = requests.Session()
		self.urlLogin = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
		self.loginData = {'i_user': username, 'i_pass': password}
		self.cookies = self.session.post(self.urlLogin, data=self.loginData, verify=False).cookies
		self.semester = '2017-2018-1'
		self.currentCourse = self.getCourseInfo()

	def getCourseInfo(self):
		courseListUrl = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester
		res = self.session.get(courseListUrl, cookies=self.cookies).json()
		return (res['resultList'])
	
	def getCourseTime(self):
		classList = []
		startTime = {
		'1':'8:00',
		'2':'9:50',
		'3':'13:30',
		'4':'15:20',
		'5':'17:05',
		'6':'19:20',
		}
		endTime ={
		'1':'9:35', 
		'2':'11:25', 
		'3':'15:05', 
		'4':'16:55', 
		'5':'18:40', 
		'6':'20:55', 
		}
		
		for i in self.currentCourse:
			logging.info('course time for course id ' + i['course_name'] + ':')
			
			timeplaceListUrl = 'http://learn.cic.tsinghua.edu.cn/b/course/info/timePlace/' + i['courseId']
			res = self.session.get(timeplaceListUrl, cookies=self.cookies).json()
			
			currentCourseName = i['course_name']
			currentCourseTeacherName = i['teacherInfo']['name']
			currentCourseTeacherEmail = i['teacherInfo']['email']

			if res['message'] == 'success':
				for records in res['resultList']:
					coursePlace = records['skdd']
					if records['skjc'].encode("utf-8") == '0':
						logging.info('unfixed course time ' + currentCourseName)
					else:
						courseStartTime = startTime[records['skjc'].encode("utf-8")]
						courseEndTime = endTime[records['skjc'].encode("utf-8")]
						if records['skzc'] =="前8周":
							repeatTimes = '8'
							timeFlag = "2017-9-"+str(17+int(records['skxq'])) +" "
						elif records['skzc'] =="后8周":
							repeatTimes = '8'
							timeFlag = "2017-11-"+str(12+int(records['skxq'])) +" "
						elif records['skzc'] =="全周":
							repeatTimes = '16'
							timeFlag = "2017-9-"+str(17+int(records['skxq'])) +" "
						else:
							return -1
						courseTimeStart = timeFlag + courseStartTime
						courseTimeEnd = timeFlag + courseEndTime
						repeatFlag = [False, False, False, False, False, False]
						repeatFlag.insert(int(records['skxq'])-1,True)
						courseInfoList = [currentCourseName, coursePlace, \
						courseTimeStart, courseTimeEnd, 0, 0, '课程' ,'' ,'' ,'' ,'' ,\
						'1', '1', [False, True, False], repeatTimes, '', repeatFlag, \
						"教师姓名："+currentCourseTeacherName + "\r教师邮箱：" + currentCourseTeacherEmail\
						 + "\r课程类型：" + records['skzc'] ]
						classList.append(courseInfoList)
		return classList
	


if __name__ == '__main__':
	scraper = NewWebLearningScraper(username='', password='')  # TODO:change username and password
	print(json.dumps(scraper.getCourseTime(),ensure_ascii=False,indent = 4))
