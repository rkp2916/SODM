#!/usr/bin/python 
#
# wget wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
# unzip imm6010.zip

import math
import time
import re
import os
import sys
#import pymongo
from pymongo import MongoClient
import datetime
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')

#Open a connection to MongoDb (localhost)
client=MongoClient("localhost", 27017)
db=client.streamline

# word list is as of December 2011 
filenameWords = 'words/wordweightings.txt'
wordlist = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameWords) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    sentiments1 = map(lambda word: wordlist.get(word, 0), words)
    sentiments = []
    for k in sentiments1:
	if k != 0:
		sentiments.append(k)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
    else:
        sentiment = 0
    print 'from function',sentiment
    return sentiment



if __name__ == '__main__':
    # Get the records from Mongo and plot a graph
    fig = plt.figure()
    plt.axis([0,200,-3,3])
    i = 0
    x = list()
    y = list()
    plt.ion()
    plt.show()
    fil = open('RecentHarvest.txt')
    content = fil.read()
    print content
    os.makedirs('./'+content)
    prev = 0

    while i<1000:
	records = db.streaming.find()
#	j = sum(sentiments)/math.sqrt(len(sentiments))
#	db.sentiment.insert({'sentiment': "%6.2f" % j, 'date': datetime.datetime.utcnow()})
#	print("%6.2f" % j)
	sentiments = map(sentiment, [ tweet['text'] for tweet in records ])
	j = sum(sentiments)/math.sqrt(len(sentiments))
	print("%6.2f" % j)
	if prev != j:
		prev = j;
		x.append(i)
		y.append(j)
		plt.plot(x,y,'k')
		plt.draw()
	if i%10 == 0:
		plt.savefig('./'+content+'/result'+str(i)+'.png')
	i+=1
	time.sleep(1.5)
