#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_p1.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/18/2018 11:04 AM
# 体育新闻第一段生成
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import re

data = dict()
path = '/home/ivy/文档/wanxiaojun/NLPCC2016Eval-Task5-AllData/sampleData/SampleData'


# 从文字直播获取比赛过程精彩瞬间，随后进行句子排序，生成相应段落
def get_process():
    # exciting_moment = ["威胁", "防守", "禁区", "没收", "队医", "远射", "换上场", "射门", "头球", "打门", "登场", "任意球", "直塞"
    #                    "单刀", "球网", "破门", "角球", "换人", "黄牌", "红牌"]
    exciting_moment = ["手球", "越位", "铲球", "拉扯", "换人", "阻挡", "抬脚过高", "犯规", "黄牌", "红牌", "扑救", "解围", "射门", "出界",
                       "进球", "得分", "点球"]
    sen_dir = dict()
    # for dir_item in os.listdir(path):
    #     if dir_item.endswith("live.csv"):
    #         print "dir_item", dir_item
    #         before_after_time = dict()
    #         scripts_time = dict()
    #         dir_item_path = os.path.join(path, dir_item)
    #         time_box = list()
    #         key_box = list()
    #         if os.path.isfile(dir_item_path):
    #             with open(dir_item_path, 'r') as f:
    #                 lines = f.readlines()
    #                 ind = 0
    #                 for line in lines:
    #                     line = line.strip().split(",")
                        # print "lineline", line[1]
                        # if line[1] == "未赛" or line[1] == "中场" or line[1] == "完赛":
    #                     if "上半场" not in line[1]:
    #                         continue
    #                     time = line[1].split(" ")[0][:3] + line[1].split(" ")[1].replace("'", "")
    #                     # print "time", time, time[3:]
    #                     # 这里以文字内容为key,但其实文字内容也有重复的，以10.live为例，实际上半场直播有133条，但key值只有131条，但本系统
    #                     # 认为影响不大，重复的key值默认被删除
    #                     scripts_time[line[0]] = time
    #                 for word in exciting_moment:
    #                     print "word1", word
    #                     for k, v in scripts_time.items():
    #                         before_after = list()
    #                         ind = 0
    #                         if word in k:
    #                             print "word2", word
    #                             ind += 1
    #                             if ind > 1:
    #                                 break
    #                             print k, v
    #                             print k
    #                             before_after.append(k)
    #                             for key, value in scripts_time.iteritems():
    #                                 # print 22222, int(v[3:])-1, value, int(v[3:])+1
    #                                 if value == v[:3] + str(int(v[3:])-1):  # 如果判断是精彩瞬间，就把此前1分钟和此后1
    #                                     # 分钟的文本结合
    #                                     # print "jjj", key, value
    #                                     before_after.append(key)
    #                                     before_after = before_after[::-1]  # 前一分钟的内容要前置，所以反转
    #                                     # 后一分钟的内容要在前一分钟内容已经找到的前提下
    #                                     if value == v[:3] + str(int(v[3:]) + 1):  # 如果判断是精彩瞬间，就把此前1分钟和此后1
    #                                         before_after.append(key)
    #                             before_after_str = "。".join(before_after)
    #                             print "before_after_str", before_after_str, v[:3] + str(int(v[3:])-1)
    #                             before_after_time[v[:3] + str(int(v[3:])-1)] = before_after_str
    # f.close()
    # return sen_dir

# 将live文本同一分钟的内容合并，这样key值就唯一
def text_preprocess():
    time_content = dict()
    for dir_item in os.listdir(path):
        time_content = dict()
        # if dir_item.endswith("live.csv"):
        if dir_item.endswith("10.live.csv"):
            print "dir_item", dir_item
            before_after_time = dict()
            scripts_time = dict()
            dir_item_path = os.path.join(path, dir_item)
            time_box = list()
            key_box = list()
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    lines = f.readlines()
                    ind = 0
                    for line in lines:
                        # print line
                        line = line.strip().split(",")
                        if "上半场" not in line[1]:
                            continue
                        # if line[1] not in time_box:
                        #     time_box.append(line[1])
                        time = int(line[1].split(" ")[1].replace("'", ""))  # 注意是int,否则底下排序就根据str排序了，1，10,11...
                        print "time", time
                        if time_content.has_key(time):
                            time_content[time] = time_content[time] + " " + line[0]
                            print 1111, time, time_content[time]
                        else:
                            time_content[time] = line[0]
                            print 2222, time, line[0]
            print len(time_content)
            time_content_sort = sorted(time_content.items(), key=lambda d: d[0])  # 根据key值排序
            print len(time_content_sort)
            print time_content_sort[0][1]
            print time_content_sort[1]
            print time_content_sort[2]
    f.close()


if __name__ == '__main__':
    # get_process()
    text_preprocess()