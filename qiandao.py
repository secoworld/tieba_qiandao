#!/usr/bin/python3

#所需要的库
import urllib.parse
import urllib.request
import json
import re
import random
import time

#需要的header和cookie
header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
#从浏览器中获取的Cookie
header['Cookie'] = "BAIDUID=86621B730BE1B8DDB30BC86D1A85A323:FG=1; BIDUPSID=86621B730BE1B8DDB30BC86D1A85A323; PSTM=1510202295; TIEBA_USERTYPE=a0f753280142945b5a4bbacc; TIEBAUID=75e4e6f45b39ef6e8f3a84d2; bdshare_firstime=1510218040536; FP_UID=e08af8562ccadff9846439e077c09364; BDUSS=pnbWtQUUszaXhDOUJxZGpGMXRUWW5iflBXVzFuUVZpTFZkNnRINTdVcDItaXRhSVFBQUFBJCQAAAAAAAAAAAEAAAAhwRBbztJnb29nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHZtBFp2bQRaZV; STOKEN=4e4b7446008e3da9c8d89852d35118e62498b8b6ceea3d08d9b478d905c00498; rpln_guide=1; pgv_pvi=3431114752; pgv_si=s4384706560; BDRCVFR[korV8YiOINC]=9xWipS8B-FspA7EnHc1QhPEUf; PSINO=1; H_PS_PSSID=; FP_LASTTIME=1510376661933; fixed_bar=1; wise_device=0; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1510282024,1510282950,1510376659,1510376874; Hm_lpvt_287705c8d9e2073d13275b18dbd746dc=1510376874"

tebs =['cd5e9cf18f4d11f91510816114','ce3fd8665a87554b1510379837','f1323634f7a7e0e91510816573']

def tieba_login(name,passwd):
    pass

#获得贴吧的列表
def tieba_getlist():
    ''' 获取百度贴吧所关注的贴吧列表'''

    url = 'http://tieba.baidu.com/f/like/mylike?pn='    #获取贴吧列表的网址
    page = 1    #列表的页数
    result =[]

    while(1):
        url2 = url + str(page)
        response = urllib.request.Request(url = url2,headers = header )
        html = urllib.request.urlopen(response).read().decode('gbk','ignore')

        #正则表达式获取贴吧的名称
        re1 = re.compile(r' title="([^<>/]*)">([^<>/]*)</a></td><td><a class="cur_exp" target="_blank"')
        name = re.findall(re1,html)
        for i in name:
            result.append(i[0])     #将贴吧的名称进行保存

        if html.find('下一页') == -1:      #判断列表是否为最后一页
            break
        else:
            page += 1

    print(result)
    return result

def tieba_onekey():
    url = 'https://tieba.baidu.com/tbmall/onekeySignin1'
    data = {
        'ie': 'utf - 8',
    }
    data['tbs'] = tebs[random.randint(0,len(tebs))]

    data = urllib.parse.urlencode(data).encode('utf-8')

    request = urllib.request.Request(url,data=data,headers=header)
    request = urllib.request.urlopen(request)

    html = request.read().decode('utf-8')
    jsons = json.loads(html)

    print('贴吧一键签到： %s'%jsons['error'])



def tieba_nevcod():
    data = {
        'captcha_vcode_str': 'captchaservice336331326a332f4368574c4564595966464b6d51415756465a79362f4e5169527035624e665643397037726735564268376931726c4331664c432b69644c365254614d59764e72306672465479777161565274316e526665786d4c592b4d5469393974312f39574e615a3771756d75496673786b574d336f6a61446e5157794c775842413232496553324369576f416d4c6e5a36526e44616e6666516f33327153364c54304f7132334b715643596d32684b4278346e6a5a626e3938595744706a567953444c614b353072675a503865494a76426c525444786e6435627459546f436266634243483552472f796b385945395473613377316446576f30307a6c6f496768413148596175436c4455544666394669337174594f664e41712b394c504832736937614c3236776d6d376f6f363738',
        'captcha_code_type': '4',
        'captcha_input_str': '00010002000200000000000200010001',
        'fid':''
    }

    url = 'http://tieba.baidu.com/sign/checkVcode'
    request = urllib.request.Request(url, data=data, headers=header)
    request = urllib.request.urlopen(request)

    html = request.read().decode('utf-8')
    jsons = json.loads(html)



def tieba_qiandao(name):
    ''' 贴吧签到 '''

    urls = 'http://tieba.baidu.com/sign/add'
    data = {
        'ie': 'utf - 8',
        'tbs': 'ce3fd8665a87554b1510379837'
    }
    data['kw'] = name

    data = urllib.parse.urlencode(data).encode('utf-8')

    response = urllib.request.Request(url = urls,data = data,headers = header)
    html = urllib.request.urlopen(response).read().decode('utf-8')

    #获取返回的信息
    jsons = json.loads(html)
    #信息解析：
    return jsons



if __name__ == '__main__':

    try:
        result = tieba_getlist()
        succ = 0
        err = 0
        tieba_onekey()
        time.sleep(5)

        while err == 0:
            for name in result:
                #print(i)
                jsons =tieba_qiandao(name)
                if jsons['error'] != '':
                    print('%-10s : 签到失败      原因：%s' % (name, jsons['error']))
                    err += 1
                else:
                    print('%-10s : 签到成功' % name)
                    succ += 1
                time.sleep(0.5)      #为防止贴吧验证码，所以每签到一个贴吧，休息一段时间,
                                    # 签到20个就需要验证
    except  e:
        print('退出贴吧签到!')
        print(e)
    finally:
        with open('tieba.txt','a') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
            f.write('       成功签到的贴吧数为： ' + str(succ))
            f.write('       签到失败的贴吧数为： ' + str(err))
            f.write('\r\n')
            f.close()
        print('成功签到的贴吧数为：%d'%succ)
        print('签到失败的贴吧数为：%d'%err)