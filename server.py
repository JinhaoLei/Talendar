#-*- coding: utf-8 -*-
from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import time
import json
import hashlib
import random
#import threading
#import tensorflow as tf
#from ai2017 import start
#from ai2017 import feed
#import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def wechat():
    if request.method=='GET':
        token='qianqiao'
        data=request.args
        signature=data.get('signature','')
        timestamp=data.get('timestamp','')
        nonce=data.get('nonce','')
        echostr=data.get('echostr','')
        s=[timestamp,nonce,token]
        s.sort()
        s=''.join(s)
        if(hashlib.sha1(s).hexdigest()==signature):
            return make_response(echostr)
    else:
        rec=request.stream.read()
        xml_rec=ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        
        #content = xml_rec.find('Content').text.encode('utf-8', 'ignore')
        content = xml_rec.find('Content').text
        infos = content.split('$$')[:-1]
        f = open('remind.json', 'w')
        for i in range(len(infos)):
            title, loc, startTime, endTime, tags, reminderUnit, reminderNumber, ddlFlag, email, note = infos[i].split('\t')
            data = {'title':title, 'loc':loc, 'startTime':startTime, 'endTime':endTime, 'tags':tags, 'reminderUnit':reminderUnit, 'reminderNumber':reminderNumber, 'ddlFlag':ddlFlag, 'email':email, 'note':note}
            json.dump(data, f)
            f.write('\n')
        f.close()
        time = xml_rec.find('CreateTime').text
        #msgid = xml_rec.find('MsgId').text
        #content = feed(sess,content,1)
        #response = random.sample(content,1)
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>" % (fromu, tou, time, 'hello')
        return make_response(xml_rep)

#sess=start()
app.run(host='115.182.62.173', port=8080)
#print('jj')
