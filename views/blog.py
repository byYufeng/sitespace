#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os, time
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from utils.db.db_sqlite import *
from utils.common import trans_data_to_str


blog = Blueprint('blog', __name__)


#首页展示
@blog.route('/show')
def show_articles():
    fields = ['id', 'title', 'text', 'author', 'publishtime']

    conn = get_conn()
    sql = 'select %s from articles order by id desc' % ','.join(fields)
    res = select(conn, sql)
    records = [result for result in res]

    # 将文本的\r\n换行符替换为html的<br/>
    for i in range(len(records)):
        record = list(records[i])
        record[2] = str(record[2]).replace('\r\n', '<br/>').replace('\r', '<br/>').replace('\n', '<br/>')
        records[i] = record
    articles = [dict(zip(fields, record)) for record in records]

    # 读取markdown tutorial

    print sys.path
    with open('test/markdown/markdown_template') as fin:
        markdown_template = fin.read()
    return render_template('blog.html', articles=articles, markdown_template=markdown_template)


#检查登录状态并添加文章
@blog.route('/add', methods=['POST'])
def add_article():
    if not session.get('logged_in'):
        abort(401)

    conn = get_conn()
    title, text, author, publishtime = trans_data_to_str(request.form['title'], request.form['text'], session.get('logged_in'), time.strftime("%Y-%m-%d", time.localtime()))
    sql = 'insert into articles (title, text, author, publishtime) values (?, ?, ?, ?)'
    params = [title, text, author, publishtime]
    insert(conn, sql, params)
    flash('New article has been successfully published')
    return redirect(url_for('blog.show_articles'))
