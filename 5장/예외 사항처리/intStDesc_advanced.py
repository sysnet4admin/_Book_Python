#!/bin/env python
#-*- coding: utf-8 -*-

try :
    from cli import cli
except :
    try : 
        from cisco import cli
    except :
        print "cli 함수를 이용하기 위한 모듈이 설치되어 있지 않습니다."
import time

def bef_run():
    now = time.localtime()
    st= "%04d%02d%02d_%02d%02d%02d"%(now.tm_year,  now.tm_mon, now.tm_mday,
                                      now.tm_hour,  now.tm_min, now.tm_sec)
    cli("show interface status >> bootflash:cdp-history/%s_intStaNdesc.txt"%st)
    cli("show interface description >> bootflash:cdp-history/%s_intStaNdesc.txt"%st)

if __name__ == '__main__':
    bef_run()
