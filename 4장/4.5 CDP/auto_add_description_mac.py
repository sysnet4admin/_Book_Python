#!/bin/env python
#-*- coding: utf-8 -*-

from cli import *
import httplib

def get_mac_info() :
    str = cli("show mac address-table | grep 'Eth1/'")
    mac_info = {}
    
    for line in str.split("\n") :       # 명령 결과를 한 줄씩 읽습니다.
        data = line.split()             # 한 줄을 스페이스 단위로 나눠 리스트로 작성
        if len(data) < 2 :              # 2번째 열의 MAC 주소가 없으면 동작하지 않음
            continue
        
        mac_addr = data[2]              # MAC 주소 추출
        mac_port = data[len(data)-1]    # 인터페이스 정보 추출(마지막 열)
        
        mac_list = []
        if mac_info.get(mac_port) != None:      # 딕셔너리에 인터페이스가 기존에 있는지 확인
            mac_list = mac_info.get(mac_port)   # 이미 있다면 MAC 주소 리스트를 가져옴
            
        mac_list.append(mac_addr)               # MAC 주소를 추가함
        mac_info[mac_port] = mac_list           # 딕셔너리에 인터페이스의 MAC 주소 리스트 적용
        
    return mac_info

def add_description(mac_info):
    for mac_port in mac_info :                  # 인터페이스(mac_port) 수만큼 반복해서 동작
        mac_list = mac_info.get(mac_port)       # 인터페이스 MAC 주소 리스트 조회

        mac_addr = ""
        if len(mac_list) > 1 :                  # MAC 주소가 여러 개일 때
            i = 0
            print "*"* 30
            print "Num", "MAC Address"
            print "="* 30
            while i < len(mac_list) :           # MAC 주소 리스트를 출력
                print i, mac_list[i]
                i = i + 1
            print "%s 의 MAC Address가 1개 이상입니다." % mac_port
            select = input("중복된 내용 중 상세 내용에 입력하고자 하는 MAC을 선택하세요 : ")
            mac_addr = mac_list[select]         # 선택한 MAC 주소를 mac_addr 변수에 지정
        else :
            mac_addr = mac_list[0]
                
        mac = mac_addr[0:7]                     # MAC 주소 중 앞의 7자리 추출
        mac = mac.replace(".", "").upper()      # MAC 주소 중 .(dot)을 제거
        
        # 웹 페이지에서 데이터 추출하는 코드
        try :
            conn = httplib.HTTPConnection("aruljohn.com")       # 해당 웹 페이지에 접속
            conn.request("GET", "/mac/%s"% mac)                 # /mac/<MAC 6자리>를 url에 추가
            res = conn.getresponse()                            # 웹페이지의 HTML 소스를 받음
            data = res.read()
            description = "*auto* "
            
            oui = "%s:%s:%s"% (mac[0:2],mac[2:4],mac[4:6])      # OUI -> 00:00:00 형식의 MAC
            search_word = "<tr><td>%s</td><td>"% oui            # OUI의 앞뒤 태그를 포함해서 찾기

            index = data.find(search_word) + len(search_word)   # OUI 뒤에 제조사 정보가 있음
            if index >= 0 :
                vender = data[index : data.find("</td>", index)].strip()    # 앞뒤의 HTML 태그를 제거

                # 제조사 정보를 찾으면 설명 항목에 입력할 데이터를 작성합니다.
                description = "*auto* %s - %s" % (vender , mac_addr)

            # configure terminal 모드에서 설명 항목에 수정하는 명령을 수행합니다.
            cmd = "configure terminal ; interface %s ; " % mac_port
            cmd = cmd + "description %s" % description
            cli(cmd)
        except IOError as e:
            print "%s(%s)의 정보는 조회할 수 없습니다." % (mac_port, mac_addr)
        
def show_description(mac_list):
    for mac_port in mac_info :
        print cli("show interface %s description" % mac_port)
        
if __name__ == "__main__":
    mac_info = get_mac_info()
    add_description(mac_info)
    show_description(mac_info)
