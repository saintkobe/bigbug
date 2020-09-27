# -*- coding = utf-8 -*-
# @Time:  11:23
# @Author : floyd
# @File :.py
# @Software :PyCharm
import requests
import re
from fake_useragent import UserAgent
from lxml import etree
import pandas as pd
import urllib.request
from StyleFrame import StyleFrame, Styler, utils

ua=UserAgent()

headers={

    "user-agent":ua.random
}
prox= {
    'HTTP': '121.232.148.92:9000',
    'HTTP': '175.42.128.25:9999'

}

def ask_url(url):
    res=requests.get(url,headers=headers,proxies=prox).text
    return res
# print(res)
# res=res.replace("\r|\n|\\s",'')
# with open("1.text",'w') as f:
#     f.write(res)
def get_list(word,page):
    url = "https://www.liepin.com/zhaopin/?compkind=&dqs=050090&pubTime=&pageSize=40&salary=&compTag=&sortFlag=&degradeFlag=0&compIds=&subIndustry=&jobKind=&industries=&compscale=&key={}&siTag=fw3F47vuJXKzz2u6l56qUQ%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp_bar&d_ckId=9889c680259efb59c06ece940b903913&d_curPage=0&d_pageSize=40&d_headId=9889c680259efb59c06ece940b903913&curPage={}".format(word,page)
    #print(url)
    res=ask_url(url)
# title=re.findall('<a href=".*" data-promid=".*" target=".*"[\s]+>(.*?)</a>',res,re.S)
    link=re.findall('<a href="(.*?)" data-promid=".*" target=".*"',res)
    # print(link)
    return link

def get_all(word,page):
    link=get_list(word,page)
    # print(link)
    title_list=[]
    company_list=[]
    money_list=[]
    city_list=[]
    info_list=[]
    adder_list=[]
    edu_list=[]
    exp_list=[]
    age_list=[]
    type_list=[]
    scale_list=[]
    url_list=[]
    for i in link:


        try:
            res=ask_url(i)
        except:
            continue
        html=etree.HTML(res)
        try:
            title=re.findall('<h1 title=".*">(.*?)</h1>',res)[0]
            title_list.append(title)
        except:
            title_list.append(None)

        try:
            # company=re.findall('<a href=".*" data-ipromid="" target="_blank"[\s]+title=".*">(.*?)</a>',res)
            company=html.xpath('//div[1]/h3/a/text()')[0]
            company_list.append(company)
        except:
            company_list.append(None)

        try:
            city=html.xpath('//*[@class="job-title-left"]//p[2]/span/a/text()')[0]
            city_list.append(city)
        except:
            city_list.append(None)

        try:
            # money=html.xpath('//*[@class="job-title-left"]//p[1]/text()')
            money=re.findall('<p class="job-item-title">(.*?)[\s]+<em>',res,re.S)[0]
            money_list.append(money)
        except:
            money_list.append(money)

        try:
            info=html.xpath('//div[@class="content content-word"]/text()')
            info=''.join(info[:-1]) #用空字符连接起来
            info_list.append(info)
        except:
            info_list.append(None)

        try:
            adder=html.xpath('//*[@class="new-compwrap"]//ul/li[3]/text()')[0]
            adder=adder.replace('公司地址：','')
            adder_list.append(adder)
        except:
            adder_list.append(None)

        try:
            edu=html.xpath('//div[@class="job-qualifications"]/span[1]/text()')[0]
            edu_list.append(edu)
        except:
            edu_list.append(None)

        try:
            exp = html.xpath ( '//div[@class="job-qualifications"]/span[2]/text()' )[0]
            exp_list.append(exp)
        except:
            exp_list.append(None)

        try:
            age = html.xpath ( '//div[@class="job-qualifications"]/span[4]/text()' )[0]
            age_list.append(age)
        except:
            age_list.append(None)

        try:
            type=html.xpath('//*[@class="new-compwrap"]//ul/li[1]/a/text()')[0]
            type_list.append(type)
        except:
            type_list.append(None)

        try:
            scale=html.xpath('//*[@class="new-compwrap"]//ul/li[2]/text()')[0]
            scale=scale.replace ( '公司规模：', '' )
            scale_list.append(scale)
        except:
            scale_list.append ( None)

        url_list.append(i)


    # a={
    #             '公司名':company_list,
    #             '招聘岗位':title_list,
    #             '薪资':money_list,
    #             '公司位置':city_list,
    #
    #         }
    # df=pd.DataFrame.from_dict(a,orient='index')
    df=pd.DataFrame({
                '公司名':company_list,
                '所属行业':type_list,
                '招聘岗位':title_list,
                '薪资':money_list,
                '办公地点':city_list,
                '年龄要求':age_list,
                '学历要求':edu_list,
                '经验要求':exp_list,
                '公司地址':adder_list,
                '公司规模':scale_list,
                '岗位信息' : info_list,
                '申请网址':url_list,
            })

    return df

def main():
    word1=input("要搜索的职业:")
    word=urllib.request.quote(word1)
    df_all=pd.DataFrame()

    for page in range(1,20):
        print ( f'正在读取第{page}页的数据' )
        df=get_all(word,page)
        df_all=df_all.append(df)
        df_all.to_excel( '猎聘-{}.xlsx'.format ( word1 ), encoding='utf_8_sig', index=False )
    print ( f'已读取总共{page}页的数据' )

    sf=StyleFrame.read_excel('猎聘-{}.xlsx'.format ( word1 ))
    print('data read successful!')
    #sf.set_column_width(columns=['公司名','岗位信息'],width=200)
    sf.set_column_width_dict(col_width_dict = {"公司名":20,"岗位信息":100,"招聘岗位":20,'申请网址':30})
    ew=StyleFrame.ExcelWriter('猎聘-{}.xlsx'.format(word1))
    sf.to_excel(ew)
    ew.save()
    print("data updated successful!")

if __name__=="__main__":
    main()
