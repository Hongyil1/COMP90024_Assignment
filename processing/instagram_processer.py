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

import argparse
import datetime
import json
from argparse import Namespace

import pycouchdb
from shapely.geometry import Polygon
from shapely.geometry.point import Point

# pass the filename from the command line
# Command : python sourceFile targetFile
# Such as python assignment.py 9,10,12 Untitled.csv test

parser = argparse.ArgumentParser()
parser.add_argument("SuburbFile", default="check_string_for_empty")
parser.add_argument("SourceFile", default="check_string_for_empty")
# Dataset : instagram
parser.add_argument("Dataset", default="check_string_for_empty")

args: Namespace = parser.parse_args()
# filename cannot be empty
if args.SuburbFile == 'check_string_for_empty' or args.SourceFile == 'check_string_for_empty' \
        or args.Dataset == 'check_string_for_empty':
    print("Please input the filename.")

# server = connection.conn_couchDB()
server = pycouchdb.Server("http://%s:%s@127.0.0.1:5984/" % ('admin', 'admin*230'))
if args.Dataset == "instagram":
    dbname = 'instagram'

db = server.database(dbname)
mel_polygon = {}


# read json
def read_json(suburbs_melb):
    with open(suburbs_melb, encoding='utf-8') as f:
        geo_data = json.load(f)
        sub_list = geo_data['features']
        # print(len(geo_data['features']))
        for sub in sub_list:
            sub_name = sub["properties"]["name"]
            sub_name = sub_name.lower()
            sub_cor_list = sub["geometry"]["coordinates"][0][0]
            polygon = Polygon(sub_cor_list)
            mel_polygon[sub_name] = polygon

    # Merge two dic
    suburb_dic = {
        "Big_Mel": mel_polygon
    }

    return suburb_dic


def get_tweet_suburb(lat, long, sub_dic):
    # sub_dic = suburbs_shapely_processor.read_json(suburbs_melb, suburbs_syd)
    # lati=-37, long=144
    point_cor = Point([long, lat])
    # Detect in Mel
    for name, pol_area in sub_dic['Big_Mel'].items():
        if pol_area.contains(point_cor):
            return name
    return None


# sort the created_at into "morning", "afternoon", or "night"
def get_tweet_when(time):
    hour = int(time)
    if 4 <= hour < 12:
        return "morning"
    elif 12 <= hour < 20:
        return "afternoon"
    else:
        return "night"


# out = open(args.TargetFile, 'w')
with open(args.SourceFile, 'r') as f:
    list = {}
    next(f)
    line = f.readline()
    suburbs_melb = "melbourne.json"
    sub_dic = read_json(args.SuburbFile)
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
            instagram = json.loads(line_validate)
            doc = instagram['doc']
            if 'caption' not in doc:
                continue
            else:
                if doc["caption"] is not None:
                    if 'coordinates' in doc:
                        coordinates = doc["coordinates"]
                        if coordinates["coordinates"] is not None:
                            if coordinates["coordinates"] != [None, None]:
                                x, y = coordinates["coordinates"]
                                temp = get_tweet_suburb(float(x), float(y), sub_dic)
                                zone = get_tweet_when(datetime.datetime. \
                                    fromtimestamp(int(instagram["doc"]["created_time"])).strftime(
                                    '%H'))
                                if temp != None:
                                    data = {"text": instagram["doc"]["caption"]["text"],
                                            "created_time": zone, "suburb": temp}
                                    # out.write(str(json.dumps(data)) + '\n')
                                    try:
                                        db.save(data)
                                    except:
                                        pass
        line = f.readline()
f.close()
# out.close()
print("Parsing Instagram file successfully.")
