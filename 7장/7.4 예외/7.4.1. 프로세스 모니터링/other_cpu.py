#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import PIPE
from subprocess import call
from syslog import syslog
import os
import ConfigParser
import sys
import shutil

cfg_path = "./cpu_monitoring.cfg"
conf_list = {}
def get_config() :          # 환경 설정 파일을 가져옵니다.
    config = ConfigParser.RawConfigParser()
    if os.path.exists(cfg_path) :
        config.read(cfg_path)
    return config

def save_cfg(config):       # 환경 설정 파일을 저장합니다.
    configfile = open(cfg_path, "wb")
    config.write(configfile)
    configfile.close()

def add_cfg_environment(key, value):        # 환경 설정 파일에 환경 정보를 추가합니다. [Environment] 섹션에 CPU 사용률을 저장합니다.
    config = get_config()
    if (config.sections().count("Environment") == 0 ) :
        config.add_section("Environment")
    config.set("Environment", key, value)
    save_cfg(config)

def add_cfg_proc(user, pid, command):       # 환경 설정 파일에 선택한 보호 프로세스를 추가합니다. [프로세스ID] 섹션에 PID와 User를 저장합니다.
    config = get_config()
    if (config.sections().count(pid) == 0 ) :
        config.add_section(pid)
    config.set(pid, user, command)
    save_cfg(config)

def add_cfg_additional_proc(proc_command):  # 환경 설정 파일에 추가로 등록할 보호 프로세스를 추가합니다. [AdditionalProcess] 섹션에 프로세스명을 저장합니다.
    config = get_config()
    if (config.sections().count("AdditionalProcess") == 0 ) :
        config.add_section("AdditionalProcess")
    if proc_command != "" :
        config.set("AdditionalProcess", proc_command, proc_command)
    save_cfg(config)

def load_cfg():                             # 환경 설정의 내용 읽어서 보호 프로세스 및 모니터링 설정을 가져옵니다.
    global conf_list
    config = get_config()
    protect_process_list = []
    if config != None :
        sections = config.sections()
        for section in sections :
            if section == "Environment" :
                conf_list["max_cpu_usage"]= config.get(section, "max_cpu_usage")
            elif section == "AdditionalProcess" :
                procs = config.items(section)
                for (name, value) in procs :
                    protect_process_list.append(("0", "", name))
            else:
                procs = config.items(section)
                for (user, command) in procs :
                    protect_process_list.append((section, user, command))
    conf_list["ProtectProcess"] = protect_process_list

def exec_bash(cmd) :
    # 명령어를 실행한 결과를 반환합니다.
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret.strip()

def get_proc_status_list() :
    # ps aux --sort -pcpu | head -n 21 명령어의 실행 결과로부터 필요한 데이터 추출
    cmd = "ps aux --sort -pcpu | head -n 21"        # CPU 사용률이 높은 20개의 프로세스 조회(헤더 포함 21줄이 조회됩니다.)
    ret = exec_bash(cmd)
    proc_status_list = []
    for i, line in enumerate(ret.split("\n")) :
        if i == 0 :                     # 첫 번째 줄은 헤더 정보입니다.
            continue
        data_list = line.split()        # 한 줄을 공백으로 나눕니다.
        user = data_list[0]             # 첫 번째 데이터는 사용자
        pid = data_list[1]              # 두 번째 데이터는 프로세스 ID
        cpu = data_list[2]              # 세 번째 데이터는 CPU 사용률
        command = data_list[10]         # 열한 번째 데이터부터 그 뒤까지는 커맨드
        column_idx = 11
        while column_idx < len(data_list):
            command = command + " " + data_list[column_idx]
            column_idx = column_idx + 1
        proc_status_list.append((user, pid, float(cpu), command))   # (user, 프로세스 ID, cpu 사용률, Command) 튜플을 리스트에 적재
    return proc_status_list                                         # 튜플 리스트를 반환

def print_proctect_list (protect_proc_list, other_processes) :      # 보호할 프로세스 리스트를 출력합니다.
    if conf_list.get("ProtectProcess") == None :
        load_cfg()
    print " ** PID <1-100> 은 기본으로 보호됩니다. ** "       # 1 ~100의 프로세스 ID는 기본 보호 대상
    print " 101 이상의 선택된 보호 프로세스 : "
    print "  ", ("-" * 40)
    print "\tPID\tUSER\tCOMMAND"
    for (user, pid, command) in protect_proc_list:
        if int(pid) >100 :
            print "\t%s\t%s\t%s"%(pid, user, command)
    for proc in other_processes:
        print "\t \t \t%s"%proc
    print "  ", ("-" * 40)

def get_monitoring_input() :        # 필터 조건과 모니터링할 프로세스를 선택하기 위해 사용자 입력을 받습니다.
    global conf_list
    i = 1
    print "\n***********[ 현재 가장 CPU를 많이 점유하는 프로세스 20 개 ]************\n"
    print "\tNum\tUser\tPID\tCPU\tCOMMAND"
    print "\t" + ("-" * 40)
    proc_status_list = get_proc_status_list()
    for (user, pid, cpu, cmd) in proc_status_list :
        print "\t%d)\t%s\t%s\t%s\t%s" % (i, user, pid, cpu, cmd)
        i = i + 1
    print "\n" + ("*" * 70)
    print "1. 보호할 프로세스 번호를 선택하세요. (콤마로 여러 개 선택 가능)"
    print "\t입력하지 않으면 모두 보호하고, 0을 입력하면 모두 보호하지 않습니다"
    print "\t예) 1번과 2번을 선택할 때 입력값 : 1,2"
    protect_proc_list = []
    select_num = ""
    try :
        select_num = raw_input("\t보호할 번호를 선택하세요 : ")
    except :
        select_num == ""
    if select_num == "":
        for i, (user, pid, cpu, command) in enumerate(proc_status_list):
            protect_proc_list.append((user, pid, command))
    elif not select_num == "0" :
        for select_num in select_num.split(",") :
            try :
                index = int(select_num) - 1
                (user, pid, cpu, command) = proc_status_list[index]
                protect_proc_list.append((user, pid, command))
            except :
                continue
    print "\n2. 위의 선택 사항에는 없으나, 추후 발생할 프로세스에 대해서 보호하고자 하는 이름을 입력하세요."
    print "\t입력하지 않으면 추가로 보호하지 않으며, 여러 개 입력 가능합니다."
    print "\t예) 'alpha' 프로세스와 'omega' 프로세스를 모니터링할 때 입력값 : alpha,omega"
    other_processes = raw_input("\t추가 보호 대상 프로세스 : ")
    other_processes = other_processes.strip()
    other_proc_list = other_processes.split(",")
    print " ** 선택하지 않은 모든 프로세스들은 모니터링 대상입니다. **"
    print_proctect_list (protect_proc_list, other_proc_list)
    print "\n3. 모니터링할 프로세스의 최대 CPU 사용률을 지정해주세요."
    max_cpu_usage = 100
    try :
        max_cpu_usage = input("\t소수점으로 입력할 수 있습니다. [100] : ")
    except :
        max_cpu_usage = 100
    conf_list["max_cpu_usage"] = max_cpu_usage
    return (protect_proc_list, other_proc_list)

def get_user_input() :      # 모니터링 시간 단위를 지정하기 위해 사용자 입력을 받습니다.
    sche_seconds = 60
    try :
        sche_seconds = input("\n4. 몇 초 간격으로 스케줄링하시겠습니까?(5,10,15,30,60초)[60] : ")
        if sche_seconds not in (5,10,15,30,60):
            raise NotImplementedError
    except :
        if sche_seconds == 60 :
            pass
        else :
            print "입력한 값은 %d 입니다. " % sche_seconds
            print "허용 값이 아니므로 기본값(60초)으로 설정됩니다."
            sche_seconds = 60
    return sche_seconds

def show_set():             # 스케줄러 설정 상태를 확인합니다.
    set_mon = 'Y'
    set_mon = raw_input("설정된 스케줄러를 확인하시겠습니까? [Y/n] : ")
    if set_mon== 'y' or set_mon == 'Y' or set_mon =='':
        print "설정된 crontab은 다음과 같습니다."
        print "-" * 50
        print exec_bash('crontab -l')
        print "-" * 50
        print "\n현재의 cron 데몬의 상태는 다음과 같습니다."
        print "-" * 50
        print exec_bash('systemctl status crond')
        print "-" * 50
            
def sche_conf(seconds):     # 스케줄러 설정
    active_user = exec_bash('whoami').split("\n")[0]
    active_path = exec_bash('pwd').split("\n")[0]
    shutil.copy(cfg_path, "/%s/cpu_monitoring.cfg"%active_user)
    crn_cmd = "python %s/other_cpu.py"%active_path

    if seconds == 60:       # 크론 정책에 따라 60초는 sleep을 사용하지 않아야 함
        cmd = "* * * * * %s \n" %crn_cmd
    else:
	cmd = "* * * * * %s" %crn_cmd
	rotation = 60/seconds-1
	for i in range(rotation):
	    cmd += " &sleep %d; %s " %(seconds,crn_cmd)
        cmd +=" \n"

    with open("./cron_%s.conf"%active_user,"w") as out:
        out.write(cmd)
    exec_bash('crontab cron_%s.conf'%active_user)
        
def get_monitoring_list () :        # 모니터링할 리스트를 가져옵니다.
    if conf_list.get("ProtectProcess") == None :
        load_cfg()
    monitoring_list = []
    for (user, pid, cpu, cmd) in get_proc_status_list() :       # CPU 사용률이 높은 20개의 프로세스
        is_protect_proc = False
        for (pt_pid, pt_user, pt_cmd) in conf_list["ProtectProcess"]:
            if pt_user == "" and cmd.find(pt_cmd) >= 0 :
                is_protect_proc = True
            if user == pt_user and pid == pt_pid and cmd == pt_cmd :
                is_protect_proc = True
        if not is_protect_proc :
            monitoring_list.append((user, pid, cpu, cmd))       # 보호 프로세스가 아니면 모니터링 대상임
    return monitoring_list
    
def monitoring() :                  # 보호된 프로세스 외에 CPU 사용률이 높은 프로세스를 중지시킵니다.
    load_cfg()
    max_cpu_usage = 50
    try :
        max_cpu_usage = float(conf_list["max_cpu_usage"])
    except :
        max_cpu_usage = 50
    for (user, pid, cpu, cmd) in get_monitoring_list():
        if cpu <= max_cpu_usage :
            continue
        if int(pid) <= 100 :
            continue
        exec_bash("kill -FPE %s" % pid)     # 프로세스를 종료시킴
        core_path = "/var/crash/core-%s-%s" % (cmd.split()[0], pid)
        syslog(2, "PID %s(%s) 프로세스의 CPU 사용률이 %s로 종료되었습니다. 코어파일위치 : %s" %(pid,cmd,cpu,core_path))        # 시스템 로그 작성
    
if __name__ == "__main__":
    if len(sys.argv) > 1 :
        option = sys.argv[1]
        if option == "conf" and os.path.exists(cfg_path) :
            os.remove(cfg_path)

    # 환경 설정 파일이 없으면 모니터링을 위한 환경 설정 정보를 입력받습니다.
    if not os.path.exists(cfg_path) :        
        (protect_proc_list, additional_proc_list) = get_monitoring_input()
        add_cfg_environment("max_cpu_usage", conf_list["max_cpu_usage"])
        for (user, pid, command) in protect_proc_list :
            add_cfg_proc(user, pid, command)
        for other_proc in additional_proc_list :
            add_cfg_additional_proc(other_proc.strip())
        print "\n모니터링 환경설정이 완료되었습니다 : %s" % cfg_path
        
        sche_seconds = get_user_input()
        sche_conf(sche_seconds)
        show_set()
    else :
        monitoring()
