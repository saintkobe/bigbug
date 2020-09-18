# -*- coding = utf-8 -*-
# @Time:  15:06
# @Author : floyd
# @File :.py
# @Software :PyCharm

from selenium import webdriver
import time
import requests


head = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

count =24

def askURL():
    #url = 'https://bbs.hupu.com/32034561.html'
    url ='https://bbs.hupu.com/32034515.html'
    fb=webdriver.ChromeOptions()
    fb.add_argument ('--headless')
    fb.add_argument ('--disable-gpu')
    fb.add_argument ("window-size=1024,768")
    fb.add_argument ("--no-sandbox")
    fb =webdriver.Chrome(options=fb,executable_path=r'C:\Users\Administrator\Desktop\chromedriver.exe')
    fb.get (url)
    a=fb.find_elements_by_class_name('img-gif')
    for i in a:
        i.click()
        #time.sleep(1)
        b=fb.find_elements_by_class_name('downimg')
        for i in b:
            c=i.get_attribute('href')
            if c !=None:
                ImgSave(c)

def ImgSave(imgurl):
    global count
    response =requests.get(imgurl,headers=head)
    with open('./data/img/{}.gif'.format(count),'ab') as f:
        f.write(response.content)
        count +=1

if __name__=="__main__":
    askURL()