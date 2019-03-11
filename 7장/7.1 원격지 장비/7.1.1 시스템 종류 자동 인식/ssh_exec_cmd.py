#!/bin/env python
#-*- coding: utf-8 -*-

import paramiko
import time

client = None
(host, port_num, user, pw) = ("", 22, "", "")
def connect(host, port_num, user, pw) :
    # 접속에 성공하면 SSHClient를 client 변수로 생성하고 접속 결과를 True/False로 반환
    global client                   # 접속한 SSHClient를 global 변수 client로 설정
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try :
        # 접속한 접속 정보를 모두 global 변수로 설정합니다.
        set_connection_info(host, port_num, user, pw) 
        client.connect(hostname=host, port=port_num, username=user, password=pw)
        return True
    except :
        return False

def close() :
    client.close()       # SSH 접속을 해제
    
def exec_cmd(cmd) :     # 명령어를 수행한 결과를 읽습니다.
    if connect(host, port_num, user, pw) : 
        try : 
            (stdin, stdout, stderr) = client.exec_command(cmd)
            if stderr.read().strip() != "" :        
                return invoke_shell(cmd)
            return stdout.read().strip()
        except :
            print "명령어를 수행할 수 없습니다. :", cmd
        close() 

def invoke_shell(cmd) :     # 원격지 시스템과 상호 메시지를 주고받는 식으로 명령어를 수행한 결과를 읽어서 반환
    channel = client.invoke_shell()         # invoke_shell로 SSH 채널을 설정합니다.
    response = channel.recv(9999)           # 응답을 받습니다(접속과 관련된 응답 메시지).
    channel.send(cmd + "\n")                # 실행할 명령어를 보냅니다("\n" 또는 "\r"을 붙여서 실행).
    while not channel.recv_ready():         # 명령어를 실행하고 응답할 준비가 됐는지 대기합니다.
        time.sleep(3)               
    response = channel.recv(9999)           # 명령어 실행 결과를 받습니다.
    out = response.decode("utf-8")          # 명령어 실행 결과를 utf-8 문자열로 바꿉니다.

    # 첫 번째 줄은 제거합니다(2번째 줄부터 실제 명령어 실행 결과가 출력되기 때문입니다).
    first_enter_index = min(out.find("\r"), out.find("\n"))

    # "\r\n"을 일반 엔터로 바꾸어 표시합니다.
    # 바꾸지 않고 그대로 표시하면 \r이 화면에서는 알 수 없는 문자(♪)로 표시됩니다.
    out = out[first_enter_index : len(out)]
    out = out.replace("\r\n", "\n")
    return out.strip()  

def get_connection_input() :
    host = raw_input("원격지 시스템의 IP를 입력하세요. : ")
    port_num = 22
    try :
        port_num = input("원격지 시스템의 Port 번호를 입력하세요. [22] : ")
    except :
        port_num = 22
    user = raw_input("관리자 ID를 입력하세요. : ")
    pw = raw_input("암호를 입력하세요. : ")
    return (host, port_num, user, pw)

def set_connection_info(input_host, input_port_num, input_user, input_pw):
    global host, port_num, user, pw
    host = input_host
    port_num = input_port_num
    user = input_user
    pw = input_pw
    
if __name__ == '__main__':
    # 원격지 시스템 접속을 위한 접속 정보를 입력받음
    (host, port_num, user, pw) = get_connection_input()
    
    connnected = connect(host, port_num, user, pw)      # 접속을 수행합니다.
    if connnected:
        close()
    else :
        print "원격지 시스템 접속에 실패하였습니다."    
    if connnected:
        cmd = "dir"
        print "수행 명령어 :", cmd
        print exec_cmd(cmd)
        print "*" * 70        
        cmd = "ls"
        print "수행 명령어 :", cmd
        print exec_cmd(cmd)
        print "*" * 70
