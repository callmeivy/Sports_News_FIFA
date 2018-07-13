#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/09/2018 15:53 PM
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import re

data = dict()
path = '/home/ivy/文档/wanxiaojun/NLPCC2016Eval-Task5-AllData/sampleData/SampleData'


# 读取比赛名称库
# 函数前面应当有两个空行
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
    ma = ["半决赛", "四分之一决赛", "八分之一决赛", "预赛", "淘汰赛"]
    return ma


# 获取比赛名称及时间，并根据相应的句子模板，生成句子
def get_time_match_name():
    match_names = match_name()
    sen_dir = dict()
    for dir_item in os.listdir(path):
        # print "dir_item", dir_item
        if dir_item.endswith("live.csv"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    name_found_tag = False  # 注意位置，否则一旦true了，就无法还原判断
                    date_found_tag = False  # 注意位置
                    time_found_tag = False  # 注意位置
                    # GMT_8 = False
                    for i in range(15):  # 比赛名称、日期、时间一般出现在文字直播前十行，不需要全文读取
                        line = f.readline().strip()
                        # print "line", line
                        # if not GMT_8:  # 是否北京时间
                        #     if "北京时间" in line:
                        #         GMT_8 = True
                        number = (re.findall('(\d+)', line[:len(line) - 4]))  # 数字抽取
                        # 开始查找比赛名称
                        for name in match_names:
                            if not name_found_tag:  # 一旦找到，就不用继续下文了
                                ind = 0
                                if name in line:
                                    ind += 1
                                    if ind > 3:  # 下文可能提到其他历史比赛名称，并不是该场比赛名称
                                        break
                                    if len(number) == 0:
                                        name_match = name
                                        match_number = 0
                                    if len(number) > 1:
                                        if line.index(name) < line.index(number[-1]):  # 比赛名称中的数字定在名称之后，防止提取
                                            # 出来是日期数字等
                                            name_match = name
                                            match_number = number
                                            if number[0] + '/' + number[1] in line:
                                                match_number = number[0] + '/' + number[1] + "决赛"  # 1/8决赛
                                            if number[0] + '-' + number[1] in line:
                                                match_number = number[0] + '-' + number[1]  # 15-16赛季英超联赛
                                    if len(number) == 1:
                                        name_match = name
                                        match_number = "第" + number[0] + "轮的一场焦点战"
                                        # print "ooo",match_number, type(match_number),len(match_number)
                                    for ma_ty in match_type_chinese():  # 八分之一决赛
                                        if ma_ty in line:
                                            name_match = name_match + ma_ty
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
                # print "name, number,date,time,dir_item", name_match, match_number, date, time, dir_item
                for sentence in get_sen_template():  # 句子模板套用
                    # 此处为第一段第一句
                    if sentence[1] == "p1s1":
                        # replace可连用
                        ss = (sentence[2]).replace("【", "").replace("】", "").replace("date", date).replace("time", \
                             time)
                    # 此处为第一段第二句
                    if sentence[1] == "p1s2":
                        ss_1 = (sentence[2]).replace("【", "").replace("】", "").replace("match_name", name_match + \
                                                                                       str(match_number))
                        sen_dir[dir_item] = ss + ss_1

    f.close()
    # print sen_dir.keys()
    return sen_dir


# 获取句子模板
def get_sen_template():
    sen_template = list()
    with open('sentence_template', 'r') as f:
        for line in f.readlines():
            line = line.strip().split("   ")
            sen_template.append(line)
    f.close()
    return sen_template


# 获取比赛队名，并根据相应的句子模板，生成句子
def get_match_teams():
    sent_dir = dict()
    for dir_item_mn in os.listdir(path):
        if dir_item_mn.endswith("tec.csv"):
            dir_item_path = os.path.join(path, dir_item_mn)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    for i in range(1):
                        line = f.readline().strip()
                        # 阿森纳VS切尔西，左边是主场，右边是客场
                        home_team = line.split(",")[0]
                        away_team = line.split(",")[2]
                    # print home_team, away_team, dir_item
                for sentence in get_sen_template():  # 句子模板套用
                    # 此处为第一段第三句
                    if sentence[1] == "p1s3":
                        ss_mn = (sentence[2]).replace("【", "").replace("】", "").replace("home_team", home_team)\
                            .replace("away_team", away_team)
                        # sen_mn = (ss_mn).replace("】", "")
                        # sent_mn = sen_mn.replace("home_team", home_team)
                        # sentee_mn = sent_mn.replace("away_team", away_team)
                        sent_dir[dir_item_mn] = ss_mn

    f.close()
    # print sent_dir.keys()
    return sent_dir


def generate_paragraph_1():
    a = get_time_match_name()
    b = get_match_teams()
    for dir in a.keys():
        dir_b = dir.replace("live", "tec")  # 文件名数字一样，并不完全一样
        if b.has_key(dir_b):
            print a[dir] + b[dir_b]


if __name__ == '__main__':
    # get_time_match_name()
    # match_name()
    # get_match_teams()
    # get_sen_template()
    generate_paragraph_1()