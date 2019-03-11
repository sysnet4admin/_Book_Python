#!/bin/env python
#-*- coding: utf-8 -*-

from ssh_get_status_file import *

def get_host_list(host):            # 입력받은 IP 범위 값 사이에 있는 모든 주소를 리스트로 작성
    hosts = []
    ipv4_num = host.split('.')
    exist_ip_range = False
    for i,ip_range in enumerate(ipv4_num):
        exist_ip_range = "-" in ip_range
        if exist_ip_range:
            range1 = int(ip_range.split("-")[0])        # 범위 시작 값
            range2 = int(ip_range.split("-")[1]) + 1    # 범위 마지막 값(range로 사용하기 위해 1을 더함)
            for digit in range(range1, range2):
                ip = '.'.join(ipv4_num[:i] + [str(digit)] + ipv4_num[i+1:])     # IP 형식으로 바꿈
                hosts += get_host_list(ip)
            break
    if not exist_ip_range:          # 범위값이 포함되지 않으면 더이상 재귀 호출을 하지 않습니다.
        hosts.append(host)
    return hosts

def get_connection_range_input() :      # 원격지 시스템에 접속하기 위한 IP(범위 값), 포트 번호, 관리자 ID, 암호를 입력받습니다.
    print "IP 범위 예시 "
    print "192.168.0.1-192.168.0.10\t\t192.168.0.1-10 까지"
    print "172.16.0.100-172.16.10.200\t\t172.16.0-10.100-200까지"
    host_list = []
    while True :
        host = raw_input("원격지 시스템의 IP 범위를 입력하세요. : ")
        if host.find("-") < 0 :             # "-"가 포함돼 있지 않다면 하나의IP 를 입력한 것입니다.
            host_list.append(host)
            break
        host_list = get_host_list(host)     # 입력한 범위 사이의 IP 리스트를 찾습니다.
        if len(host_list) < 1 :
            print "IP 범위를 잘못 입력하였습니다."
        else :
            break
    port_num = 22
    try :
        port_num = input("원격지 시스템의 Port 번호를 입력하세요. [22] : ")
    except :
        port_num = 22
    user = raw_input("관리자 ID를 입력하세요. : ")
    pw = raw_input("암호를 입력하세요. : ")
    return (host_list, port_num, user, pw)

if __name__ == '__main__':
    # get_connection_range_input 함수를 이용해 원격지 시스템에 접속하기 위한 접속 정보를 입력받음
    (host_list, port_num, user, pw) = get_connection_range_input()

    # 입력한 범위의 IP 주소로 각 시스템에 접속해 상태 정보를 파일로 출력    
    for host in host_list :
        connnected = connect(host, port_num, user, pw)
        if connnected:
            close()
        else :
            print "*" * 50
            print "%s 에 접속할 수 없습니다." % host  
        if connnected:
            print "*"* 50
            print "%s 에 접속하여 로그 기록 중..." % host
            (system_type, cmd_result) = check_type()
            prepare_dir(host)
            save_status_files(system_type)
