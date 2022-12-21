import dbconnection1
from dbconnection1 import dbkey, arunachal_col, dbname
from bs4 import BeautifulSoup
import os
import requests
import selenium
from selenium import webdriver
import numpy as np
import pandas as pd
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import urllib
import pymongo
from pymongo import MongoClient
import ssl
import certifi
ca = certifi.where()
gail_up = []
gail_in = []
client = MongoClient(dbkey)
db = client[dbname]
col = db[arunachal_col]
driver = webdriver.Chrome("C:\\Users\\HP\\Chromedriver.exe")

try:
    for i in range(1, 2):
        url1 = 'https://gailtenders.in/Gailtenders/general_url.asp?val=4&inb=1&gotopage=' + str(i) + ''
        driver.get(url1)

        rows = len(driver.find_elements("xpath", '/html/body/table/tbody/tr/td/table[2]/tbody/'
                                                 'tr/td/table/tbody/tr'))
        cols = len(driver.find_elements("xpath",
                                        '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/'
                                        'tr[1]/td'))
        for m in range(2, rows):
            for n in range(2, cols + 1):
                data = driver.find_element("xpath",
                                           '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[' + str(
                                               m) + ']/td[' + str(n) + ']')
                data_ = data.text
                gail_up.append(data_)
            a = len(gail_up) // 3
            b = np.array(gail_up).reshape(a, 3)
            c = pd.DataFrame(b)
            c.columns = ['Closing Date', 'Tender Subject', 'Ref_No']
            d = c.to_dict('records')
            for di in d:
             Closing_date = str(di['Closing Date'])
             Tender_Subject = str(di['Tender Subject'])
             Ref_No = str(di['Ref_No'])
             #remove main in main code here it is used to test code
             col.update_one({'Ref_No': Ref_No},
                            {'$set': {'Closing date main': Closing_date, 'Tender Subject main': Tender_Subject}},
                            upsert=True)

        for o in range(2, rows):
            driver.find_element("xpath", "/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[" + str(
                                o) + "]/td[3]/table/tbody/tr[1]/td/a").click()
            rows1 = len(driver.find_elements("xpath", '/html/body/table/tbody/tr[1]/td/table[2]/tbody/tr/td/'
                                                  'table[2]/tbody/tr'))
            cols1 = len(driver.find_elements("xpath", '/html/body/table/tbody/tr[1]/td/table[2]/tbody/tr/td/'
                                                  'table[2]/tbody/tr[1]/td'))

            for k in range(1, rows1 + 1):
                data = driver.find_element("xpath",
                                           '/html/body/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table[2]/'
                                           'tbody/tr[' + str(k) + ']/td[2]')
                data1_ = data.text
                gail_in.append(data1_)
            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, 'html.parser')
            folder_location = r'C:\Users\HP\Downloads'
            z = soup.find_all('a', href=True)
            for link in z:
                if ('Tender' in link.get('href')):
                    print(True)
                    response = requests.get('https://gailtenders.in/Gailtenders/' + link.get('href'))
                    filename = os.path.join(folder_location, link['href'].split('/')[-1])
                    pdf = open(filename, 'wb')
                    pdf.write(response.content)
                    pdf.close()
                    print("File ", " downloaded")

            e = len(gail_in) // 15
            f = np.array(gail_in).reshape(e, 15)
            g = pd.DataFrame(f)
            g.columns = ['Tender_Reference_No', 'Tender Type', 'Product Category', 'Tender Receiving Location',
                         'Tender Subject', 'Inviting Officer', 'Form Contract', 'Tender Category',
                         'Tender Publication Date',
                         'Tender Issuance Date', 'Tender Closing Date', 'Tender Opening Date',
                         'Pre-Bid Meeting Date / Pre-Tender Meeting Date', 'ti_ck', 'Tender Document']
            g.drop(['ti_ck'], axis=1, inplace=True)
            h = g.to_dict('records')
            for di1 in h:
                Ref_No = str(di1['Tender_Reference_No'])
                Tender_Type = str(di1['Tender Type'])
                Product_Category = str(di1['Product Category'])
                Tender_Receiving_Location = str(di1['Tender Receiving Location'])
                Tender_Subject = str(di1['Tender Subject'])
                Inviting_Officer = str(di1['Inviting Officer'])
                Form_Contract = str(di1['Form Contract'])
                Tender_Category = str(di1['Tender Category'])
                Tender_Publication_Date = str(di1['Tender Publication Date'])
                Tender_Issuance_Date = str(di1['Tender Issuance Date'])
                Tender_Closing_Date = str(di1['Tender Closing Date'])
                Tender_Opening_Date = str(di1['Tender Opening Date'])
                Pre_Tender_Meeting_Date = str(di1['Pre-Bid Meeting Date / Pre-Tender Meeting Date'])
                Tender_Document = str(di1['Tender Document'])

                col.update_one({'Ref_No': Ref_No},
                               {'$set': {'Tender type': Tender_Type, 'Product category': Product_Category,
                                         'Tender Receiving Location': Tender_Receiving_Location,
                                         'Tender Subject': Tender_Subject, 'Inviting Officer': Inviting_Officer,
                                         'Form Contract': Form_Contract, 'Tender Category': Tender_Category,
                                         'Tender Publication Date': Tender_Publication_Date,
                                         'Tender Issuance Date': Tender_Issuance_Date,
                                         'Tender Closing Date': Tender_Closing_Date,
                                         'Tender Opening Date': Tender_Opening_Date,
                                         'Pre-Bid Meeting Date / Pre-Tender Meeting Date ': Pre_Tender_Meeting_Date,
                                         'Tender Document': Tender_Document}}, upsert=True)

            driver.get(url1)
except NoSuchElementException:
    print('Done')





