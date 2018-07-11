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
                    name_found_tag = False
                    date_found_tag = False
                    time_found_tag = False
                    for i in range(10):  # 比赛名称、日期、时间一般出现在文字直播前十行，不需要全文读取
                        line = f.readline().strip()
                        print "line", line
                        if not name_found_tag:  # 说明比赛名称未找到
                            for name in match_names:
                                if name in line:
                                    # print "111", name, line
                                    number = (re.findall('(\d+)', line[:len(line)-4]))  # 数字抽取，意在抓取第几轮比赛
                                    print type(number)
                                    if len(number) == 0:
                                        number = 0
                                    print "111", name, number, dir_item, line
                                    name_found_tag = True
                                    break  # 比赛名称一旦找到，就跳出循环，不用再继续下文了
                        else:
                            if not date_found_tag:  # 开始查找比赛日期
                                print "line2", line
                                number = (re.findall('(\d+)', line[:len(line) - 4]))
                                if len(number) >= 2:
                                    if number[0] + "月" + number[1] + "日" in line:
                                        date = number[0] + "月" + number[1] + "日"  # 日期匹配
                                        print '222', date, line, dir_item
                                        date_found_tag = True
                                        if len(number) >= 4:
                                            if number[2] + "：" + number[3] in line:
                                                time = number[2] + "：" + number[3]  # 时间匹配，注意中文":"
                                                print "333", time, line, dir_item
                                        break
                        # else:
                        #     if not time_found_tag:
                        #



    f.close()

if __name__ == '__main__':
    get_time_match_name()
    # match_name()