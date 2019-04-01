#!/usr/bin/env python
#coding:utf-8
"""
Author: fsrm
Create Time: 2019-03-29 18:45:44
Last modify: 2019-03-29 18:45:44
"""

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os, time
import traceback, json
import requests


def main():
    cookie={
            "session": ""
    }

    id_ = -1
    title = 'test_api5'
    text = \
"""
#123
##456
>hahaha
"""
    text_type = 'markdown'
    payload = {
            'id': id_,
            'title': title,
            'text': text.split('\n', 1)[1].rsplit('\n', 1)[0],
            'text_type': text_type
    }
    print add(payload, cookies=cookie)


def show():
    return requests.request('get', 'http://60.205.206.140:6080/blog/show' )


def add(payload, cookies=None):
    return requests.request('post', 'http://60.205.206.140:6080/blog/add', data=payload, cookies=cookies)


if __name__ == "__main__":
    main()
