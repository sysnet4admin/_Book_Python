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
    return (system_type, data)

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
    (host, port_num, user, pw) = get_connection_input()
    connnected = connect(host, port_num, user, pw)
    if connnected:
        close()
    else :
        print "원격지 시스템 접속에 실패하였습니다."        
    if connnected : 
        (system_type, cmd_result) = check_type()
        print get_message(system_type, cmd_result)
