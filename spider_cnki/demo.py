# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 21:40:10 2018

@author: lzy
"""
'''
主要数据库结构：
主键、论文号、论文名称、论文作者、发表时间、被引用、插入多个url
关系库
主键、外键、引证url、index、状态
'''

from selenium import webdriver
import time
from lxml import etree
#导入xlwt库用于写excel文件
import xlwt

def write_to_excel(self,data_array):
    # 初始化并创建一个工作簿
    file = xlwt.Workbook()
    # 创建一个名为sheetname的表单
    sheet = file.add_sheet('sheetname')

    if not data_array:
        return ''
    header = [u'编号', u'论文名称', u'作者', u'来源', u'发表时间', u'数据库', u'论文地址']
    i = 0
    # 写表头
    for each_header in header:
        sheet.write(0, i, each_header)
        i += 1
    row = 1
    # 填充每行的数据
    for each_row in data_array:
        col = 0
# 填充一行的每列数据
        for each_col in header:
            sheet.write(row, col, each_row[each_col])
            col += 1
        row += 1
# 将工作簿以bookname命名并保存
    file.save('cnki_out.xls')


def get_paper(page, index):
    html_parse = etree.HTML(page)
    ul = html_parse.xpath('//div[@class="essayBox"]/ul')[index]
    li_list = ul.findall('li')
    for li in li_list:
        a_list = li.findall('a')
        for index in range(0, len(a_list)):
            print(a_list[index].text)
            if index == 0:
                print(a_list[index].tail)

            # 在知网的查询框中输入体育学刊，获得cookie


def get_cookie():
    driver.get('http://kns.cnki.net/kns/brief/default_result.aspx')
    time.sleep(3)
    driver.find_element_by_name('txt_1_value1').send_keys('智慧城市')
    driver.find_element_by_xpath('//select[@id="txt_1_sel"]//option[@value="SU$%=|"]').click()
    driver.find_element_by_id('btnSearch').click()
    time.sleep(3)


# 缺少paperid
# 点击论文列表中的论文，进入到论文的页面，获得引证论文的url
def get_url(num):
    elements = driver.find_elements_by_xpath('//table[@class="GridTableContent"]//tr[@bgcolor]')
    data_array = []
    source_array = []
    for element in elements:
        try:
            a = element.find_element_by_xpath('td/a[@class="fz14"]')
            #print(a.get_attribute('href'))
            paper_info = element.text.replace('\n', ' ').split(' ')
            paper_info.append(a.get_attribute('href'))
            #print(type(paper_info))
            source = paper_info[4]
            #print(source)
            source_array.append(source)
            data_array.append(paper_info)
            print(paper_info)
            #while ('智慧城市' not in paper_info[index]):
            #    author = author + pa
            #
            #    per_info[index]
            #    index = index + 1
            #    date = paper_info[index + 1]
            #    author = paper_info[index]
            #    reference = paper_info[index + 3]
            #    print('author---' + author + 'data' + date)

        except Exception as arg:
            print()
        time.sleep(5)
        #print("source_array:",source_array)
    return num


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    get_cookie()
    num = 0
    now_page = 1
    # 抓包得到iframe中的url，由于有cookie，所以我们可以直接访问
    #driver.get('http://kns.cnki.net/kns/brief/brief.aspx?ctl=%E8%87%AA%E7%84%B6%E5%A4%A7%E6%95%B0%E6%8D%AE&dbPrefix=SCDB&PageName=ASP.brief_default_result_aspx&ShowHistory=1&isinEn=1')
    #driver.get('http://kns.cnki.net/kns/brief/brief.aspx?ctl=%E5%A4%A7%E6%95%B0%E6%8D%AE&action=5&dbPrefix=SCDB&PageName=ASP.brief_default_result_aspx&ShowHistory=1&isinEn=1')
    driver.get('http://kns.cnki.net/kns/brief/brief.aspx?ctl=%E6%99%BA%E6%85%A7%E5%9F%8E%E5%B8%82&action=5&dbPrefix=SCDB&PageName=ASP.brief_default_result_aspx&ShowHistory=1&isinEn=1')
    # 需要爬取300页的论文
    while (now_page < 301):
        num = get_url(num)
        a_list = driver.find_elements_by_xpath('//div[@class="TitleLeftCell"]//a')
        for a in a_list:
            if (a.text == '下一页'):
                a.click()
                break
        now_page = now_page + 1
        time.sleep(5)

