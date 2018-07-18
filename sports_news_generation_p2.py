#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_p2.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/13/2018 09:15 AM
# 体育新闻第二段生成
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import re

data = dict()
path = '/home/ivy/文档/wanxiaojun/NLPCC2016Eval-Task5-AllData/sampleData/SampleData'


# 获取破门机会，并根据相应的句子模板，生成句子
def get_shooting():
    # sen_dir = dict()
    for dir_item in os.listdir(path):
        # print "dir_item", dir_item
        if dir_item.endswith("tec.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                i = 0
                with open(dir_item_path, 'r') as f:
                    for i in range(2):  # 破门机会只看前4行
                        i += 1
                        line = f.readline().strip()
                        if i == 1:
                            continue
                        line = line.split(',')
                        del line[1]
                        print "line", line
                        if line[0] > 3 and line[1] > 3:
                            print "双方均有多次破门的机会。", dir_item
                        if line[0] <= 3 and line[1] <= 3:
                            print "双方并没有获得什么破门的机会。", dir_item
    f.close()


# 获取句子模板
def get_sen_template():
    sen_template = list()
    with open('sentence_template', 'r') as f:
        for line in f.readlines():
            line = line.strip().split("   ")
            sen_template.append(line)
    f.close()
    return sen_template


# 获取每场比赛主客场名称
def get_home_away():
    for dir_item in os.listdir(path):
        if dir_item.endswith("tec.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    for i in range(1):
                        line = f.readline().strip().split(",")
                        print "lin", line[0], line[2], dir_item


# 获取主场门将表现，并根据相应的句子模板，生成句子
def get_goalkeeper():
    # sen_dir = dict()
    for dir_item in os.listdir(path):
        if dir_item.endswith("home.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                i = 0
                with open(dir_item_path, 'r') as f:
                    for i in range(2):
                        i += 1
                        line = f.readline().strip()
                        if i == 1:
                            continue
                        line = line.split(',')
                        print "line", line[2], line[13], dir_item
    f.close()


# 获取最终比分
def get_final_score():
    # sen_dir = dict()
    for dir_item in os.listdir(path):
        # print "dir_item", dir_item
        if dir_item.endswith("live.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    line = f.readlines()
                    score_final = (line[-1].split(','))[-1]
                    print "score_final", score_final
    f.close()


if __name__ == '__main__':
    # get_final_score()
    # get_shooting()
    # get_goalkeeper()
    get_home_away()