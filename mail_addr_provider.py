import urllib2
import json

def get_addr_provider(count):
    mail_list = []
    url = "http://127.0.0.1:8889/get_qq_list?count=%d" % count
    resp = urllib2.urlopen(url).read()
    qq_list = json.loads(resp)
    return ["%s@qq.com"%qq for qq in qq_list]