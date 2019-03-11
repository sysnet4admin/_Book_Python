#!/bin/env python
#-*- coding: utf-8 -*-

from cli import *
import datetime
from interface_data_variation import *
    
def get_max_rate() :
    sh_int_data = cli("show interface ethernet 1/1")        # 명령어 실행
    keyword = "full-duplex, "                               # 'full-duplex, '라는 단어 뒤의 위치
    index = sh_int_data.find(keyword) + len(keyword)
    if index < 0 :
        max_rate = 0
        unit = ""
        return (max_rate, unit)
        
    max_rate_line = sh_int_data[index : sh_int_data.find(",", index)]   # 예를 들어, 1000 Mb/s 라는 값이 추출되었다면
    datas = max_rate_line.split()                       # 공백 단위로 나누어 리스트로 만들고,
    max_rate = int(datas[0])                            # 리스트 중, 0번째의 1000은 숫자로 바꿉니다.
    unit = datas[1][0]                                  # 1번째의 'Mb/s'에서 M만 추출합니다.
    return (max_rate, unit)
    
def draw_graph(start_pk_list, end_pk_list, chang_pk_list, port_types, max_value, unit_str):
    # 추출한 데이터로 그래프를 작성
    if max_value == 0 :
        return ""    
    
    str_list = []
    str_list.append("MAX = %i%s\n"% (max_value, unit_str))
    
    measure = max_value / 10
    i = max_value / measure
    while i > 0 :
        # 데이터 양인 "#"을 표시할지 결정하는 print_mark 함수를 별도로 정의함
        str_list.append(print_mark(i, start_pk_list, end_pk_list, chang_pk_list, unit_str, measure))
        i = i-1

    # 포트 종류를 1글자씩 표시
    str_list.append(print_port(port_types, unit_str))

    # X축의 인터페이스 번호를 표시(인터페이스 번호가 2자리이면 2줄로 표시)
    str_list.append(print_x_label(len(chang_pk_list), unit_str))
    return ''.join(str_list)
    
def print_mark(i, start_pk_list, end_pk_list, chang_pk_list, unit_str, measure):        #지정된 위치에 눈금값과 # + - 와 같은 마크를 출력합니다.
    str_list = []
    # Y축 눈금의 값을 구합니다.
    num = i * measure

   # 눈금에 표시할 값을 지정합니다. 글자가 3자리면 공백 1개, 2자리면 공백 2개, 1자리면 공백 3개를 붙입니다.
    if num >= 1000 :
        str_list.append("%i%s "%(num, unit_str))
    elif num >= 100 :
        str_list.append(" %i%s "%(num, unit_str))
    elif num >= 10 :
        str_list.append("  %i%s "%(num, unit_str))
    else :
        str_list.append("   %i%s "%(num, unit_str))

    # 한 줄의 데이터 중에서 해당 눈금과 값을 비교해서 #, +, -을 표시합니다.
    for i, change_pk in enumerate(chang_pk_list):
        display_pk = 0
        if change_pk > 0 :
            display_pk = end_pk_list[i]
            if(display_pk >= num) :
                if(start_pk_list[i] >= num) :
                    str_list.append("# ")
                else :
                    str_list.append("+ ")
            else :
                str_list.append("  ")
        else :
            display_pk = (-1 * change_pk)+ end_pk_list[i]
            if(display_pk >= num) :
                if(end_pk_list[i] >= num) :
                    str_list.append("# ")
                else :
                    str_list.append("- ")
            else :
                str_list.append("  ")
    str_list.append("\n")
    return ''.join(str_list)

def print_port(port_types, unit_str):       # 포트 타입을 출력합니다.
    str_list = []

    # Y축 0과 단위 출력, 열을 맞추기 위해 공백 문자 3개를 작성함.
    str_list.append("   0")
    str_list.append(unit_str)
    str_list.append(" ")

    #port 타입을 작성
    for port in port_types:
        str_list.append(port[0])
        str_list.append(" ")
    str_list.append("\n")
    return ''.join(str_list)

def print_x_label(largest_value, unit_str) :    # X축 라벨을 출력합니다.
    str_list = []
    i = 1
    
    # Y축만큼의 공백 작성
    # Y축에서 단위를 포함했으면 공백 문자를 작성함.
    str_list.append("     ")
    str_list.append(" "* len(unit_str))
    
    while i <= largest_value :
        if i < 10 :
            str_list.append("%i " % i)      # 한 자리 숫자는 그냥 출력
        else :
            str_list.append("%i "%(i/10))   # 두 자리 숫자는 앞자리만 출력
        i = i + 1
    str_list.append("\n")
    str_list.append("      ")
    i = 1
    while i <= largest_value :
        if i < 10 :
            str_list.append("  ")           # 한 자리 숫자는 두 번째 줄에서 공백
        elif i < 20 :
            str_list.append("%i " % (i%10))
        else :
            str_list.append("%i " % (i%20))
        i = i + 1
    str_list.append("\n")
    return ''.join(str_list)

if __name__ == "__main__":
    print "데이터 증감량을 그래프로 그리기 위하여 다음을 선택하십시오."
    interface_num = input("몇 개의 인터페이스를 확인하시겠습니까? : ")
    seconds = input("몇 초 후의 데이터 증감량을 확인하시겠습니까? : ")
    minutes = input("몇 분 후까지 반복해서 확인하시겠습니까? : ")
    end_time = datetime.datetime.now() + datetime.timedelta(minutes = minutes)

    cnt = 1
    while True :
        (max_rate, unit) = get_max_rate()
        
        start_time = datetime.datetime.now()
        (port_types,start_input_pks, end_input_pks, change_input_pks,
            start_output_pks, end_output_pks, change_output_pks) = get_rate_change(
                interface_num, get_byte_num(unit), seconds)

        print cnt, "회차 데이터 수집 시간:", start_time, "~", datetime.datetime.now()

        # 그래프 작성
        title = "Input Rate(bps)"
        print " " * (interface_num -len(title)/2 + 5), title
        print draw_graph(
            start_input_pks, end_input_pks, change_input_pks, port_types, max_rate, unit)

        title = "Output Rate(bps)"
        print " " * (interface_num -len(title)/2 + 5), title
        print draw_graph(
            start_output_pks,end_output_pks, change_output_pks, port_types, max_rate, unit)
        if datetime.datetime.now() >= end_time :
            break

        cnt = cnt + 1
