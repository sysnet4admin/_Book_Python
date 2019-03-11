#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
from ethanalyzer import *
import threading
import time
from datetime import datetime

log_index_date = datetime.today()
stop_ethanalyzer=False
def check_log(check_word) :         # 시스템 로그에서 특정 단어를 찾습니다.
    global log_index_date
    ret = cli("show logging log | include '%s'" % check_word)
    ret = ret.strip()
    lines = []
    if ret == "" :
        return lines
    for line in ret.split("\n"):
        try :
            date_str = line[0:20]
            log_date = datetime.strptime(date_str, "%Y %b %d %H:%M:%S")
            if log_index_date < log_date :
                lines.append(line)
        except :
            continue
    log_index_date = datetime.today()
    return lines

def write_syslog(check_word, log) :         # 시스템 로그 작성
    log = "%s 로그가 발생해서 ethanalyzer를 종료합니다." % check_word
    print log
    cli("logit [Ethanalyzer] %s has been detected. - %s" % (check_word, log))

def remake_cmd_pcap_name(cmd, is_before) :
    # ethanalyzer 프로세스 실행 명령어에서 pcap 파일명을 바꾸어 반환
    pcap_index_start = cmd.find("write ") + 6           # 명령어 내용 중 "write " 뒤에서부터,
    pcap_index_end = cmd.find(".pcap")                  # ".pcap" 사이의 값이 파일명입니다.
    pcap_name = cmd[pcap_index_start : pcap_index_end]
    if is_before :
        return "%s%s_before.pcap"%(cmd[:pcap_index_start], pcap_name)
    else :
        return "%s%s_after.pcap"%(cmd[:pcap_index_start], pcap_name)
    
class EthanalyzerThread(threading.Thread):  # 덤프를 작성하는 클래스
    cmd = ""
    def run(self) :
        while not stop_ethanalyzer :        # stop_ethanalyzer가 True로 설정되지 않으면 반복
            cli(self.cmd)
            time.sleep(0.01)

def monitoring_log(cmd, check_time) :       # 로그를 모니터링해서 수행할 동작을 정의한 함수
    global stop_ethanalyzer
    while True :
        log_list = check_log(check_word)
        if len(log_list) > 0 :
            stop_ethanalyzer= True          # EthanalyzerThread의 동작을 중지시킵니다.
            print "로그가 발견되어 2차 실행 되는 ethanalyzer 입니다."
            cmd = remake_cmd_pcap_name(cmd, False)
            print "="*80,"\n",cmd
            cli(cmd)                        # 저장되는 이름에 after를 붙여서 저장
            log = log_list[len(log_list)-1]
            write_syslog(check_word, log)
            break
        time.sleep(check_time)

if __name__ == "__main__":
    check_word = ""
    check_time = 1
    while True :
        # 로그에서 모니터링할 내용을 입력받습니다.
        check_word = raw_input("로그에서 모니터링할 내용을 입력하세요 : ")
        try :
            # 모니터링 주기를 입력받습니다.
            check_time = input("로그를 모니터링할 주기를 입력하세요 [10초] : ")
        except :
            check_time = 10
        if check_word != "":
            break
    disk_size = avail_disk_size()
    if avail_disk_size()  < 1035  :
        print "\t현재 여유 공간 :", disk_size, "M"
        print "여유 공간이 1035M(여유공간 1024M와 ethanalyzer파일 11M) 미만으로 종료합니다."
    else :
        # 사용자의 입력을 받아 pcap 작성 명령어를 만듭니다.
        write_file_yn = get_user_input_file_write()         # ethanalyzer 모듈의 get_user_input_file_write 함수
        filter_str = get_user_input_filter(write_file_yn)   # ethanalyzer 모듈의 get_user_input_filter 함수
        cmd = get_cmd(write_file_yn, filter_str)            # ethanalyzer 모듈의 get_cmd 함수
        if write_file_yn  :
            print "1차 실행 명령어는 다음과 같습니다. 로그가 발생할 때까지 덮어 쓰기를 실행합니다."
            t = EthanalyzerThread()
            t.cmd = remake_cmd_pcap_name(cmd, True)
            print "="*80,"\n",t.cmd
            t.start()
            time.sleep(1)

            # 로그 모니터링
            monitoring_log(cmd, check_time)
        else :
            print "선택한 옵션이 포함된 ethanalyzer 실행 명령어는 다음과 같습니다."
            print cmd
