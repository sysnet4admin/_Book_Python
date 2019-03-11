#!/bin/env python
#-*- coding: utf-8 -*-

from ssh_check_type import *

def print_exec_cmd(cmd) :       # 명령어 실행 결과를 화면에 출력
    print "*" * 70
    print exec_cmd(cmd)

def print_cpu_mem_disk_status(system_type) :        # 시스템별 CPU, 메모리, 디스크 상태를 출력하는 명령어 실행
    print "=" * 70
    print "CPU/메모리/디스크 정보 조회"
    if system_type == "Linux" :
        print_exec_cmd("top -b -n1")
        print_exec_cmd("free -mt")
        print_exec_cmd("ps aux --sort=-pcpu | head -5")
        print_exec_cmd("ps aux --sort=-pmem | head -5")
        print_exec_cmd("df -h")
    elif system_type == "NX-OS_Switch" :
        print_exec_cmd("show system resource")
        print_exec_cmd("show processes cpu sort | head")
        print_exec_cmd("show processes memory shared | head")
        print_exec_cmd("dir")
        
if __name__ == '__main__':
    (host, port_num, user, pw) = get_connection_input()     # 접속 정보를 입력받고, 
    connnected = connect(host, port_num, user, pw)          # 원격지 시스템에 접속합니다.
    if connnected:
        close()
    else :
        print "원격지 시스템 접속에 실패하였습니다."    
    if connnected:
        (system_type, cmd_result) = check_type()
        if system_type == "Linux" or system_type == "NX-OS_Switch" :
            print_cpu_mem_disk_status(system_type)          # 시스템별 CPU, 메모리, 디스크 상태를 출력
        else :
            print "리눅스/네트워크 시스템이 아니어서 실행할 수 없습니다."
