#coding: utf-8    
  
import smtplib    
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText    
from email.mime.image import MIMEImage 
from email.header import Header   
import datetime
import json
import time
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf8')
#设置smtplib所需的参数
#下面的发件人，收件人是用于邮件传输的。
smtpserver = 'smtp.163.com'
username = 'Talendar@163.com'
password='talendar123'
sender='Talendar@163.com'
#receiver='XXX@126.com'
#收件人为多个收件人
def send(info):
    title, loc, reminderNumber, reminderUnit, time, tags, ddlflag, em, note= info

    receiver=[em]
    print receiver
    if reminderUnit == '0':
        reminder = "分钟"
    elif reminderUnit == '1':
        reminder = "小时"
    elif reminderUnit == '2':
        reminder = "天"
    if ddlflag == '1':
           
        subject = "【Talendar】距离" + title + "到期还有" + reminderNumber + reminder +  "！" 
        timesen = "截止时间："
    else:
        subject = "【Talendar】距离" + title + "开始还有" + reminderNumber + reminder +  "！"
        timesen = "开始时间："
    subject=Header(subject, 'utf-8').encode()
    tags = tags.split(',')[:-1]
    t = ''
    for i in tags:
        if i != '':
            t += i + '\t'
    time = time.split(' ')[0].split('-')[0] + "年" + time.split(' ')[0].split('-')[1] + "月" + time.split(' ')[0].split('-')[2] + "日 " + time.split(' ')[1]  + "点" +  time.split(' ')[2] + "分"
    text = "事件名称：" + title + "\n" + "地点：" + loc +  "\n" + timesen + time + "\n" + "备注：" + note +  "\n" + "标签：" + t + "\n\n" + "Talendar小组敬上"
    #print title, loc, note, tags
    #text = u'事件名称：' + title + "\n" + u'地点：' + loc + + "\n" + u'备注：' + note +  "\n" + u'标签：' + tags
    msg = MIMEText(text,'plain', 'utf-8')  
    msg['Subject'] = subject
    msg['From'] = 'Talendar<Talendar@163.com>'
    #msg['To'] = 'XXX@126.com'
    #收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receiver) 
    #msg['Date']='2012-3-16' '''  
  




    #发送邮件
    smtp = smtplib.SMTP()    
    smtp.connect('smtp.163.com')
    #我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    #smtp.set_debuglevel(1)  
    smtp.login(username, password)    
    smtp.sendmail(sender, receiver, msg.as_string())    
    smtp.quit()
def main():
    while(1):
        try:
            f = open('remind.json')
        except:
            sleep(10)
            continue
        info = []
        for n, line in enumerate(f):
            info.append(json.loads(line))
        f.close()
        f = info
        for i in range(len(info)):
            title = f[i]['title']
            loc = f[i]['loc']
            reminderUnit = f[i]['reminderUnit']
            reminderNumber = f[i]['reminderNumber']
            startTime = f[i]['startTime']
            endTime = f[i]['endTime']
            tags = f[i]['tags']
            ddlFlag = f[i]['ddlFlag']
            note = f[i]['note']
            em = f[i]['email']
            #print ddlFlag
            if ddlFlag == '1':
                endTime = endTime
            else:
                endTime = startTime
            if reminderUnit == '0':
                reminder = int(reminderNumber)
            elif reminderUnit == '1':
                reminder = 60 * int(reminderNumber)
            elif reminderUnit == '2':
                reminder = 1440 * int(reminderNumber)            

            endtime = datetime.datetime(int(endTime.split()[0].split('-')[0]), int(endTime.split()[0].split('-')[1]), int(endTime.split()[0].split('-')[2]), int(endTime.split()[1]), int(endTime.split()[2]))
            now = datetime.datetime.now()
            print int((endtime - now).total_seconds())
            if int((endtime - now).total_seconds()) / 60 ==  reminder:
                #print [title, loc, reminderNumber, reminderUnit, endTime, tags, ddlFlag, em, note]
                #print 'bingo!'
                threads = []
                s = [title, loc, reminderNumber, reminderUnit, endTime, tags, ddlFlag, em, note]
                t = threading.Thread(target = send,args=(s,))
                #threads.append(t)
                t.setDaemon(True)
                t.start()
                t.join()
                #send([title, loc, reminderNumber, reminderUnit, endTime, tags, ddlFlag, em, note])
                print 'finish'
                #return
                #send([title, loc, reminderNumber, reminderUnit, endTime, tags, ddlFlag, em, note])
        
        time.sleep(60)
main()
