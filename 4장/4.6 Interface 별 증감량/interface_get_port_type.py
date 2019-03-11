#!/bin/env python
#-*- coding: utf-8 -*-

from cli import *

def get_port_type(interface_num) :
    str = cli("show interface ethernet 1/%i"%interface_num)
    title_idx = str.find("Port mode is ")
    port_type = "None"
    if title_idx >= 0 :
        enter_idx = str.find("\n", title_idx)   # 해당 줄의 마지막에 있는 줄 바꿈 문자를 찾습니다.
        
        # 명령어 실행 결과에 'Port mode is access'가 포함돼 있다면,
        # line_str의 결과는 'Port mode is access'입니다.
        # str[title_idx : enter_idx].split()의 결과는 ['Port', 'mode', 'is', 'access']입니다.
        line_str = str[title_idx : enter_idx].split()       
        port_type = line_str[len(line_str)-1]
    return port_type


if __name__ == "__main__":
    interface_num = 24                          # 인터페이스 숫자를 24로 고정
    port_types = []

    i = 1
    while i <= interface_num :
        port_types.append(get_port_type(i))     # 명령어 실행
        i = i + 1

    print port_types
