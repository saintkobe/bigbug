import requests
import re
import os
import time

headers = {
    'cookie':'__cfduid=d0bfaa5751f2a76d47ab01258ebb28e991599911782; __dtsu=10401599911769CD98BE75137ECF714A; CzG_cookietime=2592000; CzG_auth=6658Z9RzT4NiKV5g5%2FX6XGM4ciqxpkpexY4rFnpXhtrZ85tMrI8q6c5GIeRzZmMsbiY6gkDxDFfQ01UE%2FRWX28PCL1R5; smile=1D1; __utmc=93056010; __utmz=93056010.1599963389.2.2.utmcsr=91porn.com|utmccn=(referral)|utmcmd=referral|utmcct=/v.php; CzG_sid=PI6T6I; __utma=93056010.1656203198.1599911785.1599966057.1599980881.4; CzG_fid19=1599981563; CzG_fid4=1599979090; CzG_fid21=1599981959; CzG_visitedfid=4D21D19D33; CzG_oldtopics=D384284D389397D237928D193593D389286D389114D389119D389167D389184D389172D389190D389243D389249D389278D389362D389425D389400D389321D; __utmb=93056010.38.10.1599980881',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',}
url=input("请输入要下载的网址：\n")
#url="https://f1022.wonderfulday27.live/viewthread.php?tid=389172&extra=page%3D4"
res=requests.get(url,headers=headers).content.decode('utf-8')
img_url=re.findall(r'<img .*? file="(.*?)"',res)
title=re.findall(r'<h1>(.*?)</h1>',res)[0]
# print(img_url)
# print(title)
os.mkdir(title)
print('文件夹:{} 已创建'.format(title))
os.chdir(title)
a=0
for img in img_url:
    r=requests.get(img,headers=headers)
    # print(img.split('/')[-1])
    with open(img.split('/')[-1],'wb') as f:
        print('正在下载第{}张图片'.format(a))
        f.write(r.content)
        f.flush()
        time.sleep(1)
        a+=1

