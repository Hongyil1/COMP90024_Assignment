"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney

 This script is used to process the saved tweets in local and input them to CouchDB
 You need to change the file name in line 64
====================================================
"""

import json

import pycouchdb
import suburbs_shapely_processor
import tweet_processer
from mpi4py import MPI


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

def read_data(filename, rank, size, sub_dic, db):
    """
    This method is used to read data from local files and extract the data with coordinates.
    :param filename: the file to read
    :param rank: the rank number
    :param size: the number of cores
    :return:
    """

    try:
        with open(filename) as f:
            for i, line in enumerate(f):
                if i % size == rank:
                    data = json.loads(line)
                    processor = tweet_processer.Proccesser()
                    text = data["full_text"]
                    hashtags = data["entities"]["hashtags"]
                    dic_tweet = processor.get_formated_tweet(data, text, hashtags, sub_dic)

                    # Save to db
                    try:
                        db.save(dic_tweet)
                    except:
                        print("Duplicated tweet")
                        pass

    except Exception as e:
        print(data)
        pass


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    suburbs_melb = "melbourne.json"
    suburbs_syd = "sydney.json"
    sub_dic = suburbs_shapely_processor.read_json(suburbs_melb, suburbs_syd)

    # Database
    # server = connection.conn_couchDB()
    server = pycouchdb.Server("http://%s:%s@127.0.0.1:5984/" % ('admin', 'admin'))
    dbname = 'processed_data'
    db = server.database(dbname)

    data_dic = read_data("tweets_REST_RAW_4_23.txt", rank, size, sub_dic, db)
