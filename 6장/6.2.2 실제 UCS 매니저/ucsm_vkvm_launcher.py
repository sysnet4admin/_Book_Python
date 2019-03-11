#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucskvmlaunch import ucs_kvm_launch

def vKVM_launch(ucsm_ip,user,password,chassis,blade):
    handle = UcsHandle(ucsm_ip,user,password)
    handle.login()
    mo = handle.query_dn("sys/chassis-{0}/blade-{1}".format(chassis,blade))
    print mo
    ucs_kvm_launch(handle, blade=mo)
    handle.logout()

if __name__ == "__main__":
    ucsm_ip = raw_input("UCS 매니저 IP를 입력하세요 : ")
    user = raw_input("관리자 ID를 입력하세요 : ")
    password = raw_input("암호를 입력하세요 : ")
    chassis = raw_input("접속할 샤시 번호를 입력하세요 : ")
    blade = raw_input("접속할 블레이드 서버 번호를 입력하세요 : ")
    vKVM_launch(ucsm_ip,user,password,chassis,blade)
