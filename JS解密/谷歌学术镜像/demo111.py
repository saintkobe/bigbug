# -*- coding = utf-8 -*-
# @Time:  10:35
# @Author : floyd
# @File :.py
# @Software :PyCharm
import execjs
import requests
from lxml import etree
import re

with open('demo111.js', 'r', encoding='utf-8') as f:
    js1 = f.read()
    ctx = execjs.compile(js1)


def get_html(url):
    try:
        html = requests.get(url).text
    except:
        pass
    return html


def parse_content(html):
    tree = etree.HTML(html)
    script_text = tree.xpath('//script/text()')[0]
    securty = re.findall ( r'var autourl=(.*?);var ts=.*', script_text,re.S)[0]
    securty1=securty.replace('"','')
    securty1 = securty1.replace ( '[', '' )
    securty1 = securty1.replace ( ']', '' )
    securty2=securty1.split(',')

    return securty2

if __name__ == '__main__':
    html = get_html("http://ac.scmor.com/")
    security_list = parse_content(html)
    # print(security_list)
    for security_text in security_list:
        # print(security_text)
        print(ctx.call('strdecode',security_text))