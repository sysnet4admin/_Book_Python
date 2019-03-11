#!/bin/env python
#-*- coding: utf-8 -*-

from mylog import get_log_data
from time import sleep
import os
import sys
import datetime

# 색상 코드
errcolor_fatal= '\033[31m'
errcolor_none = '\033[0m'
errcolor_except = '\x1b[36m'

def check(file_name, search_word) :
    if os.path.exists(file_name):
        print "모니터링 시작 :", file_name
        print "대상 : ", search_word
        print "-" * 70
    else :
        print "찾으려는 파일이 없습니다 :", file_name
        
    index = 0
    while os.path.exists(file_name) :
        fp = open(file_name)
        file_data =fp.read()
        index = file_data.find(search_word, index)
        fp.close() 
        
        if index >= 0 :
            alert(search_word)    # 코드 수정
            (data, count) = get_log_data(file_data, search_word, index, 2, 2)
            print data
        else :
            sys.stdout.write("...")
            sys.stdout.flush()

        index = len(file_data)
        sleep(5)
        
# search_word 인자 추가 및 색상 적용(검색한 단어의 종류에 따라 다른 글자색을 적용하도록 수정)
def alert(search_word) :
    now = datetime.datetime.now()
    if search_word == "FATAL" :
        print errcolor_fatal + "\n", now, "심각한 문제가 발생했습니다!!" +errcolor_none
    elif search_word == "except" :
        print errcolor_except + "\n", now, "문제가 발견됐습니다!!" +errcolor_none
        
if __name__ == "__main__":
    check("/var/log/messages", "FATAL")
