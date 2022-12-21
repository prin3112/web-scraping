from PIL import Image
import dbconnection1
from dbconnection1 import dbkey, arunachal_col, dbname
from pytesseract import pytesseract
from selenium import webdriver
import pandas as pd
import numpy as np
from time import sleep
import cv2
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import urllib
import pymongo
from pymongo import MongoClient
import ssl
import certifi
ca = certifi.where()

pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
driver = webdriver.Chrome("C:\\Users\\HP\\Chromedriver.exe")
url = 'https://arunachaltenders.gov.in/nicgep/app?page=FrontEndAdvancedSearch&service=page'
driver.get(url)
sleep(2)

driver.find_element("xpath", '/html/body/div/table/tbody/tr[1]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/span/span[2]/span[1]/a').click()
driver.find_element("xpath", '//*[@id="published"]').click()

arun = []
x = 1
while True:
    try:
        for i in range(x, 4):
            x += 1
            img = driver.find_element("xpath", '//*[@id="captchaImage"]').screenshot('captcha.png')
            image = cv2.imread('captcha.png', 0)
            gray_filtered = cv2.inRange(image, 0, 75)
            cv2.imwrite("cleaned.png", gray_filtered)
            text = pytesseract.image_to_string('cleaned.png')
            print(text)
            sleep(2)
            inputelement = driver.find_element("xpath", "//*[@id='captchaText']")
            inputelement.send_keys(text)
            row = len(driver.find_elements("xpath", "//*[@id='table']/tbody/tr"))
            print("number of rows = ", row)
            cols = len(driver.find_elements("xpath", "//*[@id='table']/tbody/tr[1]/td"))
            print(cols)
            for j in range(2, row):
                for k in range(1, cols+1):
                    data = driver.find_element("xpath", "/html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[12]/td/table/tbody/tr["+str(j)+"]/td["+str(k)+"]")
                    data_ = data.text
                    print(data_, end=" ")
                    arun.append(data_)
            driver.find_element("xpath", "//*[@id='linkFwd']").click()
            driver.find_element("xpath", '//*[@id="captchaText"]').clear()
    except (NoSuchElementException, ElementClickInterceptedException):
        continue
    break

c = len(arun)//7
arunar = np.array(arun).reshape(c, 7)
arundf = pd.DataFrame(arunar)
arundf.columns = ['S.No', 'e-Published-Date', 'Bid Submission Closing Date', 'Tender Opening Date', 'Title and Ref.No./Tender ID', 'Organisation Chain', 'Tender Value in ₹']
#arundf.set_index('S.No')
arundf.drop(['S.No'], axis=1, inplace=True)

arun_dict = arundf.to_dict('records')
print(arun_dict)

client = MongoClient(dbkey)
db = client[dbname]
col = db[arunachal_col]
for l in arun_dict:

 E_Published_Date = str(l['e-Published-Date'])
 Bid_closing_date = str(l['Bid Submission Closing Date'])
 Tender_opening_date = str(l['Tender Opening Date'])
 Tender_ID = str(l['Title and Ref.No./Tender ID'])
 Organisation_Chain = str(l['Organisation Chain'])
 Tender_value = str(l['Tender Value in ₹'])
 col.update_one({"Title and Ref.No./Tender ID": Tender_ID}, {"$set": {"e-published-date": E_Published_Date, "Bid Submission Closing Date": Bid_closing_date,
                          "Tender Opening Date": Tender_opening_date,
                          "Organisation chain": Organisation_Chain, "Tender Value in ₹": Tender_value}}, upsert=True)
# email_col.update_one({"Bid_No": BID_NO}, {
    # "$set": {"Items": Items, "Quantity_Required": Quantity_Required, "Department_Name_And_Address": Department,
                 # "Start_Date": Start_Date, "End_Date": End_Date}}, upsert=True)
