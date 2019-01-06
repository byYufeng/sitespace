#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os, sqlite3

database = 'mysitespace.db'

#模块被导入使用时，db路径其实是在入口模块（..）下 所以需修正到db目录
def get_conn(database = 'data/' + database):
    conn = sqlite3.connect(database)
    #conn.row_factory = sqlite3.Row
    conn.text_factory = str
    return conn


def db_init(database):
    conn = get_conn('../../data/' + database)
    with open('schema.sql', mode='r') as fin:
        cursor = conn.cursor()
        cursor.executescript(fin.read())
    conn.commit()


def select(conn, sql, params=None):
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    result = cur.fetchall()
    return result


def execute(conn, sql, params=None):
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    conn.commit()
    return True


def close_conn(conn):
    conn.close()


#表结构定义的是string，为啥取出来就成int了?!坑
def test():
    db = 'test.db'
    db_init(db)
    conn = get_conn(db)
    insert(conn, 'insert into users(username, password) values(?, ?)', ['test', '111'])
    result = select(conn, 'select * from users')
    print result

if __name__ == "__main__":
    db_init(database)
    #print 'init db ok!'

    #test()
