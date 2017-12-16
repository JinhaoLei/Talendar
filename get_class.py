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
		self.url_login = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
		self.login_data = {'i_user': username, 'i_pass': password}
		self.cookies = self.session.post(self.url_login, data=self.login_data, verify=False).cookies
		self.semester = '2017-2018-1'
		self.currentCourse = self.get_course_info()

	def get_course_info(self):
		course_list_url = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/courseList/loadCourse4Student/' + self.semester
		res = self.session.get(course_list_url, cookies=self.cookies).json()
		#for item in res['resultList']:
		#	logging.info('get course id:' + item['courseId'])
		return (res['resultList'])
	
	def get_course_time(self):
		class_list = []
		start_time = {
		'1':'8:00',
		'2':'9:50',
		'3':'13:30',
		'4':'15:20',
		'5':'17:05',
		'6':'19:20',
		}
		end_time ={
		'1':'9:35', 
		'2':'11:25', 
		'3':'15:05', 
		'4':'16:55', 
		'5':'18:40', 
		'6':'20:55', 
		}
		
		for i in self.currentCourse:
			logging.info('course time for course id ' + i['course_name'] + ':')
			
			timeplace_list_url = 'http://learn.cic.tsinghua.edu.cn/b/course/info/timePlace/' + i['courseId']
			res = self.session.get(timeplace_list_url, cookies=self.cookies).json()
			
			current_course_name = i['course_name']
			current_course_teacher_name = i['teacherInfo']['name']
			current_course_teacher_email = i['teacherInfo']['email']

			if res['message'] == 'success':
				for records in res['resultList']:
					course_place = records['skdd']
					#current_course_day = records['skxq']
					if records['skjc'].encode("utf-8") == '0':
						logging.info('unfixed course time ' + current_course_name)
					else:
						
						course_start_time = start_time[records['skjc'].encode("utf-8")]
						course_end_time = end_time[records['skjc'].encode("utf-8")]

						#current_course_type = records['skzc']
						if records['skzc'] =="前8周":
							repeat_times = '8'
							time_flag = "2017-9-"+str(17+int(records['skxq'])) +" "
						elif records['skzc'] =="后8周":
							repeat_times = '8'
							time_flag = "2017-11-"+str(12+int(records['skxq'])) +" "
						elif records['skzc'] =="全周":
							repeat_times = '16'
							time_flag = "2017-9-"+str(17+int(records['skxq'])) +" "
						else:
							return -1
						course_time_start = time_flag + course_start_time
						course_time_end = time_flag + course_end_time
						repeat_flag = [False, False, False, False, False, False]
						repeat_flag.insert(int(records['skxq'])-1,True)
						course_info_list = [current_course_name, course_place, \
						course_time_start, course_time_end, 0, 0, '课程' ,'' ,'' ,'' ,'' ,\
						'1', '1', [False, True, False], repeat_times, '', repeat_flag, \
						"教师姓名："+current_course_teacher_name + "\r教师邮箱：" + current_course_teacher_email\
						 + "\r课程类型：" + records['skzc'] ]
						class_list.append(course_info_list)
		return class_list
	


if __name__ == '__main__':
	scraper = NewWebLearningScraper(username='', password='')  # TODO:change username and password
	print(json.dumps(scraper.get_course_time(),ensure_ascii=False,indent = 4))

