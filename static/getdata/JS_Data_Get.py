import requests
from lxml import etree
import pandas as pd
import os

import sqlalchemy as sqla

from static.getdata.pre_value import pre_value

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}
try:
    os.mkdir('data')
except:
    # 忽略文件已存在的异常
    pass


def parse_url(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return etree.HTML(response.content)
    return False


def get_date(response):
    # 得到股票代码，开始和结束的日期
    start_date = ''.join(response.xpath('//input[@name="date_start_type"]/@value')[0].split('-'))
    end_date = ''.join(response.xpath('//input[@name="date_end_type"]/@value')[0].split('-'))
    code = response.xpath('//h1[@class="name"]/span/a/text()')[0]

    return code, start_date, end_date


def download(code, start_date, end_date):
    download_url = ''
    try:
        print(code)
        # 判断股票为深证还是上证
        if code[0:2] == '00':  # 深股判断
            download_url = "http://quotes.money.163.com/service/chddata.html?code=1" + code + "&start=" + start_date + "&end=" + end_date + \
                           "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        elif code[0:2] == '60' or code[0:2] == '90':  # 沪股判断
            download_url = "http://quotes.money.163.com/service/chddata.html?code=0" + code + "&start=" + start_date + "&end=" + end_date + \
                           "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        elif code[0:2] == '30' or code[0:2] == '68' or code[0:2] == '16':  # 创业股
            download_url = "http://quotes.money.163.com/service/chddata.html?code=1" + code + "&start=" + start_date + "&end=" + end_date + \
                           "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        print(download_url)
        data = requests.get(download_url, headers=headers)

        f = open(r'./data//' + code + '.csv', 'wb')
        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print('股票---', code, '历史数据正在下载')
    except:
        print('该股数据已存在，正在分析中....')
        pass


def pd_sort(code, G_bh):

    print(G_bh)
    df = pd.read_csv(r'./data/' + code + '.csv', usecols=[0, 1, 3, 4, 5, 6, 11], encoding='gbk')
    df.head()
    # df_new =df.columns['time',]
    # df_new = df.iloc[:365,:]
    df_new = df.iloc[:3000, :]
    df_new_sort = df_new.sort_values('日期', ascending=True)  # by指定按哪列排序，ascending表示是否升序    将日期这一列以升序排序
    # df_new_sort.head()
    # 日期,股票代码,名称,收盘价,最高价,最低价,开盘价

    df_new_sort.rename(
        columns={'日期': 'Date', '股票代码': 'Code', '收盘价': 'Close', '最高价': 'Highest', '最低价': 'Lowest', '开盘价': 'Open',
                 '成交量': 'Volume'}, inplace=True)
    b = len(df_new_sort['Date'].value_counts())
    df_new_sort.insert(0, 'id', range(1, b + 1))
    day_5 = df_new_sort.tail(5)
    print(day_5)
    day_5.to_csv(r'./data//' + code + '_5day.csv', index=False)
    df_new_sort.to_csv(r'./data//' + code + '.csv', index=False)
    try:
        names = ['id', 'Date', 'Code', 'Close', 'Highest', 'Lowest', 'Open', 'Volume']
        tablename = pd.read_csv(r'./data//' + code + '_5day.csv', header=None, engine='python', names=names)
        db = sqla.create_engine('mysql+pymysql://Wzh:Wzh1192548088.@120.77.58.237/WebSite'
                                '?charset=utf8')
        tablename.to_sql('{}'.format(code), db, index=False, if_exists='replace')
        print("----数据插入成功----")
        return pre_value(G_bh)
    except:
        print("----数据插入失败----")
        return False




def out(gp):
    G_bh = gp
    url = 'http://quotes.money.163.com/trade/lsjysj_' + str(G_bh) + '.html'

    response = parse_url(url)

    code, start_date, end_date = get_date(response)
    download(code, start_date, end_date)
    return pd_sort(code, G_bh)
