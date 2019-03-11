#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import *

def exec_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def grep_login_defs(keyword) :
    # 사용자 계정 정보에서 필요한 값을 추출
    ret = exec_cmd("grep '%s' /etc/login.defs" % keyword)
    return ret.split()[1]

def get_accounts() :
    # grep_login_defs 함수로 일반 사용자 ID의 계정 범위 정보 추출
    min_u = grep_login_defs("^UID_MIN")
    max_u = grep_login_defs("^UID_MAX")

    # 일반 사용자 계정 범위 정보를 조합한 명령어로 계정 리스트를 작성해서 반환
    cmd = "awk -F':' -v 'min=%s'" % min_u
    cmd = cmd + " -v 'max=%s'" % max_u
    cmd = cmd + " '{ if ( $3 >= min && $3 <= max ) print $1}' /etc/passwd"
    return exec_cmd(cmd).split()

if __name__ == "__main__":
    accounts = get_accounts()
    for account in accounts :
        print account
