#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

from flask import Blueprint
from flask import url_for, send_from_directory, render_template, flash, redirect, request, session, abort
from werkzeug import secure_filename
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
#from flask_wtf.csrf import CsrfProtect

from utils.common import trans_data_to_str 
from utils.db.db_sqlite import *

home = Blueprint('home', __name__)

@home.route('/', methods=('GET', 'POST'))
def homepage():
    #custom_form.validate_on_submit()  # to get error messages to the browser
    #flash('error message', 'error')
    #flash('info message', 'info')
    #flash('debug message', 'debug')
    #flash('different message', 'different')
    #flash('uncategorized message')

    conn = get_conn()
    sql = 'select name, url, params from modules order by id asc'
    res = select(conn, sql)
    records = [result for result in res]
    modules= [dict(name=record[0], url=record[1], params=record[2]) for record in records]
    return render_template('home.html', modules=modules)

@home.route('/search', methods=('GET', 'POST'))
def search():
    #get text
    #get types
    #query...
    params = {}
    for k, v in request.form.items():
        print k, v
        params[''.join(k.split('-', 1)[1:]) if '-' in k else k] = v
    url = params.get('url','bad_url') + params.get('params','bad_parms')
    return redirect(url)

@home.route('/add_module', methods=('GET', 'POST'))
def add_module():
    if not session.get('logged_in'):
        abort(401)
    conn = get_conn()

    name, url= trans_data_to_str(request.form['name'], request.form['url'])
    if name and url:
        sql = 'insert into modules (name, url, params) values (?, ?, ?)'
        params = [name, url, '']
        insert(conn, sql, params)

        flash('New module has been added.')
    return redirect(url_for('home.homepage'))

