#!/bin/env python
# -*- coding: utf-8 -*-

from ImcSdk import *
import time

def cimc_techsupport(cimc_ip,c_user,c_password,ftp_ip,ftp_user,ftp_password):
    now = time.localtime()
    s= "%04d%02d%02d_%02d%02d%02d_"%(now.tm_year, now.tm_mon, now.tm_mday,
                                     now.tm_hour, now.tm_min, now.tm_sec)
        
    handle = ImcHandle()
    handle.login(cimc_ip,username=c_user,password=c_password)
    filename = s+handle.imc+"_techsupport.tar.gz"
    
    print "%s에 로그를 받아서 %s에 %s 파일로 저장됩니다."%(cimc_ip,ftp_ip,filename)
    
    get_imc_techsupport(handle,ftp_ip,filename,protocol="ftp",username=ftp_user,
                        password=ftp_password,timeout_sec=600,dump_xml=None)
    handle.logout()
    
if __name__ == "__main__":
    cimc_ip = raw_input("로그 수집할 랙 서버 매니저의 IP를 입력해 주세요 : ")
    c_user = raw_input("관리자 ID를 입력하세요 : ")
    c_password = raw_input("암호를 입력하세요 : ")
    print "\n로그 파일은 원격지에 저장됩니다. 이번 예제에서는 FTP에 저장하겠습니다.\n"
    ftp_ip = raw_input("로그 파일을 저장할 FTP 주소를 입력하세요 : ")
    ftp_user = raw_input("FTP 사용자 이름을 입력하세요 : ")
    ftp_password = raw_input("FTP 사용자 암호를 입력하세요 : ")
    cimc_techsupport(cimc_ip,c_user,c_password,ftp_ip,ftp_user,ftp_password)
