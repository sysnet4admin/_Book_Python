#!/bin/env python
#-*- coding: utf-8 -*-

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host =<원격지 시스템 주소>
port_num = <원격지 시스템 포트>     # host, user, pw는 문자열이지만 port_num은 숫자입니다.
user = <관리자 ID>
pw = <관리자 암호>
client.connect(hostname=host, port=port_num, username=user, password=pw)
print client
client.close()
