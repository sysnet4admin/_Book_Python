#!/bin/env python
#-*- coding: utf-8 -*-

from fan_re import *
import time
import os
import shutil

def write_header(file_path, key_list) :
    fp = open(file_path, "w")
    text_data = "Count"                             # 1번째 헤더는 횟수이며 2번째부터는 키 값
    for key in key_list :
        text_data = "%s\t%s" % (text_data, key)     # 헤더를 탭(\t)으로 구분해 작성

    text_data = text_data + "\n"
    fp.write(text_data)
    fp.close()
    
def append_value(file_path, count, value_list) :
    fp = open(file_path, "a")
    text_data = str(count)                          # 1번째 값은 횟수이며 2번째부터는 상태 값
    for value in value_list :
        text_data = "%s\t%s" % (text_data, value)   # 값을 탭(\t)으로 구분해 작성

    text_data = text_data + "\n"
    fp.write(text_data)
    fp.close()

if __name__ == "__main__":
    args = get_server_input()
    (count, sleep_time) = get_input()
    
    file_dir = "./fan"
    if os.path.isdir(file_dir) :
        shutil.rmtree(file_dir)
    if not os.path.isdir(file_dir) :
        os.mkdir(file_dir)
        
    c = 1
    file_path = ""
    file_separator = 10
    while c <= count or count == 0:
        # 팬 정보(상태 키, 상태 값)에 대한 리스트 추출
        (key_list, value_list) = check_fan(args)

        # 파일 분할 기준값에 따라 파일 이름을 계산하며 파일 기본 이름은 현재 시각을 포함
        if c % file_separator == 1 :
            now = time.localtime()
            file_path = "%s/%04d%02d%02d_%02d%02d%02d_FanLog.txt" % (
                file_dir, now.tm_year, now.tm_mon, now.tm_mday,
                now.tm_hour, now.tm_min, now.tm_sec)
            
            print "팬과 온도 상태 기록 파일 생성 : %s" % file_path
        print "[%d회] 팬과 온도 상태 기록 중..." % c

       # 파일 분할 기준값에 따라 새로운 파일에 작성하게 되면 헤더를 씀
        if c % file_separator == 1 :
            write_header(file_path, key_list)
        
        # 상태 값을 헤더 아래에 작성
        append_value(file_path, c, value_list)

        time.sleep(sleep_time)
        c = c + 1
