ad_div = u'''
        <div>
			<img src="http://www.anzhi.com/icon.php?u=dGh1bWJ8MjAxMjA3fDI0fG9kQnFBVFo0RlZHWnN0MXpVZ2dzeldUN3Y0RElNN3BUN1E2dzllenRvaDU4aEJnclZ0ND0="></img>
			<img src="http://www.anzhi.com/icon.php?u=dGh1bWJ8MjAxMjA3fDI0fG9kQnFBVFo0RlZHWnN0MXpVZ2dzeldUN3Y0RElNN3BTNlFpMitlVHRvaDU5aEJnclZ0ND0="></img>
		</div>
		<div>
			<p>下载地址:<p>
			<a href="http://nighteyes.sinaapp.com/wheel/takeoff_download" target="_blank">
				http://nighteyes.sinaapp.com/wheel/takeoff_download
			</a>
			<p>官方网站(知名安卓市场):<p>
			<a href="http://nighteyes.sinaapp.com/wheel/takeoff" target="_blank">
				http://nighteyes.sinaapp.com/wheel/takeoff
			</a>
		</div>
		<div>
			<p>二维码下载:</p>
			<img src="http://nf.anzhi.com/QRcode.php?url=http%3A%2F%2Fwww.anzhi.com%2Fdl_app.php%3Fs%3D1307285&time=1389628800&key=11ebf7fe8ec0adf5f9f22a1ac0a77492">
		</div>
		<div>
			<p>玩儿法：</p>
			<p>
				画面上会有一个不断旋转的轮盘,用户点击屏幕便会暂停在指定选项上,游戏里的美女便会根据轮盘选项做出服饰变更.有难度,有耐心才会有惊喜哦
			</p>
		</div>
    '''

mix_up_text = u'''
'''

body_div_list = [ad_div]


def initialize():
    global body_div_list
    global mix_up_text
    global ad_div
    count = len(mix_up_text)
    div_count = 15
    seg_size = count/div_count
    seg_list = [ad_div]
    for i in range(0,div_count):
        start = seg_size*i
        if i == div_count-1:
            this_div = mix_up_text[start:]
        else:
            end = seg_size*(i+1)
            this_div = mix_up_text[start:end]
        this_div = u'<div style="display:none">%s</div>' % this_div
        body_div_list.append(this_div)


if __name__ == "__main__":
    initialize()
    for item in body_div_list:
        print item
    raw_input("press")