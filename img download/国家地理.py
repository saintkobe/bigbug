# -*- coding = utf-8 -*-
# @Time:  16:10
# @Author : floyd
# @File :.py
# @Software :PyCharm
import requests
import re
import os
import time


headers={
'Cookie':'__cfduid=dde7218a86b08d0332802e3947fcebd221600676366; robots=1; PHPSESSID=sv9gn87eti3qdc4p2363pfolb1; Hm_lvt_ca8fdc4afd8dbaec0d0f29ebf69ff42a=1600676370,1600676409; Hm_lpvt_ca8fdc4afd8dbaec0d0f29ebf69ff42a=1600676607',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}

def get_res(url):
    res=requests.get(url,headers=headers)
    return  res

def get_list():
    url="http://www.ngchina.com.cn/photography/photocontest/2019"
    # res=requests.get(url,headers=headers).text
    res=get_res(url).text
    # res=re.findall(r'<div class="index_img_list_box" style="height: 530px;">(.*?)</div>',res,flags=re.DOTALL)
    # type=re.findall(r'<h4><span>(.*?)</span></h4>',res,flags=re.DOTALL)
    # title=re.findall(r'<b class="pic_title"><a href=".*" target="_blank">(.*?)</a></b>',res)
    # link=re.findall(r'<b class="pic_title"><a href="(.*?)" target="_blank">.*</a></b>',res)
    link=re.findall(r'<a href="(.*?)" target="_blank">[\s]+<div class="thumb-wrapper">',res)
    return link

def get_type():
    link=get_list()
    url_list=[]
    for a in range ( 1, 10 ) :
        for i in link :
            url=i+'&page=%d'%a
            url_list.append(url)

    return url_list

def get_all():
    link=get_type()
    for i in link:
        res = get_res (i).text
        url = re.findall ( r'<h4 class="photo_list_title"><a href="(.*?)" target="_blank">.*</a></h4>', res )
        save_img(url)

def save_img(link):
    for i in link:
    #     res=requests.get(i).text
    #     print(i)
        res=get_res(i).text
        try:
            img=re.findall(r'<div id="detailPic" class="dasai_detail_pic">[\s]+<img src="(.*?)">',res)[0]
            title=re.findall(r'<h3>(.*?)<span>',res)[0]
            type=re.findall(r'</span><a href=".*">(.*?)</a><span> >',res)[0]
            # bar=tqdm.tqdm(type)
            # bar.set_description("获取[%s]帖子列表"%type)
            a=img.split('/')[-1]
            try:
                os.makedirs(str(type))
            except:
                pass
            if os.path.exists ( str ( type ) ) :
                if img:
                    with open ( str ( type ) + "/{}-{}".format ( title ,a), 'wb' ) as f :
                        # print ( img )
                        b = get_res ( img ).content
                        f.write ( b )
                        print ( "【{}】download finish!".format(title) )
        except:
            continue

if __name__=="__main__":
    if os.path.exists("./images"):
        print("path[images] exists")
        os.chdir("./images")
    else:
        os.mkdir("./images")
        os.chdir("./images")
    get_all()
    # save_img()