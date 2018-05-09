"""
===================================================
 Xiaolu Zhang 886161
 Jianbo Ma 807590
 Hongyi Lin 838776
 Xiaoyu Wang 799778
 Shalitha Weerakoon Karunatilleke 822379

 COMP90024 Cluster and Cloud Computing
 Social Media Analytics on Melbourne & Sydney
 
 This script is used to generate the suburb dictionary
====================================================
"""

import json

from shapely.geometry.polygon import Polygon

mel_polygon = {}
syd_polygon = {}


# read json
def read_json(suburbs_melb, suburbs_syd):
    print("melb: ", suburbs_melb)
    print("syd: ", suburbs_syd)
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

    with open(suburbs_syd, encoding='utf-8') as f:
        geo_data = json.load(f)
        sub_list = geo_data['features']
        # print(len(geo_data['features']))
        for sub in sub_list:
            sub_name = sub["properties"]["name"]
            sub_name = sub_name.lower()
            sub_cor_list = sub["geometry"]["coordinates"][0][0]
            polygon = Polygon(sub_cor_list)
            syd_polygon[sub_name] = polygon

    # Merge two dic
    suburb_dic = {
        "Big_Mel": mel_polygon,
        "Big_Syd": syd_polygon,
    }

    return suburb_dic
