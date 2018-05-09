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
import json
from argparse import Namespace

# pass the filename from the command line
# Command : python columnNumber1,columnNumber2 sourceFile targetFile
# Such as python assignment.py 9,10,12 Untitled.csv test
parser = argparse.ArgumentParser()
parser.add_argument("ColumnList", default="check_string_for_empty")
parser.add_argument("SourceFile", default="check_string_for_empty")
parser.add_argument("TargetFile", default="check_string_for_empty")

args: Namespace = parser.parse_args()
# filename cannot be empty
if args.ColumnList == 'check_string_for_empty' or args.SourceFile == 'check_string_for_empty' \
        or args.TargetFile == 'check_string_for_empty':
    print("Please input the filename.")

lineNumber = 0
keyList = ["suburb", "num"]
valueList = []
list = []

with open('suburb.json', 'r') as f:
    suburb = json.load(f)

for temp in suburb["doc"]:
    list.append(temp["suburb"].upper())
dict = {key: 0 for key in list}

lineNumber = 0
numTotal = 0
temp = []
for line in open(args.SourceFile):
    lineNumber = lineNumber + 1
    if lineNumber > 1:
        temp = line.split(',')
        tempSuburb = temp[int(args.ColumnList) - 1].upper()
        if tempSuburb in dict:
            dict[tempSuburb] += 1
            numTotal += 1

f = open(args.TargetFile, 'w')
sorted = sorted(dict.items(), key=lambda desc: desc[1], reverse=True)
f.write(str(json.dumps(sorted)) + '\n')
f.write(',')
f.write(str(numTotal))
f.close()
print("Parsing CSV file successfully.")
