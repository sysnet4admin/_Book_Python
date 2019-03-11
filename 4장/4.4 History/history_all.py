#!/bin/env python
#-*- coding: utf-8 -*-

from user_list import *
from datetime import datetime

def remove_num(string):
    tmp = string.strip()            # 예를 들어 string 이 ' 10 dir'라고 한다면 strip()을 적용한 후 '10 dir'이 되고,
    first_space = tmp.find(" ")     # '10 dir'에서 첫 번째 공백은 10뒤에 있습니다.
    if first_space < 0 :
        return string
    tmp = tmp[first_space : len(tmp)]
    return tmp.strip()

def history(account) :
    # 이력 조회를 위한 명령어 실행
    ret = exec_cmd("sudo -H -u %s bash -i -c 'history -r;history'" % account)
    ret_split = ret.strip().split("\n")
    i = len (ret_split) - 1

    # 실행 결과로부터 (명령어 수행 시간, 명령어) 형식의 이력 정보를 최신부터 추출해서 반환
    history_list = []
    while i > 0 :
        cmd = ret_split[i].strip()
        timestamp = ret_split[i-1]
        i = i - 2
    
        if timestamp.find("#") < 0 :
            break

        # 명령어를 cmd 변수에, 타임스탬프를 timestamp 변수로 추출
        cmd = remove_num(cmd)
        timestamp = remove_num(timestamp)

        timestamp = timestamp.replace("#", "")
        date = str(datetime.fromtimestamp(float(timestamp)))
        history_list.append((date, cmd))
    return history_list
                       
if __name__ == "__main__":
    accounts = get_accounts()
    for account in accounts :
        print "계정 :", account
        history_list = history(account)
        if len(history_list) == 0:
            print "\t기록된 이력 없음"
        for h in history_list :
            print "\t%s\t%s" % h
        print "-" * 70
