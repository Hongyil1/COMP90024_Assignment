"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney
====================================================
"""

# !/usr/bin/env python

import json

import connection
import pycouchdb
import suburbs_shapely_processor
import tweepy
import tweet_processer
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

server = pycouchdb.Server("http://%s:%s@127.0.0.1:5984/" % ('admin', 'admin*230'))
dbname = 'processed_data'

db = server.database(dbname)
suburbs_melb = "melbourne.json"
suburbs_syd = "sydney.json"
sub_dic = suburbs_shapely_processor.read_json(suburbs_melb, suburbs_syd)


# Twitter Stream with location
class MyListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        text = data["extended_tweet"]["full_text"] if "extended_tweet" in data else data["text"]
        hashtags = data["extended_tweet"]["entities"]["hashtags"] if "extended_tweet" in data else data["entities"][
            "hashtags"]
        processor = tweet_processer.Proccesser()
       
       # Skip some tweets with strange format
        try:
            # Process the tweet
            dic_tweet = processor.get_formated_tweet(data, text, hashtags, sub_dic)
           
            # Aviod duplication 
            try:
                db.save(dic_tweet)
            except:
                print("Duplicated tweet")
                pass
        except:
            pass

    def on_error(self, status):
        print(status)
        return True

# Key of APP
consumer_key, consumer_secret, access_token, access_secret = connection.access_stream_twitter_configuration()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Set up the API
api = tweepy.API(auth)
# Geobox covers NSW and VIC
geobox = [144.5937418, -38.4338593, 145.5125288, -37.5112737]

# Start Stream API
twitter_stream = Stream(auth, MyListener(), tweet_mode='extended')
twitter_stream.filter(locations=geobox)
