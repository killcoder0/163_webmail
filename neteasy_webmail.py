# -*- coding: utf-8 -*-

import base
import session.session as session
import mail_addr_provider
import content_provider
import random

class NeteasyMailbox(object):
    def __init__(self):
#        self.__browser = session.AsyncSession()
        self.__browser = session.Session()
        self.__username = ""
        self.__password = ""

    def on_login(self,response):
        print response.body

    def login(self,username,password):
        self.__username = username
        self.__password = password
        action = "https://ssl.mail.163.com/entry/coremail/fcg/ntesdoor2?df=mail163_letter&from=web&funcid=loginone&iframe=1&language=-1&net=c&passtype=1&product=mail163&race=59_19_11_bj&style=-1&uid=%s" % username
        data = {
                   "savelogin":"0",
                   "username":username,
                   "password":password
                }
        add_header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36",
                      }
        response = self.__browser.send_form(action,"POST",data,add_header)
        new_url = ""
        if response:
            html = response.body
            seg = 'top.location.href = "'
            pos = html.find(seg)
            if pos != -1:
                start = pos + len(seg)
                pos = html.find('"',start)
                if pos != -1:
                    new_url = html[start:pos]
        new_resp = self.__browser.fetch(new_url,"GET",add_header,None)
        pos = new_url.rfind("=")
        sid = new_url[pos+1:]
        mail_data = {"var":'''<?xml version="1.0"?><object><string name="id">c:1393217890609</string><object name="attrs"><string name="account">"meiboyking7"&lt;meiboyking7@163.com&gt;</string><boolean name="showOneRcpt">false</boolean><array name="to"><string>"151916524@qq.com"&lt;151916524@qq.com&gt;</string></array><array name="cc"/><array name="bcc"/><string name="subject">I'm here as always</string><boolean name="isHtml">true</boolean><string name="content">&lt;div style='line-height:1.7;color:#000000;font-size:14px;font-family:arial'&gt;jiaren&amp;nbsp;&lt;/div&gt;</string><int name="priority">3</int><boolean name="requestReadReceipt">false</boolean><boolean name="saveSentCopy">true</boolean><string name="charset">GBK</string></object><boolean name="returnInfo">false</boolean><string name="action">deliver</string></object>'''}
        action = "http://cwebmail.mail.163.com/js5/s?sid=%s&func=mbox:compose&from=nav&action=goCompose&cl_send=1&l=compose&action=deliver"%sid
        resp_mail = self.__browser.send_form(action,"POST",mail_data,add_header)
        #handler = open("awp.html","w")
        #handler.write(new_resp.body)
        #handler.close()
        self.__browser.report()

if __name__ == "__main__":
    box = NeteasyMailbox()
    box.login("game_works_003@163.com","abc123")
    raw_input("press")