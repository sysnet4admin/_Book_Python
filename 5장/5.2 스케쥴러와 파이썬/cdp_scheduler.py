#!/bin/env python
#-*- coding: utf-8 -*-

from syslog import syslog
from cli import cli,clip
import sys
import os

def dirc():
    try:
        cli("mkdir bootflash:cdp-history")
    except:
        pass

def sche_conf(day,hour,minute):
    cli("configure terminal ; no feature scheduler")
    cli("configure terminal ; feature scheduler")
    cli("configure terminal ;                       \
        scheduler job name cdp-log ;                \
        python bootflash:scripts/intStDesc.py ;     \
        python bootflash:scripts/auto_add_description_mac.py ; \
        exit")
    cli("configure terminal ;               \
        scheduler schedule name cdp-log ;   \
        job name cdp-log ;                  \
        time start now repeat %s:%s:%s"%(day,hour,minute))

def term_set():
    log_mon = 'Y'
    log_mon = raw_input("로그를 화면에 출력하겠습니까?[Y]")
    if log_mon== 'y' or log_mon == 'Y' or log_mon =='':
        cli('terminal monitor')

def show_set():
    set_mon = 'Y'
    set_mon = raw_input("설정된 스케줄러를 확인하시겠습니까?[Y]")
    if set_mon== 'y' or set_mon == 'Y' or set_mon =='':
        clip('show scheduler schedule')

if __name__ == '__main__':
    day = sys.argv[1]
    hour = sys.argv[2]
    minute = sys.argv[3]
    dirc()
    sche_conf(day,hour,minute)
    term_set()
    show_set()
    syslog(2,'스케줄러가 cdp-log를 bootflash:cdp-history디렉터리에 %s일 %s시간 %s분 \
간격으로 기록합니다'%(day,hour,minute))
