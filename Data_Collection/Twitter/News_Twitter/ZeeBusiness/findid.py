import tweepy
from tweepy import *
SCREEN_NAME=""
consumer_key="rqx0gOwAJmdhxMGAr7rNpw"
consumer_secret="zNADjG8Hlt8NSS64iAPtlrXqh6aJuTwFLEwDwd0rts"
access_key="166944864-6ZoEEJbN3Ip6ss6FtcTGGlR1bDEeJOWnaYY4OxBx"
access_secret="cLvvL9j4oxZCNI8ZcTccookGWXLZ7aRvp5pKoEbM"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
#myfile1 = open("illusiobaba.txt","w+")
tweet = api._lookup_users(screen_name = "Arsenal")
for t in tweet:
	id2=t.id
	#myfile1.write(id2 + "\n")
print id2
#myfile=open("CrypticShamTweets.txt","wb")
#page_list = []
#n = 0
#for page in tweepy.Cursor(api.user_timeline, count=200,user_id = id2, include_rts = True).pages(16):
#	page_list.append(page)
#	n = n+1
#	print n
#
#for page in page_list:
#	for status in page:
#		s = status.text
#		print s
#		myfile.write(s.encode("utf8")+"\n")
#myfile.close()

