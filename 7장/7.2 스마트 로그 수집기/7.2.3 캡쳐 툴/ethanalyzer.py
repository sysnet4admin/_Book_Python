#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
from subprocess import Popen
from subprocess import PIPE
import time
import socket
import os

def exec_bash(cmd) :
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def avail_disk_size():
    # 가용 디스크를 확인
    ret = exec_bash("df -m /bootflash")
    data_line = ret.split("\n")[1]
    avail = data_line.split()[3]
    return int(avail)

def get_pcap_name(filter_str) :                 # 작성할 pcap 이름을 지정합니다.
    dir_path = "/bootflash/ethanalyzer_log"     # pcap을 ethanalyzer_log 디렉토리에 작성합니다.
    if os.path.isdir(dir_path) == False :       # 이 디렉터리가 없다면
        os.mkdir(dir_path)                      # 디렉터리를 생성합니다.
    now = time.localtime()
    str_now = "%04d%02d%02d_%02d%02d%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday,
        now.tm_hour, now.tm_min, now.tm_sec)
    if filter_str == None :                         # 필터 옵션에서 대상 호스트를 추출
        filter_str = ""                             # 호스트를 추출할 수 없으면 빈 값
    elif filter_str.find("==") >= 0 :               # == 이후에 지정한 값이 있다면 이 값에서 추출
        filter_str = filter_str.split("==")[1]
    else :
        temp_list = filter_str.split()              # ==가 없으면 맨 마지막 단어로 추출
        filter_str = temp_list[len(temp_list) - 1]
    filter_str = filter_str.replace("'", "")        # '가 있으면 제거
    pcap_name = "bootflash:ethanalyzer_log/%s_%s_%s_dump.pcap" % (
        socket.gethostname(), str_now, filter_str)
    return pcap_name

def get_user_input_file_write() :
    print "\n" + ("-" *50)
    print "\t1. ethanalyzer 실행 명령어 생성"
    print "\t2. ethanalyzer 파일로 저장"
    print ("-" *50) + "\n"
    input_task_num = raw_input("어떤 작업을 진행하시겠습니까? [1]: ")
    return (input_task_num == "2")

def get_user_input_filter(is_write_file) :      # 필터 옵션을 입력받습니다.
    print "\n--------[ 필터 조건 ]---------"
    print "\t1. IP"
    print "\t2. 서비스 타입"
    print "\t3. Port"
    print "\t4. 지정하지 않음"
    print ("-" *30) + "\n"
    filter_num = 1
    try :
        filter_num = input("사용할 필터 조건을 선택해주세요. [4]: ")
    except :
        filter_num = 4

    if filter_num <= 1 or filter_num > 4 :
        print "\n--------[ 필터 옵션 ]---------"
        print "\t1. 호스트 지정"
        print "\t2. 출발지 지정"
        print "\t3. 도착지 지정"
        print ("-" *30) + "\n"

        try :
            filter_option_num = input("필터 옵션을 선택해주세요. [1] : ")
        except :
            filter_option_num = 1
        if filter_option_num < 1 or filter_option_num > 3 :
            filter_option_num = 1

        filter_option_str = raw_input("주소를 입력해주세요. : ")

        if is_write_file :
            filter_name_list = ["host", "src", "dst"]
            filter_name = filter_name_list[filter_option_num - 1]
            return ("'%s %s'" %(filter_name, filter_option_str))
        else :
            filter_name_list = ["ip.addr", "ip.src", "ip.dst"]
            filter_name = filter_name_list[filter_option_num - 1]
            return ("%s==%s" %(filter_name, filter_option_str))

    elif filter_num == 2 :
        sv_type = "icmp"
        try :
            sv_type = raw_input("서비스 타입을 입력하세요. [icmp] : ")
        except :
            sv_type = "icmp"

        if sv_type == "" :
            sv_type = "icmp"
        return sv_type

    elif filter_num == 3 :
        print "\n--------[ 포트 옵션 ]---------"
        print "\t1. tcp"
        print "\t2. udp"
        print ("-" *30) + "\n"
        port_option = "tcp"
        try :
            port_option_num = input("포트 옵션을 선택해주세요. [1] : ")
            if port_option_num == 2 :
                port_option = "udp"
        except :
            port_option = "tcp"

        port = raw_input("포트 번호를 입력해주세요. : ")

        if is_write_file :
            return "'%s port %s'" % (port_option, port)
        else :
            return "'%s.port==%s'" % (port_option, port)

def get_cmd(write_file_yn, filter_str) :
    filter_option = ""
    if write_file_yn :
        if filter_str == None :
            filter_option = ""
        else :
            filter_option = " capture-filter %s" % filter_str
    else :
        if filter_str == None :
            filter_option = ""
        else :
            filter_option = " display-filter %s" % filter_str

    last_option = "| no-more"
    if write_file_yn :
        last_option = " write % s" % get_pcap_name(filter_str)

    cmd = "ethanalyzer local interface inband%s limit-captured-frames 0 %s" % (
        filter_option, last_option)
    return cmd

if __name__ == "__main__":
    disk_size = avail_disk_size()
    if avail_disk_size() < 1035  :
        print "\t현재 여유 공간 :", disk_size, "M"
        print "\t여유 공간이 1035M (여유 공간 1024M, ethanalyzer파일11M) 미만으로 종료합니다."
    else :
        write_file_yn = get_user_input_file_write()
        filter_str = get_user_input_filter(write_file_yn)
        cmd = get_cmd(write_file_yn, filter_str)
        if write_file_yn :
            print "실행 명령어 :", cmd
            cli(cmd)        # ethanalyzer 명령 실행
        else :
            print "선택한 옵션이 포함된 ethanalyzer 실행 명령어는 다음과 같습니다."
            print cmd
