#!/bin/env python
#-*- coding: utf-8 -*-

from mylog import get_log_data
from time import sleep
import os
import sys
import datetime

# 로그 전체 내용을 보고 단어의 위치를 알아봅니다.
def check(file_name, search_word) :
    if os.path.exists(file_name):
        print "모니터링 시작 :", file_name
        print "대상 : ", search_word
        print "-" * 70
    else :
        print "찾으려는 파일이 없습니다 :", file_name

    index = 0
    while os.path.exists(file_name) :
        # 파일에 찾을 단어('FATAL')가 있는지 확인
        fp = open(file_name)
        file_data =fp.read()
        index = file_data.find(search_word, index)
        fp.close()

        # 찾았다면 alert 함수로 메시지를 출력하고, 관련 로그의 앞으로 1줄, 뒤로 2줄을 출력
        # 찾지 못했다면 ...을 출력
        if index >= 0 :
            alert()
            (data, count) = get_log_data(file_data, search_word, index, 2, 2)
            print data
        else :
            sys.stdout.write("...")
            sys.stdout.flush()

        index = len(file_data)
        sleep(5)                # 5초 동안 쉬기

def alert() :
    print "\n", datetime.datetime.now(), "문제가 발생했습니다!!"

# 메인 함수
if __name__ == "__main__":
    check("/var/log/messages", "FATAL")
