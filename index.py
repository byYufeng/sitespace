#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append('libs')
sys.path.append('../../riven/utils')

import os
from flask import Flask,__version__
from flask_bootstrap import Bootstrap
from flask import request
from flask import send_from_directory
import logging
from flask.logging import default_handler
from common import *


app = Flask(__name__)

#register app and blueprint
from views.home import home
from views.login import login
from views.personal import personal
from views.blog import blog
app.register_blueprint(home)
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(personal, url_prefix='/personal')
app.register_blueprint(blog, url_prefix='/blog')

#add logger
logger = logging.getLogger()
logging.getLogger('werkzeug').disabled = True

log_formatter = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
logging_formatter = logging.Formatter(log_formatter)
file_handler = logging.FileHandler('logs/site.log', encoding='UTF-8')
file_handler.setFormatter(logging_formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_formatter)
logger.addHandler(console_handler)


@app.after_request
def log(response):
    #request_info = print_split((get_current_datetime(), request.remote_addr, request.method, request.path, request.values), '--')
    request_info = print_split((request.remote_addr, request.method, request.path, request.values), ' - ')
    app.logger.info(request_info)
    return response


#@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


Bootstrap(app)
app.config['SECRET_KEY'] = 'dev_rainwind'

#CsrfProtect(app)
#csrf = CsrfProtect()
#csrf.init_app(app)


def main():
    debug = True
    host = '0.0.0.0'
    port = 6081 if len(sys.argv) < 2 else int(sys.argv[1])
    app.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    main()
