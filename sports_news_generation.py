#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/09/2018 15:53 PM
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import sys
import re
# from nltk.corpus import treebank

data = dict()
path = '/home/ivy/文档/wanxiaojun/NLPCC2016Eval-Task5-AllData/sampleData/SampleData'

# 读取比赛名称库
def match_name():
    match_names = list()
    with open('match_name', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            match_names.append(line)
    f.close()
    return match_names

# 读取比赛方式
def match_type_chinese():
    ma = ["决赛", "半决赛", "四分之一决赛", "八分之一决赛", "预赛", "淘汰赛"]
    return ma

# 获取比赛名称及时间
def get_time_match_name():
    match_names = match_name()
    name_numer = list()
    for dir_item in os.listdir(path):
        # print "dir_item", dir_item
        if dir_item.endswith("live.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    name_found_tag = False  # 注意位置，否则一旦true了，就无法还原判断
                    date_found_tag = False  # 注意位置
                    time_found_tag = False  # 注意位置
                    GMT_8 = False
                    for i in range(10):  # 比赛名称、日期、时间一般出现在文字直播前十行，不需要全文读取
                        line = f.readline().strip()
                        # print "line", line
                        # if not GMT_8:  # 是否北京时间
                        #     if "北京时间" in line:
                        #         GMT_8 = True
                        number = (re.findall('(\d+)', line[:len(line) - 4]))  # 数字抽取
                        # 开始查找比赛名称
                        for name in match_names:
                            if not name_found_tag:  # 一旦找到，就不用继续下文了
                                if name in line:
                                    if len(number) == 0:
                                        match_number = 0
                                    if len(number) > 1:
                                        if line.index(name) < line.index(number[-1]):  # 比赛名称中的数字定在名称之后，防止提取出来是日期数字等
                                            name_match = name
                                            match_number = number
                                            if number[0] + '/' + number[1] in line:
                                                match_number = number[0] + '/' + number[1] + "决赛"  # 1/8决赛
                                            if number[0] + '-' + number[1] in line:
                                                match_number = number[0] + '-' + number[1]  # 15-16赛季英超联赛
                                    else:
                                        name_match = name
                                        match_number = number
                                    for ma_ty in match_type_chinese():  # 八分之一决赛
                                        if ma_ty in line:
                                            name_match = name_match + ma_ty
                                    # print "111", name_match, match_number, dir_item, line
                                    name_found_tag = True
                                    # break  # name_found_tag判断就可以，无需break

                        # ===============================================================================
                        # 注意：日期与时间必须同时提。否则，日期提取完成后，有可能时间与日期在同一行，但日期已经break，
                        # 那么可能导致时间获取不到
                        # ===============================================================================
                        if type(number) == list and len(number) >= 2:
                            for index in range(len(number)-1):  # 注意“-1”，否则“list index out of range”
                                # 开始查找比赛日期
                                if not date_found_tag:
                                    if number[index] + "月" + number[index+1] + "日" in line:  # 日期匹配 匹配“2月3日”
                                        date = number[index] + "月" + number[index+1] + "日"
                                        date_found_tag = True
                                # 开始查找比赛时间
                                if not time_found_tag:
                                    if number[index] + "：" + number[index+1] in line:  # 时间匹配，注意中文":"，匹配“3：45”
                                        if len(str(number[index])) + len(str(number[index+1])) > 2:  # 避免混淆比分，如1：5
                                            time = number[index] + "：" + number[index+1]
                                            # print "333", time, line, dir_item
                                            time_found_tag = True
                                            continue
                                    if number[index] + "点" + number[index+1] in line:  # 匹配“3点45”
                                        time = number[index] + "点" + number[index+1]
                                        # print "334", time, line, dir_item
                                        time_found_tag = True
                if not date_found_tag:
                    date = "#"
                if not time_found_tag:
                    time = "#"
                print "name, number,date,time,dir_item",name_match,match_number,date,time,dir_item
    f.close()

# 获取比赛队名
def get_match_teams():
    for dir_item in os.listdir(path):
        if dir_item.endswith("tec.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    for i in range(1):
                        line = f.readline().strip()
                        teams = line.split(",")[0] + "," + line.split(",")[2]
                        print teams, dir_item


if __name__ == '__main__':
    get_time_match_name()
    # match_name()
    # get_match_teams()