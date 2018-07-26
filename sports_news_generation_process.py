#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_p1.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/25/2018 10:30 AM
# 体育新闻精彩片段生成，根据文字直播内容
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import csv
import re

data = dict()
# path = '/home/ivy/文档/wanxiaojun/NLPCC2016Eval-Task5-AllData/sampleData/SampleData'
path = r'C:\Users\Administrator\PycharmProjects\Sports_News_FIFA'


# 获取句子模板
def get_sen_template():
    sen_template = list()
    with open('sentence_template', 'r') as f:
        for line in f.readlines():
            line = line.strip().split("   ")
            sen_template.append(line)
    f.close()
    return sen_template


# 从文字直播抽取比赛过程精彩瞬间，将该瞬间前后一分钟的内容进行拼接，若拼接过程有重复，去重，生成相应段落
def get_process():
    exciting_moment = ["手球", "越位", "铲球", "拉扯", "换人", "阻挡", "抬脚过高", "犯规", "黄牌", "红牌", "扑救", "解围", "射门", "出界",
                       "进球", "得分", "点球"]
    time_connect_content = dict()
    content_box = list()
    time_content_sort = text_preprocess()
    # =======================================================================
    # time_content_sort:
    # 1 上半场比赛开始！！ 切尔西后场拿球给到边路 南安普敦边路上抢没有碰到 奥斯丁前场停球失误
    # 2 阿斯皮利奎塔边路出球 米克尔拿球给到边路 阿斯皮利奎塔右路进攻上来 禁区前沿并没有选择挑传
    # ......
    # 46 球被对方后卫碰了一下 球也是从门线上划过出了底线 切尔西这段时间形成围攻
    # =======================================================================
    count = 0
    for record in time_content_sort:
        connect_content = ''
        time = record[0]
        content = record[1]
        for word in exciting_moment:
            if word in content:
                for re in time_content_sort:
                    # ======================================================
                    # 第一种方式，将含“精彩标志”的句子，前后一分钟的文本做连接
                    # ======================================================
                    # 前后1分钟文本内容拼接，避免重复拼接
                    # 1 min before
                    # 不是加时赛
                    # if time == int(time):
                    #     if re[0] == time-1:  # re[0] is timeline
                    #         if re[1] not in content_box:  # re[1] is live script
                    #             connect_content = re[1] + "##" + content
                    #             content_box.append(re[1])  # 将1分钟前的文本放入
                    #             content_box.append(content)  # 将本条文本放入
                    #     # dict已经sorted, 另外不存在同一分钟多条直播内容的情况
                    #     # 1 min after
                    #     if re[0] == time+1:
                    #         if re[1] not in content_box:
                    #             connect_content = connect_content + "##" + re[1]
                    #             content_box.append(re[1])  # 将1分钟后的文本放入
                    #             count += 1
                    #             time_connect_content[time-1] = connect_content
                    #             break
                    # else:  # 加时赛
                    #     if re[0] == time-0.1:  # 0.1
                    #         if re[1] not in content_box:  # re[1] is live script
                    #             connect_content = re[1] + "##" + content
                    #             content_box.append(re[1])  # 将1分钟前的文本放入
                    #             content_box.append(content)  # 将本条文本放入
                    #     # dict已经sorted, 另外不存在同一分钟多条直播内容的情况
                    #     # 1 min after
                    #     if re[0] == time+0.1:  # 0.1
                    #         if re[1] not in content_box:
                    #             connect_content = connect_content + "##" + re[1]
                    #             content_box.append(re[1])  # 将1分钟后的文本放入
                    #             count += 1
                    #             time_connect_content[time-1] = connect_content
                    #             break
                    # ======================================================
                    # ======================================================
                    # 第二种方式，将含“精彩标志”的句子单独拿出来
                    # ======================================================
                    time_connect_content[time] = content
                    # ======================================================
    time_connect_content_sort = sorted(time_connect_content.items(), key=lambda d: d[0])
    # if len(time_connect_content_sort)
    for data in time_connect_content_sort:
        para_3 = '第{0}分钟，{1}。\n'.format(
            data[0], data[1])
        print(para_3)


# 将live文本同一分钟的内容合并，这样key值就唯一
def text_preprocess():
    time_content = dict()
    time_content_sort = list()
    for dir_item in os.listdir(path):
        time_content = dict()
        ind = 0
        if os.path.isfile('01.csv'):
            with open("01.csv", "r") as f:
                reader = csv.reader(f)
                # 这里不需要readlines
                for line in reader:
                    # print(line)
                    ind += 1
                    if ind < 2:
                        continue
                    if line[2] == "已结束":  # python3中似乎不能用in string
                        continue
                    try:
                        time = int(line[2].replace("'", ""))  # 注意是int,否则底下排序就根据str排序了，1，10,11...
                    except:
                        # 加赛，45+1---->45.1
                        time = float(line[2].replace("+", ".").replace("'", ""))
                    # 文本预处理，主要是标点符号规整
                    live_script = line[0].replace("！", "")
                    # 同一分钟直播内容合并
                    if time in time_content:
                        time_content[time] = time_content[time] + "，" + live_script
                    else:
                        time_content[time] = live_script

                    time_content_sort = sorted(time_content.items(), key=lambda d: d[0])  # 根据key值排序

        f.close()
    # for i in time_content_sort:
    #     print(i[0], i[1])
    return time_content_sort


if __name__ == '__main__':
    # text_preprocess()
    get_process()