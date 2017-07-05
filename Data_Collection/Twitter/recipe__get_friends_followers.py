# -*- coding: utf-8 -*-

import sys
import twitter
from recipe__make_twitter_request import make_twitter_request
from recipe__oauth_login import oauth_login
import functools

SCREEN_NAME = 'smileshah_'
MAX_IDS = 50000

file = open("smileshah__following_ids.txt","wb")
file2= open("smileshah__follower_ids.txt","wb")

if __name__ == '__main__':

    # Not authenticating lowers your rate limit to 150 requests per hr. 
    # Authenticate to get 350 requests per hour.

    #t = twitter.Twitter(domain='api.twitter.com', api_version='1')
    t = oauth_login()

    # You could call make_twitter_request(t, t.friends.ids, *args, **kw) or 
    # use functools to "partially bind" a new callable with these parameters

    get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)

    # XXX: Ditto if you want to do the same thing to get followers...

    

    cursor = -1
    ids = []
    while cursor != 0:

        # Use make_twitter_request via the partially bound callable...

        response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor)
        ids += response['ids']
        cursor = response['next_cursor']

        print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)

        file1 = open("smileshah__following_ids.txt","wb")

        # Consider storing the ids to disk during each iteration to provide an 
        # an additional layer of protection from exceptional circumstances

        if len(ids) >= MAX_IDS:
            break

	for i in ids:
		file1.write(str(i)+'\n')

        #file1 = open("followers.txt","wb")



    get_followers_ids = functools.partial(make_twitter_request, t, t.followers.ids)
    

    cursor = -1
    ids = []
    while cursor != 0:
        
        response = get_followers_ids(screen_name=SCREEN_NAME, cursor=cursor)
        ids += response['ids']
        cursor = response['next_cursor']

        print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)

        file3 = open("smileshah__follower_ids.txt","wb")

        if len(ids) >= MAX_IDS:
        	break

    for i in ids:
    	file3.write(str(i) + '\n')




    # Do something useful with the ids like store them to disk...

    #print ids 

