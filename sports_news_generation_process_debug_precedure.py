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


# 从文字直播抽取比赛过程精彩瞬间，将该瞬间前后一分钟的内容进行拼接，若拼接过程有重复，去重，生成相应段落
def get_process():
    # exciting_moment = ["威胁", "防守", "禁区", "没收", "队医", "远射", "换上场", "射门", "头球", "打门", "登场", "任意球", "直塞"
    #                    "单刀", "球网", "破门", "角球", "换人", "黄牌", "红牌"]
    exciting_moment = ["手球", "越位", "铲球", "拉扯", "换人", "阻挡", "抬脚过高", "犯规", "黄牌", "红牌", "扑救", "解围", "射门", "出界",
                       "进球", "得分", "点球"]
    time_content_sort = text_preprocess()
    # =======================================================================
    # time_content_sort:
    # 1 上半场比赛开始！！ 切尔西后场拿球给到边路 南安普敦边路上抢没有碰到 奥斯丁前场停球失误
    # 2 阿斯皮利奎塔边路出球 米克尔拿球给到边路 阿斯皮利奎塔右路进攻上来 禁区前沿并没有选择挑传
    # ......
    # 46 球被对方后卫碰了一下 球也是从门线上划过出了底线 切尔西这段时间形成围攻
    # =======================================================================
    time_connect_content = dict()
    content_box = list()
    for record in time_content_sort:
        connect_content = ''
        time = record[0]
        content = record[1]
        # content_box.append(content)  # 位置不对
        # print "kkk", time, content
        for word in exciting_moment:
            if word in content:
                for re in time_content_sort:
                    # print 'uuu', re[0], re[1]
                    # 1 min before
                    if re[0] == time-1:  # re[0] is timeline
                        # print 'eee', re[0], re[1]
                        if re[1] not in content_box:  # re[1] is live script
                            # print 'ppp', re[1]
                            connect_content = re[1] + "##" + content
                            content_box.append(re[1])
                            content_box.append(content)
                            # print "hhhh", re[1], re[0]
                            # print "ooo", content, time
                            # print "ggg",connect_content
                    # dict已经sorted, 另外不存在同一分钟多条直播内容的情况
                    # 1 min after
                    if re[0] == time+1:
                        if re[1] not in content_box:
                            connect_content = connect_content + "##" + re[1]
                            # print "yyy", re[1]
                            # print "zzzz", connect_content
                            content_box.append(re[1])
                            time_connect_content[time-1] = connect_content
                            break
    time_connect_content = sorted(time_connect_content.items(), key=lambda d: d[0])
    # for content in time_connect_content:
    #     print content[0], content[1]
    return time_connect_content


# 将live文本同一分钟的内容合并，这样key值就唯一
def text_preprocess():
    time_content = dict()
    for dir_item in os.listdir(path):
        time_content = dict()
        if dir_item.endswith("10.live.csv"):
            # print "dir_item", dir_item
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip().split(",")
                        if "上半场" not in line[1]:
                            continue
                        time = int(line[1].split(" ")[1].replace("'", ""))  # 注意是int,否则底下排序就根据str排序了，1，10,11...
                        # print "time", time
                        if time_content.has_key(time):
                            time_content[time] = time_content[time] + " " + line[0]
                            # print 1111, time, time_content[time]
                        else:
                            time_content[time] = line[0]
                            # print 2222, time, line[0]
            # print len(time_content)
            time_content_sort = sorted(time_content.items(), key=lambda d: d[0])  # 根据key值排序
    f.close()
    return time_content_sort


if __name__ == '__main__':
    get_process()
    # text_preprocess()