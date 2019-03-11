#!/bin/env python
#-*- coding: utf-8 -*-

from exec_ipmi_set import ipmitool
from exec_ipmi_set import get_server_input
import time

def check_hw(args) :
    ipmitool( args + ' fru print | grep "Product Name"')
    ipmitool( args + ' fru print | grep "Chassis Serial"')

def check_sensor(args) :
    print "a. 전체 내용 조회"
    print "b. 팬과 온도 상태 조회"
    abc = raw_input("무엇을 실행하시겠습니까? : ")
    
    if abc =='a' :
        ipmitool( args + ' sdr list')
        ipmitool( args + ' sensor')
    elif abc =='b' :        # IPMI 명령 실행 후에 10초씩 여유를 둡니다.
        ipmitool( args + ' sensor | grep FAN"[1-9]"_SPEED')
        time.sleep(10)
        ipmitool( args + ' sensor | grep FAN"[1-6]"_TACH"[1-2]"')
        time.sleep(10)
        ipmitool( args + ' sensor | grep PSU"[1-9]"_TEMP')
        time.sleep(10)
        ipmitool( args + ' sensor | grep FP_TEMP_SENSOR')
        time.sleep(10)

def check_event_log(args) :
    print "a. 사용량 조회"
    print "b. 전체 내용 조회"
    abc = raw_input("무엇을 실행하시겠습니까? : ")
    
    if abc =='a' :
        ipmitool( args + ' sel info | grep "Percent Used"')
    elif abc =='b' :
        ipmitool( args + ' sel list > /tmp/sellist.txt')
        print '/tmp/sellist.txt에 저장하였습니다.'

def check_power(args) :
    print "a. 파워 상태 조회"
    print "b. 파워 켜기"
    print "c. 파워 끄기"
    print "d. 파워 사이클 실행"
    abc = raw_input("무엇을 실행하시겠습니까? : ")

    if abc =='a' :
        ipmitool( args + ' power status')
    elif abc =='b' :
        ipmitool( args + ' power on')
    elif abc =='c' :
        ipmitool( args + ' power off')
    elif abc =='d' :
        ipmitool( args + ' power cycle')

if __name__ == "__main__":
    args = get_server_input()

    print "1. 시스템 하드웨어 정보"
    print "2. 시스템 센서 정보"
    print "3. 시스템 이벤트 로그(SEL)"
    print "4. 시스템 파워"
    inputValue = input("어떤 정보를 조회하시겠습니까? : ")

    # if와 elif를 사용하지 않고 if만으로도 동일하게 구현 가능합니다.
    # 하지만 성능면으로는 elif를 쓰는 것이 좋습니다.
    if inputValue == 1:
        check_hw(args)
    if inputValue == 2:
        check_sensor(args)
    if inputValue == 3:
        check_event_log(args)
    if inputValue == 4:
        check_power(args)
