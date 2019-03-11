#!/bin/env python
#-*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import os
import re

def send_mail(host, port, login_id, login_pw, sender_addr, reciever_addr, subject, attach_list) :
    # 메일 메시지(msg) 작성
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_addr
    msg["To"] = reciever_addr

    # 메일 메시지(msg)에 첨부 파일 추가
    for file_path in attach_list:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file_path, 'rb').read())
        Encoders.encode_base64(part)

        split_path = os.path.split(file_path)
        file_name = split_path[len(split_path) - 1]
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
        msg.attach(part)

    # 메일 전송
    smtp_svr = smtplib.SMTP_SSL(host, port)         # 서버/포트 설정(SSL일 때 SMTP_SSL() 함수 사용)
    smtp_svr.login(login_id, login_pw)              # 메일 서버에 로그인
    smtp_svr.sendmail(sender_addr, reciever_addr, msg.as_string())      # 메일 전송
    smtp_svr.quit()                                                     # 메일 서버와 접속 종료

def get_attach_list(file_dir, file_pattern) :               # file_dir은 소스 코드와 같은 경로
    file_names = os.listdir(file_dir)
    attach_list = []
    for file_name in file_names :
        if os.path.isfile(file_name) :                      # file_dir 하위의 파일 리스트를 확인
            match_file = re.match(file_pattern, file_name)
            if match_file == None :                         # 정규식으로 파일명 패턴을 확인
                continue
            attach_list.append(file_dir + "/" + file_name)  # 패턴에 맞는 파일명만 리스트에 추가
    return attach_list

if __name__ == "__main__":
    host = <SMTP 호스트 주소>
    port = 465    # SMTP 포트 : SSL로 보낼 때는 465, TLS로 보내려면 587
    login_id = <SMTP 호스트 주소에 접속할 아이디>
    login_pw = <SMTP 호스트 주소에 접속할 아이디의 암호>

    sender_addr = <보내는 사람 메일 주소>
    reciever_addr = <받는 사람 메일 주소>
    subject = "[알림] 메일이 도착했습니다."

    attach_list = get_attach_list(".", ".*sample.*\.xml")
    send_mail(host, port, login_id, login_pw, sender_addr, reciever_addr, subject, attach_list)
    print reciever_addr, "로 메일을 전송했습니다."
    print "첨부 파일 :", attach_list
