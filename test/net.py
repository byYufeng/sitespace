#!/usr/bin/env python
#coding:utf-8
#Created by fsrm at 16/6/16

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests

class Net(object):
    headers = {
                "Accept":"text/html, */*; q=0.01",
                "Connection":"keep-alive",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        }

    @staticmethod
    def request(method, url, **kwargs):
        return requests.request(method, url, **kwargs) 

    @staticmethod
    def get(url, params=None, **kwargs):
        return requests.get(url, params, **kwargs)

    @staticmethod
    def post(url, data=None, **kwargs):
        return requests.post(url, data, **kwargs)


if __name__ == "__main__":
    res = Net.get('http://localhost:8001','')
    print res
    print res.content

    res = Net.get('http://localhost:8001?b=1','a=1')
    print res
    print res.content

    res = Net.post('http://localhost:8001','{a:1}')
    print res
    print res.content
