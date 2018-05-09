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

import io
import sys

from mpi4py import MPI

from processing.archived import dictionary_formate

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

count_dic = dictionary_formate.return_formate()


def read_data(data, rank, size, suburbs_melb, suburbs_syd):
    """
    This method is used to read data from local files and extract the data with coordinates.
    :param filename: the file to read
    :param rank: the rank number
    :param size: the number of cores
    :return:
    """

    id = data["id"]
    rows_list = data['rows']
    count_dic = dictionary_formate.return_formate(id, suburbs_melb, suburbs_syd)

    for i in range(len(rows_list)):
        if i % size == rank:
            json_data = rows_list[i]
            count_dic = data_counter(id, json_data, count_dic)

    return count_dic

    # try:
    #     with open(filename) as f:
    #         for i, line in enumerate(f):
    #             if i % size == rank:
    #                 data = json.loads(line)
    #                 # print(data)
    #                 if data['location']['coordinates'] != None:
    #                     coordiantes = data['location']['coordinates']['coordinates']
    #                     latitude = coordiantes[1]
    #                     longitude = coordiantes[0]
    #                     # print("lat: ", latitude, "long: ", longitude)
    #                     geo_list = get_geoarea(latitude, longitude)
    #                     city = geo_list[0]
    #                     state = geo_list[1]
    #                     if state == "NSW" or state =="Victoria":
    #                         text = data["content"]["text"]
    #                         category = keyword_pool.word_pool(text)
    #                         data_counter(data, geo_list, category)
    #
    # except Exception as e:
    #     print(data)
    #     logger = logging.getLogger()
    #     logger.error(str(e))


# def get_geoarea(lat, long):
#     """
#     This method is used to get the area the coordinates belong to using geopy API
#     :param lat: lattitude
#     :param long: longtitude
#     :return: list = [suburb, city, state]
#     """
#
#     # goo_api = "AIzaSyDm9pQsJAIFk8w5yBoD49pAtBiJkPMUK0M"
#     # gmps = googlemaps.Client(key=goo_api)
#
#     geolocator = geopy.Nominatim()
#     loc = geolocator.reverse("{0}, {1}".format(lat, long))
#     print(loc, flush=True)
#
#     State = loc.address.split(",")[-3].strip()
#
#     if "Sydney" in str(loc):
#         City = "Sydney"
#     elif "Melbourne" in str(loc):
#         City = "Melbourne"
#     else:
#         City = "Others"
#
#     print(City, State)
#
#     return [City, State]

# def data_counter(data, geo_list, category):
#     city = geo_list[0]
#     state = geo_list[1]
#     sentiment = data["sentiment"]
#
#     # Update count)dic
#     count_dic[state]["Sentiment_total"][sentiment] += 1
#     count_dic[state][city]["Sentiment_total"][sentiment] += 1
#     if len(category) != 0:
#         for ele in category:
#             key = ele[0]
#             count_dic[state]["Category"][key][sentiment] += 1
#             count_dic[state][city]["Category"][key][sentiment] += 1
#
#     return count_dic

def data_counter(id, json_data, count_dic):
    if id == "case1":
        sentiment = json_data["sentiment"]
        lifestyle = json_data["lifestyle"]
        suburb = json_data["suburb"]
        for keyword in lifestyle:
            count_dic[suburb][keyword][sentiment] += 1

    return count_dic


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    suburbs_melb = "suburbs_melb.json"
    suburbs_syd = "suburbs_sydney.json"

    data = "Something read from couchdb"

    count_dic = read_data(data, rank, size, suburbs_melb, suburbs_syd)
    newData = comm.gather(count_dic, root=0)

    if rank == 0:
        result = {}
        for dic in newData:
            result = {key: dic.get(key, 0) + result.get(key, 0) for key
                      in set(dic)}
        print(result)
