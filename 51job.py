#coding=gbk
#@Time:  15:30
#@Author : floyd
#@File :.py
#@Software :PyCharm
import re
import requests
from fake_useragent import UserAgent
import json
import xlwt

ua=UserAgent()
header={
    "User-Agent":ua.random,
    'Connection': 'close',
    'Cookie':'partner=www_baidu_com; guid=20affb8813fe44a25dbbc292cf6324d3; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60040000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60040000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; _ujz=NDc3OTUxMTgw; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20200910%26%7C%26; ps=needv%3D0; 51job=cuid%3D47795118%26%7C%26cusername%3Dwskanb%26%7C%26cpassword%3D%26%7C%26cname%3D%25BA%25CE%25BD%25E0%26%7C%26cemail%3D564884042%2540qq.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0AgSFSDcnsRc%26%7C%26cconfirmkey%3D56xRPCvceD7mE%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D1%26%7C%26cnamekey%3D56%252FpHiNMXc5X6%26%7C%26to%3Da982ef522f6d9145dc76a2ad62a8c5685f59d5bc%26%7C%26'

}


def askurl(tag,page):
    url = "https://search.51job.com/list/040000,000000,0000,00,9,99,{tag},2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=".format(tag=tag, page=page)
    response=requests.get(url,headers=header)
    print(url)
    body=response.text
    return body

def get_data():
    body=askurl(tag,each)
    data = re.findall ('window.__SEARCH_RESULT__ =(.+)}</script>' , str (body))[0] + "}"
    data = json.loads (data)
    items=[]
    results=data['engine_search_result']
    for result in results:
        item=[]
        name=result['job_name']
        company_name=result['company_name']
        providesalary_text=result['providesalary_text']
        workarea_text=result['workarea_text']
        companytype_text=result['companytype_text']
        degreefrom=result['degreefrom']
        jobwelf=result['jobwelf']
        companyind_text=result['companyind_text']
        updatedate=result['updatedate']
        workyear=result['workyear']
        companysize_text=result['companysize_text']
        item.append(name)
        item.append(company_name)
        item.append(providesalary_text)
        item.append(workarea_text)
        item.append(companytype_text)
        item.append(degreefrom)
        item.append(jobwelf)
        item.append(companyind_text)
        item.append(updatedate)
        item.append(workyear)
        item.append(companysize_text)

        items.append(item)
    return items

def save_data(items,index):
    for i in range (0, 11) :
        sheet.write (0, i, col[i], style)
    for item in items:
        for j in range(0,11):

            sheet.write(index,j,item[j],style1)

        print ("第%d条" % (index))
        index+=1

tag=input('请输入要查询的内容:')

book = xlwt.Workbook (encoding='utf-8')
sheet = book.add_sheet ('51job' , cell_overwrite_ok=True)
col = ['招聘职位' , '公司' , '薪资' , '工作区域' , '公司性质' , '招聘人数' , '公司福利' , '公司行业','更新日期','工作年限','公司规模']
sheet.col (0).width = (25 * 367)  # 设置表格的宽度
sheet.col (1).width = (25 * 367)
sheet.col (2).width = (10 * 367)
sheet.col (3).width = (8 * 367)
sheet.col (4).width = (10 * 367)
sheet.col (5).width = (7 * 367)
sheet.col (6).width = (40 * 400)
sheet.col (7).width = (15 * 367)
sheet.col (8).width = (7 * 367)
sheet.col (9).width = (7 * 367)
sheet.col (10).width = (10 * 367)

style=xlwt.easyxf('font:bold on,height 220;align:wrap on ,vert centre,horiz center;')
style1=xlwt.easyxf('align:wrap on;')
# 设置单元格对齐方式
# alignment=xlwt.Alignment()
# 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
# alignment.horz=0x02
# 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
# alignment.vert=0x01
# alignment.wrap = 1
# alignment.wrap=1
# style = xlwt.XFStyle ()
# style.alignment = alignment

for each in range(1,2):
    index=(each-1)*50+1
    save_data(get_data(),index)
book.save('51job-{}.xls'.format(tag))



