#!/bin/env python
#-*- coding: utf-8 -*-

from cli import *
import re

def get_drop_packet() :
    ret = cli("show policy-map interface control-plane | in dropped")
    drop_packet_list = []
    for line in ret.split("\n") :
        line = line.strip()
        str_array = line.split()
        if len(line) > 1 :
            drop_packet_list.append(int(str_array[1]))

    return drop_packet_list

def get_policy_class_map() :
    ret = cli("show policy-map interface control-plane")
    find_list = re.findall("class-map .*match-any", ret)
    
    class_list = []

    for data in find_list :
        str_list = data.split()
        class_list.append(str_list[1])

    return class_list

def get_copp_status() :
    ret = cli("show copp status")
    if ret.find("Policy-map attached to the control-plane: copp-system-p-policy-strict") < 0:
        find_list = re.findall("Policy-map attached to the control-plane: .*", ret)
        data = find_list[0]
        data = data.split(":")[1]
        return data
    return "기본값"

if __name__ == "__main__":
    # 드랍량 출력
    print "드랍량 :", get_drop_packet()

    # 클래스맵 출력
    print "CoPP 클래스맵 :", get_policy_class_map()

    # CoPP 정책 출력
    print "CoPP 정책 :", get_copp_status()
