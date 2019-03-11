#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import *
import platform

def get_ipmi(args):
    if platform.system() == "Windows" :
        cmd = "ipmiutil " + args
    else :
        cmd = "ipmitool " + args
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def get_server_input() :
    ip = raw_input ("서버 관리 모듈 IP를 입력하세요 :")
    id = raw_input ("관리자 ID를 입력하세요 :")
    pw = raw_input ("암호를 입력하세요 :")
    if platform.system() == "Windows" :
        args = "-N %s -J 3 -U %s -P %s" % (ip, id, pw)
    else :
        args = "-I lanplus -H " + ip + " -U " + id + " -P " +pw
    return (args, ip, id, pw)

if __name__ == "__main__":
    (args, ip, id, pw) = get_server_input()

    print get_ipmi( args + ' fru print | grep "Product Name"')
    print get_ipmi( args + ' fru print | grep "Chassis Serial"')
