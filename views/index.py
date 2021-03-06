#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import request
from flask import send_from_directory
import logging

def create_app():
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
    handler = logging.FileHandler('data/site_access.log', encoding='UTF-8')
    logging_formatter = logging.Formatter(\
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_formatter)
    app.logger.addHandler(handler)

    @app.after_request
    def log(response):
        app.logger.info('client IP: %s' % request.remote_addr)
        return response

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    Bootstrap(app)

    app.config['SECRET_KEY'] = 'dev_rainwind'

    #CsrfProtect(app)
    #csrf = CsrfProtect()
    #csrf.init_app(app)
    return app


if __name__ == '__main__':
    debug = True
    host = '0.0.0.0'
    port = 6080 #if len(sys.argv) < 2 else sys.argv[1]
    #port = 80 #if len(sys.argv) < 2 else sys.argv[1]
    create_app().run(debug=debug, port=port, host=host)
