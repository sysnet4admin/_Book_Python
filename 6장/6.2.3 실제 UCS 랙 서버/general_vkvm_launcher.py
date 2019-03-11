#!/bin/env python
# -*- coding: utf-8 -*-

from subprocess import os

def vKVM_launcher(cimc_ip,c_user,c_password):
    print "%s에 vKVM에 접속합니다."%cimc_ip
    os.chdir('c:\py\kvm')
    cmd = 'launchkvm.bat -u %s -p %s -h %s'%(c_user,c_password,cimc_ip)
    os.system(cmd)
    
if __name__ == "__main__":
    cimc_ip = raw_input("vKVM에 접속할 랙 서버 매니저의 IP를 입력해 주세요 : ")
    c_user = raw_input("관리자 ID를 입력하세요 : ")
    c_password = raw_input("암호를 입력하세요 : ")
    vKVM_launcher(cimc_ip,c_user,c_password)
