#!/bin/env python
#-*- coding: utf-8 -*-

from check_interface_ui import get_user_input
from cli import cli
import re

def find_status(err_type, interface_data):      # 데이터에서 하나의 에러 코드 타입의 상태 값을 추출
    # "[숫자] [선택한 에러 코드]" 문자열 탐색
    find_datas = re.findall("[0-9]* %s"% err_type, interface_data)

    # 정규식으로 찾은 문자열은 1건입니다.
    find_data = find_datas[0].strip()
    status = find_data.split()[0]               # 찾은 문자열을 공백으로 잘라서 앞의 데이터인 상태 값을 추출
    return int(status)                          # 결과를 숫자 형태로 반환합니다.

def get_interface_data_list(interface) :        # interface(여러 개일 수 있음)의 상태 데이터에서 각 interface의 상태 데이터 추출
    ret = cli("show interface ethernet " + interface)
    find_datas = re.findall("Ethernet.* is *.", ret)        # 'Ethernet<인터페이스 번호> is up(또는 down)' 규칙대로 인터페이스별 데이터 분할
    interface_data_list = []
    start_idx = 0
    end_idx = 0
    for i, find_data in enumerate(find_datas):
        start_idx = ret.find(find_data)
        if i < len(find_datas) - 1 :
            end_idx = ret.find(find_datas[i+1])
        else :
            end_idx = len(ret)
        interface_name = find_data.split(" is")[0]          # is 앞의 값은 인터페이스 이름으로 함
        interface_data = ret[start_idx : end_idx]           # 해당 인터페이스의 데이터
        interface_data_list.append((interface_name, interface_data))
    return interface_data_list

def get_status(interface_data, packet, err_type) :  # interface 상태 데이터에서 패킷 타입, 에러 코드 타입으로 상태 값을 추출
    # packet은 "TX"나 "RX"입니다.
    title_idx = interface_data.index("  " + packet)

    # RX /TX 패킷을 기준으로 뒤따라 나오는 데이터
    interface_data = interface_data[title_idx : len(interface_data)]
    status_info = {}
    if isinstance(err_type, list) :                 # 선택한 에러 코드가 리스트 형태로 여러 개이면 반복합니다.
        for err in err_type :
            status = find_status(err, interface_data)
            status_info[err] = status
    else :
        status = find_status(err_type, interface_data)
        status_info[err_type] = status
    return status_info

if __name__ == "__main__":
    (interface, packet, err_type, err_chk_range, log_type) = get_user_input()

    # 사용자 선택 결과 출력
    print "\n\t**********[ 사용자 선택 결과 ]**********"
    print "\t인터페이스 :", interface
    print "\t패킷 종류 :", packet
    print "\t[이 코드에서는 활용 안 함] 감지할 인지 범위 :", err_chk_range
    print "\t[이 코드에서는 활용 안 함] 기록할 로그 종류 선택 번호 :", log_type
    print "\t에러 종류와 상태 :"
    print "\t" + ("="*40)

    # 인터페이스별 상태 데이터 추출
    for (interface_name, interface_data) in get_interface_data_list(interface) :
        status_info = get_status(interface_data, packet, err_type)  # 각 인터페이스의 에러 코드별 상태 정보 조회
        print "\t%s" % interface_name
        print "\t"+("-"*40)
        # 선택한 에러 종류로부터 추출한 상태 데이터 출력
        for status_err_type in status_info.keys() :
            print "\t%s\t%d" % (status_err_type, status_info[status_err_type])
        print "\t"+("*"*40)
