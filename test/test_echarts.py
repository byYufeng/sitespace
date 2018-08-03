#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Flask
import json

def get_data():
    data = \
    {
        "2017-08-15": 913214,
        "2017-08-16": 4343243,
        "2017-08-17": 1243243,
    }
    return data
    
def generate_html(title, x, y):
    html = '''
    <html>
    <head>
        <meta charset="utf-8">
        <title>ECharts</title>
        <!-- 引入 echarts.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/3.6.2/echarts.common.min.js"></script>
    </head>
    <body>
        <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
        <div id="main" style="width: 600px;height:400px;"></div>
        <script type="text/javascript">
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main'));

            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '%s',
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    //data:['']
                },
                grid: {
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    data: %s
                },
                yAxis: {
                    type: 'value',
                    data: ['counts']
                },
                series: [
                    {
                        name:'Data counts',
                        type:'line',
                        //step: 'middle',
                        data: %s
                    }

                ]
            };


            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        </script>
    </body>
    </html>
    ''' % (title, x, y)
    return html


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_yufeng'

    @app.route('/')
    def hello():
        #return 'hello thank you for votes! please enter your number:<input></input>'
        title = 'data_show'
        d = get_data()
        x, y = [k for k in d], [d[k] for k in d]
        x, y = json.dumps(x), json.dumps(y)
        print x,y
        return generate_html(title, x ,y)

    return app

if __name__ == '__main__':
    debug = False
    host = '0.0.0.0'
    port = 8888#6080 if len(sys.argv) < 2 else sys.argv[1]
    #port = 80#6080 if len(sys.argv) < 2 else sys.argv[1]
    create_app().run(debug=debug, port=port, host=host)
