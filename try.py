#!/usr/bin/python
# -*- coding: utf-8 -*-
# line = 'abcdef'
# # a.replace('a','v').replace('b','g')
# line = line.replace('a','v').replace('b','g')
# print line
# a = ['1']
# a.append("2")
# print a[::-1]
# a = [1,2]
# a.append([4,5])
# print a
import os
import json
import datetime
from datetime import timedelta
import csv

# path = '/home/ivy/PycharmProjects/Sports_News_FIFA/20180715'
# with open("final_live_sina2.csv", mode="r") as f:
#     reader = csv.reader(f)
#     # 这里不需要readlines
#     for line in reader:
#         print line[0]


# for dir_item in os.listdir(path):
#     para_1=generate_para1(dir_item)[0]
#     timearray=generate_para1(dir_item)[1]
#     first_shot=enerate_first_round_lineup(dir_item)
#     total_para = para_1 + '\n\n\n' + first_shot


for dir_item in os.listdir(path):
    if dir_item.endswith("getMatchInfo.json"):
