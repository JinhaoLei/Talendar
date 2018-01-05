import requests
def main(s):
    url = "http://115.182.62.173:8080/"

    payload = " <xml>\r\n <ToUserName><![CDATA[toUser]]></ToUserName>\r\n <FromUserName><![CDATA[fromUser]]></FromUserName>\r\n <CreateTime>12345678</CreateTime>\r\n <MsgType><![CDATA[text]]></MsgType>\r\n <Content><![CDATA[%s]]></Content>\r\n </xml>"%(s)
    headers = {
    'cache-control': "no-cache",
    'postman-token': "5b136b88-9a9b-473d-32f5-8ff3b53f4ba1"
    }

    response = requests.request("POST", url, data=payload, timeout=3.0)
