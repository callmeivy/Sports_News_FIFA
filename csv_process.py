# !/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_process.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/25/2018 10:30 AM
# 直播文字原始显示为一列，需要变成“script”,"score","timeline"
# 运行之前看看文件是否存在，若是，删除。否则会重复。
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os,sys
import csv
path = r'/home/ivy/PycharmProjects/Sports_News_FIFA_new/live_script'
path_0 = r'/home/ivy/PycharmProjects/Sports_News_FIFA_new/live_script/generate'


for dir_item in os.listdir(path):
    time_content = dict()
    ind = 0
    all_text = list()
    line_row=list()
    path_n = os.path.join(path, dir_item)
    if os.path.isfile(path_n):
        with open(path_n, mode="r") as f:
            reader = csv.reader(f)
            # 这里不需要readlines
            for line in reader:
                # print(line)
                all_text.append(line)
            all_text = all_text[::-1]
        path_1 = os.path.join(path_0, dir_item)
        # 判断文件是否存在，记得写绝对路径
        if os.path.exists(path_1):
            continue
        with open(path_1, 'w') as csvfile:
            writer = csv.writer(csvfile)
            count = 0
            for i in all_text:
                if len(i)>0:
                    if len(i[0])>3:
                        line_row.append(i[0])
                    if i[0].strip()=='*':
                        if len(line_row)==3:
                            writer.writerow(line_row)
                            print(222, line_row)
                            if "已结束" in line_row[2]:
                                break
                        line_row=list()
                        # writer.writerow(line_row)
