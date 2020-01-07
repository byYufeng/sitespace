#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('../libs')

import os
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['get', 'post'])
def hello():
    print 'data:',dict(request.args.items())
    print 'data:',request.get_data()
    return 'ok'


def app_init():
    app.config['SECRET_KEY'] = 'dev_rainwind'


if __name__ == '__main__':
    debug = False
    host = '0.0.0.0'
    port = 8001 if len(sys.argv) < 2 else sys.argv[1]
    app_init()
    app.run(debug=debug, port=port, host=host)
