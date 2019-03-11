#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
from subprocess import Popen
from subprocess import PIPE
import datetime
import time
import shutil
import os
import sys

def write_brief(brief_path) :
    # show interface brief 명령어를 실행해 결과를 파일에 작성
    ret = cli("show interface brief")
    f = open(brief_path, "w")
    f.write(ret)
    f.close()

def get_diff_data(path1, path2) :
    # diff 명령어를 실행해 두 파일을 비교함. 변경 전/후 데이터를 튜플 형태로 반환
    p = Popen("diff --context %s %s" % (path1, path2), shell=True, stdout=PIPE)
    (ret, err) = p.communicate()

    ret = ret.strip()
    if ret == "" :
        return None
        
    ret = ret.split("***************")[1]       # '**************' 이후의 데이터 추출
    ret = ret.split("--- ")                     # '--- 줄 번호 ----' 이후는 변경된 데이터이므로 이 문자열로 분할
    ret_before = ret[0]                         # 앞의 데이터는 변경 전 데이터
    ret_after = ret[1]                          # 뒤의 데이터는 변경 후 데이터
    return (ret_before, ret_after)

def get_change_data_list(ret) :
    # <두 파일의 변경 전후 데이터를 바탕으로 인터페이스 번호, 실제 변경된 줄의 전/후 정보 추출
    (ret_before, ret_after) = ret
    before_data_list = []
    for line in ret_before.split("\n") :
        eth_index = line.find("! Eth1")                 # 변경된 줄 찾기
        if eth_index == 0 :
            eth_num = line.split()[1].split('/')[1]     # 변경된 줄의 인터페이스 번호 찾기
            before_data_list.append((eth_num, line[2: len(line)]))  # "!"를 제거한 변경 전 데이터 추출

    changed_data_list = []
    for (eth_num, before_line)in before_data_list :     # 변경된 인터페이스 번호로
        idx = ret_after.find("! Eth1/"+ eth_num)        # 변경 후 데이터에서 탐색
        enter_idx = ret_after.find("\n", idx)
        after_line = ret_after[idx + 2 : enter_idx]     # "! "를 제거한 변경 후 데이터 추출

        # (변경된 인터페이스 번호, 변경 전 데이터 내용, 변경 후 데이터 내용)의 튜플 적재
        changed_data_list.append((eth_num, before_line, after_line))
    return changed_data_list

def print_run_conf(changed_data_list) :
    # show running-config interface 명령으로 변경된 인터페이스의 현재 정보를 출력
    if len(changed_data_list) == 0 :
        print "변경된 데이터가 없습니다."    

    for (eth_num, before_line, after_line) in changed_data_list :
        print "-" * 10, ("Eth1/%s 정보" % eth_num), "-" * 10
        print "[ 변경 전 인터페이스 간략 정보 ]"
        print "  ", before_line
        print "[ 변경 후 인터페이스 간략 정보 ]"
        print "  ", after_line
        print "[ 현재 인터페이스 구성 정보 ]"
        run_conf = cli("show running-config interface ethernet 1/%s" % eth_num)
        for line in run_conf.split("\n") :
            if line == "" :
                continue
            elif line.startswith("!Command:") or line.startswith("!Time:"):
                continue
            elif line.startswith("version ") :
                continue
            print line
        print "-" * 30    

if __name__ == '__main__':
    term = input("몇 초 단위로 비교하시겠습니까? : ")
    count = input("몇 번 비교하시겠습니까? : ")

    brief_dir = "/bootflash/tmp"
    if not os.path.isdir(brief_dir) :
        os.mkdir(brief_dir)
        
    cnt = 1
    while cnt <= count :
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds = term)
        now = datetime.datetime.now()

        brief_path1 = "/bootflash/tmp/brief.txt"
        brief_path2 = "/bootflash/tmp/brief2.txt"        

        # 최초 인터페이스 정보를 brief.txt에 기록합니다.
        write_brief(brief_path1)
            
        print cnt, "차 비교 중입니다."
        while now <= end_time:
            sys.stdout.write(".")
            sys.stdout.flush()        
            time.sleep(1) # 1초 단위로 .을 출력
            
            now = datetime.datetime.now()    

        # 시간이 지난 후의 인터페이스 정보를 brief2.txt에 기록합니다.
        write_brief(brief_path2)

        # 최초 인터페이스와 시간이 지난 후의 인터페이스 정보를 diff로 비교
        ret = get_diff_data(brief_path1, brief_path2)
        if ret == None :
            print "\n#### 변경된 정보 출력 (%d 번째) ####" % cnt
            print "변경된 데이터가 없습니다."
            cnt = cnt + 1
            continue
        
        changed_data_list = get_change_data_list(ret)
        
        print "\n#### 변경된 정보 출력 (%d 번째) ####" % cnt
        print_run_conf(changed_data_list)       # 변경된 인터페이스의 상세 정보 출력
            
        cnt = cnt + 1

    shutil.rmtree("/bootflash/tmp")
