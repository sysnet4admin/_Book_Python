#!/bin/env python
#-*- coding: utf-8 -*-

import os

print "어떤 파이썬 서버에 연결하시겠습니까?"

while True:
    select = raw_input("연결하고자 하는 파이썬 서버를 선택하세요(1,2) : ")

    if select =="1":
        os.system("ssh 10.10.10.100")
        break
    elif select =="2":
        os.system("ssh 10.10.10.200")
        break
    else:
        print "1 또는 2가 아닌 값입니다. 정확한 값을 선택해주세요.\n"
        continue
