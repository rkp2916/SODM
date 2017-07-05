# -*- coding: utf-8 -*-

import json
import urllib2
from recipe__oauth_login import oauth_login
from recipe__search import search

def get_entities(tweet):
    return tweet['entities']

if __name__ == '__main__':
    t = oauth_login()
    tweets = search(t, "TOIIndiaNews", max_batches=1, count=1) # Use "Python" as a sample query to get some tweets to process
    print tweets
#    tweets = ['More bombs found in Patna, suspect names two others http://t.co/erNwwZD4NT']
    entities = [ get_entities(tweet) for tweet in tweets ]
    print entities
#    for i in entities:
#	for j in i['urls']:
#		print j['expanded_url']
#    print json.dumps(entities, indent=1)
