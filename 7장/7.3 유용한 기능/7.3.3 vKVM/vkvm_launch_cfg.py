#!/bin/env python
# -*- coding: utf-8 -*-

from subprocess import os
from ssh_check_type import connect
from ssh_check_type import close
from ssh_check_type import exec_cmd
from ssh_check_type import check_type
import ConfigParser
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucskvmlaunch import ucs_kvm_launch
import re

cfg_path = "./connection_info.cfg"
conf_list = {}
def get_config() :          # 환경 설정 파일을 가져옵니다.
    config = ConfigParser.RawConfigParser()
    if os.path.exists(cfg_path) :
        config.read(cfg_path)
    return config

def load_cfg():             # 환경 설정의 내용을 읽어서 vKVM 접속 정보 리스트를 가져옵니다.
    global conf_list
    config = get_config()
    conf_list = {}
    conf_rack_list = {}
    conf_blade_list = {}
    if config != None :
        sections = config.sections()                    # 환경 설정의 섹션 값IP()을 리스트로 가져옵니다.
        for cimc_ip in sections :                       # 각 IP의 접속 ID/암호를 가져옵니다.
            c_user = config.get(cimc_ip, "user")
            c_password = config.get(cimc_ip, "password")
            c_type = config.get(cimc_ip, "type")
            conf_list[cimc_ip] = (c_user, c_password, c_type)
    return conf_list

def save_cfg(config):                       # 환경 설정 파일을 열어서 환경 내용을 저장
    configfile = open(cfg_path, "wb")
    config.write(configfile)
    configfile.close()

def remove_section_cfg(section) :
    config = get_config()
    config.remove_section(section)         # 환경 설정 파일 중 특정 섹션(IP)을 삭제합니다.
    save_cfg(config)

def add_cfg(cimc_ip, c_user, c_password, c_type):   # 환경 설정 파일에 IP, 사용자, 암호 추가, 서버 매니저 종류를 추가합니다.
    config = get_config()
    if (config.sections().count(cimc_ip) == 0 ) :   # 등록된 IP의 섹션이 없다면 섹션을 만듭니다.
        config.add_section(cimc_ip)
    config.set(cimc_ip, "user", c_user)
    config.set(cimc_ip, "password", c_password)
    config.set(cimc_ip, "type", c_type)
    save_cfg(config)

def get_new_input() :                       # vKVM에 접속하기 위해 사용자의 입력을 받습니다.
    print "************ UCS 서버 매니저 종류 ***********"
    print "\ta. 랙 서버\tb. 블레이드 서버"
    print "-" * 45
    c_type = raw_input("접속할 매니저의 종류를 선택해주세요 [a] : ")
    if c_type == "b" :
        c_type = "blade"
    else :
        c_type = "rack"
    cimc_ip = raw_input("vKVM에 접속할 매니저의 IP를 입력해주세요 : ")
    c_user = raw_input("관리자 ID를 입력하세요 : ")
    c_password = raw_input("암호를 입력하세요 : ")
    return (cimc_ip,c_user,c_password, c_type)

def vKVM_launcher(cimc_ip,c_user,c_password):   # vKVM에 접속 - 랙 서버 매니저
    print "%s에 vKVM에 접속합니다."%cimc_ip
    os.chdir("c:\kvm")
    cmd = "launchkvm.bat -u %s -p %s -h %s"%(c_user,c_password,cimc_ip)
    os.system(cmd)

def vKVM_launcher_blade(ucsm_ip,user,password,chassis,blade):   :   # vKVM에 접속 - 블레이드 서버 매니저
    handle = UcsHandle(ucsm_ip,user,password)
    handle.login()
    mo = handle.query_dn("sys/chassis-{0}/blade-{1}".format(chassis,blade))
    print mo
    ucs_kvm_launch(handle, blade=mo)
    handle.logout()

def select_manager() :          # 등록된 매니저 중 vKVM에 접속할 매니저 선택
    rack_ip_list = []
    blade_ip_list = []
    for ip in conf_list.keys() :
        (c_user,c_password, c_type) = conf_list[ip]
        if c_type == "rack" :
            rack_ip_list.append(ip)
        else :
            blade_ip_list.append(ip)
    rack_ip_list.sort()
    blade_ip_list.sort()
    ip_list = rack_ip_list + blade_ip_list      # 랙 서버/블레이드 서버를 합쳐서 판단합니다.
    if len(ip_list) == 0 :                      # 전체 서버 IP리스트 개수가 0이면 출력할 수 없습니다.
        return ("add", "")                      # 출력할 내용이 없으면 "추가" 동작으로 넘어갑니다.
    i = 1
    if len(rack_ip_list) > 0 :
        print "********* 등록된 UCS 랙 서버 매니저 *********\n"
        for rack_ip in rack_ip_list :
            print "\t%d. %s" % (i, rack_ip)
            i = i + 1
        print "\n"+ ("-" * 45) + "\n"
     
    if len(blade_ip_list) > 0 :
        print "****** 등록된 UCS 블레이드 서버 매니저 ******\n"
        for blade_ip in blade_ip_list :
            print "\t%d. %s" % (i, blade_ip)
            i = i + 1
        print "\n"+ ("-" * 45)
    print "\n*************** 다른 선택 동작 **************\n"
    print "\ta. 등록된 UCS 매니저 삭제"
    print "\tb. 새로운 UCS 매니저 접속"
    print "\n"+ ("-" * 45)
    select = raw_input("\n접속할 매니저 번호나, 수행할 동작을 선택해주세요 [b] : ")
    if select == "a" :
        remove_num = input("\t삭제할 번호를 선택해주세요 [1-%d] : " % len(ip_list))
        cimc_ip = ip_list[remove_num - 1]
        del conf_list[cimc_ip]
        remove_section_cfg(cimc_ip)
        if len(ip_list) != 0 :
            return ("remove", cimc_ip)
        return ("add", "")
    elif select != "" and select < "a":
        return ("connect", ip_list[int(select) - 1])
    return ("add", "")

def connect_test(cimc_ip, port_num, c_user, c_password) :
    # 접속 테스트 수행
    if connect(cimc_ip, port_num, c_user, c_password) == False :
        return False
    close()
    return True

def get_chassis(cimc_ip, port_num, c_user, c_password) :        # 블레이드 서버에서 샤시 정보를 출력하고, 접속할 대상을 선택합니다.
    if connect(cimc_ip, port_num, c_user, c_password) == False :
        return ("", "")
    ret = exec_cmd("show server status")
    rows = re.findall("[0-9]/[0-9] .*.", ret)
    print "-" * 70
    print "Num\tServer\tSlot Status\tAvailability\tStatus\tDiscovery"
    print "   \t      \t           \tOverall"
    print "-" * 70
    for i, row in enumerate(rows) :         # 샤시 데이터를 한 줄씩 출력
        row = row.replace("  ", "\t")       # 헤더의 각 열의 탭 간격에 맞추어 데이터의 탭 간격 조정
        row = row.replace("\t ", "\t")
        while row.find("\t\t")>= 00 :
            row = row.replace("\t\t", "\t")
        print ("%d)\t" % (i+1)), row
    print "-" * 70
    select_num = 1
    try :
        select_num = input("접속할 UCS 서버의 번호를 선택하세요. [1-%d] : " % len(rows))
    except :
        select_num = 1
    if select_num > len(rows) :
        select_num = 1
    select_data = rows[select_num-1].split()[0]         # 선택한 번호의 "Server" 열 데이터를 찾습니다.
    chassis = select_data.split("/")[0]                 # "숫자/숫자"로 이루어진 데이터 중 앞은 샤시, 
    blade = select_data.split("/")[1]                   # 뒤는 블레이드 서버 번호입니다.
    return (chassis, blade)
    
if __name__ == "__main__":
    # 등록된 서버 매니저 출력 및 선택/삭제/추가
    load_cfg()
    cimc_ip = ""
    while True > 0 :
        (action, cimc_ip) = select_manager()
        if action != "remove" :
            break

    # 접속 테스트 수행후 접속 성공시 추가된 서버 매니저를 환경 설정에 저장합니다.
    connect_success = True
    port_num = 22
    if cimc_ip == "" :
        (cimc_ip,c_user,c_password, c_type) = get_new_input()
        try :
            port_num = input("접속 테스트를 위하여 매니저의 Port 번호를 입력하세요. [22] : ")
        except :
            port_num = 22
        print "접속 테스트를 수행 중입니다..."
        connect_success = connect_test(cimc_ip, port_num, c_user, c_password)
        if connect_success :
            if c_type == "blade" :
                (system_type, cmd_result) = check_type()
                if not system_type == "UCSM_FI" :
                    print "블레이드 서버가 아닙니다."
                else :
                    add_cfg(cimc_ip, c_user, c_password, c_type)
            else :
                add_cfg(cimc_ip, c_user, c_password, c_type)
        else :
            print "UCS 서버 매니저에 접속할 수 없습니다."
    else :
        (c_user,c_password, c_type) = conf_list[cimc_ip]

    if connect_success :
        if c_type == "rack" :
            vKVM_launcher(cimc_ip, c_user,c_password)
        else :
            (chassis,blade) = get_chassis(cimc_ip, port_num, c_user,c_password)
            if chassis != "" and blade != "" :
                vKVM_launcher_blade(cimc_ip,c_user,c_password,chassis,blade)
