#!/bin/env python
#-*- coding: utf-8 -*-

from history_all import *
                   
if __name__ == "__main__":
    accounts = get_accounts()
    
    for account in accounts :
        history_list = history(account)

        newest_cnt = min(5, len(history_list))
        print "계정 : %s의 최근 사용 명령어 : % d개" % (account, newest_cnt)
        if newest_cnt == 0:
            print "\t기록된 이력 없음"
            
        i = 0
        while i < newest_cnt:
            print "\t%s\t%s" % history_list[i]
            i = i + 1
        print "-" * 70
