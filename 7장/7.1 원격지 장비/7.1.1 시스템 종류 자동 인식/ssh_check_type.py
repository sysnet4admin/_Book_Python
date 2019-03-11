#!/bin/env python
#-*- coding: utf-8 -*-

from ssh_exec_cmd import *
    
def check_type() :
    system_type = "Unknown"
    data = exec_cmd("uname -a")
    if data.find("Linux ") >= 0 :
        data = exec_cmd("grep . /etc/*-release")
        system_type = "Linux"
    elif data.find("VMkernel ") >=0 :
        system_type = "VMware"
    elif data.find("Cmd exec") >= 0 :
        data = exec_cmd("show version")
        if data.find("Cisco Nexus Operating System (NX-OS) Software") >=0:
            data = exec_cmd("show version | include version")
            system_type = "NX-OS_Switch"
    elif data.lower().find("invalid command") >= 0 :
        data = exec_cmd("show version")
        if data.find("Firmware Version") >=0 :
            system_type = "UCSC_MGMT_Port"
        elif data.find("System version") >=0:
            system_type = "UCSM_FI" # 현재 랩에서 NX-OS가 아닌 경우는 UCSM 입니다.
    return (system_type, data)      # (시스템 종류, 화면 출력 메시지(버전 정보))를 반환

def get_message(system_type, cmd_result) :
    if system_type == "Linux" :
        return "리눅스 시스템입니다. : %s" % get_line(cmd_result, 0)
    elif system_type == "VMware" :
        return "VMware 시스템입니다. : %s" % get_line(cmd_result, 0)                  
    elif system_type == "UCSC_MGMT_Port" :
        return "서버 관리 모듈입니다. : %s(%s)" % (
            get_line(cmd_result, 0), get_line(cmd_result, 2))
    elif system_type == "NX-OS_Switch" :
        return "네트워크 시스템입니다. : %s" % get_line(cmd_result, 3)
    elif system_type == "UCSM_FI" :
        return "UCS 매니저 시스템입니다. : %s" % get_line(cmd_result, 0)
    return "시스템 타입을 알 수 없습니다."

def get_line(data, row) :
    lines = data.split("\n")
    return str(lines[row]).strip()

if __name__ == '__main__':
    # ssh_exec_cmd의 get_connection_input, connect 함수를 사용할 수 있습니다.
    # 접속 정보를 입력받고, 원격지 시스템에 접속
    (host, port_num, user, pw) = get_connection_input()
    connnected = connect(host, port_num, user, pw)
    if connnected:
        close()
    else :
        print "원격지 시스템 접속에 실패하였습니다."        
    if connnected : 
        (system_type, cmd_result) = check_type()        # check_type 함수로 시스템 종류를 판단
        print get_message(system_type, cmd_result)      # 시스템 종류에 따른 버전 정보 출력
