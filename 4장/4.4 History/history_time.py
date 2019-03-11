#!/bin/env python
#-*- coding: utf-8 -*-

from history_all import *
import datetime

def get_datetime(date_str) :
    # 문자열 형식의 날짜를 datetime 형식으로 변환
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def history_by_date(history_list, start_date, end_date) :
    # 특정 시간 범위의 명령어 실행 이력만 추출해서 반환
    cmd_list = []
    for h in history_list :
        history_date = get_datetime(h[0])
        if(history_date >= start_date and history_date <= end_date) :
            cmd_list.append(h)
    return cmd_list    

if __name__ == "__main__":
    # 사용자에게 시간대를 입력받습니다.
    print "어느 시간에 실행한 명령어를 조회하시겠습니까?"
    input_date = raw_input("년-월-일 시각을 입력하세요(예, 2016-08-11 14) :")
    input_date = input_date + ":00:00"
    
    date = get_datetime(input_date)
    start_date = date - datetime.timedelta(hours=1)     # 입력 시각 1시간 전
    end_date = date + datetime.timedelta(hours=1)       # 입력 시각 1시간 후

    print start_date, "~", end_date, "동안 입력된 명령어"
    print "-" * 70

    accounts = get_accounts()
    for account in accounts :
        history_list = history(account)
        if len(history_list) == 0:         # 계정에 이력 정보가 없으면 건너뜀
            continue

        # history_by_date 함수를 이용해 계정별로 특정 시간대에 입력한 명령어 리스트를 출력합니다.
        # 입력한 시각을 기준으로 앞/뒤 1시간 사이의 이력 정보를 확인
        history_list = history_by_date(history_list, start_date, end_date)
        if len(history_list) == 0: 
            continue

        # 이력 정보가 확인되면 출력
        print "계정 :", account
        for h in history_list :
            print "\t%s\t%s" % h
        print "-" * 70
