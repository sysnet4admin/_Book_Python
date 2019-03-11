#!/bin/env python
#-*- coding: utf-8 -*-

import ConfigParser
import os
from PyQt4.QtCore import QString

MESSAGE_EN = {}
MESSAGE_KO = {}


MESSAGE_EN["title"] = "Cisco UCS vKVM Launcher (Powered by HoonJo, JSKim)"
MESSAGE_EN["rack_tab_title"] = "RACK Server (C-Series)"
MESSAGE_EN["blade_tab_title"] = "UCS Manager (B-Series)"
MESSAGE_EN["conn_info"] = "Connection info" 
MESSAGE_EN["ip"] = "IP Address : "
MESSAGE_EN["id"] = "Username : "
MESSAGE_EN["pw"] = "Password : "
MESSAGE_EN["port"] = "Port : " 
MESSAGE_EN["add"] = "Add/Modify"
MESSAGE_EN["delete"] = "Delete"
MESSAGE_EN["vkvm_conn"] = "Launch vKVM "
MESSAGE_EN["new_input"] = "<New>"
MESSAGE_EN["selected_blade"] = "Blade Server info"
MESSAGE_EN["status"] = "Status"
MESSAGE_EN["status_ready"] = "Ready"
MESSAGE_EN["status_attached"] = "Attached only"
MESSAGE_EN["status_etc"] = "etc"
MESSAGE_EN["status_empty"] = "empty"
MESSAGE_EN["conn_fail"] = "Connection Failure"
MESSAGE_EN["dup_ip"] = "Duplicated IP(%s)"
MESSAGE_EN["no_ucs_man"] = "No UCS Manager (For UCS B-Series) "

MESSAGE_KO["title"] = "Cisco UCS vKVM 접속 도우미 (Powered by HoonJo, JSKim)"
MESSAGE_KO["rack_tab_title"] = "등록된 랙 서버 매니저"
MESSAGE_KO["blade_tab_title"] = "등록된 블레이드 서버 매니저"
MESSAGE_KO["conn_info"] = "접속 정보"
MESSAGE_KO["ip"] = "서버 매니저의 IP : "
MESSAGE_KO["id"] = "관리자 ID : "
MESSAGE_KO["pw"] = "암      호 : "
MESSAGE_KO["port"] = "포트 번호 : "
MESSAGE_KO["add"] = "추가/수정"
MESSAGE_KO["delete"] = "삭제"
MESSAGE_KO["vkvm_conn"] = "vKVM 접속"
MESSAGE_KO["new_input"] = "<새로 입력>"
MESSAGE_KO["selected_blade"] = "선택한 블레이드 서버 정보"
MESSAGE_KO["status"] = "상태"
MESSAGE_KO["status_ready"] = "접속 가능"
MESSAGE_KO["status_attached"] = "장착만 된 상태"
MESSAGE_KO["status_etc"] = "그 외의 상태"
MESSAGE_KO["status_empty"] = "상태 정보 조회 불가"
MESSAGE_KO["conn_fail"] = "접속에 실패했습니다."
MESSAGE_KO["dup_ip"] = "이미 등록된 IP(%s) 입니다."
MESSAGE_KO["no_ucs_man"] = "블레이드 서버 매니저가 아닙니다."

lang = None
def get_language() :
    env_cfg = ConfigParser.RawConfigParser()    
    if os.path.exists("./environment.cfg") :            # environment.cfg 파일이 없으면 영문
        env_cfg.read("./environment.cfg")
    if env_cfg.sections().count("Environment") > 0 :    # Environment 섹션이 없으면 영문
        lang = env_cfg.get("Environment", "lang")       # lang=ko로 설정돼야 한글
        if lang.lower() == "ko" :
            return "ko"
    return "en"

def select_msg(msg_id) :
    global lang
    if lang == None :                   # 환경 설정을 읽은 적이 없으면 환경 설정값을 로드
        lang = get_language()
    if lang == "ko" :
        return MESSAGE_KO[msg_id]       # 한글로 설정됐다면 한글 리소스 반환
    return MESSAGE_EN[msg_id]           # 한글로 설정되지 않았다면 영문 리소스 반환

def get_message(msg_id) :
    return QString.fromUtf8(select_msg(msg_id))

# 리소스 내에 MESSAGE_KO["dup_ip"]처럼 치환할 값이 있다면 인자로 전달
def get_message_args(msg_id, args) :
    return QString.fromUtf8(select_msg(msg_id) % args)
