#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_p1.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/23/2018 09:40 AM
# 体育新闻第一段生成，基于FIFA数据及新浪文字直播内容（相对质量较高）
# 第一段模板来自C5"全场战报"
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import json
import datetime
from datetime import timedelta
from collections import Counter

# path = '/home/ivy/PycharmProjects/Sports_News_FIFA/20180715'
path = r'F:\工作\Fifa_2018\20180715'
# path = r'C:\Users\Administrator\PycharmProjects\Sports_News_FIFA'


# 获取自定义翻译词典
def get_en_ch():
    en_to_ch = list()
    with open('en_to_ch.txt', 'r', encoding='utf-8') as f:
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
        else:
            output_word = input_word

    return output_word


#  第一段：获取球赛基本情况，并根据相应的句子模板，生成句子
def generate_para1():
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
                    #  UTCDate format 转为北京时间 +8hours
                    #  2018-07-15T15:00:00.0000000Z <type 'unicode'>
                    timearray = datetime.datetime.strptime(dateUTC[:19], "%Y-%m-%dT%H:%M:%S")
                    timearray = timearray + timedelta(hours = 8 )
                    #  第几轮比赛转为中文
                    round_name = traslation(roundname)
                    stadiumname = traslation(stadiumname)
                    venuename = traslation(venuename)
                    hometeam = traslation(hometeam)
                    awayteam = traslation(awayteam)
                    para_1 = '北京时间{0}年{1}月{2}日{3}点，俄罗斯世界杯{4}在{5}{6}打响，{7}迎战{8}。'.format(
                        timearray.year, timearray.month, timearray.day, timearray.hour, round_name, venuename,
                        stadiumname, hometeam, awayteam)
    print(para_1)
    return para_1


#  首发
def generate_first_round_lineup():
    for dir_item in os.listdir(path):
        if dir_item.endswith("getLineups.json"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    match_info = json.load(f)
                    #  主队和客队
                    two_teams = ["HomeLineUpTeamDto", "AwayLineUpTeamDto"]
                    for team in two_teams:
                        mb_box = list()
                        single_team = match_info['MatchLineups'][team]['Pitch']
                        country = match_info['MatchLineups'][team]['OfficialName']
                        country_name = traslation(country)
                        for player in single_team:
                            # print(player['CommonName'],player['NumOrder'])
                            member = "{0}-{1}".format(traslation(player['CommonName']), player['NumOrder'])
                            mb_box.append(member)
                        line_up = "、".join(mb_box)
                        para_line_up = '首发及换人\n\n{0}首发：{1}\n'.format(country_name, line_up)
                        print(para_line_up)
    return para_line_up


#  换人及进球，不仅如此，所有的event都提取出来了
def generate_change():
    event_box = list()
    total_type = list()
    path_0 = r"F:\工作\Fifa_2018"  # 换人一般在60分钟以后，样本数据囊括不到
    days = ['20180715', '20180716']
    for day in days:
        path_1 = os.path.join(path_0, day)
        for dir_item in os.listdir(path_1):
            if dir_item.endswith("getEvents.json"):  # Events.json与getEvents.json似乎不一样，后者是总结？
                if (dir_item.startswith("2018071523")) or (dir_item.startswith("2018071600")):  # 决赛跨天，确保是决赛记录
                    dir_item_path = os.path.join(path_1, dir_item)  # isfile后需是路径，而不仅是文件名，所以需要join
                    if os.path.isfile(dir_item_path):  # isfile后需是路径，而不仅是文件名
                        with open(dir_item_path, 'r') as f:
                            match_info = json.load(f)
                            # print(match_info["MatchEvents"])
                            for one in match_info["MatchEvents"]:
                                #  事件类型
                                event_type = one["Type"]
                                # print(event_type)
                                #  事件发生分钟数
                                event_min = one["Minute"]
                                #  事件发生秒数
                                event_sec = one["Second"]
                                type_event = list()
                                type_event.append(event_type)
                                type_event.append(event_min)
                                if type_event not in event_box:
                                    # print(type_event)
                                    total_type.append(event_type)
                                    event_box.append(type_event)
                                    # Goal: 找出进球队及队员
                                    if event_type == 'Goal':
                                        playerfromid_goal = one["PlayerFromId"]
                                        teamtoid_goal = one["TeamToId"]
                                        print('ooo', event_type, search_id(playerfromid_goal), search_id(teamtoid_goal),
                                              event_min)
                                        goal_info = "第{0}分钟，{1}（{2}）".format(), )
                                        mb_box.append(member)
                                    # Substitution:换人
                                    if event_type == 'Substitution':
                                        # 被换的球员
                                        playerfromid = one["PlayerFromId"]
                                        # 换上场的球员
                                        playertoid = one["PlayerToId"]
                                        # 换人的球队
                                        teamfromid = one["TeamFromId"]
                                        print('kkk', event_type, playerfromid, playertoid, teamfromid)
    # ==========================================================
    # event_box：后一位是分钟数
    # ['Goal', 28], ['Assist', 29], ['Tackle', 29]
    # ==========================================================
    c = Counter(total_type)  # 各event发生的次数
    print(c)
    # ==========================================================
    # event日志有重复，需去重
    # 每种事件发生的次数
    # Counter({'ThrowIn': 46, 'Dribbling': 30, 'FreeKick': 25, 'Foul': 23, 'Tackle': 19, 'Shot': 17, 'AerialDuel': 14,
    #         'Save': 8, 'Corner': 8, 'Claim': 7, 'Goal': 6, 'Substitution': 5, 'BigChance': 4, 'DroppedBall': 4,
    #         'YellowCard': 3, 'Assist': 3, 'Offside': 2, 'StartTime': 2, 'VarNotification': 2, 'EndTime': 2,
    #         'TossCoin': 1, 'Punch': 1, 'EndMatch': 1})
    # ==========================================================


# 根据球队或球员id查找名字，查找getLineups，但似乎换人没有在名单里
def search_id(id):
    for dir_item in os.listdir(path):
        if dir_item.endswith("getLineups.json"):
            dir_item_path = os.path.join(path, dir_item)
            if os.path.isfile(dir_item_path):
                with open(dir_item_path, 'r') as f:
                    match_info = json.load(f)
                    #  主队和客队
                    two_teams = ["HomeLineUpTeamDto", "AwayLineUpTeamDto"]
                    for team in two_teams:
                        single_team = match_info["MatchLineups"][team]
                        team_id = single_team["ID"]
                        # print("nnn", team_id, team)
                        if str(id) == str(team_id):
                            team_name = single_team["Name"]
                            name_ch = traslation(team_name)
                        single_team_info = match_info['MatchLineups'][team]['Pitch']
                        for player in single_team_info:
                            player_id = player["ID"]
                            if str(id) == str(player_id):
                                player_name = player["CommonName"]
                                name_ch = traslation(player_name)
    return name_ch


if __name__ == '__main__':
    # generate_para1()
    # generate_first_round_lineup()
    generate_change()
    # search_id("375518")