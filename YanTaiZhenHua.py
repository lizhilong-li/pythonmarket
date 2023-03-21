# -*- coding:UTF-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup


def YTZH(rev_data, ifsmall, auth):
    global salelist
    username = rev_data['loginname']
    # print(username)
    pwd = rev_data['pwd']
    # print(pwd)
    session = requests.session()
    index_url = 'http://ec.zhenshang.com/bin/hdnet.dll/login'
    session = requests.session()
    session.get(index_url)
    data = 'txtEntCode=zhenhuaec&txtUsrCode=' + username + '&psdUsrPassword=' + pwd + '&txtToken=&loginbtn=%26%23160%3B%CD%A8%D3%C3%B5%C7%C2%BC%26%23160%3B'
    sign_url = 'http://ec.zhenshang.com/bin/hdnet.dll/LoginCheck'
    login = session.post(url=sign_url, data=data)
    login.encoding = 'gbk'
    result = {}
    if login.text.find('填写错误') > 0:
        result['code'] = '307'
        result['status'] = '用户名密码错误'
        return result
    # elif ifsmall:
    #     conn = dbsql()
    #     conn.w_small_account(rev_data)
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    str_yesterday = str(yesterday.year) + '.' + str(yesterday.month) + '.' + str(yesterday.day)
    try:
        str_startdate = rev_data['sale_begin_date'].replace('.', '-')
    except:
        str_startdate = str_yesterday

    try:
        str_enddate = rev_data['sale_end_date'].replace('.', '-')
    except:
        str_enddate = str_yesterday

    if auth == '4':
        salelist = []
        search_url = 'http://ec.zhenshang.com/bin/hdnet.dll/RepDisplay?Gid=55CD9C6C28E146EC9DDE38E579CFA79F'
        search_data = 'q_vdrcode=&q_vdrname=&q_date1=' + str_startdate + '&q_date2=' + str_enddate + '&q_gdcode=&q_gdcode2=&q_gdname=&q_f1=&q_storecode=&q_storename=&q_sortcode=&q_sortname=' \
                                                                                                     '&NotFirst=1&btnSearch=+%B2%E9%D1%AF+'

        saledata = session.post(url=search_url, data=search_data)
        saledata.encoding = 'gbk'
        Soup_index = BeautifulSoup(saledata.text, 'html.parser')
        recordCount = Soup_index.find(name='input', attrs={"name": "hd_CP_RecordCount"})
        records = int(recordCount.get('value'))  # 总记录数
        PageCount = Soup_index.find(name='input', attrs={"name": "hd_CP_PageCount"})
        Pages = int(PageCount.get('value'))  # 总页数
        trlist = Soup_index.find_all('tr', attrs={'class': 'listtd'})
        for tr in trlist:
            inser_data = []
            td_list = tr.find_all('td')
            if str(td_list[0].text) == '汇总信息':
                break
            inser_data.append(td_list[17].text)
            inser_data.append(td_list[18].text)
            inser_data.append(str(td_list[16].text).replace('.', '-'))
            inser_data.append(td_list[4].text)
            inser_data.append(td_list[6].text)
            inser_data.append(td_list[11].text)
            inser_data.append(td_list[12].text)
            salelist.append(inser_data)

        for i in range(2, Pages + 1):
            print('第' + str(i) + '次请求')
            page_url = 'http://ec.zhenshang.com/bin/hdnet.dll/RepDisplay?Gid=55CD9C6C28E146EC9DDE38E579CFA79F&UsrGid=94BC056E06A44F21B247DEA4A7C5D2E7'
            page_data = 'q_vdrcode=&q_vdrname=&q_date1=' + str_startdate + '&q_date2=' + str_enddate + '&q_gdcode=&q_gdcode2=&q_gdname=&q_f1=&q_storecode=' \
                                                                                                       '&q_storename=&q_sortcode=&q_sortname=&NotFirst=1&hd_CP_GoToPage=1&hd_CP_RecordCount=' + str(
                records) \
                        + '&hd_CP_PageNum=' + str(i) + '&hd_CP_PageCount=' + str(Pages) + '&hd_CP_isCP=1'
            # print(page_data)
            page_index = session.post(url=page_url, data=page_data)
            page_index.encoding = 'gbk'

            Soup_index = BeautifulSoup(page_index.text, 'html.parser')
            trlist = Soup_index.find_all('tr', attrs={'class': 'listtd'})
            for tr in trlist:
                inser_data = []
                td_list = tr.find_all('td')
                if str(td_list[0].text) == '汇总信息':
                    break
                inser_data.append(td_list[17].text)
                inser_data.append(td_list[18].text)
                inser_data.append(str(td_list[16].text).replace('.', '-'))
                inser_data.append(td_list[4].text)
                inser_data.append(td_list[6].text)
                inser_data.append(td_list[11].text)
                inser_data.append(td_list[12].text)
                salelist.append(inser_data)
    result = {}
    result['code'] = '200'
    result['salelist'] = salelist
    return result


if __name__ == '__main__':
    rev_data = {
        'loginname': '振华登录名',
        'pwd': '密码',
        'sale_begin_date': '2022-01-01',  # 开始日期sale_end_date
        'sale_end_date': '2022-01-01',  # 结束日期
        'type': 4
    }
    YTZH(rev_data, False, 4)
