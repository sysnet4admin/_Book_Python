#!/bin/env python
#-*- coding: utf-8 -*-

from copp_check import get_drop_packet
from copp_check import get_policy_class_map
from copp_check import get_copp_status
from time import sleep
from syslog import syslog

def get_term_str(seconds) :
    # 초를 문자열(x시 x분 x초)로 변경
    hours = check_term / 3600
    minutes = (check_term % 3600) / 60
    seconds = check_term % 60

    check_term_str = ""
    if hours > 0 :
        check_term_str = "%d시 " % hours
    if minutes > 0 :
        check_term_str = check_term_str + ("%d분 " % minutes)
    if seconds > 0 :
        check_term_str = check_term_str + ("%d초 " % seconds)

    return check_term_str

def subtract(packet_list1, packet_list2):
    i = 0
    change_list = []
    while i < len(packet_list1) :
        change_list.append(packet_list2[i] - packet_list1[i])
        i = i + 1
    return change_list

def write_syslog(changed_pk_list, check_term_str) :
    class_list = get_policy_class_map()

    i = 0
    packet_changed = False
    for changed_pk in changed_pk_list :
        if changed_pk != 0 :
            log = "%s에서 %s동안 %d packets이 드랍이 발생하였습니다." % (
                class_list[i], check_term_str, changed_pk)
            packet_changed = True
            syslog(2, log)
        i = i + 1

    if packet_changed :
        write_syslog_policy()

def write_syslog_policy() :
    copp = get_copp_status()
    if copp == "기본값" :
        log = "추가로 현재 CoPP는 시스코에서 권고하는 기본값입니다."
    else :
        log = "추가로 CoPP 정책이 기본값이 아닙니다. (현재값 : %s)" % copp
    syslog(2, log)

if __name__ == "__main__":
    check_term = 600    # 체크 시간은 초 단위로
    
    # 경과 시간을 문자열(x시 x분 x초)로 변경
    check_term_str = get_term_str(check_term)
    
    original_pk = get_drop_packet()
    sleep(check_term)
    changed_pk = subtract(original_pk, get_drop_packet())
    
    #드랍량을 syslog에 남김
    write_syslog(changed_pk, check_term_str)
