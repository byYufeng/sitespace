#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Flask
import json

    
def generate_html(params=[]):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MarkDown</title>
    </head>
    <script src="https://cdn.bootcss.com/showdown/1.8.6/showdown.js"></script>
    <script>%s</script>
    <!--
    <script>
        (function() {
          function getCookie(name) {
            var value = "; " + document.cookie;
            var parts = value.split("; " + name + "=");
            if (parts.length == 2) return parts.pop().split(";").shift();
          }

          var ver = getCookie('version') || 'develop',
              url = 'https://rawgit.com/showdownjs/showdown/' + ver + '/dist/showdown.min.js',
              scrp = document.createElement('script');

          scrp.setAttribute("type","text/javascript");
          scrp.src = url;
          document.getElementsByTagName("head")[0].appendChild(scrp);
        })();
    </script>
    -->
    <style>
        body {
          font-family: "Helvetica Neue", Helvetica, Microsoft Yahei, Hiragino Sans GB, WenQuanYi Micro Hei, sans-serif;
         font-size: 16px;
          line-height: 1.42857143;
          color: #333;
          background-color: #fff;
        }
        ul li {
            line-height: 24px;
        }
        blockquote {
            border-left:#eee solid 5px;
            padding-left:20px;
        }
        code {
            color:#D34B62;
            background: #F9F2F4;
        }
    </style>
    <body>
    <div>
        <textarea id="content" style="height:800px;width:45%%;float:left" onkeyup="compile()">%s</textarea>
        <div id="result" style="float:left;margin-left:50px;width:45%%"></div>
    </div>
    <script type="text/javascript">
    function compile(){
        var text = document.getElementById("content").value;
        //var converter = new showdown.Converter();
        var converter = new showdown.Converter({extensions: ['table']});

        var html = converter.makeHtml(text);
        document.getElementById("result").innerHTML = html;
    }
    </script>
    <script type="text/javascript">compile()</script>
    </body>
    </html>
    ''' % params
    return html


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_yufeng'

    @app.route('/')
    def hello():

        with open('showdown.js') as fin:
            showdown = fin.read()
        with open('table-extension-1.0.1/src/showdown-table.js') as fin:
            showdown_table = fin.read()
        with open('this.md') as fin:
            content = fin.read()
        return generate_html((showdown_table, content))

    return app

if __name__ == '__main__':
    debug = False
    host = '0.0.0.0'
    port = 8001 if len(sys.argv) < 2 else sys.argv[1]
    #port = 80#6080 if len(sys.argv) < 2 else sys.argv[1]
    create_app().run(debug=debug, port=port, host=host)
