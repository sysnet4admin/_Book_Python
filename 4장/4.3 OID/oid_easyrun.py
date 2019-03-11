#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import PIPE

def exec_cmd(cmd) :
    p = Popen(cmd, shell=True)
    p.wait()
    
def already_setup() :
    p = Popen("rpm -qa | grep net-snmp-utils", shell=True, stdout = PIPE)
    (ret, err) = p.communicate()
    
    if ret.strip()== "":
        return False
    return True

def setup(default_setupYN) :
    setupYN = raw_input(
        "snmpwalk 유틸리티 패키지를 설치하시겠습니까? (Y/N) [%s]:" %default_setupYN  )
    if (setupYN !='Y' and setupYN != 'y' and setupYN !='N' and setupYN != 'n'):
        setupYN = default_setupYN 

    if (setupYN =='Y' or setupYN == 'y'):
        exec_cmd("yum install -y net-snmp-utils")
        print "*** 설치를 완료했습니다 ***"
        
    # 재정의된 설정값 반환
    return setupYN
        
def snmpwalk(default_version, default_community):
    version = raw_input("Version [%s]:" % default_version )
    if (version ==''):
        version = default_version     

    community = raw_input("Community [%s] :" % default_community )
    if (community ==''):
        community = default_community

    ip = raw_input("IP Address :")
    oid = raw_input("OID :")
        
    exec_cmd("snmpwalk -v %s -c %s %s %s" % (version, community, ip, oid))
    
    # 재정의된 설정값 반환
    return (version, community, ip, oid)
    
if __name__ == "__main__":
    setupYN = 'Y'
    version = '2C'
    community = 'public'

    print "OID 요청을 시작합니다."
    if already_setup() == False :
        setupYN = setup(setupYN)
    else :
        print "snmpwalk 유틸리티 패키지가 이미 설치돼 있습니다."

    # 설치를 완료한 경우(이미 설치되어 설치 단계를 스킵한 경우 포함) 실행됨
    if (setupYN =='Y' or setupYN == 'y'):
        snmpwalk(version, community)
