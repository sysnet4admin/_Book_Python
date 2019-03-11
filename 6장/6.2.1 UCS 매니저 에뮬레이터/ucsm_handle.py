#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle

global handle
handle = UcsHandle('192.168.56.250','ucspe','ucspe')

def standard_login():    
    handle.login()
    print "UCS 매니저(%s)에 로그인합니다. " % (handle.ucs)
    
def standard_logout():
    handle.logout()
    print "UCS 매니저에서 로그아웃합니다."

if __name__ == "__main__":
    standard_login()
    print "UCS 매니저 접속 주소 : "+ handle.uri
    standard_logout()
