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
from argparse import Namespace

import pycouchdb

# pass the filename from the command line
# Command : python columnNumber1,columnNumber2 sourceFile targetFile State
# Such as python assignment.py 9,10,12 Untitled.csv test
parser = argparse.ArgumentParser()
# column 1, column 2...
parser.add_argument("ColumnList", default="check_string_for_empty")
parser.add_argument("SourceFile", default="check_string_for_empty")
# parser.add_argument("TargetFile", default="check_string_for_empty")
# Dataset : aurin| crime
parser.add_argument("Dataset", default="check_string_for_empty")

args: Namespace = parser.parse_args()
# filename cannot be empty
if args.ColumnList == 'check_string_for_empty' or args.SourceFile == 'check_string_for_empty' \
        or args.Dataset == 'check_string_for_empty':
    print("Please input correct parameter.")

ColumnList = args.ColumnList.split(",")
lineNumber = 0
keyList = ["suburb", "num"]
valueList = []

# server = connection.conn_couchDB()
server = pycouchdb.Server("http://%s:%s@127.0.0.1:5984/" % ('admin', 'admin'))
if args.Dataset == "aurin":
    dbname = 'aurin'
if args.Dataset == "crime":
    dbname = 'crime'
db = server.database(dbname)

list = ['south melbourne', 'brunswick west', 'carlton north', 'west melbourne', 'fitzroy north', 'south wharf',
        'southbank', 'cremorne', 'williamstown', 'kensington', 'melbourne', 'south yarra', 'fitzroy',
        'north melbourne', 'middle park', 'yarraville', 'flemington', 'albert park', 'spotswood', 'ascot vale',
        'parkville', 'northcote', 'windsor', 'brunswick', 'richmond', 'footscray', 'clifton hill', 'carlton',
        'prahran', 'east melbourne', 'newport', 'docklands', 'port melbourne', 'collingwood', 'seddon', 'maribyrnong',
        'brunswick east', 'travancore', 'princes hill', 'abbotsford']

dict = {key: 0 for key in list}
lineNumber = 0
temp = []
for line in open(args.SourceFile):
    lineNumber = lineNumber + 1
    if lineNumber > 1:
        temp = line.split(',')
        if len(ColumnList) == 1:
            tempSuburb = temp[int(ColumnList[0]) - 1].strip().lower()
            if tempSuburb in dict:
                dict[tempSuburb] += 1
        else:
            tempSuburb = temp[int(ColumnList[0]) - 1].strip().lower()
            if tempSuburb in dict:
                dict[tempSuburb] += int(ColumnList[1])

# f = open(args.TargetFile, 'w')
# f.write(str(json.dumps(dict.sorted(dict.items()))+'\n')
# sorted = sorted(dict.items(), key=lambda desc: desc[1], reverse=True)

try:
    db.save(dict)
except:
    print("Duplicated tweet")
    pass

# for key in sorted:
#     f.write(str(key))
#     f.write(',')
# f.close()

print("Parsing CSV file successfully.")
