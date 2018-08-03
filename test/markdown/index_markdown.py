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

def generate_markdown_template():
    content = '''
<!--  -->

<!-- 0.换行 -->
<!-- 通过行末两个空格或者一个空行换行 -->
row1
row2  
row3

row4

<!-- 1.标题 -->
# 一级标题
## 二级标题
###三级标题
#### 四级标题
##### 五级标题
###### 六级标题

<!-- 还可以在下一行使用=或-标记一级或二级标题 -->
一级标题
=
二级标题
-

<!-- 2.强调(斜体和粗体) -->
<!-- 可使用*/_两种标记 -->
*斜体* **粗体** ***粗斜体***  
_斜体_ _粗体__ ___粗斜体___

<!-- 3.分割线 -->
<!-- 可使用*/_/-三种标记 -->
***

---

___


<!-- 4.列表 -->
<!-- 4.1无序列表 可使用*/_/+三种标记 -->
* A1
* A2

- B1
- B2

+ C1
+ C2

<!-- 可通过缩进嵌套 -->
+ D1
    + D1.1
    + D1.2

<!-- 4.2有序列表 -->
1. AA 
2. BB
3. CC

<!-- 5.引用 -->
<!-- 可嵌套 -->
>老子最吊
>>老子最吊前传版

<!-- 6.超链接 -->
[百度](https://www.baidu.com)
![百度](https://www.baidu.com/img/baidu_jgylogo3.gif)

<!-- 7.表格 -->
| Name | Age | Sex |
| ---- | --- | --- |
| 11 | 22 | 33 |

<!-- 8.代码块 -->
<!-- 使用反引号表示单行或行初四个空格缩进以表示多行 -->
`print(666)`

    def main():
        print(666)

<!-- 9.转义 -->
\*嘿嘿*哈哈*哦哦

<!-- 10.其他 -->
[![GitHub issues](https://img.shields.io/github/issues/byYufeng/riven.svg)](https://github.com/byYufeng/riven/issues)
[![GitHub forks](https://img.shields.io/github/forks/byYufeng/riven.svg)](https://github.com/byYufeng/riven/network)
[![GitHub stars](https://img.shields.io/github/stars/byYufeng/riven.svg)](https://github.com/byYufeng/riven/stargazers)
'''.strip()
    return content

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_yufeng'

    @app.route('/')
    def hello():

        with open('showdown.js') as fin:
            showdown = fin.read()
        with open('table-extension-1.0.1/src/showdown-table.js') as fin:
            showdown_table = fin.read()
        content = generate_markdown_template()
        return generate_html((showdown_table, content))

    return app

if __name__ == '__main__':
    debug = False
    host = '0.0.0.0'
    port = 4321#6080 if len(sys.argv) < 2 else sys.argv[1]
    #port = 80#6080 if len(sys.argv) < 2 else sys.argv[1]
    create_app().run(debug=debug, port=port, host=host)
