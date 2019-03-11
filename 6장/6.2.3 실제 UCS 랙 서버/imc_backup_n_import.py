#!/bin/env python
# -*- coding: utf-8 -*-

from ImcSdk import *

def cimc_config_backup(cimc_ip,c_user,c_password,cb_ftpip,cb_ftpuser,cb_password,
                       cb_passphrase):
    handle = ImcHandle()
    handle.login(cimc_ip,username=c_user,password=c_password)
    print "%s에 구성을 백업합니다"%cimc_ip
    backup_imc(handle,cb_ftpip,cimc_ip+"-config_backup.xml",protocol="ftp",
               username=cb_ftpuser, password=cb_password,passphrase=cb_passphrase)
    print "%s에 구성 백업이 %s에 %s로 완료되었습니다"%(cimc_ip,cb_ftpip,
                                        cimc_ip+"-config_backup.xml")
    handle.logout()

def cimc_config_import(cimc_ip,c_user,c_password,ci_ftpip,ci_ftpuser,ci_password,
                       ci_passphrase):
    handle = ImcHandle()
    handle.login(cimc_ip,username=c_user,password=c_password)
    print "%s에 구성 복원을 시작합니다"%cimc_ip
    import_imc_backup(handle,ci_ftpip,cimc_ip+"-config_backup.xml",protocol="ftp",
                      username=ci_ftpuser, password=ci_password,passphrase=ci_passphrase)
    print "%s에 구성 복원이 완료되었습니다"%cimc_ip
    handle.logout()

if __name__ == "__main__":
    cimc_ip = raw_input("백업 또는 복원할 랙 서버 매니저의 IP를 입력해 주세요 : ")
    c_user = raw_input("관리자 ID를 입력하세요 : ")
    c_password = raw_input("암호를 입력하세요 : ")
    
    print "\n"+"=-"*10
    print "1. 구성 파일 백업"
    print "2. 구성 파일 복원"
    print "-="*10+"\n"

    while True:
        select = raw_input("작업을 선택해 주세요 : ")
        if select =='1':
            cb_ftpip = raw_input("백업 파일을 저장할 FTP 주소를 입력하세요 : ")
            cb_ftpuser = raw_input("FTP 사용자 이름을 입력하세요 : ")
            cb_password = raw_input("FTP 사용자 암호를 입력하세요 : ")
            cb_passphrase = raw_input("새로 생성될 백업 파일의 암호를 입력하세요 : ")
            cimc_config_backup(cimc_ip,c_user,c_password,cb_ftpip,cb_ftpuser,
                               cb_password,cb_passphrase)
            break
        elif select =='2':
            ci_ftpip = raw_input("복원할 파일이 위치한 FTP 주소를 입력하세요 : ")
            ci_ftpuser = raw_input("FTP 사용자 이름을 입력하세요 : ")
            ci_password = raw_input("FTP 사용자 암호를 입력하세요 : ")
            ci_passphrase = raw_input("복원할 백업 파일의 암호를 입력하세요 : ")
            print "복원은 백업에 비해 다소 많은 시간이 소요되며, 일반적으로 10분에서 20분 정도 소요됩니다."
            cimc_config_import(cimc_ip,c_user,c_password,ci_ftpip,ci_ftpuser,
                               ci_password,ci_passphrase)
            break
        elif select =='exit':
            break
        else:
            print "1 또는 2가 아닌 값입니다. 프로그램을 종료하시려면 exit를 입력하세요 "
            continue
