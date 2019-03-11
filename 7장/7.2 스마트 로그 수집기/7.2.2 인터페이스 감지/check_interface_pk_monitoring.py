#!/bin/env python
#-*- coding: utf-8 -*-

from check_interface_pk import get_user_input
from check_interface_pk import get_interface_data_list
from check_interface_pk import get_status
from time import sleep
from cli import cli
import sys
import time
import os

def monitoring(interface, packet, err_type, err_chk_range, log_type):   # 특정 interface, 패킷 타입, 에러 코드 타입으로 얻은 상태 값이 변화하는지 모니터링
    past_status_list = {}
    while True :
        alert_list = []
        interface_data_list = get_interface_data_list(interface)
        for (interface_name, interface_data) in interface_data_list :
            current_status = get_status(interface_data, packet, err_type)

            # 맨 처음 실행했을 때는 과거 데이터가 없으므로 현재 데이터로 대체
            past_status_exist = False
            for key in past_status_list.keys() :        # past_status_list에서 키가 인터페이스 이름인 데이터가 적재된 적이 있는지 확인
                if key == interface_name :
                    past_status_exist = True
            if past_status_exist == False :             # 과거 데이터가 없으면 현재 데이터로 대체
                past_status_list[interface_name] = current_status

            # 현재 상태(current_status)와 과거 상태(past_status)를 비교해서 상태 값 변화를 확인
            past_status = past_status_list[interface_name]
            for err_key in current_status :             # current_status는 {에러 코드:상태 값}을 포함합니다.
                current = current_status[err_key]       # 현재 상태 값
                past = past_status[err_key]             # 과거 상태 값
                gap = current - past                    # 현재와 과거의 상태 값 변화 확인
                if gap >= err_chk_range :               # 상태 변화가 지정한 값보다 큰지 확인                    
                    alert_list.append((interface_name, err_key, gap, past, current))    # 문제가 되는 에러 코드 확인 -> alert_list에 문제가 되는 내용 적재
            past_status_list[interface_name] = current_status   # 과거/현재 데이터를 비교한 다음에는 현재 데이터를 과거 데이터로 변경

        # 문제가 되는 에러 코드가 있다면 상태 변화를 화면에 출력하고 로그 작성
        if len(alert_list) > 0:
            print "\n*********************[상태 변화]*********************"
        for (interface_name, err_key, gap, past, current) in alert_list :
            print "[%s] %s : %i 만큼 변화하였습니다. (%i->%i)" % (
                interface_name, err_key, gap, past, current)
        if len(alert_list) > 0:
            print "-"*55
            write_logs(log_type, interface)
       
        sys.stdout.write ("...")
        sys.stdout.flush()
        sleep(5)

def write_file(default_log_name, data) :                # 로그 파일을 디렉터리별로 작성하는 함수입니다. 인자인 default_log_name은 명령어 종류가 넘어옵니다.
    now = time.localtime()
    dir_path = "/bootflash/%s" % default_log_name       # bootflash 하위에 디렉터리를 작성합니다.
    if os.path.isdir(dir_path) == False :
        os.mkdir(dir_path)
    str_date = "%04d%02d%02d_%02d%02d%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday,now.tm_hour, now.tm_min, now.tm_sec)
    log_name = "/bootflash/%s/%s_%s.log" % (
        default_log_name, default_log_name, str_date)   # 날짜, 시각을 포함한 파일을 생성합니다.

    log_file = open(log_name, "w")
    log_file.write(data)
    log_file.close()
    print "작성된 로그 :", log_name                      # 로그 작성이 완료되면 파일 경로를 출력.

def write_logs(log_type, interface) :           # 사용자가 선택한 타입의 로그 작성
    if log_type == 'a' or log_type == "d" :
        write_file("sh_int_ethernet", cli("show interface ethernet %s" % interface))
    if log_type == 'b'or log_type == "d" :
        write_file("sh_int_ethernet_detail",
              cli("show interface ethernet %s transceiver details" % interface))
    if log_type == 'c' or log_type == "d" :
        write_file("sh_tech_support_pktmgr", cli("show tech-support pktmgr"))

if __name__ == "__main__":
    (interface, packet, err_type, err_chk_range, log_type) = get_user_input()
    monitoring(interface, packet, err_type, err_chk_range, log_type)
