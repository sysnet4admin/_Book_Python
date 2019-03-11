#!/bin/env python
#-*- coding: utf-8 -*-

from ssh_check_type import *
import os
import time
from datetime import datetime

def save_exec_cmd(cmd, file_name) :     # 명령어를 실행한 결과를 파일로 저장
    data = exec_cmd(cmd)
    file_path = "%s/%s" %(dir_name, file_name)
    f = open(file_path, "w")
    f.write(data)
    f.close()
    print "파일 저장 완료 : ", os.path.abspath(file_path)

def get_date_str() :            # 현재 날짜를 문자열 yyyyMMdd_HHmmss 형식으로 반환
    now = time.localtime()
    return ("%04d%02d%02d_%02d%02d%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday,
        now.tm_hour, now.tm_min, now.tm_sec))

def save_cpu_mem_disk_status(system_type) :         # CPU, 메모리, 디스크 상태를 저장하는 명령어 실행
    def_file_name = "%s_result.txt" % get_date_str()
    if system_type == "Linux" :
        save_exec_cmd("top -b -n1", "top_%s"%def_file_name)
        save_exec_cmd("free -mt", "free_%s"%def_file_name)
        save_exec_cmd("ps aux --sort=-pcpu | head -5", "ps_aux_pcpu_%s"%def_file_name)
        save_exec_cmd("ps aux --sort=-pmem | head -5", "ps_aux_pmpm_%s"%def_file_name)
        save_exec_cmd("df -h", "df_%s"%def_file_name)
    elif system_type == "NX-OS_Switch" :
        save_exec_cmd("show system resource", "sys_resource_%s"%def_file_name)
        save_exec_cmd("show processes cpu sort | head", "show_cpu_%s"%def_file_name)
        save_exec_cmd("show processes memory shared | head", "show_mem_%s"%def_file_name)
        save_exec_cmd("dir", "dir_%s"%def_file_name)

def save_mgmt_route_status(system_type) :           # 관리 네트워크 정보를 저장하는 명령어 실행
    def_file_name = "%s_result.txt" % get_date_str()
    if system_type == "Linux" :
        save_exec_cmd("hostname", "hostname_%s"%def_file_name)
        save_exec_cmd("ip addr", "ip_addr_%s"%def_file_name)
    elif system_type == "NX-OS_Switch" :
        save_exec_cmd("show hostname", "show_hostname_%s"%def_file_name)
        save_exec_cmd("show interface mgmt0","show_int_mgmt_%s"%def_file_name)
        save_exec_cmd("show running-config interface mgmt0",
                      "show_run_int_mgmt0_%s"%def_file_name)
        save_exec_cmd("show running-config | in 'ip route'",
                      "show_run_ip_route_%s"%def_file_name)

def save_route_status(system_type) :                # IP 경로 정보를 저장하는 명령어 실행
    def_file_name = "%s_result.txt" % get_date_str()
    if system_type == "Linux" :
        save_exec_cmd("route", "route_%s"%def_file_name)
    elif system_type == "NX-OS_Switch" :
        save_exec_cmd("show ip route", "show_ip_route_%s"%def_file_name)

def save_status_files(system_type) :                # 시스템별 CPU, 메모리, 디스크, 관리 네트워크, IP 경로 정보를 조회하고 파일에 저장
    if system_type == "Linux" or system_type == "NX-OS_Switch" :
        save_cpu_mem_disk_status(system_type)
        save_mgmt_route_status(system_type)
        save_route_status(system_type)
    else :
        print "리눅스/네트워크 시스템이 아니어서 실행할 수 없습니다."

def prepare_dir(host) :         # 로그를 작성할 디렉터리 준비
    global dir_name
    dir_name = "./logs"
    if not os.path.isdir(dir_name):     # 디렉터리가 있는지 확인
        os.mkdir(dir_name)              # 디렉터리 만들기
    dir_name = "./logs/%s" % host       # 원격지 시스템 주소를 포함해서 디렉터리명을 정의
    if not os.path.isdir(dir_name):     # 디렉터리가 있는지 확인
        os.mkdir(dir_name)              # 디렉터리 만들기

if __name__ == '__main__':
    (host, port_num, user, pw) = get_connection_input()
    connnected = connect(host, port_num, user, pw)
    if connnected:
        close()
    else :
        print "원격지 시스템 접속에 실패하였습니다."
    if connnected :
        (system_type, cmd_result) = check_type()

        # 파일을 작성할 디렉터리 생성
        prepare_dir(host)

        # CPU, 메모리, 디스크, 관리 네트워크, IP 경로 정보를 조회해서 저장
        save_status_files(system_type)
