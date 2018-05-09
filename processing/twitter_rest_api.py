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

import datetime

import connection
import pycouchdb
import suburbs_shapely_processor
import tweepy
import tweet_processer
from tweepy import AppAuthHandler


def get_tweets(api, time, geo_code, db, maxTweets, sub_dic):

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1
    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))

    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                # The first time to send request
                new_tweets = api.search(geocode=geo_code, tweet_mode='extended', count='100', until=time)
            else:
                # The next time to send request
                new_tweets = api.search(geocode=geo_code, tweet_mode='extended', count='100', until=time,
                                        max_id=str(max_id - 1))
            
            # Stop when get the ordest tweets
            if not new_tweets:
                print("no more tweets found")
                break
            for tweet in new_tweets:
                tweet = tweet._json
                processor = tweet_processer.Proccesser()
                text = tweet["full_text"]
                hashtags = tweet["entities"]["hashtags"]
                dic_tweet = processor.get_formated_tweet(tweet, text, hashtags, sub_dic)

                # Avoid duplication
                try:
                    db.save(dic_tweet)
                except:
                    print("Duplicated tweet")
                    pass
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id

        except:
            # Some tweets may have strange formate, just skip it
            pass

    print("downloaded {0} tweets, saved to couchdb".format(tweetCount))

if __name__ == "__main__":

    # Database
    server = pycouchdb.Server("http://%s:%s@127.0.0.1:5984/" % ('admin', 'admin'))
    dbname = 'processed_data'
    db = server.database(dbname)

    suburbs_melb = "melbourne.json"
    suburbs_syd = "sydney.json"
    sub_dic = suburbs_shapely_processor.read_json(suburbs_melb, suburbs_syd)

    now = datetime.datetime.now()
    date_time = "{0}-{1}-{2}".format(now.year, now.month, now.day)

    # Tweeter API
    consumer_key, consumer_secret = connection.access_rest_twitter_configuration()
    auth = AppAuthHandler(consumer_key, consumer_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    # geocode for VIC and NSW
    geocode = '-33.307519,147.548481,800km'
    maxTweets = 20000000
    get_tweets(api, date_time, geocode, db, maxTweets, sub_dic)
