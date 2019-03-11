#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import PIPE
import time
import socket
import re
import sys
import os

def exec_bash(cmd) :            # 명령어를 실행
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def avail_disk_size():
    # 가용 디스크를 확인
    ret = exec_bash("df -m /bootflash")
    data_line = ret.split("\n")[1]      # 명령어 결과에서 2번째 줄의
    avail = data_line.split()[3]        # 4번째 데이터를 추출
    return int(avail)

def get_pcap_name(interface) :          # 작성할 덤프 이름을 지정합니다.
    dir_path = "/bootflash/tcpdump_log"
    if os.path.isdir(dir_path) == False :
        os.mkdir(dir_path)
    exec_bash("chown -R tcpdump:tcpdump %s" % dir_path)
    now = time.localtime()              # 호스트 이름과 현재 날짜로 이름을 정합니다.
    str_now = "%04d%02d%02d_%02d%02d%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday,
        now.tm_hour, now.tm_min, now.tm_sec)
    pcap_name = dir_path + "/%s_%s_%s_tcpdump.pcap" % (
        socket.gethostname(), str_now, interface)
    return pcap_name

def get_user_input_size() :     # 작성할 덤프 파일의 크기와 개수를 사용자에게 입력습니다.
    size_pcap = 1
    try :
        size_pcap = input("누적할 tcpdump 크기(메가(M))를 지정해주세요.[1] : ")
    except :
        size_pcap = 1
    count_pcap = 1
    try :
        count_pcap = input("누적할 tcpdump 개수를 지정해주세요.[1] : ")
    except :
        count_pcap = 1
    max_pcap = size_pcap * count_pcap
    disk_size = avail_disk_size()
    max_size = disk_size / 5
    print "*"*70
    print "\t현재 여유 공간 : %sM (덤프 저장 허용 공간 : %sM)" % (disk_size, max_size)
    print "\t%dM의 덤프 %d개를 저장하기 위해 소요되는 디스크 공간 : %dM" % (
        size_pcap, count_pcap, max_pcap)
    print "*"*70
    if max_size < max_pcap or max_size < 1000:
        print "여유 공간이 부족하여 실행할 수 없습니다."
    else :
        confirm = raw_input("계속 진행하시겠습니까? [Y/n] :")
        if confirm == "" or confirm == "y" or confirm == "Y" :
            return (size_pcap, count_pcap)    
    return (0, 0)

def get_user_input_interface() :
    ret = exec_bash("ifconfig")
    int_list = re.findall(".*: ", ret)
    i = 1
    print "\n" + ("-" * 23) + "[ 인터페이스 리스트 ]" + ("-" * 23) 
    for interface in int_list :                 # 정규식으로 추출한 인터페이스
        interface = interface.split(": ")[0]    # 인터페이스로 추출한 단어에서 ": " 뒤는 제거
        sys.stdout.write("%s\t"% interface)        
        if i % 5 == 0 or i == len(int_list) :   # 한 줄에 5개씩 출력함(5번째라면 줄 바꿈)
            print
        i = i + 1
    print "-"*70    
    interface = ""
    while True :
        interface = raw_input("인터페이스 명을 입력해주세요. : ")
        if interface != "" :
            return interface

def get_user_input_filter() :
    print "\n--------[ 필터 조건 ]---------"
    print "\t1. IP"
    print "\t2. MAC"
    print "\t3. Port"
    print "\t4. 지정하지 않음"
    print ("-" *30) + "\n"
    filter_num = 4
    try :
        filter_num = input("사용할 필터 조건을 선택해주세요. [4]: ")
    except :
        filter_num = 4        
    if filter_num == 1 or filter_num == 2 :
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
        filter_name_list = ["host", "src", "dst"]
        filter_name = ""
        if filter_num== 2 :
            filter_name = "ether "
        filter_name = filter_name + filter_name_list[filter_option_num - 1]
        return (filter_name, filter_option_str)
    
    elif filter_num == 3 : 
        filter_option_str = raw_input("포트 번호를 입력해주세요. : ")
        return ("port", filter_option_str)
    return ("", "")
    
def get_cmd(size, count, interface, filter_name, filter_option) :
    cmd = "tcpdump -C %d -W %d -i %s " % (size, count, interface)
    if filter_name != "" :
        cmd = cmd + ("%s %s " % (filter_name, filter_option))
    cmd = cmd + "-w " + get_pcap_name(interface)
    return cmd
    
if __name__ == "__main__":
    # get_user_input_size 함수로 만들고자 하는 덤프의 크기와 개수를 입력받습니다.
    (size_pcap, count_pcap) = get_user_input_size()
    if size_pcap > 0 and count_pcap > 0 :
        interface = get_user_input_interface()
        (filter_name, filter_option) = get_user_input_filter()
        cmd = get_cmd(size_pcap, count_pcap, interface, filter_name, filter_option)
        print "실행 명령어 :", cmd
        exec_bash(cmd)
