#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
from time import sleep
import sys

def get_proc_status_list() :
    # 'show processes cpu sort | head' 명령어의 실행 결과로부터 필요한 데이터 추출
    ret = cli("show processes cpu sort | head")
    ret = ret.strip()                               # 빈 행 제외
    proc_status_list = []

    for i, line in enumerate(ret.split("\n")) :
        if i < 2 :                                  # 헤더와 구분자 행 제외
            continue
        columns = line.split()                      # 한 줄 데이터를 공백 단위로 분리
        CPU_IDX = len(columns) - 2
        PROC_IDX = len(columns) - 1
        pid = columns[0]                            # 분리된 데이터 중 첫 번째는 PID
        cpu_usage = columns[CPU_IDX]                # 뒤에서 두 번째 데이터는 CPU 사용량
        process = columns[PROC_IDX]                 # 마지막 데이터는 프로세스 이름
        proc_status_list.append((pid, cpu_usage, process))
    return proc_status_list         # (프로세스 ID, cpu 사용률, Process) 튜플의 리스트 반환

def get_monitoring_input() :        # 모니터링할 프로세스를 선택하기 위해 사용자의 입력을 받습니다.
    # 현재 동작 중인 프로세스의 리스트 출력    
    mon_proc_status_list = get_proc_status_list()
    print "\n*********************[ 현재 동작 중인 프로세스 ]**********************\n"
    print "\t번호\tPID\tCPU\tProcess"
    print "\t" + ("-" * 40)
    for i, (pid, cpu_usage, process) in enumerate(mon_proc_status_list) :
        print "\t%i\t%s\t%s\t%s" % ((i + 1), pid, cpu_usage, process)
    print "\n" + ("*" * 70)

    proc_cnt = len(mon_proc_status_list)
    select_num = 0
    while True :
        try :
            select_num = input("1. 모니터링 프로세스의 번호를 선택하세요. [1-%i] : "% proc_cnt)
            if select_num <= proc_cnt :
                break
        except :
            continue
    (pid, cpu, process) = mon_proc_status_list[select_num-1]
    return process

def get_user_input() :      # 모니터링 조건(시간 단위, CPU 사용률 범위)을 지정하기 위해 사용자의 입력을 받습니다.
    sleep_time = 30
    try :
        sleep_time = input("\n2. 모니터링할 시간 단위(초)를 5초 이상으로 입력해 주세요 [30]: ")
        if sleep_time < 5 :
            sleep_time = 5
    except :
        sleep_time = 30
    print "\n3. 모니터링할 프로세스의 정상범위 CPU 사용률을 지정해주세요."
    print "\t소수점으로 입력할 수 있습니다."
    min_cpu_usage = input("\t최소 사용률 : ")
    max_cpu_usage = input("\t최대 사용률 : ")

    print "\n", sleep_time, "초 단위로",
    print min_cpu_usage,"~",max_cpu_usage,"사이의 CPU 사용률을 유지하는지 모니터링합니다."
    if min_cpu_usage > max_cpu_usage :
        max_cpu_usage = min_cpu_usage
    return (sleep_time, float(min_cpu_usage) , float(max_cpu_usage))

def monitoring(mon_process, sleep_time, min_cpu_usage, max_cpu_usage) :     # 선택한 프로세스를 모니터링
    while True :
        alert_list = []
        for (pid, cpu, process) in get_proc_status_list() :
            # 모니터링하려고 선택한 프로세스가 아니면 모니터링에서 제외합니다.
            if process != mon_process :
                continue
            cpu_usage = float(cpu.split("%")[0])

            # 모니터링 조건에서 사용자가 입력한 CPU의 사용 범위에 맞는지 확인합니다
            if cpu_usage >= min_cpu_usage and cpu_usage <= max_cpu_usage :
                continue

            # CPU 사용 범위에서 벗어나면 사용자에게 알려줄 문제 프로세스 리스트로 추가합니다
            alert_list.append((pid, cpu, process))
        if len(alert_list) > 0 :
            print "\n\n*********************[ 문제가 발견된 프로세스 ]**********************\n"
            print "\tPID\tProcess\tCPU"
            print "\t" + ("-" * 40)
        for (pid, cpu, process) in alert_list :
            print "\t%s\t%s\t%s" % (pid, cpu, process)
        if len(alert_list) > 0 :
            print "\t" + ("-" * 40)
        sys.stdout.write("...")
        sys.stdout.flush()
        sleep(sleep_time)

if __name__ == "__main__":
    # 모니터링 조건 입력
    mon_process = get_monitoring_input()    # 모니터링할 프로세스를 선택합니다.
    (sleep_time, min_cpu_usage, max_cpu_usage) = get_user_input()

    # 모니터링 실행
    monitoring(mon_process, sleep_time, min_cpu_usage, max_cpu_usage)
