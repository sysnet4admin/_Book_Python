#!/bin/env python
#-*- coding: utf-8 -*-

from interface_get_data import *
import time

def get_rate_change(interface_num, measure, seconds) :
    # 각 인터페이스의 포트 타입 리스트 조회
    port_types = []
    i = 1
    while i <= interface_num :
        # 인터페이스 개수만큼 배열에 적재합니다.
        port_types.append(get_port_type(i))
        i = i + 1
        
    # 최초 레이트 값
    (start_input_pks, start_output_pks) = get_rate_list(interface_num, measure)
    
    time.sleep(seconds)
    
    (input_pks, output_pks) = get_rate_list(interface_num, measure)
    
    return (port_types,
        start_input_pks, input_pks, subtract(start_input_pks, input_pks),
        start_output_pks, output_pks, subtract(start_output_pks, output_pks))

def get_rate_list(interface_num, measure):
    input_pks = []
    output_pks = []
    i = 1
    while i <= interface_num :
        # 각 레이트 값은 일반 byte 단위이므로 기준 데이터 단위로 바꿉니다.
        input_pk = get_rate("input rate", i) / measure
        output_pk = get_rate("output rate", i) / measure
        
        # 인터페이스 개수만큼 배열에 적재합니다
        input_pks.append(input_pk)
        output_pks.append(output_pk)
        i = i + 1
        
    return (input_pks, output_pks)

def subtract(start_rate_list, end_rate_list):
    i = 0
    change_list = []
    while i < len(start_rate_list) :
        change_list.append(end_rate_list[i] - start_rate_list[i])
        i = i + 1
    return change_list

if __name__ == "__main__":
    print "데이터 증감량을 확인하기 위해 다음을 선택하십시오."
    interface_num = input("몇 개의 인터페이스를 확인하시겠습니까? : ")
    seconds = input("몇 초 후의 데이터 증감량을 확인하시겠습니까? : ")
    (port_types,start_input_pks, end_input_pks, change_input_pks,
     start_output_pks, end_output_pks, change_output_pks) = get_rate_change(
         interface_num, get_byte_num("M"), seconds)
    
    print "Input Rate(bps)"
    print "시작 값 : ", start_input_pks
    print "종료 값 : ", end_input_pks
    print "증감량 : ", change_input_pks
    print "=" * 70
    
    print "Output Rate(bps)"
    print "시작 값 : ", start_output_pks
    print "종료 값 : ", end_output_pks
    print "증감량 : ", change_output_pks
    print "=" * 70
    print "포트타입 : ", port_types
