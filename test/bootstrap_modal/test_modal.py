#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Flask
import json

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_fsrm'

    @app.route('/')
    def hello():
        with open('test_modal.html') as fin:
            html = fin.read().strip()
        return html

    return app

if __name__ == '__main__':
    debug = False
    host = '0.0.0.0'
    port = 6666 if len(sys.argv) < 2 else sys.argv[1]
    create_app().run(debug=debug, port=port, host=host)
