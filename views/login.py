#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Blueprint, session, flash, redirect, url_for
from flask import request, render_template
from utils.db.db_sqlite import *
from utils.common import trans_data_to_str

login = Blueprint('login', __name__)

#登录
@login.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    error = None
    if request.method == 'POST':
        conn = get_conn()
        username = request.form['username']
        password = request.form['password']
        username, password = trans_data_to_str(username, password)
        sql = 'select username, password from users where username=?'
        params = [username]
        result = select(conn, sql, params)
        print result
        if result:
            PASSWORD = trans_data_to_str(result[0][1])
            print 'PASSWORD:', PASSWORD, type(PASSWORD)
            if password == PASSWORD:
                session['logged_in'] = username
                flash('You have benn logged in...')
                #return redirect(url_for('home.homepage'))
                return redirect(url_for('blog.show_articles'))
            else:
                error = 'Invalid password'
                return render_template('sign_in.html', error=error)
        else:
            error = 'Invalid username'
            return render_template('sign_in.html', error=error)
    return render_template('sign_in.html', error=error)

#注册
@login.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        conn = get_conn()
        username = request.form['username']
        password = request.form['password']
        REpassword = request.form['REpassword']
        username, password, REpassword = trans_data_to_str(username, password, REpassword)
        if password != REpassword:
            error = "The password you typed twice is different!"
            return render_template('sign_up.html', error=error)

        #验证用户名是否存在
        sql = 'select username, password from users where username=?'
        params = [username]
        result = select(conn, sql, params)
        if result:
            error = 'The username has been signed!'
            return render_template('sign_up.html', error=error)
        else:
            sql = 'insert into users (username, password) values (?, ?)'
            params = [username, password]
            execute(conn, sql, params)

            #是否自动登录并跳转
            #checkbox没选的话无此key值
            auto_logged_in = request.form.get('auto_logged_in')
            if auto_logged_in:
                session['logged_in'] = username
                flash('Sign up successfully and auto logged in')
                return redirect(url_for('home.homepage'))
            else:
                flash('Sign up successfully! Now please logged in')
                return redirect(url_for('login.sign_in'))

    return render_template('sign_up.html', error=error)

#登出
@login.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    session.pop('logged_in', None)
    flash('You have been logged out')
    #return redirect(url_for('home.homepage'))
    return redirect(url_for('blog.show_articles'))
