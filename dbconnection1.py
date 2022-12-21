import pymongo
from pymongo import MongoClient
import ssl
import certifi
ca = certifi.where()
dbkey = 'mongodb://localhost:27017'

dbname = 'state_tenders'

arunachal_col = 'arunachal_tenders'
assam_col = 'assam_tenders'
haryana_col = 'haryana_tenders'
delhi_col = 'delhi_tenders'
kerala_col = 'kerala_col'

client = MongoClient(dbkey)




