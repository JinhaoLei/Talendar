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

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO)

class GetTimetable(object):
	def __init__(self, username, password):
		self.session = requests.Session()
		self.url_login = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
		self.login_data = {'i_user': username, 'i_pass': password}
		self.cookies = self.session.post(self.url_login, data=self.login_data, verify=False).cookies
		self.semester = self.get_current_semester()
		self.currentCourse = self.get_course_info()
	
	def get_current_semester(self):
		current_semester_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/getCurrentTeachingWeek'
		res = self.session.get(current_semester_url, cookies=self.cookies).json()
		logging.info("current semester is " + res['currentSemester']['semesterName'])
		
		return (res['currentSemester'])

	def get_course_info(self):
		course_list_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester['id']
		res = self.session.get(course_list_url, cookies=self.cookies).json()
		return (res['resultList'])


	def get_course_time(self):
		class_list = []
		start_time = {
		'1':28800,
		'2':35400,
		'3':48600,
		'4':55200,
		'5':61500,
		'6':69600,
		}
		end_time ={
		'1':34500,
		'2':41100,
		'3':54300,
		'4':60900,
		'5':67200,
		'6':75300,
		}
		semester_start_day = self.semester['startDate']
		stamp = time.mktime(time.strptime(semester_start_day,"%Y-%m-%d"))
		for i in self.currentCourse:
			current_course_name = i['course_name']
			current_course_teacher_name = i['teacherInfo']['name']
			current_course_teacher_email = i['teacherInfo']['email']

			timeplace_list_url = 'http://learn.cic.tsinghua.edu.cn/b/course/info/timePlace/' + i['courseId']
			res = self.session.get(timeplace_list_url, cookies=self.cookies).json()
			for records in res['resultList']:
				course_place = records['skdd']
				if records['skjc'].encode("utf-8") == '0':
					logging.info('unfixed course time ' + current_course_name)
				else:
					
					repeat_gap = '1'
					if records['skzc'] =="前8周":
						repeat_times = '8'
						time_flag = stamp + (int(records['skxq']) - 1) * 86400.0
						#time_flag = time.strftime("%Y-%m-%d ", (stamp + (int(records['skxq']) - 1) * 86400.0 ))
					elif records['skzc'] =="后8周":
						repeat_times = '8'
						time_flag = stamp + (int(records['skxq']) - 1 + 56) * 86400.0
						#time_flag = "2017-11-"+str(12+int(records['skxq'])) +" "
					elif records['skzc'] =="全周":
						repeat_times = '16'
						#time_flag = "2017-9-"+str(17+int(records['skxq'])) +" "
						time_flag = stamp + (int(records['skxq']) - 1) * 86400.0
					elif records['skzc'] =="双周":
						repeat_times = '8'
						repeat_gap = '2'
						#time_flag = "2017-9-"+str(24+int(records['skxq'])) +" "
						time_flag = stamp + (int(records['skxq']) - 1 + 7) * 86400.0
					elif records['skzc'] =="单周":
						repeat_times = '8'
						repeat_gap = '2'
						#time_flag = "2017-9-"+str(17+int(records['skxq'])) +" "
						time_flag = stamp + (int(records['skxq']) - 1) * 86400.0
					else:
						logging.info(current_course_name + "未识别的上课类型：" + records['skzc'])
					#course_time_start = time_flag + start_time[records['skjc'].encode("utf-8")]
					#course_time_end = time_flag + end_time[records['skjc'].encode("utf-8")]
					course_time_start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_flag + start_time[records['skjc'].encode("utf-8")]))
					course_time_end = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_flag + end_time[records['skjc'].encode("utf-8")]))

					repeat_flag = [False, False, False, False, False, False]
					repeat_flag.insert(int(records['skxq'])-1,True)
					course_info_list = [current_course_name, course_place, \
					course_time_start, course_time_end, 0, 0, '课程' ,'' ,'' ,'' ,'' ,\
					'1', repeat_gap, [False, True, False], repeat_times, '', repeat_flag, \
					"教师姓名："+current_course_teacher_name + "\r教师邮箱：" + current_course_teacher_email\
					 + "\r课程类型：" + records['skzc'] ]
					class_list.append(course_info_list)
		return class_list



class WebLearningScraper(object):
	def __init__(self, username, password):
		self.old_login(username, password)
		self.new_login(username, password)
		self.semester = self.get_current_semester()
		self.currentCourse = self.get_course_info()

	def old_login(self,username, password):
		self.session_old = requests.Session()
		self.old_url_login = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
		self.login_data_old = {'userid':username, 'userpass':password}
		r = self.session_old.post(self.old_url_login,self.login_data_old )
		#if(len(r.content)) > 120:
		#	logging.INFO("login failed")
		#else:
		#	logging.INFO("login success")
	def new_login(self,username, password):
		self.session_new = requests.Session()
		self.new_url_login = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
		self.login_data_new = {'i_user': username, 'i_pass': password}
		self.cookies = self.session_new.post(self.new_url_login, data=self.login_data_new, verify=False).cookies
	def get_current_semester(self):
		current_semester_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/getCurrentTeachingWeek'
		res = self.session_new.get(current_semester_url, cookies=self.cookies).json()
		logging.info("current semester is " + res['currentSemester']['semesterName'])
		return (res['currentSemester']['id'])

	def get_course_info(self):
		course_list_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester
		res = self.session_new.get(course_list_url, cookies=self.cookies).json()
		return (res['resultList'])

	def get_course_info_dict(self):
		course_list_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester
		res = self.session_new.get(course_list_url, cookies=self.cookies).json()
		info_dict = {}
		for item in res['resultList']:
			info_dict[item['courseId']] = item
		return (info_dict)

	def make_soup(self,url):
		r = self.session_old.get(url)
		r.encoding = 'bgk'
		soup = BeautifulSoup(r.content, "html.parser")
		return soup
	def courses(self):
		soup = self.make_soup('http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?typepage=1')
		homework_list = []
		new_web_learning_list = []
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
				soup = self.make_soup(url)
				for i in soup.find_all('tr', class_=['tr1', 'tr2']):
					tds = i.find_all('td')
					if (( '已经提交' in tds[3].contents[0]) == 1):
						continue
					else:
						detail_url = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/' + i.find('a')['href']
						id = re.search(r'(\d+)', url).group(0)
						title = i.find('a').contents[0]
						logging.info('course homework for course ' + name + ':' + title)
						start_time = tds[1].contents[0] + " 0:00:00"
						end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.strptime(tds[2].contents[0],"%Y-%m-%d")) + 86399))
						#submitted = ( '已经提交' in tds[3].contents[0])
						soup = self.make_soup(detail_url)
						try:
							details = soup.find_all('td', class_='tr_2')[1].textarea.contents[0]
						except:
							details = ""
						homework_list.append(["[" + name +"]" + title, None, start_time, end_time, \
							'0', '0','-1', '作业,,,,,', '-1', '-1', '[False, False, False]', '-1', '1000-0-0',\
							 '[False, False, False, False, False, False, False]', '0,1', ',' ,details])
			else:
				continue
		for i in self.currentCourse:
			logging.info('course homework for course ' + i['course_name'] + ':')
			homework_course_name = i['course_name']
			new_homework_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/homework/list4Student/' + i['courseId'] +'/0'
			res = self.session_new.get(new_homework_url, cookies=self.cookies).json()
			for records in res['resultList']:
				#0，尚未提交；1，已经提交；3，已经批改
				if (records['courseHomeworkRecord']['status'] =='0'):
					homework_title = records['courseHomeworkInfo']['title']
					homework_detail = records['courseHomeworkInfo']['detail']
					homework_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(records['courseHomeworkInfo']['beginDate']/1000))
					homework_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(records['courseHomeworkInfo']['endDate']/1000))

					homework_list.append(["[" + homework_course_name +"]" + homework_title, None, homework_start_time, homework_end_time, \
						'0', '0','-1', '作业,,,,,', '-1', '-1', '[False, False, False]', '-1', '1000-0-0',\
						 '[False, False, False, False, False, False, False]', '0,1', ',' ,homework_detail])
		return homework_list
	
if __name__ == '__main__':
	username=''
	password=''  # TODO:change username and password
	if username is None or password is None:
        	username = input("TsinghuaId:")
        	password = getpass.getpass("Password:")
	print(json.dumps(WebLearningScraper(username, password).courses(),ensure_ascii=False,indent = 4))
	print(json.dumps(GetTimetable(username, password).get_course_time(),ensure_ascii=False,indent = 4))


