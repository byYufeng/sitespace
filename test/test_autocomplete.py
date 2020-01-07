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

def main():
    debug = True
    host = '0.0.0.0'
    port = 8001 if len(sys.argv) < 2 else sys.argv[1]
    app_init()
    app.run(debug=debug, port=port, host=host)


#此代码因输入法不同可能存在bug：keyup触发之后无法再绑定autocomplete
demo = """
<!DOCTYPE html>
<html>
<head>
    <title>搜索输入框demo</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <style type="text/css">
      .ui-com {
        font-size: 14px;
        max-height: 100px;
        max-width: 172px;
        overflow-y: auto;
        /* 防止水平滚动条 */
        overflow-x: hidden;
      }
    </style>  
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>  
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>  
</head>
<body>
<nav class="navbar navbar-default" role="navigation">
    <div class="container-fluid"> 
    <div class="navbar-header">
        <a class="navbar-brand" href="#">搜索自动提示</a>
    </div>
    <div class="navform">
        <form class="navbar-form navbar-left" role="search">       
            <input id="search_kw" type="text" name="myname" class="form-control ui-com"  placeholder="请输入IOC关键字">
        </form>
    </div>
    </div>
</nav>
</body>
<script type="text/javascript">
$(document).ready(function () {  
    var autocomplete_url = "/search";  
    search_input_id="search_kw";

    /*    
    //页面加载时初始化绑定，适用于不敏感的小数据量
    $.ajax({
        url: autocomplete_url,
        data: {"skeyword": ""},
        success: function (data) {
            insertOptions(data);
        }
    });
    */

    //每次输入均查询请求，适用于大数据量，并且较为保密
    //因为是在触发按键后才绑定事件，需要再次触发才能生效。需寻求解决办法
    var result = new Array();  
    $("#"+search_input_id).autocomplete({  
        source: result  
    });  
    $("#"+search_input_id).keyup(function(){  
        var skeyword = $("#"+search_input_id).val();
        $.ajax({
            url: autocomplete_url,
            data: {"skeyword": skeyword},
            success: function (data) {
                result = new Array();
                $.each($.parseJSON(data), function(i, item){  
                    result.push(item);  
                });  
            }
        });
    });  

});  
</script>
</html>
"""

@app.route('/')
def hello():
    return demo

@app.route('/search/', methods=['GET', 'POST'])
def search():
    #data = request.get_data()
    word = request.args.get("skeyword")
    print word
    l = ["a11", "b12", "c13"]
    #l = [["a11",213], ["b12",231], ["c13",2131]] # error
    return json.dumps(filter(lambda x: word in x, l))

def app_init():
    app.config['SECRET_KEY'] = 'dev_rainwind'


if __name__ == '__main__':
    main()
