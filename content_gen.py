import random
import constant
import copy

def random_list_seq(item_list_arg):
    item_list = copy.copy(item_list_arg)
    result = []
    while True:
        count = len(item_list)
        if count < 1:
            break
        index = random.randint(0,count-1)
        result.append(item_list[index])
        del item_list[index]
    return result

def random_fetch(item_list):
    index = random.randint(0,len(item_list)-1)
    return item_list[index]

def post_process(sentence):
    new_sentence = ""
    count = 0
    for charactor in sentence:
        new_sentence += charactor
        if count <2 and random.randint(1,2) == 1:
            new_sentence += " "
            count += 1
    return new_sentence.strip()


def create_subject():
    human = (u"美女",u"女神",u"女生",u"小女",u"萝莉",u"萌妹",u"妹子",u"萌妹子",u"宅女",u"御姐",u"小清新",
                     u"私房美女",u"校花",u"校服女生",u"淑女",u"少女",u"美少女",u"卡通美女",u"卡通美少女",u"白富美")
    predicat = (u"换衣",u"转轮盘",u"更衣",u"脱衣",u"换衣服",u"装扮",u"梳妆",u"穿衣",)
    noun = (u"游戏",u"小游戏",u"手机游戏",u"手机小游戏",u"刺激小游戏",u"单机游戏",u"单机手机游戏",u"单机移动游戏",u"安卓游戏",
            u"安卓手机游戏",u"安卓小游戏",)
    addition = (u"",)
    subject = ""
    total = 1
    for item_list in (human,predicat,noun,addition):
        subject += random_fetch(item_list)
        total = total*len(item_list)
    #print "total: ",total
    #return post_process(subject)
    return subject

def create_body(subject):
    body_start = u'''
    <html>
	<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
	<head>
		<title>%s</title>
	</head>
	<body>
		<div style="text-align:center;">
			<b>%s</b>
		</div>
		<div>
			<p>%s</p>
		</div>
    ''' % (subject,subject,subject)
    body_end =u'''
                </body>
                <jj<>
                <))）
            </html>
        '''
    content_list = random_list_seq(constant.body_div_list)
    html = body_start
    for item in content_list:
        html += item
    html += body_end
    return html

if __name__ == "__main__":
    #for i in range(0,100):
    #    print i+1,":",create_subject()

    #item_list = [1,2,3,4,5]
    #for i in range(30):
    #    print random_list_seq(item_list)
    constant.initialize()
    for i in range(10):
        html = create_body(u"美女啊美女")
        fp = open("%d.html"%i,"w")
        fp.write(html.encode("utf8"))
        fp.close()
    raw_input("press")

