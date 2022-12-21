import pymongo
from pymongo import MongoClient
import ssl
import certifi
ca = certifi.where()
# dBKey = ""

# Replace <username>:<password> with your own username and password in mongoDB
#<username:> searchmytenders
#<password:> E57ZrT8pbYY2E35Q
#DB NAME
dBName="searchmyTDB"
# "scrapedtendersdtl"
#Collection Names
eproc_col= "eproc_all_data"
scrapedTenderDtlCol="scrapedTenderDtlCol"
#For the gem different tab different collection will be used
#bidlist
bidlistCol ="bidlistDetail"
#Service Bid
serviceBidCol ="serviceBidDetail"
#Bunch Bid
bunchBidCol ="bunchBidDetail"
#Service Bunch
serviceBunchCol ="serviceBunchDetail"
#Bids to RA
bidsToRaCol ="bidsToRaDetail"
#Custom items
customItemsCol ="customItemsDetail"

customerDetailCol="customerMaster"
collectionNameDelta='siteDetail'
collectionGemPageList='gemPageList'
customerUID = "Cust123"
Epwd="SearchMyTenders@1234"
#incase of key uncomment below line
# client = pymongo.MongoClient(dBKey,tlsCAFile=ca)
# try:
#     client = pymongo.MongoClient(dBKey,tlsCAFile=ca)
# except pymongo.errors.ServerSelectionTimeoutError :
#
#     print('issue')

# client = MongoClient(dBKey)
client = pymongo.MongoClient()



#code to extract the sequencerCode from DB


#code to extract the Array of keywords
# Code for Keyword extraction starts here--------
smtDB = client[dBName]
colscrapedTenderDtl = smtDB[scrapedTenderDtlCol]
colName =smtDB[customerDetailCol]
# Declare a list variable to store whole string keyword in it.
keywordResults = colName.find() #removed customerUID as scraping require all customer keywords
keywordList = []
# Declare a set variable to store individual keyword in it and to avoid duplication
keywordListSet = set()
# Adding each keyword in set after removing white spaces before and after it
for keywordResult in keywordResults:
    keywordList = keywordResult['CustKeywords'].split(',')
    for l in keywordList:
        keywordListSet.add(l.strip())

# Set into a list. So we get a list of keywords without any duplication.
keywordArr = list(keywordListSet)
#print(keywordArr)


def eproc_col():
    return None