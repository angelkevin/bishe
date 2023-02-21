from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import threading
import pymysql
from sqlalchemy import create_engine
import os

pymysql.install_as_MySQLdb()
user_name = 'root'
password = 'zkw666..'

DB_STRING = f"mysql+mysqldb://{user_name}:{password}@127.0.0.1:3306/gpdb?charset=utf8"
engine = create_engine(DB_STRING)

URLs = [
    'https://quote.eastmoney.com/center/gridlist.html#bj_a_board',
    ]

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')


def spider(url):
    result = []
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_num = driver.find_element(by=By.XPATH, value='//*[@id="main-table_paginate"]/span[1]/a[5]').text
    for i in range(0, int(page_num)):
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        massage = soup.find_all(id="table_wrapper-table")
        page = massage[0]
        page_massage = page.findAllNext('td')
        m = 0
        for j in range(int(len(page_massage) / 20.0) + 1):
            l = []
            tt = page_massage[m:m + 19]
            l.append(tt[0].text)

            l.append(tt[1].text)

            l.append(tt[2].text)

            if str(tt[4]).split("\"")[3] == 'red':
                l.append(tt[4].text)
            elif str(tt[4]).split("\"")[3] == 'green':
                l.append('-' + tt[4].text)
            else:
                l.append(tt[4].text)

            if "%" in tt[5].text:
                l.append(str(round(float(tt[5].text.split("%")[0]) * 0.01, 2)))
            else:
                l.append(tt[5].text)

            if str(tt[6]).split("\"")[1] == 'red':
                l.append(tt[6].text)
            else:
                l.append(tt[6].text)

            if "万" in tt[7].text:
                l.append(str(round(float(tt[7].text.split("万")[0]) * 10000, 2)))
            elif "亿" in tt[7].text:
                l.append(str(round(float(tt[7].text.split("万")[0]) * 100000000, 2)))
            else:
                l.append(tt[7].text)

            if "万" in tt[8].text:
                l.append(str(round(float(tt[8].text.split("万")[0]) * 10000, 2)))
            elif "亿" in tt[8].text:
                l.append(str(round(float(tt[8].text.split("亿")[0]) * 100000000, 2)))
            else:
                l.append(tt[8].text)

            if "%" in tt[9].text:
                l.append(str(round(float(tt[9].text.split("%")[0]) * 0.01, 2)))
            else:
                l.append(tt[9].text)

            l.append(tt[10].text)
            l.append(tt[11].text)
            l.append(tt[12].text)
            l.append(tt[13].text)
            l.append(tt[14].text)

            if "%" in tt[15].text:
                l.append(str(round(float(tt[15].text.split("%")[0]) * 0.01, 2)))
            else:
                l.append(tt[15].text)
            l.append(tt[16].text)
            l.append(tt[17].text)
            m = m + 19
            result.append(l)
        button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/a[2]')
        driver.execute_script("$(arguments[0]).click()", button)
        time.sleep(1)
    print(len(result))
    print(url)
    driver.close()
    return result


def save_data(data, name):
    today = time.strftime('%Y-%m-%d', time.localtime())
    today1 = str(time.time())
    df = pd.DataFrame(data, columns=[
        'serial_number',
        'code',
        'name',
        'latest_price',
        'rise_and_fall',
        'rise_and_fall_amount',
        'volume',
        'turnover',
        'amplitude',
        'highest',
        'lowest',
        'open_today',
        'yesterday',
        'volume_ratio',
        'turnover_rate',
        'ratio_p/b',
        'ratio'
    ])
    df = df.replace('-', '0')
    df = df.drop_duplicates(subset=['code'], keep='first')
    df.insert(17, 'create_time', str(today1), allow_duplicates=False)
    df.to_sql('stock_market_data', con=engine, chunksize=10000, if_exists='append', index=False)
    #os.mkdir(f"/opt/bishe/data/{name}")
    df.to_csv(path_or_buf=f"/opt/bishe/data/{name}/{today}.csv", index=False, header=False, encoding="UTF-8",mode='a')

if __name__ == '__main__':

    for i in URLs:
        data = spider(i)
        save_data(data,i.split('#')[1])


