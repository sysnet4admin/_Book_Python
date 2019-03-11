#!/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime
from subprocess import Popen
from subprocess import PIPE
import os

def get_scp_back_dir(path) :
    # 구성 정보가 백업된 네트워크 장비 리스트를 가져옵니다.
    dir_list = []
    for dir_name in os.listdir(path) :
        if dir_name.startswith("scp_backup_from-") :
            dir_list.append(dir_name)
    dir_list.sort()
    return dir_list

def get_scp_back_date(path) :
    # 백업 파일이 작성된 날짜 리스트를 가져옵니다.
    date_list = []
    for file_name in os.listdir(path) :
        if file_name.find("-running-config-") :
            date = file_name.split("-running-config-")[1]
            date = date.split("_")[0]
            date_list.append(date)
    date_list = list(set(date_list))
    date_list.sort()
    return date_list

def get_file_date(f_name) :
    # 파일명에 포함된 날짜를 datetime 형태로 변환합니다.
    first_str = f_name.split()[0]
    str_list = first_str.split("-")
    date_str = str_list[len(str_list) -1]
    date_str = date_str[0:15]
    return datetime.strptime(date_str , '%Y%m%d_%H%M%S')

def get_file_list(file_dir, start_date, end_date) :     # 특정 날짜 구간에 작성된 구성 정보 백업 파일을 가져옵니다.
    file_list = os.listdir(file_dir)
    file_list_range = []
    for f_name in file_list :
        file_path = file_dir + "/" + f_name
        create_date = get_file_date(f_name)
        if create_date >= start_date and create_date <= end_date :
            file_list_range.append(file_path)
    file_list_range.sort()
    return file_list_range

def diff(file_path1, file_path2) :
    # diff 명령어로 두 파일을 비교합니다.
    cmd = "diff --context %s %s" % (file_path1, file_path2)
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def get_input_data() :
    # 백업 파일이 저장된 네트워크 장비 목록을 출력합니다.
    dir_path = "/var/log"
    dir_list = get_scp_back_dir(dir_path)

    print "*****[ 백업 파일이 저장된 네트워크 장비 목록 ]*****"
    if len(dir_list) == 0 :
        print "\t\t없음\n" + ("*" * 50)
        return None

    for i, dir_name in enumerate(dir_list) :
        print "\t%d)%s" % ((i+1), dir_name.split("scp_backup_from-")[1])
    print ("*" * 50) + "\n"

    # 네트워크 장비 목록 중에서 비교할 장비를 선택합니다.
    try :
        select_num= input("비교할 네트워크 장비를 선택해 주세요 [1-%d]: " % len(dir_list))
        if select_num <= 0 or select_num > len(dir_list) :
            select_num = 1
        dir_path = dir_path + "/" + dir_list[select_num - 1]
    except : 
        dir_path = dir_path + "/" + dir_list[0]

    print ">>> %s가 선택되었습니다" % dir_path.split("scp_backup_from-")[1]

    # 백업 파일이 저장된 날짜 목록을 출력합니다.
    date_list = get_scp_back_date(dir_path)
    print "*****[ 백업 파일이 저장된 날짜 목록 ]*****"
    if len(date_list) == 0 :
        print "\t\t없음\n" + ("*" * 50)
        return None

    for i, date in enumerate(date_list) :
        print "\t%d)%s" % ((i+1), date)
    print ("*" * 50) + "\n"

    # 백업 파일 중 비교를 시작할 구간을 선택합니다.
    print "\n선택한 기간 동안의 백업 파일을 비교합니다."
    while True :
        select_num = input("시작 기간을 선택하세요 [1-%d]: " % len(date_list))
        select_num2 = input("종료 기간을 선택하세요 [%d-%d]: " % (select_num, len(date_list)))
        select_date = date_list[select_num - 1]
        select_date2 = date_list[select_num2 - 1]
        start_date = datetime.strptime(select_date + "_000000", '%Y%m%d_%H%M%S')
        end_date = datetime.strptime(select_date2 + "_235959", '%Y%m%d_%H%M%S')
        return (dir_path, start_date, end_date)     # 네트워크 장비 백업 파일과 비교할 날짜 구간을 반환합니다.
    
if __name__ == "__main__":
    # 사용자 입력을 받아서, 비교할 네트워크 장비와 비교할 날짜 구간을 선택받습니다.
    input_data = get_input_data()

    # 사용자 입력을 바탕으로 파일을 비교
    if input_data != None :
        (dir_path, start_date, end_date) = input_data
        scp_file_list = get_file_list(dir_path, start_date, end_date)        
        if len(scp_file_list) == 0 :
            print "선택한 기간 동안 백업된 파일이 없습니다."
        elif len(scp_file_list) == 1 :
            print "선택한 기간 동안 백업된 파일이 1건이어서 변경 사항을 비교할 수 없습니다."
        else :
            i = 0
            while i < len(scp_file_list) - 1 :
                cmd_result = diff(scp_file_list[i], scp_file_list [i+1])
                print cmd_result
                print "=" * 50
                i = i + 1
