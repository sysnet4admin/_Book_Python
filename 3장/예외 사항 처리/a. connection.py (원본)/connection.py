#!/bin/env python
#-*- coding: utf-8 -*-

import os

print "어떤 파이썬 서버에 연결하시겠습니까?"
select = input("연결하고자 하는 파이썬 서버를 선택하세요(1,2) : ")

if select ==1:
    os.system("ssh 10.10.10.100")
elif select ==2:
    os.system("ssh 10.10.10.200")
else:
    print "1 또는 2가 아닌 값입니다. 프로그램을 다시 시작해주세요."
