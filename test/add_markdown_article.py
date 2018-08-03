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
    <link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdn.bootcss.com/showdown/1.8.6/showdown.js"></script>
    <script>%s</script>
    <script>
    // 添加入库操作
    function add_info()
    {
        var form_data = $("#form_data").serialize();
        alert(form_data);
    }
    </script>
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

        <!-- 按钮触发模态框 -->
        <button class="btn btn-primary btn-lg" data-toggle="modal" data-target="#myModal">
            New
        </button>

        <!-- 模态框（Modal） -->
        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                            &times;
                        </button>
                        <h4 class="modal-title" id="myModalLabel">
                            New Article
                        </h4>
                    </div>
                    <form id="form_data">
                    <div class="modal-body">
                        <textarea id="content" style="height:600px;width:45%%;float:left" onkeyup="compile()">%s</textarea>
                        <div id="result" style="height:600px;width:45%%;float:left""></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">
                            关闭
                        </button>
                        <button type="button" onclick="add_info()" class="btn btn-primary">
                            提交更改
                        </button>
                    </div>
                    </form>
                </div><!-- /.modal-content -->
            </div><!-- /.modal -->
        </div>
    <div>
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
    app.config['SECRET_KEY'] = 'dev_fsrm'

    @app.route('/')
    def hello():
        with open('markdown/table-extension-1.0.1/src/showdown-table.js') as fin:
            showdown_table = fin.read()
        with open('markdown/markdown_template') as fin:
            content = fin.read()
        return generate_html((showdown_table, content))

    return app

if __name__ == '__main__':
    debug = True
    host = '0.0.0.0'
    port = 8001 if len(sys.argv) < 2 else sys.argv[1]
    create_app().run(debug=debug, port=port, host=host)
