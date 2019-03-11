#!/bin/env python
#-*- coding: utf-8 -*-


import paramiko
import time


client = None
(host, port_num, user, pw) = ("", 22, "", "")
def connect(host, port_num, user, pw) :
    global client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try :
        set_connection_info(host, port_num, user, pw) 
        client.connect(hostname=host, port=port_num, username=user, password=pw)
        return True
    except :
        return False


def close() :
    client.close()
    
def exec_cmd(cmd) :
    if connect(host, port_num, user, pw) : 
        try : 
            (stdin, stdout, stderr) = client.exec_command(cmd)
            if stderr.read().strip() != "" :        
                return invoke_shell(cmd)
            return stdout.read().strip()
        except :
            print "명령어를 수행할 수 없습니다. :", cmd
        close() 


def invoke_shell(cmd) :
    channel = client.invoke_shell()
    response = channel.recv(9999)            
    channel.send(cmd + "\n")
    while not channel.recv_ready():
        time.sleep(3)               
    response = channel.recv(9999)
    out = response.decode("utf-8")
    first_enter_index = min(out.find("\r"), out.find("\n"))
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
    (host, port_num, user, pw) = get_connection_input()
    connnected = connect(host, port_num, user, pw)
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
