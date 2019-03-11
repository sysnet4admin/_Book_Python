#!/bin/env python
#-*- coding: utf-8 -*-

from mylog import get_log_data
from time import sleep
import os
import sys
import datetime

errcolor_fatal= '\033[31m'
errcolor_none = '\033[0m'
errcolor_except = '\x1b[36m'

# 로그를 저장하기 위한 파일명(out_file_name) 인자 추가 수정
def check(file_name, search_word, out_file_name) :
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
            alert(search_word)
            (data, count) = get_log_data(file_data, search_word, index, 2, 2)
            
            # 코드 수정 시작
            out_file = open(out_file_name, "a")
            out_file.write("\n" + ("*" * 70) )
            out_file.write("\n문제(" + search_word +")가 모니터링된 시각 : ")
            out_file.write(str(datetime.datetime.now()))
            out_file.write("\n" +("-" * 70) + "\n")
            out_file.write(data)
            print "로그가 기록된 파일을 확인하세요 :", out_file_name
            out_file.close()
            # 코드 수정 완료
        else :
            sys.stdout.write("...")
            sys.stdout.flush()

        index = len(file_data)        
        sleep(5)

def alert(search_word) :
    now = datetime.datetime.now()
    if search_word == "FATAL" :
        print errcolor_fatal + "\n", now, "심각한 문제가 발생했습니다!!" +errcolor_none
    elif search_word == "except" :
        print errcolor_except + "\n", now, "문제가 발견됐습니다!!" +errcolor_none

if __name__ == "__main__":    
    check("/var/log/messages", "FATAL", "/var/log/customized_warn")
