"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney

 This script is used to process the existing tweets in local and input them to couchdb.
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

    with open(filename) as f:
        list = {}
        next(f)
        i = 0
        line = f.readline()
        while line:
            line_validate = line.strip('\n')
            try:
                if line_validate[-1] == ",":
                    line_validate = line_validate[:-1]
                elif line_validate == "]}":
                    break
            except IndexError:
                # invalid line
                break
            else:
                if i % size == rank:
                    data = json.loads(line_validate)
                    processor = tweet_processer.Proccesser()
                    text = data["doc"]["text"]
                    hashtags = data["doc"]["entities"]["hashtags"]
                    try:
                        dic_tweet = processor.get_formated_tweet(data["doc"], text, hashtags, sub_dic)
                    except:
                        pass
                    # Save to db
                    try:
                        db.save(dic_tweet)
                        print("success")
                    except:
                        print("Duplicated tweet or system error")
                        pass
            i += 1
            line = f.readline()


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

    # need to change file name
    data_dic = read_data("Tweets-100.json", rank, size, sub_dic, db)
