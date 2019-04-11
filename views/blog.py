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
#只能查看所有人可见和登陆者自己可见的
@blog.route('/show')
def show_articles():
    fields = ['id', 'title', 'text', 'author', 'text_type', 'publishtime', 'visiable']
    page_size = 10

    user = session.get('logged_in', 'Anonym') 
    conn = get_conn()
    sql = 'select %s from articles where visiable=1 or (visiable=0 and author="%s") order by id desc' % (','.join(fields), user)
    res = select(conn, sql)
    records = [result for result in res]
    articles = [dict(zip(fields, record)) for record in records]

    # 做一些枚举值的映射
    for article in articles:
        if article['visiable'] == 1:
            article['visiable'] = '所有人可见'
        if article['visiable'] == 0:
            article['visiable'] = '仅自己可见'
    print 'user:%s' % user
    for a in articles[:3]:
        print a

    # 读取markdown tutorial作为placeholder
    with open('static/markdown_template') as fin:
        markdown_template = fin.read()
    return render_template('blog.html', articles=articles, markdown_template=markdown_template)


#检查登录状态并添加/修改文章 
@blog.route('/add', methods=['POST'])
def add_article():
    #(未登录默认为匿名用户，可以发文，但固定为所有人可见，并且发布后不能编辑和删除)
    user = session.get('logged_in', 'Anonym') 
    if user == 'Anonym':
        pass
        #abort(401)
        #return redirect(url_for('blog.show_articles'))

    params = {
                'id': int(request.form.get('id')), 
                'title': request.form.get('title'),
                'text': request.form.get('text'),
                'author': user,
                'text_type':request.form.get('text_type'),
                'publishtime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'visiable': 1,
            }
    params = {k: trans_data_to_str(params.get(k)) for k in params}
    article_id = params.get('id')
    author = params.get('author')
    #print request.form

    #upsert
    conn = get_conn()
    res = select(conn, 'select * from articles where id=%s' % article_id)
    if not res:
        fields = [k for k in params if k != 'id']
        sql = 'insert into articles (%s) values (%s)' % (','.join(fields), ','.join(["?"] * len(fields)))
        #print params
        execute(conn, sql, [params[k] for k in fields])

        if author == 'Anonym':
            flash('You have not been log in!Publish as Anonym.')
        else:
            flash('New article has been successfully published')
    else:
        original_author = res[0][3]
        if author == original_author and author != 'Anonym':
            sql = 'update articles set title=?, text=?, text_type=? where id = ?'
            params = [params.get('title'), params.get('text'), params.get('text_type'), params.get('id')]
            execute(conn, sql, params)

            flash('Edit successed!')
        else:
            flash('Edit failed!You must have the right', 'error')
            

    return redirect(url_for('blog.show_articles'))


#删除文章(先检查登陆状态 只有本人和root用户可以删)
@blog.route('/del', methods=['GET', 'POST'])
def del_article():
    if not session.get('logged_in'):
        #abort(401)
        flash('Delete failed!You must log in to have the right!', 'error')
        return redirect(url_for('blog.show_articles'))

    if request.method == 'GET':
        article_id = trans_data_to_str(int(request.args.get('id')))
    elif request.method == 'POST':
        article_id = trans_data_to_str(int(request.form.get('id')))

    conn = get_conn()
    res = select(conn, 'select * from articles where id=%s' % article_id)
    original_author = res[0][3]
    user = session.get('logged_in') 

    if user == original_author or user == 'root':
        sql = 'update articles set visiable=-1 where id = ?'
        params = [article_id]
        execute(conn, sql, params)

        flash('Delete successed!')
    else:
        flash('Delete failed!You must have the right!', 'error')
            
    return redirect(url_for('blog.show_articles'))
