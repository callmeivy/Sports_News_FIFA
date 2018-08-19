#!/usr/bin/python
# -*- coding: utf-8 -*-
# file: sports_news_generation_FIFA.py
# author: Ivy Jin(c.ivy.jin@foxmail.com)
# time: 07/23/2018 09:40 AM
# 体育新闻第一段生成，基于FIFA数据及新浪文字直播内容（相对质量较高）
# 第一段模板来自C5"全场战报"
# Copyright 2018 Ivy Jin. All Rights Reserved.
import os
import io
import json
import datetime
from datetime import timedelta
from collections import Counter
import pymysql
import logging

import sports_news_generation_process as process


# path = '/home/ivy/PycharmProjects/Sports_News_FIFA/20180715'
# path = r'F:\工作\Fifa_2018\20180715'
# path = r'C:\Users\Administrator\PycharmProjects\Sports_News_FIFA'
# path = r'/home/ivy/PycharmProjects/Sports_News_FIFA_backup20180726/20180715/random'
# path = r'/home/ivy/文档/Fifa_2018/20180701'
path = r'/home/ivy/文档/Fifa_2018'


# 获取自定义翻译词典
def get_en_ch():
    en_to_ch = list()
    # with open(r'en_to_ch.txt', 'r') as f:
    with open(r'en_to_ch.txt', 'r') as f:  # 'rb' is binary mode, used under linux;'r' is for win
    # with open(r'en_to_ch.txt', encoding='utf-8') as f:
    # with io.open(r'en_to_ch.txt', "r", encoding='utf-8') as f:
        for line in f.readlines():
            # print(111,line)
            # print(222, line)
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
        if line[0] in [input_word, input_word_lo]:
            output_word = line[1]
            break
        else:
            output_word = input_word

    return output_word


#  第一段：获取球赛基本情况，并根据相应的句子模板，生成句子
def generate_para1(dir_item):
    # for dir_item in os.listdir(path):
    month=''
    para_1 = ''
    # dir_item_path = os.path.join(path, dir_item)
    # print(222,dir_item)
    # 日期初始化
    timearray=datetime.datetime(2018,8,19)
    if os.path.isfile(dir_item):
        with open(dir_item, 'r') as f:
            # print(4444)
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
            print(timearray)
            #  第几轮比赛转为中文
            round_name = traslation(roundname)
            stadiumname = traslation(stadiumname)
            venuename = traslation(venuename)
            hometeam = traslation(hometeam)
            awayteam = traslation(awayteam)
            # month=timearray.month
            para_1 = '北京时间{0}年{1}月{2}日{3}点，俄罗斯世界杯{4}在{5}{6}打响，{7}迎战{8}。'.format(
                timearray.year, timearray.month, timearray.day, timearray.hour, round_name, venuename,
                stadiumname, hometeam, awayteam)
                # ============================================================================
                # para_1
                # 北京时间2018年7月15日23点，俄罗斯世界杯Final在莫斯科卢日尼基体育场打响，法国迎战克罗地亚。
                # ============================================================================
    # print(month)
    # print(para_1)
    return para_1,timearray


#  首发
def generate_first_round_lineup(dir_item):
    first_shot = list()
    # for dir_item in os.listdir(path):
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
                para_line_up = '首发及换人\n{0}首发：{1}\n'.format(country_name, line_up)
                first_shot.append(para_line_up)
                # print(para_line_up)
                # ==========================================================
                # para_line_up
                #
                # 首发及换人
                #
                # 法国首发：乌戈·洛里斯-1、Benjamin PAVARD-2、Raphael VARANE-3、Samuel UMTITI-4、保罗·博格巴-5、
                # 安东尼·格里兹曼-6、Olivier GIROUD-7、基利安·姆巴佩-8、Ngolo KANTE-9、Blaise MATUIDI-10、
                # Lucas HERNANDEZ-11
                #
                # 首发及换人
                #
                # 克罗地亚首发：达尼耶尔·苏巴西奇-1、Sime VRSALJKO-2、Ivan STRINIC-3、伊万·佩里西奇-4、Dejan LOVREN-5、
                # Ivan RAKITIC-6、Luka MODRIC-7、Marcelo BROZOVIC-8、马里奥·曼祖基奇-9、Ante REBIC-10、
                # Domagoj VIDA-11
                # ==========================================================
    return first_shot


#  换人及进球，不仅如此，所有的event都提取出来了
def generate_change(month, day, hour):
    print(month,day,hour)
    days=list()
    hour_n = ''
    day_until=''
    hour_until=''
    day_n=''
    print(hour)
    if len(str(month))==1:
        month_n="0"+str(month)
    if len(str(day))==1:
        day_n="0"+str(day)
    if len(str(hour))==1:
        hour_n="0"+str(hour)
    else:
        hour_n=str(hour)
    if int(hour_n)+2>24:
        day_until = str(day+1)
        hour_until = str(int(hour_n)+2-24)
        if len(day_until)==1:
            day_until='0'+str(day_until)
        days.append("2018"+month_n+day_n)
        days.append("2018"+month_n+day_until)
    elif int(hour_n)+2==24:
        hour_until='23'
        day_until=day_n
        days.append("2018" + month_n + day_n)
    else:
        days.append("2018" + month_n + day_n)
    event_box = list()
    total_type = list()
    # path_0 = r"F:\工作\Fifa_2018"  # 换人一般在60分钟以后，样本数据囊括不到
    # path_0 = r"/home/ivy/PycharmProjects/Sports_News_FIFA/FIFA_DATA_FEED"  # 换人一般在60分钟以后，样本数据囊括不到
    path_0 = r"/home/ivy/文档/Fifa_2018"  # 换人一般在60分钟以后，样本数据囊括不到
    # days = ['20180715', '20180716']
    gi_box = list()
    exciting_moment = ['Offside', 'Assist', 'YellowCard', 'DroppedBall', 'BigChance', 'Substitution', 'Goal', 'Corner',
                       'Save']
    exciting_min_box = list()
    # print(len(days))
    for day in days:
        if day=='201806':
            day='20180701'
        path_1 = os.path.join(path_0, day)
        for dir_item in os.listdir(path_1):
            if dir_item.endswith("getEvents.json"):  # Events.json与getEvents.json似乎不一样，后者是总结？
                # print("2018"+month_n+day_n+hour_n)
                # print("2018"+month_n+day_until+hour_until)
                if (dir_item.startswith("2018"+month_n+day_n+hour_n)) or (dir_item.startswith("2018"+month_n+day_until+hour_until)):  # 决赛跨天，确保是决赛记录
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
                                        # try:
                                        #     if len(playerfromid_goal) >4:
                                        #         print(66666666666666666)
                                        goal_info = "第{0}分钟，{1}（{2}）".format(
                                            event_min, traslation(search_id(playerfromid_goal,path_1)),
                                            traslation(search_id(teamtoid_goal,path_1)))
                                            # event_min, search_id(playerfromid_goal), search_id(teamtoid_goal))
                                        # print(goal_info)
                                        gi_box.append(goal_info)
                                        # except:
                                        #     "error"
                                    # Substitution:换人
                                    if event_type == 'Substitution':
                                        # 被换的球员
                                        playerfromid = one["PlayerFromId"]
                                        # 换上场的球员
                                        playertoid = one["PlayerToId"]
                                        # 换人的球队
                                        teamfromid = one["TeamFromId"]
                                        # print('kkk', event_type, playerfromid, playertoid, teamfromid)
                                    # 根据events提起exciting moment的时间点，从而将直播文字相关文字提取出来
                                    if event_type in exciting_moment:
                                        if event_min not in exciting_min_box:
                                            exciting_min_box.append(event_min)  # event提取的精彩瞬间时间点

    # ==========================================================
    # event_box：后一位是分钟数
    # ['Goal', 28], ['Assist', 29], ['Tackle', 29]
    # ==========================================================
    c = Counter(total_type)  # 各event发生的次数
    # print(c)
    # ==========================================================
    # event日志有重复，需去重
    # 每种事件发生的次数,如6次进球，5次换人
    # Counter({'ThrowIn': 46, 'Dribbling': 30, 'FreeKick': 25, 'Foul': 23, 'Tackle': 19, 'Shot': 17, 'AerialDuel'
    #         争顶高空球: 14,
    #         'Save': 8, 'Corner': 8, 'Claim': 7, 'Goal': 6, 'Substitution': 5, 'BigChance': 4, 'DroppedBall': 4,
    #         'YellowCard': 3, 'Assist': 3, 'Offside'直塞: 2, 'StartTime': 2, 'VarNotification': 2, 'EndTime': 2,
    #         'TossCoin': 1, 'Punch': 1, 'EndMatch': 1})
    # ==========================================================
    total_goal_info = "；".join(gi_box)
    para_goal_info = '进球信息\n\n{0}\n'.format(total_goal_info)
    # print(para_goal_info)
    # ==========================================================
    # para_goal_info
    #
    # 进球信息
    #
    # 第18分钟，马里奥·曼祖基奇（法国）；第28分钟，伊万·佩里西奇（法国）；第38分钟，安东尼·格里兹曼（克罗地亚）；第59分钟，保罗·博格巴（克罗
    # 地亚）；第65分钟，基利安·姆巴佩（克罗地亚）；第69分钟，马里奥·曼祖基奇（法国）
    #
    # ==========================================================
    return para_goal_info, exciting_min_box


# 根据球队或球员id查找名字（英文），查找getLineups，但似乎换人没有在名单里
def search_id(id,path_1):
    name_info=''
    # print(888,path_1)
    for dir_item in os.listdir(path_1):
        if dir_item.endswith("getLineups.json"):
            dir_item_path = os.path.join(path_1, dir_item)
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
                            name_info = single_team["Name"]
                        single_team_info = match_info['MatchLineups'][team]['Pitch']
                        for player in single_team_info:
                            player_id = player["ID"]
                            if str(id) == str(player_id):
                                name_info = player["CommonName"]
    return name_info


def join_para():
    para_1 = generate_para1()[0]
    date_time = generate_para1()[1]
    para_3 = "".join(process.get_process_by_event())
    first_shot = "".join(generate_first_round_lineup())
    goal = generate_change()[0]
    # print(goal)
    total_para = para_1+'\n'+ para_3+'\n\n\n'+first_shot+'\n'+goal
    # print(para_1)
    title = para_1.split("，")[2]
    print (total_para)
    return str(title), str(date_time), str(para_1),total_para


def into_mysql():
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='',
                           database='ajaxdemo')
    cur = conn.cursor()
    result = join_para()
    # print(type(result))
    # print(len(result))
    # print(result)

    # exit(0)
    try:
        cur.execute("INSERT INTO tdt_archives (title, pubdate, abstract) VALUES (%s, %s, %s)", list(result[:3]))
        cur.execute("INSERT INTO tdt_addonarticle (title, body) VALUES (%s, %s)", (result[0], result[3]))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.exception('Insert operation error')
    finally:
        cur.close()
        conn.close()


def whole_data():
    # 文件名20180701015932454_108599_getMatchInfo.json，最前面部分没有用，仅看108599_getMatchInfo.json
    first_para = ''
    first_shot = ''
    file_unique_no=''
    already = list()
    first_all = list()
    first_shot_all=list()
    days=['20180701', '20180702']
    # days=['20180701']
    # for dir_file in os.listdir(path):
    #     print (dir_file)
    for day in days:
        path_1 = os.path.join(path, day)
        # path_1 = os.path.join(path, dir_file)
        for dir_item in os.listdir(path_1):
            if dir_item.endswith("getMatchInfo.json"):
                # print(999, dir_item)
                dir = os.path.join(path_1, dir_item)
                if dir_item.split("_")[1] not in already:
                    print(111, dir)
                    first_para = generate_para1(dir)[0]
                    print("first_para",first_para)
                    first_all.append(first_para)
                    file_unique_no = dir_item.split("_")[1]
                    already.append(file_unique_no)
                # print(111,first_para)
                    timearray = generate_para1(dir)[1]
                    # print(5555,timearray)
                    month=timearray.month
                    day=timearray.day
                    hour=timearray.hour
                    goal = generate_change(month,day,hour)[0]
                    # print(goal)
            if dir_item.endswith("getLineups.json"):
                if file_unique_no in dir_item:
                    if first_shot not in first_shot_all:
                        dir_1 = os.path.join(path_1, dir_item)
                        first_shot = "".join(generate_first_round_lineup(dir_1))
                        first_shot_all.append(first_shot)
                        # print(222, first_shot)
            if len(first_para)>0 and len(first_shot)>0:
                total_para = first_para + '\n\n\n' + first_shot+'\n'+goal
                # print (total_para)

if __name__ == '__main__':
    # generate_para1()
    # generate_first_round_lineup()
    # generate_change()
    # search_id("375518")
    # join_para()
    # into_mysql()
    whole_data()