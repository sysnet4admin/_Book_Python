#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import PIPE
from time import sleep
import sys

cmd_filter = ""

def exec_bash(cmd) :            # 명령어를 실행한 결과를 반환
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret.strip()

def get_HDB_Info() :        # HDB info 명령어의 실행 결과로부터 필요한 데이터 추출합니다.
    # HDB info 명령을 실행하면서 필터값 반영
    cmd = "HDB info"
    if cmd_filter != "" :
        cmd = "HDB info | grep %s" % cmd_filter
    ret = exec_bash(cmd)

    # 명령어 결과를 한 줄씩 읽으면서 데이터 추출
    hdb_info_list = []
    for i, line in enumerate(ret.split("\n")) :
        if i == 0 :                                     # 맨 처음 데이터는 헤더 값이므로 제외
            continue
        if line.find("grep %s" % cmd_filter) >= 0 :     # 필터 조건 적용 프로세스 제외
            continue
        data_list = line.split()    # 한 줄 데이터를 공백 단위로 분리
        user = data_list[0]         # 분리된 데이터 중 첫 번째는 user
        pid = data_list[1]          # 두 번째 데이터는 PID
        cpu = data_list[3]          # 세 번째 데이터는 CPU 사용량
        
        hdb_cmd = data_list[6]      # 일곱 번째 데이터부터는C ommand이므로 붙여서 한 줄로 표현
        column_idx = 7
        while column_idx < len(data_list):
            hdb_cmd = hdb_cmd + " " + data_list[column_idx]
            column_idx = column_idx + 1
        hdb_info_list.append((user, pid, float(cpu), hdb_cmd))
    return hdb_info_list        # (user, 프로세스 ID, cpu 사용률, Command) 튜플의 리스트를 반환>

def get_monitoring_input() :    # 필터 조건과 모니터링할 프로세스를 선택하기 위해 사용자 입력을 받습니다.
    # 필터 조건 입력    
    global cmd_filter
    print "현재 동작 중인 프로세스를 표시하기 위해 필터 조건을 입력하세요."
    cmd_filter = raw_input("입력하지 않으면 모든 프로세스를 출력합니다. : ")

    # 필터 조건을 적용해서 현재 동작 중인 프로세스의 리스트 출력
    hdb_info_list = get_HDB_Info()
    i = 1
    print "\n*********************[ 현재 동작 중인 프로세스 ]**********************\n"
    print "\tNum\tUser\tPID\tCPU\tCOMMAND"
    print "\t" + ("-" * 40)
    for hdb_info in hdb_info_list :
        (user, pid, cpu, cmd) = hdb_info
        print "\t%d)\t%s\t%s\t%s\t%s" % (i, user, pid, cpu, cmd)
        i = i + 1
    print "\n" + ("*" * 70)

    # 출력된 프로세스 중에서 모니터링할 프로세스 선택
    print "1. 모니터링할 번호는 콤마로 여러 개 선택 가능합니다."
    print "\t예) 1번과 2번을 선택할 때 입력값 : 1,2"

    while True :
        # 사용자가 선택한 프로세스 번호를 리스트로 만듭니다.
        select_num = raw_input("\t모니터링할 번호를 선택하세요 : ")
        if select_num == "" :
            return hdb_info_list

        select_num_list = select_num.split(",")
        if len(select_num_list) == 0 :
            continue

        # 사용자가 선택한 프로세스 번호 리스트를
        # 선택한 프로세스의 (User, PID, CPU, Command) 정보 리스트로 만들어 반환합니다.
        mon_hdb_info_list = []
        for select_num in select_num_list :
            index = int(select_num) - 1
            mon_hdb_info_list.append(hdb_info_list[index])
        return mon_hdb_info_list

def get_user_input() :      # 모니터링 조건(시간 단위, CPU 사용률 범위)을 지정하기 위해 사용자 입력을 받습니다.
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

def monitoring(mon_hdb_info_list, sleep_time, min_cpu_usage, max_cpu_usage) :       # 선택한 프로세스를 모니터링
    while True :
        hdb_info_list = get_HDB_Info()
        alert_list = []
        for mon_info in mon_hdb_info_list :
            mon_user = mon_info[0]
            mon_pid = mon_info[1]
            mon_cmd = mon_info[len(mon_info) - 1]
            for (user, pid, cpu, cmd) in hdb_info_list :
                # 모니터링 조건에서 사용자가 선택한 리스트가 아니면 모니터링에서 제외합니다.
                if user != mon_user or pid != mon_pid or cmd != mon_cmd :
                    continue
                
                # 모니터링 조건에서 사용자가 입력한C PU의 사용 범위에 맞는지 확인합니다.
                if cpu >= min_cpu_usage and cpu <= max_cpu_usage :
                    continue

                # CPU 사용 범위에서 벗어나면 사용자에게 알려줄 문제 프로세스 리스트에 추가합니다.
                alert_list.append((user, pid, cpu, cmd))

        if len(alert_list) > 0 :
            print "\n\n*********************[ 문제가 발견된 프로세스 ]**********************\n"
            print "\tUser\tPID\tCPU\tCOMMAND"
            print "\t" + ("-" * 40)
        for (user, pid, cpu, cmd) in alert_list :
            print "\t%s\t%s\t%s\t%s" % (user, pid, cpu, cmd)
        if len(alert_list) > 0 :
            input_yn = raw_input("\n재시작하시겠습니까? [y/n] : ")
            if input_yn == "y" or input_yn == "Y" :
                print "모니터링을 종료하고 재시작합니다..."
                exec_bash("HDB stop;HDB start")
                break
            else :
                print "모니터링을 계속 수행합니다."

        sys.stdout.write("...")
        sys.stdout.flush()
        sleep(sleep_time)

if __name__ == "__main__":
    # 모니터링 조건 입력
    mon_hdb_info_list = get_monitoring_input()
    sleep_time, min_cpu_usage, max_cpu_usage = get_user_input()

    # 모니터링 실행
    monitoring(mon_hdb_info_list, sleep_time, min_cpu_usage, max_cpu_usage)
