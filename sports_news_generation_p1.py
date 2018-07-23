#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_p1.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/23/2018 09:40 AM
# 体育新闻第一段生成，基于FIFA数据及CNTV文字直播内容
# 第一段模板来自C5"全场战报"
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import json
import datetime
from datetime import timedelta

path = '/home/ivy/PycharmProjects/Sports_News_FIFA/20180715'


# 获取自定义翻译词典
def get_en_ch():
    en_to_ch = list()
    with open('en_to_ch', 'r') as f:
        for line in f.readlines():
            line = line.strip().split("   ")
            en_to_ch.append(line)
    f.close()
    return en_to_ch


# 基本英文翻译成中文
def traslation(input_word):
    output_word = ""
    en_to_ch = get_en_ch()
    input_word_lo = input_word.lower()  # 基本翻译 为小写, 注意()
    for line in en_to_ch:
        # 如果找不到，单词转为全部小写
        if input_word_lo == line[0] or input_word == line[0]:
            output_word = line[1]
            break
    return output_word


#  第一段：获取球赛基本情况，并根据相应的句子模板，生成句子
def load_info():
    for dir_item in os.listdir(path):
        if dir_item.endswith("getMatchInfo.json"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    match_info = json.load(f)
                    #  主队
                    hometeam = match_info['MatchInfo']['HomeTeamName']
                    #  客队
                    awayteam = match_info['MatchInfo']['AwayTeamName']
                    #  UTC日期
                    dateUTC = match_info['MatchInfo']['DateUTC']
                    #  第几轮
                    roundname = match_info['MatchInfo']['RoundName']
                    #  体育场
                    stadiumname = match_info['MatchInfo']['StadiumName']
                    #  体育场所在城市
                    venuename = match_info['MatchInfo']['VenueName']
                    print dateUTC, type(dateUTC)
                    #  UTCDate format 转为北京时间 +8hours
                    #  2018-07-15T15:00:00.0000000Z <type 'unicode'>
                    timearray = datetime.datetime.strptime(dateUTC[:19], "%Y-%m-%dT%H:%M:%S")
                    timearray = timearray + timedelta(hours = 8 )
                    print timearray
                    #  第几轮比赛转为中文
                    print stadiumname, venuename, hometeam, awayteam
                    round_name = traslation(roundname)
                    stadiumname = traslation(stadiumname)
                    venuename = traslation(venuename)
                    hometeam = traslation(hometeam)
                    awayteam = traslation(awayteam)
                    print '北京时间{0}年{1}月{2}日{3}点，俄罗斯世界杯{4}在{5}{6}打响，{7}迎战{8}。'.format(
                        timearray.year, timearray.month, timearray.day, timearray.hour, round_name, venuename,
                        stadiumname, hometeam, awayteam)


if __name__ == '__main__':
    load_info()