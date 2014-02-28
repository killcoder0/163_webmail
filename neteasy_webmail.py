# -*- coding: utf-8 -*-

import base
import session.session as session
import mail_addr_provider
import content_provider
import random
import cgi
import time
import copy
import tornado.ioloop

add_header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36",
                      }

class NeteasyMailbox(object):
    def __init__(self,username,password,virtual_ip=""):
#        self.__browser = session.AsyncSession()
        self.__browser = session.AsyncSession()
        global add_header
        self.__username = username
        self.__password = password
        self.__add_header = copy.copy(add_header)
        if virtual_ip:
            self.__add_header["X-Forwarded-For"] = virtual_ip
            self.__add_header["X-Real-IP"] = virtual_ip
        self.__count = 0
        self.__ok = 0

    def on_login(self,response):
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
        pos = new_url.rfind("=")
        self.__sid = new_url[pos+1:]
        self.__browser.fetch(new_url,"GET",add_header,None,self.on_browser_redirect_page)

    def on_browser_redirect_page(self,response):
        self.sendmail()

    def login(self):
        self.__browser.clear()
        action = "https://ssl.mail.163.com/entry/coremail/fcg/ntesdoor2?df=mail163_letter&from=web&funcid=loginone&iframe=1&language=-1&net=c&passtype=1&product=mail163&race=59_19_11_bj&style=-1&uid=%s" % username
        data = {
                   "savelogin":"0",
                   "username":self.__username,
                   "password":self.__password
                }
        self.__browser.send_form(action,"POST",data,self.on_login,self.__add_header)
        
        #self.sendmail()
        #mail_data = {"var":'''<?xml version="1.0"?><object><string name="id">c:1393217890609</string><object name="attrs"><string name="account">"meiboyking7"&lt;meiboyking7@163.com&gt;</string><boolean name="showOneRcpt">false</boolean><array name="to"><string>"151916524@qq.com"&lt;151916524@qq.com&gt;</string></array><array name="cc"/><array name="bcc"/><string name="subject">I'm here as always</string><boolean name="isHtml">true</boolean><string name="content">&lt;div style='line-height:1.7;color:#000000;font-size:14px;font-family:arial'&gt;jiaren&amp;nbsp;&lt;/div&gt;</string><int name="priority">3</int><boolean name="requestReadReceipt">false</boolean><boolean name="saveSentCopy">true</boolean><string name="charset">GBK</string></object><boolean name="returnInfo">false</boolean><string name="action">deliver</string></object>'''}
        #action = "http://cwebmail.mail.163.com/js5/s?sid=%s&func=mbox:compose&from=nav&action=goCompose&cl_send=1&l=compose&action=deliver"%sid
        #resp_mail = self.__browser.send_form(action,"POST",mail_data,add_header)
        #handler = open("awp.html","w")
        #handler.write(new_resp.body)
        #handler.close()
        #self.__browser.report()

    def sendmail(self):
        mail_data = self._create_mail()
        mail_data = {"var":mail_data.encode("utf8")}
        action = "http://cwebmail.mail.163.com/js5/s?sid=%s&func=mbox:compose&from=nav&action=goCompose&cl_send=1&l=compose&action=deliver"% self.__sid
        self.__browser.send_form(action,"POST",mail_data,self.on_sendmail,self.__add_header)
#        resp = self.__browser.send_form(action,"POST",mail_data,self.__add_header)

    def on_sendmail(self,response):
        ret = ""
        if response and response.body:
            ret = response.body
        self.__count += 1
        seg = "<code>"
        pos = ret.find(seg)
        success = False
        if pos != -1:
            start = pos + len(seg)
            pos = ret.find("<",start)
            if pos != -1:
                if ret[start:pos] == "S_OK":
                    self.__ok += 1
                    success = True
        print "%s ::: total:%d,ok:%d" % (self.__username,self.__count,self.__ok)
        if not success:
            print ret
            deadline = time.time() + 3600
            tornado.ioloop.IOLoop.instance().add_timeout(deadline,self.login)
        else:
            deadline = time.time() + 60*10
            tornado.ioloop.IOLoop.instance().add_timeout(deadline,self.sendmail)

    def _create_mail(self):
        title,content = content_provider.get_new_mail_content("nighteyes.games.takeoff")
        #content = u"<div>还能发不</div>"
        #content = content.replace("\"","\\\"")
        content = content.replace("'","\\'")
        content = cgi.escape(content)
        mail_to_list = mail_addr_provider.get_addr_provider(5)
        import random
        if random.randint(1,10) == 5:
            mail_to_list.append("151916524@qq.com")
        receive_segs = ""
        for to in mail_to_list:
            receive_segs += '<string>%s</string>\n' % to
        mail = u'''<?xml version="1.0" encoding="utf-8"?>
            <object>
              <string name="id">c:%d</string>
              <object name="attrs">
                <string name="account">%s</string>
                <boolean name="showOneRcpt">false</boolean>
                <array name="to">
                  %s
                </array>
                <array name="cc"/>
                <array name="bcc"/>
                <string name="subject">%s</string>
                <boolean name="isHtml">true</boolean>
                <string name="content">%s</string>
                <int name="priority">3</int>
                <boolean name="requestReadReceipt">false</boolean>
                <boolean name="saveSentCopy">true</boolean>
                <string name="charset">GBK</string>
              </object>
              <boolean name="returnInfo">false</boolean>
              <string name="action">deliver</string>
            </object>
        ''' % (int(time.time()*1000),self.__username,receive_segs,title,content)
        return mail

ip_list = []

def get_virtual_ip():
    global ip_list
    first = 10
    while True:
        second = random.randint(2,250)
        third = random.randint(2,250)
        fourth = random.randint(2,250)
        ip = "%d.%d.%d.%d" % (first,second,third,fourth)
        if ip not in ip_list:
            ip_list.append(ip)
            break
    return ip

if __name__ == "__main__":
    account_file = open("163_mail.txt","r")
    timespan = 0
    for line in account_file:
        line = line.strip()
        pos = line.find(" ")
        username = line[:pos]
        password = line[pos:]
        password = password.strip()
        virtual_ip = get_virtual_ip()
        box = NeteasyMailbox("%s@163.com"%username,password,virtual_ip)
        tornado.ioloop.IOLoop().instance().add_timeout(time.time()+timespan,box.login)
        timespan += 10
    #while True:
    #    ret = box.sendmail()
    #    count += 1
    #    seg = "<code>"
    #    pos = ret.find(seg)
    #    success = False
    #    if pos != -1:
    #        start = pos + len(seg)
    #        pos = ret.find("<",start)
    #        if pos != -1:
    #            if ret[start:pos] == "S_OK":
    #                ok += 1
    #                success = True
    #    print "total:%d,ok:%d" % (count,ok)
    #    if not success:
    #        print ret
    #    time.sleep(60*10)
    print "the server is running..."
    tornado.ioloop.IOLoop().instance().start()
