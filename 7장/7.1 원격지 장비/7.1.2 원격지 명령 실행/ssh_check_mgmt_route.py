#!/bin/env python
#-*- coding: utf-8 -*-

from ssh_check_cpu_status import *

def print_mgmt_status(system_type) :        # 관리 네트워크 정보를 출력하는 명령어 실행
    print "=" * 70
    print "관리 네트워크 정보 조회"
    if system_type == "Linux" :
        print_exec_cmd("hostname")
        print_exec_cmd("ip addr")
    elif system_type == "NX-OS_Switch" :
        print_exec_cmd("show hostname")
        print_exec_cmd("show interface mgmt0 ")
        print_exec_cmd("show running-config interface mgmt0")
        print_exec_cmd("show running-config | in \"ip route\"")
        
def print_route_status(system_type) :       # IP 경로 정보를 출력하는 명령어 실행
    print "=" * 70
    print "IP 경로 정보 조회"
    if system_type == "Linux" :
        print_exec_cmd("route")
    elif system_type == "NX-OS_Switch" :
        print_exec_cmd("show ip route")
           
def print_status(system_type) :             # 시스템별 CPU, 메모리, 디스크, 관리 네트워크, IP 경로 정보를 조회하고 화면에 출력
    if system_type == "Linux" or system_type == "NX-OS_Switch" :
        print_cpu_mem_disk_status(system_type)      # ssh_check_cpu_status의 함수
        print_mgmt_status(system_type)
        print_route_status(system_type)
    else :
        print "리눅스/네트워크 시스템이 아니어서 실행할 수 없습니다."
                
if __name__ == '__main__':
    # 접속 정보를 입력받고, 원격지 시스템에 접속합니다.
    (host, port_num, user, pw) = get_connection_input()
    connnected = connect(host, port_num, user, pw)
    if connnected:
        close()
    else :
        print "원격지 시스템 접속에 실패하였습니다."
    if connnected:
        # 시스템별 CPU, 메모리, 디스크 상태를 출력합니다.
        (system_type, cmd_result) = check_type()
        print_status(system_type)
