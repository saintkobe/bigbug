#-*- coding = utf-8 -*-
#@Time:  17:43
#@Author : floyd
#@File :.py
#@Software :PyCharm
import requests
import json
from fake_useragent import UserAgent

ua=UserAgent()
def fanyi(word):
    data={
    'from':'en',
    'to':'zh',
    'query':word,
    'transtype':'translang',
    'simple_means_flag':'3',
    'sign':'704513.926512',
    'token':'2b03bb02439027e78bb0e65809fdd5c5',
    'domain':'common',
    'raw_trans':word
    }
    proxies={
        'HTTP' : '113.194.28.125:9999'
    }
    header={

    'user-agent':str(ua.random),
    'x-requested-with':'XMLHttpRequest'
    }
    url="https://fanyi.baidu.com/multitransapi"
    res=requests.post(url,data=data,headers=header,proxies=proxies).text
    res=json.loads(res)
    result=res['data']['cands'][0]
    return result

if __name__=="__main__":
    word=''
    while word != 'q':
        word = input ('请输入:')
        if word != 'q':
            print(fanyi(word))


