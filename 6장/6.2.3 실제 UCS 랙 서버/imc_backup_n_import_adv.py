#!/bin/env python
# -*- coding: utf-8 -*-

from ImcSdk import *
from urllib2 import URLError        # 예외처리를 위해 추가 임포트됨

def conn_ip(select):
    global cimc_ip
    if select =='0':
        cimc_ip = raw_input("UCS 랙 서버 매니저의 IP를 입력해 주세요 : ")
    elif select =='1':
        cimc_ip = raw_input("백업할 UCS 랙 서버 매니저의 IP를 입력해 주세요 : ")
    elif select =='2':
        cimc_ip = raw_input("복원할 UCS 랙 서버 매니저의 IP를 입력해 주세요 : ")

def conn_auth():
    global c_user; global c_password
    c_user = raw_input("관리자 ID를 입력하세요 : ")
    c_password = raw_input("암호를 입력하세요 : ")

def ftp_conn_info(select):
    global ftp_ip; global ftp_user; global ftp_password; global ftp_passphrase
    if select =='1':
        ftp_ip = raw_input("백업 파일을 저장할 FTP 주소를 입력하세요 : ")
    elif select =='2':
        ftp_ip = raw_input("복원에 필요한 백업 파일이 저장된 FTP 주소를 입력하세요 : ")
    ftp_user = raw_input("FTP 사용자 이름을 입력하세요 : ")
    ftp_password = raw_input("FTP 사용자 암호를 입력하세요 : ")
    if select =='1':
        ftp_passphrase = raw_input("새로 생성될 백업 파일의 암호를 입력하세요 : ")
    if select =='2':
        ftp_passphrase = raw_input("암호가 걸려 있는 백업 파일의 암호를 입력하세요 : ")
    
def cimc_config_backup():
    handle = ImcHandle()

    #백업을 위해 UCS 랙 서버 접속#
    
    while True:
        try:
            handle.login(cimc_ip,username=c_user,password=c_password)
        except URLError:
            print "\n%s는 UCS 랙 서버가 아닙니다."%cimc_ip
            print "랙 서버 매니저의 정보를 확인해서 다시 입력해 주세요."
            print "-="*15
            conn_ip(select)
        except ImcException:
            print "\nUCS 랙 서버 매니저의 계정 정보가 맞지 않습니다."
            print "랙 서버 매니저의 계정 정보를 확인해서 다시 입력해 주세요."
            print "-="*15
            conn_auth()
        except :
            print "예상치 못한 오류가 발생했습니다. 관리자에게 문의하시기 바랍니다"
            break
        else:
            print "%s에 구성을 백업합니다"%cimc_ip
            break

    #백업을 위해 FTP 접속 #
        
    while True:
        try:
            backup_imc(handle,ftp_ip,cimc_ip+"-config_backup.xml",protocol="ftp",
                       username=ftp_user, password=ftp_password,passphrase=ftp_passphrase)
        except ImcValidationException:
            print "\nUCS 랙 서버 매니저의 정보가 정상적으로 백업되지 않았습니다."
            print "백업 FTP 사이트의 정보를 확인해서 다시 입력해 주세요."
            print "-="*15
            ftp_conn_info(select)
        except:     # 에러 오류 내용을 e인자로 보내고 출력함
            print "예상치 못한 오류가 발생했습니다. 관리자에게 문의하시기 바랍니다"
            break
        else:
            print "%s에 구성 백업이 %s에 %s로 완료되었습니다"%(cimc_ip,ftp_ip,
                                                cimc_ip+"-config_backup.xml")
            break
    handle.logout()

def cimc_config_import():
    handle = ImcHandle()
    while True:
        try:
            handle.login(cimc_ip,username=c_user,password=c_password)
        except URLError:
            print "\n%s는 UCS 랙 서버가 아닙니다."%cimc_ip
            print "랙 서버 매니저의 정보를 확인해서 다시 입력해 주세요."
            print "-="*15
            conn_ip(select)
        except ImcException:
            print "\nUCS 랙 서버 매니저의 계정 정보가 맞지 않습니다."
            print "랙 서버 매니저의 계정 정보를 확인해서 다시 입력해 주세요."
            print "-="*15
            conn_auth()
        except :
            print "예상치 못한 오류가 발생했습니다. 관리자에게 문의하시기 바랍니다"
            break
        else:
            print "%s에 구성 복원을 시작합니다"%cimc_ip
            print "복원은 백업에 비해 다소 많은 시간이 소요되며, 일반적으로 10분에서 20분 정도 소요됩니다."
            break    

    while True:
        try:
            import_imc_backup(handle,ftp_ip,cimc_ip+"-config_backup.xml",protocol="ftp",
                              username=ftp_user, password=ftp_password,passphrase=ftp_passphrase)
        except ImcValidationException as e:
            print e
            ftp_conn_info(select)
        except :
            print "예상치 못한 오류가 발생했습니다. 관리자에게 문의하시기 바랍니다"
            break
        else:
            print "%s에 구성 복원이 완료되었습니다"%cimc_ip
            break
        
    handle.logout()

if __name__ == "__main__":
    select ='0'
    conn_ip(select)
    conn_auth()
    print "\n"+"=-"*10
    print "1.구성 파일 백업"
    print "2.구성 파일 복원"
    print "-="*10+"\n"

    while True:
        select = raw_input("작업을 선택해 주세요 : ")
        if select =='1':
            ftp_conn_info(select)
            cimc_config_backup()
            break
        elif select =='2':
            ftp_conn_info(select)
            cimc_config_import()
            break
        elif select =='exit':
            break
        else:
            print "1 또는 2가 아닌 값입니다. 프로그램을 종료하시려면 exit를 입력하세요 "
            continue
