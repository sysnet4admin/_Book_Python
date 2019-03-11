#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import PIPE

def get_ipmi(args):
    cmd = 'ipmitool ' + args
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def get_server_input() :
    ip = raw_input ("서버 관리 모듈 IP를 입력하세요 :")
    id = raw_input ("관리자 ID를 입력하세요 :")
    pw = raw_input ("암호를 입력하세요 :")
    args = '-I lanplus -H ' + ip + ' -U ' + id + ' -P ' +pw
    return args

if __name__ == "__main__":
    args = get_server_input()  

    print get_ipmi( args + ' fru print | grep "Product Name"')
    print get_ipmi( args + ' fru print | grep "Chassis Serial"')
