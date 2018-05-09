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

from configparser import ConfigParser

import pycouchdb


def access_stream_twitter_configuration():
    config = ConfigParser()
    config.read('configuration.ini')
    consumer_key = config.get('twitter_api_hongyi', 'consumer_key')
    consumer_secret = config.get('twitter_api_hongyi', 'consumer_secret')
    access_token = config.get('twitter_api_hongyi', 'access_token')
    access_secret = config.get('twitter_api_hongyi', 'access_secret')

    return consumer_key, consumer_secret, access_token, access_secret


def access_rest_twitter_configuration():
    config = ConfigParser()
    config.read('configuration.ini')
    consumer_key = config.get('twitter_api_jianbo', 'consumer_key')
    consumer_secret = config.get('twitter_api_jianbo', 'consumer_secret')
    # access_token = config.get('twitter_api_hongyi', 'access_token')
    # access_secret = config.get('twitter_api_hongyi', 'access_secret')

    return consumer_key, consumer_secret


def access_twitter_id_configuration():
    config = ConfigParser()
    config.read('configuration.ini')
    consumer_key = config.get('twitter_api_shalitha', 'consumer_key')
    consumer_secret = config.get('twitter_api_shalitha', 'consumer_secret')
    access_token = config.get('twitter_api_shalitha', 'access_token')
    access_secret = config.get('twitter_api_shalitha', 'access_secret')

    return consumer_key, consumer_secret, access_token, access_secret


# connect to couchDB
def conn_couchDB():
    # CouchDB configurations
    config = ConfigParser()
    config.read('configuration.ini')
    # print(config.sections())
    user = config.get('couchdb_config', 'couchdb_user')
    password = config.get('couchdb_config', 'couchdb_password')
    server = pycouchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user, password))

    return server


def get_database_name():
    config = ConfigParser()
    config.read('configuration.ini')
    db_name = config.get('couchdb_config', 'couchdb_database')
    return db_name
