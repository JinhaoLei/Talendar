# -*- coding:utf-8 -*-
import sys
from collections import OrderedDict
from pyexcel_xls import get_data
from pyexcel_xls import save_data
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def get_class(file_path):
	tin = 0
	jin = 0
	class_list =[]
	xls_data = get_data(unicode(file_path, 'utf-8'))

	for sheet_n in xls_data.keys():
	    for column in xls_data[sheet_n]:
	    	tin = tin+1
	    	jin = 0
	    	for line in column:
	    		jin +=1
	        	if line != "":
	        		if tin > 2 and tin < 9:
	        			#每一个课程栏目
	        			m = str(line)
	        			#排除其他单元格
	        			if re.findall('第.*节',m)==[]:
	        				#可能单个单元格有多个课程
	        				if m.find(u'\r\n')== -1:
	        					#单个单元格有1个课程
		        				s = [x for x in re.split(u'\(|；|\)',line) if x ]
			        			class_list.append(savetxt(s, jin-1, tin-2))
		        			else:
		        				#单个单元格有多个课程
		        				sub_class = [x for x in re.split(u'\r\n',line) if x ]
		        				for subitem in sub_class :
		        					s = [x for x in re.split(u'\(|；|\)',subitem) if x ]
		        					class_list.append(savetxt(s, jin-1, tin-2))
		        					"""
	        						print "**********************************************************"
				        			
				        			print ("课程名："+s[0])
				        			print ("教师姓名："+s[1])
				        			print ("课程类型："+s[2])
				        			print ("时间："+s[3])
				        			print ("上课地点："+s[4])
				        			print ("上课时间：周"+str(jin-1)+"第"+str(tin-2)+"节")
				        			print m
				        			print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				        			"""
	return class_list

def savetxt(s, j, t):
	if s[3] =="前八周":
		repeat_times = '8'
		time_flag = "2017-9-"+str(17+j)
	elif s[3] =="后八周":
		repeat_times = '8'
		time_flag = "2017-11-"+str(12+j)
	elif s[3] =="全周":
		repeat_times = '16'
		time_flag = "2017-9-"+str(17+j)
	else:
		return -1


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
	repeat_flag = [False, False, False, False, False, False]
	repeat_flag.insert(j-1,True)
	lists = [str(s[0]), str(s[4]), time_flag+' '+start_time[str(t)], time_flag+' '+end_time[str(t)],
		 '0', '0', "课程,,,,,", '1', '1', [False, True, False], 
		 repeat_times, "", repeat_flag, "教师姓名："+str(s[1])+"\r课程类型："+str(s[2])]
	return lists

if __name__ == '__main__':
    #提供一个文件
	filepath = r"./null.xls"
	#读取文件中的课程信息，返回标准列表
	classlist = get_class(filepath)
	#demo中的存成文件
	file_object = open('classfile.txt', 'w')
	file_object.write(str(classlist).decode("utf-8"))
	file_object.close()
	        			