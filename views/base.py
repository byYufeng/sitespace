#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from utils.db.db_sqlite import *
from utils.common import trans_data_to_str

blog = Blueprint('blog', __name__)

#首页展示
@blog.route('/show')
def show_articles():
    conn = get_conn()
    sql = 'select title, text, author from articles order by id desc'
    res = select(conn, sql)
    records = [result for result in res]
    articles = [dict(title=record[0], text=record[1], author=record[2]) for record in records]
    return render_template('blog.html', articles=articles)

#检查登录状态并添加文章
@blog.route('/add', methods=['POST'])
def add_article():
    if not session.get('logged_in'):
        abort(401)
    conn = get_conn()
    title, text, author = trans_data_to_str(request.form['title'], request.form['text'], session.get('logged_in'))
    sql = 'insert into articles (title, text, author) values (?, ?, ?)'
    params = [title, text, author]
    insert(conn, sql, params)
    flash('New article has been successfully published')
    return redirect(url_for('blog.show_articles'))
