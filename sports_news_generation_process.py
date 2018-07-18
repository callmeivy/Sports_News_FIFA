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
    for dir_item in os.listdir(path):
        if dir_item.endswith("live.csv"):
            before_after_time = dict()
            scripts_time = dict()
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip().split(",")
                        # print "lineline", line[1]
                        if line[1] == "未赛":
                            continue
                        time = line[1].split(" ")[1].replace("'", "")
                        scripts_time[line[0]] = time
                        # scripts_time.append(line[0] + "   " + time)
                        for word in exciting_moment:
                            for k, v in scripts_time.items():
                                if word in k:
                                    print k, v
                                    print k
                                    before_after.append(k)
                                    for key, value in scripts_time.items():
                                        if value == v-1 or value == v+1:  # 如果判断是精彩瞬间，就把此前1分钟和此后1分钟的文本结合
                                            before_after.append(key)
                                    before_after = before_after.join("。")
                                    before_after_time[v-1] = before_after


    f.close()
    return sen_dir


if __name__ == '__main__':
    get_process()