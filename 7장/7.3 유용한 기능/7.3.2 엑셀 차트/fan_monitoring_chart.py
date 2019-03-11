#!/bin/env python
#-*- coding: utf-8 -*-

from fan_re_any_platform import *
import time
import os
import shutil
from xlsx_chart import write_chart_xlsx

def convert_number_list(value_list) :
    num_list = []
    for val in value_list :
        if val == "na" :
            num_list.append(0)
        else :
            num_list.append(float(val))
    return num_list
    
if __name__ == "__main__":
    (args, ip, id, pw) = get_server_input()
    (count, sleep_time) = get_input()

    file_dir = "./fan"
    if not os.path.isdir(file_dir) :
        os.mkdir(file_dir)
    
    print "팬과 온도 상태 모니터링을 시작합니다.\n"
    c = 1
    file_path = ""
    file_separator = 10
    data = []
    while c <= count or count == 0:
        # 팬 정보 (상태 키, 상태 값)에 대한 리스트 추출
        (key_list, value_list) = check_fan(args)
        
        # 파일 분할 기준값에 따라 파일 이름을 계산하며 파일 기본 이름은 현재 시각을 포함
        if c % file_separator == 1 :
            now = time.localtime()
            file_path = "%s/%04d%02d%02d_%02d%02d%02d_%s_FanLog.xlsx" % (
                file_dir, now.tm_year, now.tm_mon, now.tm_mday,
                now.tm_hour, now.tm_min, now.tm_sec, ip)
            
            print "팬과 온도 상태 기록 파일 생성 : %s" % file_path
        print "[%d회] 팬과 온도 상태 기록 중..." % c
      
        # 파일 분할 기준값에 따라 새로운 파일에 작성하게 되면 헤더를 추가함  
        if c % file_separator == 1 :
            data = []
            data.append(key_list)

        # 상태 값을 추가
        num_value_list = convert_number_list(value_list)
        data.append(num_value_list)

        # 엑셀 파일에 차트를 포함하여 저장
        write_chart_xlsx(file_path, data)

        time.sleep(sleep_time)       
        c = c + 1
        
    print "%d회 팬과 온도 상태 모니터링을 모두 완료하였습니다." % count
