# -*- coding: utf-8 -*-

import sys
import json
import twitter
import tweepy
import datetime
import re
import urllib2
from recipe__oauth_login import oauth_login
from pymongo import *
#from networkx import Connection
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
import string

#TWEET_ID = 57305746 # Example: 24877908333961216

myfile=open("rkp1107_following_ids.txt","r")
idlist=myfile.readlines()
client=MongoClient("localhost", 27017)
db = client.twitter

# word list is as of December 2011 
filenameWords = 'words/wordweightings.txt'
wordlist = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameWords) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

SCREEN_NAME="rkp1107"
consumer_key="rqx0gOwAJmdhxMGAr7rNpw"
consumer_secret='zNADjG8Hlt8NSS64iAPtlrXqh6aJuTwFLEwDwd0rts'
access_key='166944864-6ZoEEJbN3Ip6ss6FtcTGGlR1bDEeJOWnaYY4OxBx'
access_secret='cLvvL9j4oxZCNI8ZcTccookGWXLZ7aRvp5pKoEbM'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

list1 = ['author', 'contributors', 'coordinates', 'created_at', 'destroy', 'entities', 'favorite', 'favorite_count', 'favorited', 'filter_level', 'geo', 'id', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'lang', 'parse', 'parse_list', 'place', 'possibly_sensitive', 'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'source_url', 'text', 'truncated', 'user']

x = 0
while 1:
	try:
		
		id1=idlist[x]
		if not idlist: break	
		tweet = api._lookup_users(user_id = id1)
		for t in tweet:
			screen_name=t.screen_name
			print screen_name
			
			page_list = []
			n = 0
			myfile = open(screen_name,"wb")
			try:
				result = tweepy.Cursor(api.user_timeline, count=200,user_id = id1, include_rts = True).pages(2)
			except:
				x = True
				while x:
					try:
						print 'Waiting for internet connection...'
						x = False
						urllib2.urlopen("http://google.com", timeout = 1)
					except:
						x = True
				continue
			for page in result:
				page_list.append(page)
				n = n+1
				print n
				for page in page_list:
					for status in page:
	#					print dir(status)
						author_description = status.author.description
						author_id_str = status.author.id_str
						author_favourites_count = status.author.favourites_count
						author_name = status.author.name
						author_screen_name = status.author.screen_name
						author_followers_count = status.author.followers_count
						author_location = status.author.location
						author_friends_count = status.author.friends_count
						author_url = status.author.url
						author_verified = status.author.verified
						author_statuses_count = status.author.statuses_count
						status_id_str = status.id_str
						d = status.created_at
						status_created_at_date_str = status.created_at.strftime("%d-%m-%Y")
						status_created_at_time_str = status.created_at.strftime("%H:%M:%S")
						status_entities = status.entities
						status_favorite_count = status.favorite_count
						status_in_reply_to_screen_name = status.in_reply_to_screen_name
						status_in_reply_to_status_id_str = status.in_reply_to_status_id_str
						status_in_reply_to_user_id_str = status.in_reply_to_user_id_str
						status_retweet_count = status.retweet_count
						status_source = status.source
						status_text = str(status.text.encode('ascii','ignore'))
	
						str1 = status_text.translate(string.maketrans("",""), string.punctuation)
	#					print 'Removing punctuation marks'
	
						str1 = str1.lower()
	#					print 'Normalizing to lower case:'
		
						lst = nltk.word_tokenize(str1)
	#					print 'After tokenization:'
					
						minlength = 2
						lst = [token for token in lst if(not token in stopwords.words('english')) and len(token) >=minlength]
						lst1 = lst
	#					print 'Removing Stop Words:'
		
						sentiments = map(lambda word: wordlist.get(word, 0), lst)
						print zip(lst,sentiments)
						if sentiments:
							# How should you weight the individual word sentiments? 
							# You could do N, sqrt(N) or 1 for example. Here I use N
							sentiment = float(sum(sentiments))/len(lst)
						else:
						        sentiment = 0
						print status_text
						print sentiment
						db.trial.insert	({'author_description':author_description,'author_id_str':author_id_str,'author_favourites_count':author_favourites_count,'author_name':author_name,'author_screen_name':author_screen_name,'author_followers_count':author_followers_count,'author_location':author_location,'author_friends_count':author_friends_count,'author_url':author_url,'author_verified':author_verified,'author_statuses_count':author_statuses_count,'status_id_str':status_id_str,'status_created_at':d,'status_created_at_date_str':status_created_at_date_str,'status_created_at_time_str':status_created_at_time_str,'status_entities':status_entities,'status_favorite_count':status_favorite_count,'status_in_reply_to_screen_name':status_in_reply_to_screen_name,'status_in_reply_to_status_id_str':status_in_reply_to_status_id_str,'status_in_reply_to_user_id_str':status_in_reply_to_user_id_str,'status_retweet_count':status_retweet_count,'status_source':status_source,'status_text':status_text,'tokens':lst,'wl_score':sentiment})
						myfile.write(status_text+'\n')
			myfile.close()
			x += 1
	except EOFError:
		print "End Of File"
# No authentication required, but rate limiting is enforced

#twee = t.statuses.show(id=TWEET_ID, include_entities=1) 

#s = tweet.text
#print s.encode("utf8")

#print json.dumps(twee, indent=1)
