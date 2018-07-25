#!/usr/bin/python
# -*- coding: utf-8 -*-
# line = 'abcdef'
# # a.replace('a','v').replace('b','g')
# line = line.replace('a','v').replace('b','g')
# print line
# a = ['1']
# a.append("2")
# print a[::-1]
# a = [1,2]
# a.append([4,5])
# print a
import os
import json
import datetime
from datetime import timedelta

import jieba.posseg as pseg
path = 'F:\工作\\2018世界杯全场战报'

sentences = sent_tokenize
for dir_item in os.listdir(path):
        dir_item_path = os.path.join(path, dir_item)
        if os.path.isfile(dir_item_path):
            with open(dir_item_path, 'r') as f:
                line = f.readline().strip()
                print(line)
                words = pseg.cut(line)
                for word, flag in words:
                    print('%s %s' % (word, flag))



# # 获取基本中英翻译
# def get_en_ch():
#     en_to_ch = list()
#     with open('en_to_ch', 'r') as f:
#         for line in f.readlines():
#             print "line", line
#             line = line.strip().split("   ")
#             en_to_ch.append(line)
#     f.close()
#     return en_to_ch


# def traslation(input_word):
#     output_word = ""
#     en_to_ch = get_en_ch()
#     input_word_lo = input_word.lower()  # 基本翻译 为小写, 注意()
#     for line in en_to_ch:
#         # 如果找不到，单词转为全部小写
#         print line[0], line[1]
#         if input_word_lo == line[0] or input_word == line[0]:
#             output_word = line[1]
#             break
#     return output_word
#
#
#
# def loadinfo():
#     for dir_item in os.listdir(path):
#         if dir_item.endswith("getMatchInfo.json"):
#             dir_item_path = os.path.join(path, dir_item)
#             if os.path.isfile(dir_item_path):
#                 with open(dir_item_path, 'r') as f:
#                     match_info = json.load(f)
#                     #  主队
#                     hometeam = match_info['MatchInfo']['HomeTeamName']
#                     #  客队
#                     awayteam = match_info['MatchInfo']['AwayTeamName']
#                     #  UTC日期
#                     dateUTC = match_info['MatchInfo']['DateUTC']
#                     #  第几轮
#                     roundname = match_info['MatchInfo']['RoundName']
#                     #  体育场
#                     stadiumname = match_info['MatchInfo']['StadiumName']
#                     #  体育场所在城市
#                     venuename = match_info['MatchInfo']['VenueName']
#                     #  UTCDate format 转为北京时间 +8hours
#                     #  2018-07-15T15:00:00.0000000Z <type 'unicode'>
#                     timearray = datetime.datetime.strptime(dateUTC[:19], "%Y-%m-%dT%H:%M:%S")
#                     timearray = timearray + timedelta(hours = 8 )
#                     #  第几轮比赛转为中文
#                     round_name = traslation(roundname)
#                     print "b4", stadiumname
#                     stadiumname = traslation(stadiumname)
#                     print stadiumname
#                     venuename = traslation(venuename)
#                     hometeam = traslation(hometeam)
#                     awayteam = traslation(awayteam)
#                     print '北京时间{0}年{1}月{2}日{3}点，俄罗斯世界杯{4}在{5}{6}打响，{7}迎战{8}。'.format(timearray.year,
#                         timearray.month, timearray.day, timearray.hour, round_name, venuename, stadiumname, hometeam, awayteam)


# if __name__ == '__main__':
#     loadinfo()