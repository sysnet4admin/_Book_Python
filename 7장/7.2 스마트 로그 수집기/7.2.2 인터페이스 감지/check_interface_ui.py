#!/bin/env python
#-*- coding: utf-8 -*-

def get_user_input() :
    interface = raw_input("1. 감지하고자 하는 인터페이스를 입력하세요 (예 : 1/1 , 1/1-10) : ")

    print "\n\t*************[ 패킷 종류 ]***************"
    print "\t\ta. RX\t\tb. TX\t\t"
    print "\t"+("*"*40) + "\n"
    packet = raw_input("2. 감지하고자 하는 패킷 종류를 선택하세요 [a/b]: " )
        
    RX_ERR = ["jumbo packets","storm suppression packets","runts","giants",
              "CRC", "no buffer", "input error", "short frame", "overrun",
              "underrun", "ignored", "watchdog", "bad etype drop", "bad proto drop",
              "if down drop", "input with dribble", "input discard", "Rx pause" ]
    TX_ERR = ["jumbo packets","output error", "collision", "deferred", "late collision",
              "lost carrier", "no carrier", "babble ", "output discard", "Tx pause" ]

    if packet == "a":
        packet = "RX"
        error_kind_list = RX_ERR
    else :
        packet = "TX"
        error_kind_list = TX_ERR
        
    print "\n\t*************[ 에러 종류 ]***************"
    for index, err_code in enumerate(error_kind_list) :
        print "\t\t%d. %s" % ((index + 1), err_code)
    print "\t\t%d. all" % (index + 2)
    print "\t"+("*"*40) + "\n"

    index = input("3. 감지하고자 하는 에러 종류를 선택하세요 : ")
    while (index < 1 or index > len(error_kind_list) + 1) :
        print ("잘못 입력하셨습니다")
        index = input("3. 감지하고자 하는 에러 종류를 선택하세요 : ")

    if index <= len(error_kind_list) :
        err_type = error_kind_list[index - 1]       # 에러 코드 리스트 중 1개 코드 선택
    else :
        err_type = error_kind_list                  # 모든 에러 코드 리스트 선택

    err_chk_range = input("\n4. 감지할 인지 범위를 입력하세요 (예 : 1, 10, 100) : ")

    print "\n\t********[ 에러가 감지됐을 때 기록할 로그 종류 ]*********"
    print "\t\ta. show interface ethernet %s" % interface
    print "\t\tb. show interface ethernet %s transceiver details" % interface
    print "\t\tc. show tech-support pktmgr"
    print "\t\td. All"
    print "\t"+("*"*50) + "\n"
    log_type = raw_input("5. 에러가 감지됐을 때 기록할 로그를 선택하세요 [d]: " )
    if log_type != "a" and log_type != "b" and log_type != "c":
        log_type = "d"

    return (interface, packet, err_type, err_chk_range, log_type)

if __name__ == "__main__":
    (interface, packet, err_type, err_chk_range, log_type) = get_user_input()
    print "\n\t******[ 사용자 선택 결과 ]******"
    print "\t인터페이스 :", interface
    print "\t패킷 종류 :", packet
    print "\t감지할 인지 범위 :", err_chk_range
    print "\t기록할 로그 종류 선택 번호 :", log_type
    print "\t감지할 에러 종류 :", err_type
