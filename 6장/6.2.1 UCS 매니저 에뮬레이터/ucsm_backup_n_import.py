#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucsbackup import backup_ucs
from ucsmsdk.utils.ucsbackup import import_ucs_backup

def ucsm_config_backup(ucsm_ip,user,password):
    handle = UcsHandle(ucsm_ip,user,password)
    handle.login()
    backup_ucs(handle,backup_type="config-all", file_dir=r"C:\py\config",file_name=ucsm_ip+"_"+"config-all.xml")
    handle.logout()
    
def ucsm_config_import(ucsm_ip,user,password):
    handle = UcsHandle(ucsm_ip,user,password)
    handle.login()
    import_ucs_backup(handle, file_dir=r"C:\py\config",file_name=ucsm_ip+"_"+"config-all.xml")
    handle.logout()

if __name__ == "__main__":
    ucsm_ip = raw_input("백업 또는 복원할 UCS 매니저의 IP를 입력해 주세요 : ")
    print "\n"+"=-"*30
    print "1. 설정 파일 백업"
    print "2. 설정 파일 복원"
    print "-="*30+"\n"
    
    while True:
        select = raw_input("작업을 선택해 주세요 : ")
        if select =='1':
                ucsm_config_backup(ucsm_ip,'ucspe','ucspe')
                break
        elif select =='2':
                ucsm_config_import(ucsm_ip,'ucspe','ucspe')
                break
        elif select =='exit':
                break                                   
        else:
                print "1 또는 2가 아닌 값입니다. 프로그램을 종료하시려면 exit를 입력하세요 "
                continue
