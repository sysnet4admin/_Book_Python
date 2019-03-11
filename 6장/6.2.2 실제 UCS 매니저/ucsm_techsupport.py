#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucstechsupport import get_ucs_tech_support
import time

global s
now = time.localtime()
s= "%04d%02d%02d_%02d%02d%02d_"%(now.tm_year, now.tm_mon, now.tm_mday,
                                 now.tm_hour, now.tm_min, now.tm_sec)

def fullGetTechSupport(ucsm_ip,user,password):
        print "블레이드 샤시 로그를 수집합니다"
        print "해당 수집 작업은 5분에서 20분 정도 소요될 예정입니다."
        handle = UcsHandle(ucsm_ip,user,password)
        handle.login()
        get_ucs_tech_support(handle,file_dir="/root/techsupport",file_name=s+'FI_UCSM.tar',
                             timeout_in_sec=600, remove_from_ucs=True)
        handle.logout()

def singleGetTechSupport(ucsm_ip,user,password,chassis,blade):
        print chassis+'-'+blade+"블레이드 로그를 수집합니다."
        print "해당 수집 작업은 5분에서 20분 정도 소요될 예정입니다."
        handle = UcsHandle(ucsm_ip,user,password)
        handle.login()
        get_ucs_tech_support(handle,file_dir="/root/techsupport",
                             file_name=s+'FI_BL'+chassis+'-'+blade+'.tar',
                             chassis_id=chassis,cimc_id=blade,timeout_in_sec=600,
                             remove_from_ucs=True)
        handle.logout()

if __name__ == "__main__":
        ucsm_ip = raw_input("UCS 매니저 IP 주소를 입력하세요 : ")
        user = raw_input("관리자 ID를 입력하세요 : ")
        password = raw_input("암호를 입력하세요: ")

        print "\n\t"+"#"*25
        print "\t1.블레이드 샤시 로그 수집"
        print "\t2.블레이드 서버 로그 수집"
        print "\t"+"#"*25

        while True:
                select = raw_input("\n어느 작업을 실행하시겠습니까? (1,2,exit): ")
                if select=='1':
                    fullGetTechSupport(ucsm_ip,user,password)
                    break
                elif select=='2':
                    chassis = raw_input("샤시 번호를 입력하세요 : ")
                    blade = raw_input("블레이드 번호를 입력하세요 : ")
                    singleGetTechSupport(ucsm_ip,user,password,chassis,blade)
                    break
                elif select=='exit':
                    break
                else:
                    print "-="*20
                    print "1 또는 2가 아닌 값입니다.\n프로그램을 종료하시려면 exit를 입력하세요"
                    print "=-"*20
                    continue
