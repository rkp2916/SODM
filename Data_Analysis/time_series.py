import sys	
import time
import os
import datetime
from pymongo import Connection
from pylab import *
import matplotlib.pyplot as plt

#open a connection to mongoDB
connection =  Connection()
db = connection.twitter

result = db.news.aggregate([ {"$match":{"news_title_tokens":"sensex"}}, {"$group":{"_id":"$status_created_at_date_str","total":{"$sum":"$wl_score"}}},{"$sort":{"_id":1}} ])['result']
print result
time.sleep(15.0)
