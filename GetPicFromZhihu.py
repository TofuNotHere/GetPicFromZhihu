#知乎扒图用脚本
#
from os.path import basename
import urllib
import re
import requests
import os
import json




Qcode = input('输入要扒图的问题号\n')
url = 'https://www.zhihu.com/question/' + Qcode

if not os.path.exists(Qcode):
    os.mkdir(Qcode)

offset = 0
answers_l = urllib.request.urlopen(url).read().decode('utf-8')
answers = re.findall('h3 data-num="(.*?)"', answers_l)
limits = int(answers[0])
page_size = 20
print('此问题下共有%d个答案，分为%d部分' % (limits, (limits+1)/20 +1),end='')

while offset < limits:
    post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
    params = json.dumps({
        'url_token': Qcode,
        'pagesize': page_size,
        'offset': offset
    })
    data = {
        '_xsrf': '',
        'method': 'next',
        'params': params
    }
    header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
        'Host': "www.zhihu.com",
        'Referer': url
    }
    response = requests.post(post_url, data=data, headers=header)
    answer_list = response.json()["msg"]
    img_urls = re.findall('img .*?src="(.*?_b.*?)"', ''.join(answer_list))
    i = 0
    print('\n第%d部分,共有%d张图片' % ((offset+1)/20 + 1,int(len(img_urls)/2)))
    for img_url in img_urls:
        if img_url[0] == '/':
            continue
        try:
            i += 1
            img_data = urllib.request.urlopen(img_url).read()
            file_name = basename(urllib.parse.urlsplit(img_url)[2])
            output = open(Qcode + '/' + file_name, 'wb')
            output.write(img_data)
            output.close()
            
            print("\r已下载%d张图片" % i,end='')
        except:
            pass
    print('\r已下载完成    ')
    offset += page_size
