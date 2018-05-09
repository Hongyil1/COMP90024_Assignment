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

from harvesting import suburbs_shapely_processor
from processing import keyword_pool


def return_formate(id, suburbs_melb, suburbs_syd):
    sub_dic = suburbs_shapely_processor.read_json(suburbs_melb, suburbs_syd)
    word_dic = keyword_pool.word_dic()

    sub_key_list = sub_dic["Big_Mel"].keys() | sub_dic["Big_Syd"].keys()
    sub_key_list = list(sub_key_list)
    word_key_list = list(word_dic.keys())

    count_dic = {}
    sentiment_dic = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }
    keyword_dic = {}
    for keyword in word_key_list:
        keyword_dic[keyword] = sentiment_dic

    if id == "case1":
        for sub in sub_key_list:
            count_dic[sub] = keyword_dic
        return count_dic


if __name__ == "__main__":
    suburbs_melb = "suburbs_melb.json"
    suburbs_syd = "suburbs_sydney.json"
    count_dic = return_formate("case1", suburbs_melb, suburbs_syd)
    print(count_dic)

    # count_dic = {
    #   "VIC":{
    #
    #     "MELBOURNE CITY":{
    #
    #       "education":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "shopping":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "food":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "entertainment":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "living":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "travel":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "medical":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "sports":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "traffic":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       }
    #
    #     },
    #
    #     "MELBOURNE":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "SHEPPARTON":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "SUNBURY":{
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "WANGARATTA":{
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "BALLARAT":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "MELTON":{
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "MILDURA":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "WARRNAMBOOL":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "BENDIGO":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "WODONGA":{
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "SALE":{
    #
    #       "education": 0,
    #
    #       "shopping": 0,
    #
    #       "food": 0,
    #
    #       "entertainment": 0,
    #
    #       "living": 0,
    #
    #       "travel": 0,
    #
    #       "medical": 0,
    #
    #       "sports": 0,
    #
    #       "traffic": 0
    #
    #     },
    #
    #     "SOUTH YARRA":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "GEELONG":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0
    #
    #     },
    #
    #     "CARLTON":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #
    #
    #     },
    #
    #     "SOUTH MELBOURNE":{
    #
    #       "positive": 0,
    #
    #       "negative": 0,
    #
    #       "neutral": 0,
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "SOUTHBANK":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "CARLTON NORTH":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "DOCKLANDS":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "EAST MELBOURNE":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "FLEMINGTON":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "KENSINGTON":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "NORTH MELBOUNRE":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "PARKVILLE":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "SOUTH WHARF":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     },
    #
    #     "WEST MELBOURNE":{
    #
    #       "morning": 0,
    #
    #       "afternoon": 0,
    #
    #       "night": 0
    #
    #     }
    #
    #   },
    #
    #   "NSW":{
    #
    #     "SYDNEY CITY":{
    #
    #       "education":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "shopping":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "food":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "entertainment":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "living":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "travel":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "medical":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "sports":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       },
    #
    #       "traffic":{
    #
    #             "positive": 0,
    #
    #             "negative": 0,
    #
    #             "neutral": 0
    #
    #       }
    #
    #     },
    #
    #     "Crime":{
    #
    #       "count": 0,
    #
    #       "SYDNEY":{
    #
    #         "count": 0
    #
    #     },
    #
    #       "POTTS POINT":{
    #
    #         "count": 0
    #
    #     },
    #
    #       "SURRY HILLS":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "DARLINGHURST":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "WOOLLOOMOOLOO":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "REDFERN":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "HAYMARKET":{
    #
    #         "count": 0
    #
    #     },
    #
    #       "WATERLOO":{
    #
    #         "count": 0
    #
    #     },
    #
    #       "MOORE PARK":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "PYRMONT":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "ALEXANDRIA":{
    #
    #         "count": 0
    #
    #     },
    #
    #      "ULTIMO":{
    #
    #         "count": 0
    #
    #     },
    #
    #       "THE ROCKS":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "CHIPPENDALE":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "ERSKINEVILLE":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "ZETLAND":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "RUSHCUTTERS BAY":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "ELIZABETH BAY":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "DARLINGTON":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "DAWES POINT":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "FOREST LODGE":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "EVELEIGH":{
    #
    #         "count": 0
    #
    #     },
    #
    #     "BARANGAROO":{
    #
    #         "count": 0
    #
    #     }
    #
    #     }
    #   }
    # }
    # return count_dic
