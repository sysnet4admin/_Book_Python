#!/bin/env python
#-*- coding: utf-8 -*-

from smtp import send_mail
from ucsm_backup_n_import import ucsm_config_backup
from ucsm_backup_n_import import ucsm_config_import
import time
import os

def get_config_file(file_dir, ucsm_ip) :
    # 환경 파일 경로를 가져옵니다.
    now = time.localtime()
    time_str = "%04d%02d%02d_%02d%02d%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    original_name = ucsm_ip+"_"+"config-all.xml"
    new_name = time_str + "_" + original_name
    
    original_path = file_dir + "/" + original_name
    new_path = file_dir + "/" + new_name
    os.rename(original_path, new_path)
    return new_path

if __name__ == "__main__":
    ucsm_ip = raw_input("백업 또는 복원할 UCS 매니저의 IP를 입력해 주세요 : ")
    print "\n"+"=-"*30
    print "1. 설정 파일 백업"
    print "2. 설정 파일 복원"
    print "3. 설정 파일 백업 및 메일 전송"
    print "-="*30+"\n"
    
    while True:
        select = raw_input("작업을 선택해 주세요 : ")
        if select =='1':
            ucsm_config_backup(ucsm_ip,'ucspe','ucspe')
            break
        elif select =='2':
            ucsm_config_import(ucsm_ip,'ucspe','ucspe')
            break
        elif select =='3':
            host = <SMTP 호스트 주소>
            port = 465      # SMTP 포트 : SSL로 보낼 때는 465, TLS로 보내려면 587
            login_id = <SMTP 호스트 주소에 접속할 아이디>
            login_pw = <SMTP 호스트 주소에 접속할 아이디의 비밀번호>
            
            sender_addr = <보내는 사람 메일 주소>
            reciever_addr = raw_input("받는 사람 메일 주소를 입력해 주세요 :")
            subject = "[알림] %s의 설정 백업 파일이 도착했습니다." % ucsm_ip

            ucsm_config_backup(ucsm_ip,'ucspe','ucspe')
            
            config_file = get_config_file("c:/py/config", ucsm_ip)
            attach_list = []
            attach_list.append(config_file)
            send_mail(host, port, login_id, login_pw,
                      sender_addr, reciever_addr, subject, attach_list)
            print "%s를 %s로 전송했습니다." %(config_file,reciever_addr)
            os.remove(config_file)
            break
        elif select =='exit':
            break
        else:
            print "1-3이 아닌 값입니다. 프로그램을 종료하시려면 exit를 입력하세요 "
            continue
