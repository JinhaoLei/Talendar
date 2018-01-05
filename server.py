#-*- coding: utf-8 -*-
from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import time
import json
import hashlib
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def wechat():
    if request.method=='GET':
        token=''
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
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>" % (fromu, tou, time, 'hello')
        return make_response(xml_rep)

app.run(host='', port=8080)   #IMPORTANT: to test server and client, please contact with Talendar group.

