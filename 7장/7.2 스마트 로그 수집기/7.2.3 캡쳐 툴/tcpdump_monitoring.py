#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
from tcpdump import *
import threading
import time
from datetime import datetime

log_index_date = datetime.today()
def check_log(check_word) :         # 시스템 로그에서 특정 단어를 찾습니다.
    global log_index_date
    ret = cli("show logging log | include '%s'" % check_word)       # 명령어로 로그 조회
    ret = ret.strip()
    lines = []
    if ret == "" :
        return lines
    for line in ret.split("\n"):
        try :
            date_str = line[0:20]
            log_date = datetime.strptime(date_str, "%Y %b %d %H:%M:%S")     # 조회된 로그 날짜
            if log_index_date < log_date :          # 최신 로그만 모니터링 대상입니다.
                lines.append(line)
        except :
            continue
    log_index_date = datetime.today()
    return lines

def write_syslog(check_word, log, wait_kill_time) :
    # 시스템 로그 작성
    log = "%s 로그가 발생해서 %d분 후 tcpdump를 종료합니다." % (check_word, wait_kill_time)
    print log
    cli("logit [tcpdump] %s has been detected. - %s" % (check_word, log))

def kill_tcpdump() :                # TCP 덤프 작성 프로세스 중지
    ret = exec_bash("ps -ef | grep tcpdump")        # tcpdump 프로세스를 조회
    lines = ret.split("\n")
    for line in lines :
        if line.find("grep tcpdump") >= 0 :         # grep tcpdump 명령 실행으로 나타난 프로세스는 제외
            continue
        if line.find(".py") >= 0 :                  # 파이썬 코드 실행으로 나타난 프로세스는 제외
            continue
        if line.find("tcpdump ") >= 0 :
            pid = line.split()[1]
            exec_bash("kill -9 %s" % pid)           # 동작 중인 프로세스를 중지하는 명령어

class TCPThread(threading.Thread):      # TCP 덤프를 작성하는 클래스
    cmd = ""
    def run(self) :
        exec_bash(self.cmd)             # tcpdump.py의 exec_bash 이용

if __name__ == "__main__":
    # 로그에서 모니터링할 내용을 입력받습니다.
    check_word = ""
    while True :
        check_word = raw_input("로그에서 모니터링할 내용을 입력하세요 : ")
        if check_word != "" :
            break

    # 모니터링할 내용이 검출됐을 때 tcpdump 프로세스를 중단할 대기 시간을 입력받습니다.
    wait_kill_time = 1
    try :
        wait_kill_time = input(
            "모니터링 로그가 발생한 이후로 로그를 더 수집할 기간(분)을 입력하십시오 [1] : ")
    except :
        wait_kill_time = 1

    # 사용자 입력을 받아 tcpdump 명령어를 만듭니다.
    (size_pcap, count_pcap) = get_user_input_size()
    if size_pcap > 0 and count_pcap > 0 :
        interface = get_user_input_interface()
        (filter_name, filter_option) = get_user_input_filter()
        cmd = get_cmd(size_pcap, count_pcap, interface, filter_name, filter_option)
        print "실행 명령어 :", cmd
        t = TCPThread()
        t.cmd = cmd         # 조합한 명령어(cmd)를 스레드 클래스에 지정
        t.start()           # TCP 덤프 수집 작업을 스레드에 맡김(스레드가 실행될 때 스레드가 명령어(cmd)를 실행시킵니다.)

    # 로그 모니터링
    log = ""
    while True :
        log_list = check_log(check_word)
        if len(log_list) > 0 :                  # 검출된 로그 내용이 있는지 확인
            log = log_list[len(log_list)-1]     # 검출된 로그 리스트 중 최신 로그를 log 변수에 지정
            break                               # 모니터링 중지
        time.sleep(10)
    write_syslog(check_word, log, wait_kill_time)   # 시스템 로그 작성
    time.sleep(wait_kill_time * 60)                 # 덤프 작성 중지까지 대기
    kill_tcpdump()                                  # 덤프 작성 중지
