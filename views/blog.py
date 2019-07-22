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
# 读取markdown tutorial作为placeholder
with open('static/markdown_template') as fin: markdown_template = fin.read()


@blog.route('/show')
@blog.route('/show/page/<int:page>')
def show_articles(page=1):
    user = session.get('logged_in', 'Anonym') 
    page_size = 2
    page_range = 5

    fields = ['id', 'title', 'text', 'author', 'text_type', 'publishtime', 'visiable', 'sticktime']
    conn = get_conn()
    start_offset = (page - 1 ) * page_size
    count_sql = 'select count(*) from articles where visiable=1 or (visiable=0 and author="%s")' % user
    total_count = list(select(conn, count_sql))[0][0]
    total_page = 1 + (total_count - 1) / page_size
    def cal_page(current_page, page_range, total_page):
        # 当page_size是双数时还存在问题
        start_page = current_page - page_range/2
        end_page = current_page + page_range/2
        if start_page <= 0:
            end_page = end_page + (-start_page) + 1
            start_page = 1
        if end_page > total_page:
            end_page = total_page
        return [x for x in range(start_page, end_page + 1)]
    pages = cal_page(page, page_range, total_page)

    sql = 'select %s from articles where visiable=1 or (visiable=0 and author="%s")' % (','.join(fields), user)
    sql += ' order by sticktime desc, id desc'
    sql += ' limit %s, %s' % (start_offset, page_size)
    res = select(conn, sql)
    records = [result for result in res]
    articles = [dict(zip(fields, record)) for record in records]

    # 做枚举值的映射:visiable/sticktime
    for article in articles:
        if article['visiable'] == 1:
            article['visiable'] = '所有人可见'
        if article['visiable'] == 0:
            article['visiable'] = '仅自己可见'

    print 'user:%s' % user, [[x['id'], x['title']] for x in articles]

    html_params = {
            "articles": articles,
            "markdown_template": markdown_template,
            "current_page": page,
            "total_page": total_page,
            "pages": pages,
    }

    return render_template('blog.html', html_params=html_params)


# 首页展示(all articles)
# 只能查看所有人可见和登陆者自己可见的
@blog.route('/show/all')
def show_articles_all():
    fields = ['id', 'title', 'text', 'author', 'text_type', 'publishtime', 'visiable', 'sticktime']

    user = session.get('logged_in', 'Anonym') 
    conn = get_conn()
    sql = 'select %s from articles where visiable=1 or (visiable=0 and author="%s") ' % (','.join(fields), user)
    sql += 'order by sticktime desc, id desc'
    res = select(conn, sql)
    records = [result for result in res]
    articles = [dict(zip(fields, record)) for record in records]

    # 做枚举值的映射:visiable/sticktime
    for article in articles:
        if article['visiable'] == 1:
            article['visiable'] = '所有人可见'
        if article['visiable'] == 0:
            article['visiable'] = '仅自己可见'

    print 'user:%s' % user
    for a in articles[:3]:
        print a

    html_params = {
            "articles": articles,
            "markdown_template": markdown_template
    }

    return render_template('blog.html', html_params=html_params)


#检查登录状态并添加/修改文章 
@blog.route('/add', methods=['POST'])
def add_article():
    #(未登录默认为匿名用户，可以发文，但固定为所有人可见，并且发布后不能编辑和删除)
    fields = ['id', 'title', 'text', 'author', 'text_type', 'publishtime', 'visiable']
    user = session.get('logged_in', 'Anonym') 
    if user == 'Anonym':
        pass
        #abort(401)
        #return redirect(url_for('blog.show_articles'))

    #print request.form
    params = {k:request.form.get(k) for k in fields}
    article_id = int(params.get('id'))
    params['id'] = article_id
    params['author'] = user
    params['publishtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    params = {k: trans_data_to_str(params.get(k)) for k in params}

    # 做回一些枚举值的映射
    if params['visiable'] == '所有人可见':
        params['visiable'] = 1
    if params['visiable'] == '仅自己可见':
        params['visiable'] = 0

    insert_fields = [k for k in params if k != 'id']
    update_fields = [k for k in params if k not in ['id', 'author', 'publishtime']]

    #upsert
    conn = get_conn()
    res = select(conn, 'select * from articles where id=%s' % article_id)
    if not res: # insert
        sql = 'insert into articles (%s) values (%s)' % (', '.join(insert_fields), ', '.join(["?"] * len(insert_fields)))
        execute(conn, sql, [params[k] for k in insert_fields])

        if user == 'Anonym':
            flash('You have not been log in!Publish as Anonym.')
        else:
            flash('New article has been successfully published')
    else: # update
        original_author = res[0][3]
        if user == original_author and user != 'Anonym':
            sql = 'update articles set title=?, text=?, text_type=? where id = ?'
            sql = 'update articles set %s where id = %s' % (', '.join(['%s=?' % x for x in update_fields]), article_id)
            execute(conn, sql, [params[k] for k in update_fields])

            flash('Edit successed!')
        else:
            flash('Edit failed!You must have the right', 'error')

    return redirect(url_for('blog.show_articles'))


# 删除文章(先检查登陆状态 只有本人和root用户可以删)
@blog.route('/del', methods=['GET', 'POST'])
def del_article():
    if not session.get('logged_in'):
        #abort(401)
        flash('Delete failed!You must log in to have the right!', 'error')
        return redirect(url_for('blog.show_articles'))

    user = session.get('logged_in') 
    if request.method == 'GET':
        article_id = trans_data_to_str(int(request.args.get('id')))
    elif request.method == 'POST':
        article_id = trans_data_to_str(int(request.form.get('id')))

    conn = get_conn()
    res = select(conn, 'select * from articles where id=%s' % article_id)
    original_author = res[0][3]

    if user == original_author or user == 'root':
        sql = 'update articles set visiable=-1 where id = ?'
        params = [article_id]
        execute(conn, sql, params)

        flash('Delete successed!')
    else:
        flash('Delete failed!You must have the right!', 'error')
            
    return redirect(url_for('blog.show_articles'))


# 置顶文章(先检查登陆状态 只有本人和root用户可以置顶)
@blog.route('/stick', methods=['GET', 'POST'])
def stick_article():
    if not session.get('logged_in'):
        #abort(401)
        flash('Delete failed!You must log in to have the right!', 'error')
        return redirect(url_for('blog.show_articles'))

    user = session.get('logged_in') 
    if request.method == 'GET':
        article_id = trans_data_to_str(int(request.args.get('id')))
    elif request.method == 'POST':
        article_id = trans_data_to_str(int(request.form.get('id')))
    stick_status = request.form.get('stick_status')
    if stick_status == 'true':
        stick_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if stick_status == 'false':
        stick_time = ''

    conn = get_conn()
    res = select(conn, 'select * from articles where id=%s' % article_id)
    original_author = res[0][3]

    if user == original_author or user == 'root':
        sql = 'update articles set sticktime=? where id = ?'
        params = [stick_time, article_id]
        execute(conn, sql, params)

        flash('Stick successed!')
    else:
        flash('Stick article failed!You must have the right!', 'error')
            
    return redirect(url_for('blog.show_articles'))
