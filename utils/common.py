#!/usr/bin/env python
#coding:utf-8
#Created by fsrm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#从request取回的数据类型为unicode, 从sqlite取回的数据类型为int等。所以需要统一
def trans_data_to_str(*datas):
    new_datas = []
    for data in datas:
        if type(data) == unicode:
            data = data.encode()
        elif type(data) == int:
            data = str(data)
        new_datas.append(data)
    if len(datas) > 1:
        return new_datas
    else:
        return new_datas[0]
