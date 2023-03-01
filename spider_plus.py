from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json
import requests

time_stamp = time.time()
time_stamp = int(time_stamp*1000)


pymysql.install_as_MySQLdb()
DB_STRING = "mysql+mysqldb://root:zkw666..@127.0.0.1:3306/gpdb?charset=utf8"
engine = create_engine(DB_STRING)

result = pd.DataFrame([str(time_stamp)])
result.columns=['create_time']

result.to_sql('time_stamp', con=engine, chunksize=10000, if_exists='append', index=False)








