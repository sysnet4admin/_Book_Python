#!/bin/env python
#-*- coding: utf-8 -*-

from exec_ipmi import get_ipmi
from exec_ipmi import get_server_input
import time
import re

def check_fan(args) :
    ipmi_result = get_ipmi('%s sensor' % args)
    
    # 찾으려는 데이터는 "FAN숫자_SPEED"로 시작하는 문자열입니다.
    # 찾은 데이터를 리스트로 가져옵니다.
    (key_list, value_list) = get_data_list("FAN[1-9]_SPEED.*", ipmi_result)
    
    # 찾으려는 데이터는 "FAN숫자_TACH"로 시작하는 문자열입니다.
    (key_list2, value_list2) = get_data_list("FAN[1-9]_TACH.*",ipmi_result)

    # 찾으려는 데이터는 "PSU숫자_TEMP"로 시작하는 문자열입니다.
    (key_list3, value_list3) = get_data_list("PSU[1-9]_TEMP.*",ipmi_result)

    # 찾으려는 데이터는 "FP_TEMP_SENSOR"로 시작하는 문자열입니다.
    (key_list4, value_list4) = get_data_list("FP_TEMP_SENSOR.*",ipmi_result)

    # 찾은 데이터를 리스트로 가져와서 key_list와 합칩니다.
    key_list = key_list + key_list2 + key_list3 + key_list4
    value_list = value_list + value_list2 + value_list3 + value_list4
    
    return (key_list, value_list)

def get_data_list(pattern_str, source_data) :
    str_list = re.findall(pattern_str, source_data)
    key_list = []
    value_list = []
    for str in str_list :
        array = str.split("|")  # ipmitool에서 반환한 데이터는"|"로 데이터 열이 구분돼 있습니다.
        
        if len(array) < 2 :     # 0번째 열이 상태 키, 1번째 열이 상태에 대한 값입니다.
        return ""
    
        key = array[0].strip()
        value = array[1].strip()
        key_list.append(key)
        value_list.append(value)

    return (key_list, value_list)       # (상태 키 리스트, 상태 값 리스트)의 튜플로 반환합니다.

def get_input() :
    count = input("몇 회 체크하시겠습니까? [무한대 체크는 0]:")
    if count < 0 :
        count = 0

    sleep_time = 10
    sleep_time = input("몇 초 단위로 체크하시겠습니까? [최소 30]:")

    if sleep_time < 30 :
        sleep_time = 30
    
    return (count, sleep_time)
    
if __name__ == "__main__":
    args = get_server_input()
    (count, sleep_time) = get_input()
    
    c = 1
    while c <= count or count == 0:
        print "[%d회] 팬과 온도 상태 조회 중 ..." % c
        # 팬 정보 (상태 키, 상태 값)에 대한 리스트 추출
        (key_list, value_list) = check_fan(args)

        # 첫 회에만 키 리스트를 출력하고, 그다음에는 상태 값에 관한 리스트를 출력
        if c == 1 :
            print key_list
        print value_list

        # 입력받은 대기 시간만큼 sleep
        time.sleep(sleep_time)
        c = c + 1
