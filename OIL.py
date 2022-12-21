import selenium
from selenium import webdriver
import pymongo
from pymongo import MongoClient
import dbconnection1
from dbconnection1 import dbkey, arunachal_col, dbname
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import os
import ssl
import certifi
import urllib
import json
ca = certifi.where()
Tender_des = []
Tender_no = []
client = MongoClient(dbkey)
db = client[dbname]
col = db[arunachal_col]

url = 'https://www.oil-india.com/NNational'
driver = webdriver.Chrome("C:\\Users\\HP\\Chromedriver.exe")
driver.get(url)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

a = soup.find_all("ul", {'class': 'reports-list no-icon'})
for w in range(0, 290):
    b = a[w].text
    c = b.replace(' ', '_')
    d = c.replace(';', '_')
    e = d.split()
    try:
        f = e[-2]+' '+e[-1]
    except IndexError:
        f = e[-1]
    Tender_des.append(f)
    Tender_no.append(e[0])
df = pd.DataFrame({'Tend_no': Tender_no[:288],
                  'Tend_detail': Tender_des[:288]},
                 columns=['Tend_no', 'Tend_detail'])
df_d = df.to_dict('records')
for Te in df_d:
 Ref_no = str(Te['Tend_no'])
 Tend_det = str(Te['Tend_detail'])
 col.update_one({'Tend_no': Ref_no}, {'$set': {'Tend_detail': Tend_det}}, upsert=True)


z = soup.find_all('a', href=True)
folder_location = r'C:\Users\HP\Downloads' #change location while executing
for i in z:
    if ('NIT' in i.get('href')):
        response = requests.get('https://www.oil-india.com/' + i.get('href'))
        filename = os.path.join(folder_location, i['href'].split('/')[-1])
        pdf = open(filename, 'wb')
        pdf.write(response.content)
        pdf.close()
        print("File ", " downloaded")


