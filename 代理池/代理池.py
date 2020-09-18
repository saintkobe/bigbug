#-*- coding = utf-8 -*-
#@Time:  15:36
#@Author : floyd
#@File :.py
#@Software :PyCharm

import requests
import re
import parsel
import time
import random

def get_ip():
    ip_list=[]
    for i in range(1,2):
        url="https://www.kuaidaili.com/free/inha/%d/"%i
        res=requests.get(url).text
        # # list=re.findall('<tr>([\s\S]*)<tr>',res)
        #
        # data_list={}
        # for i in range(0,140):
        #     type=re.findall(r'<td data-title="类型">(.*?)</td>',res)
        #     ip=re.findall(r'<td data-title="IP">(.*?)</td>',res)
        #     port=re.findall(r'<td data-title="PORT">(.*?)</td>',res)
        #     data_list[type[i]]=ip[i]+':'+port[i]
        #     print(data_list)
        html=parsel.Selector(res)
        data_list=html.xpath('//*[@id="list"]/table/tbody/tr')
        for data in data_list:
            p_list={}
            type=data.xpath('./td[4]/text()').extract_first()
            ip=data.xpath('./td[1]/text()').extract_first()
            port=data.xpath('./td[2]/text()').extract_first()
            p_list[type]=ip +':'+ port
            ip_list.append(p_list)
            time.sleep (0.5)
    return ip_list
    # print(ip_list)
    # print("共获得ip:{}".format(len(ip_list)))

def check_ip(ip_list):
    can_use=[]
    for i in ip_list:
        url="https://www.baidu.com/"
        try:
            res=requests.get(url,proxies=i)
            if res.status_code==200:
                can_use.append(i)
        except Exception as e:
            print(e)
        finally:
            print("共获取高质量IP:{}条".format(len(can_use)))
    return can_use

if __name__=="__main__":
    a=check_ip(get_ip())
    date=time.strftime(('%Y-%m-%d'),time.localtime())
    with open('代理池{}'.format(date)+'.csv','w') as f:
        f.write(str(a))