#!/bin/env python
#-*- coding: utf-8 -*-

from interface_get_port_type import *

def get_rate(rate, interface_num) :
    # 네트워크 명령을 실행해서 인터페이스의 레이트 값을 구하고 byte 단위로 반환
    ret = cli("show interface ethernet 1/%i | in rate"%interface_num)
    last_str = ret.split("\n")[2]
    rate_index = last_str.find(rate) + len(rate)
    rate_end_index =last_str.find("bps", rate_index)
    rate_str = last_str[rate_index : rate_end_index].strip()
    str_list = rate_str.split()         # input rate가 940.30 M 이라면, str_list = ['940.30', 'M']

    # str_list의 0번째 문자열을 0의 자리에서 반올림해서 숫자로 바꿉니다.
    rate_num = round(float(str_list[0]), 0)
    unit = ""
    if len(str_list) > 1 :
        unit = str_list[1]
    return rate_num * get_byte_num(unit)

def get_byte_num(unit):
    # 단위(unit)에 따라 실제 바이트 값을 반환: 예를 들어 단위가 K이면 2의 10승이므로 1024
    if unit == "":
        return 1
    elif unit == "K" :
        return pow(2, 10)
    elif unit == "M" :
        return pow(2, 20)
    elif unit == "G" :
        return pow(2, 30)

if __name__ == "__main__":
    interface_num = 24      # 인터페이스 숫자를 24로 고정

    port_types = []
    input_pks= []
    output_pks= []

    # 정해진 인터페이스 개수만큼 반복해서 포트 타입, input/output 레이트를 구하고 리스트에 적재
    i = 1
    while i <= interface_num :
        input_pk = get_rate("input rate", i)
        output_pk = get_rate("output rate", i)
        
        port_types.append(get_port_type(i))
        input_pks.append(input_pk)
        output_pks.append(output_pk)
        i = i + 1
        
    # 화면에 출력
    print port_types
    print input_pks
    print output_pks
