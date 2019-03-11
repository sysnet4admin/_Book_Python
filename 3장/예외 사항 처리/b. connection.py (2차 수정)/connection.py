#!/bin/env python
#-*- coding: utf-8 -*-

import os

print "어떤 파이썬 서버에 연결하시겠습니까?"

while True:
    print "1. 파이썬 서버 1호기"
    print "2. 파이썬 서버 2호기"
    select = raw_input("숫자를 입력하세요 (종료는 q) : ")
    if select =="1":
        os.system("ssh 10.10.10.100")
        break
    elif select =="2":
        os.system("ssh 10.10.10.200")
        break
    elif select =="q":
        break
    else:
        print "1 또는 2가 아닌 값입니다. 정확한 값을 선택해주세요.\n"
        continue
