# -*- coding = utf-8 -*-
# @Time:  14:35
# @Author : floyd
# @File :.py
# @Software :PyCharm
import requests
import json
import random
import time
from hashlib import md5
import execjs
import tkinter as tk

'''
        *JS解密两种方式
            1.明白了加密的方式,然后将JS代码读懂,然后用PYTHON重写一遍(反写)
            2.明白了加密的方式,然后用python库直接执行JS代码,获取结果
                用pyexec js 模块来执行(需要JS源码)
                    抠JS源码,抠出来才能用pxexec js
'''
def get_js_function(js_path,func_name,func_args):
    '''
    获取指定目录下的js代码,并且指定js代码中函数的名字以及函数的参数.
    :param js_path: js代码的位置
    :param func_name: js代码中函数的名字
    :param func_args: js代码中函数的参数
    :return: 返回调用js函数的结果
    '''
    with open(js_path,encoding='utf-8') as f:
        js_code=f.read()
        ctx=execjs.compile(js_code)
        return ctx.call(func_name,func_args)

'''方法二,重写函数'''

# appVersion='5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
# def r(e):
#     #bv 浏览器版本的加密数据
#     t=md5(appVersion.encode()).hexdigest()
#     #时间戳数据
#     r=str(int(time.time() *1000))
#     i=r+str(random.randint(0,9))
#     return {
#         'ts':r,
#         'bv':t,
#         'salt':i,
#         'sign':md5(("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m").encode()).hexdigest()
#     }
#

#画板
root=tk.Tk()
root.title('神马翻译')
root.geometry('500x400+600+300')
l1=tk.Label(root,text='输入:',font=('隶书',15))
l1.grid(row=1,column=0)
t1=tk.Entry(root,text='',width=50)
t1.grid(row=1,column=1)

def youdao(word):
    t2.delete(1.0,tk.END)
    result=get_js_function('youdao.js','youdao',word)
    head = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'243',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'OUTFOX_SEARCH_USER_ID=2010984610@10.169.0.83; JSESSIONID=abcsxub1sFLzs4jj2Qsrx; _ntes_nnid=e9a0ca69bd2ce15f3beaee8d61fce5c0,1599114798307; OUTFOX_SEARCH_USER_ID_NCOO=1351221983.191675; ___rl__test__cookies=1599115149841',
        'Host':'fanyi.youdao.com',
        'Origin':'http://fanyi.youdao.com',
        'Referer':'http://fanyi.youdao.com/?keyfrom=dict2.top',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }

    words={
    'i':word,
    'from':'AUTO',
    'to':'AUTO',
    'smartresult':'dict',
    'client':'fanyideskweb',
    'salt':result['salt'],
    'sign':result['sign'],
    'lts':result['ts'],          #时间戳
    'bv':result['bv'],
    'doctype':'json',
    'version':'2.1',
    'keyfrom':'fanyi.web',
    'action':'FY_BY_CLICKBUTTION'
    }

    url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    res=requests.post(url,data=words,headers=head)
    data=json.loads(res.text)
    print(data)
    try:
        tgt=data['translateResult'][0][0]['tgt']
    except Exception:
        t2.insert ('end' , '抱歉，我还在学习该语种中\n请重新输入')
    try:
        smartResult=data['smartResult']['entries'][1]
        t2.insert ('end' , '释义:{}'.format(tgt) + '\n\n' + '解释:{}'.format(str (smartResult)))
    except Exception:
        t2.insert ('end' , '释义:{}'.format(tgt) )
    return tgt,smartResult

def bf():
    word=t1.get()
    youdao(word)

l2=tk.Label(root,text='结果:',font=('隶书',15))
l2.grid(row=2,column=0)
t2=tk.Text(root,font=('隶书',14),height=10,width=40)
t2.grid(row=2,column=1)

b1=tk.Button(root,text='翻译',font=('Arial',16),width=8,command=bf)
b1.grid(row=7,column=1)

def del_text():
    t1.delete(0,'end')

b2=tk.Button(root,text='清除',font=('Arial',16),width=8,command=del_text)
b2.grid(row=8,column=1)

b3=tk.Button(root,text='退出',font=('Arial',16),width=8,command=root.quit)
b3.grid(row=9,column=1)

root.mainloop()
