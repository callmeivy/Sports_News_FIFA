#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/09/2018 15:53 PM
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import sys
import re
from nltk.corpus import treebank

data = dict()
path = '/home/ivy/文档/wanxiaojun/NLPCC2016Eval-Task5-AllData/sampleData/SampleData'

def match_name():
    match_names = list()
    with open('match_name', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            match_names.append(line)
    f.close()
    return match_names

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
                    for i in range(10):  # 比赛名称、日期、时间一般出现在文字直播前十行，不需要全文读取
                        line = f.readline().strip()
                        # print "line", line
                        # 开始查找比赛名称
                        if not name_found_tag:  # 一旦找到，就不用继续下文了
                            for name in match_names:
                                if name in line:
                                    number = (re.findall('(\d+)', line[:len(line)-4]))  # 数字抽取，意在抓取第几轮比赛
                                    print type(number)
                                    if len(number) == 0:
                                        number = 0
                                    print "111", name, number, dir_item, line
                                    name_found_tag = True
                                    # break  # name_found_tag判断就可以，无需break

                        # ===============================================================================
                        # 注意：日期与时间必须同时提。否则，日期提取完成后，有可能时间与日期在同一行，但日期已经break，
                        # 那么可能导致时间获取不到
                        # ===============================================================================
                        else:
                            number = (re.findall('(\d+)', line[:len(line) - 4]))
                            if len(number) >= 2:
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
                                                print "index2", index
                                                time = number[index] + "：" + number[index+1]
                                                print "333", time, line, dir_item
                                                time_found_tag = True
                                                continue
                                        if number[index] + "点" + number[index+1] in line:  # 匹配“3点45”
                                            time = number[index] + "点" + number[index+1]
                                            print "334", time, line, dir_item
                                            time_found_tag = True

    f.close()

if __name__ == '__main__':
    get_time_match_name()
    # match_name()