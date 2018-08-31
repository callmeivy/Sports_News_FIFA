#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql

import sports_news_generation_FIFA as fifa
def connect_wxremit_db():
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='',
                           database='ajaxdemo')
    cur = conn.cursor()
    # sql = ("SELECT Fcountry_name_zh"+ " FROM t_country_code"+ " WHERE Fcountry_2code='%s'" % (cc2))
    # sql = ("select * from tdt_archives;" )
    # cur.execute(sql)
    # rows = cur.fetchall()
    # print(rows)
    # cur.close()
    # conn.close()




if __name__ == '__main__':
    connect_wxremit_db()