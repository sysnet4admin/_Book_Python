#!/bin/env python
#-*- coding: utf-8 -*-

from exec_ipmi import *

def ipmitool(args):
    ret = get_ipmi(args)
    rows = ret.split('\n')
    item_set =set(rows)         # 여기서 중복되는 내용이 제거됩니다.
    item_set.remove('')         # 내용이 없으면 삭제함
    for item in item_set:
        print item

if __name__ == "__main__":
    args = get_server_input()
    
    ipmitool( args + ' fru print | grep "Product Name"')
    ipmitool( args + ' fru print | grep "Chassis Serial"')
