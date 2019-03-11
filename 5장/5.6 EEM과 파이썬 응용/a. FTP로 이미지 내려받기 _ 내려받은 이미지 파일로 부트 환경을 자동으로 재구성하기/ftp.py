#!/bin/env python
#-*- coding: utf-8 -*-
import ftplib
import sys
import os

# 글로벌 변수 영역
image_file_name = ""
local_path = "/bootflash/"
ftp_path = ""
file_size = 0
percent = 0
view_unit = 10

def ftp_down(host, id, pw):     # FTP에 접속해 파일을 내려받는 함수입니다.
    ftp = ftplib.FTP(host=host, user=id, passwd=pw, timeout=3600)
    ftp.cwd(ftp_path)
    
    global file_size
    file_size = ftp.size(image_file_name)
    
    print "Start Download... ", file_size, "bytes"
    fd = open(local_path, "ab")
    fd.close()
    ftp.retrbinary("RETR " + image_file_name, write_file_callback, 1000000)
    print "100% - Complete."
    
    ftp.close()
        
def write_file_callback(s) :    # FTP에 접속해 내려받은 파일을 바이너리로 로컬 파일에 작성하는 함수입니다.
    global percent    
    fd = open(local_path, "ab")
    fd.write(s)

    download_size = os.path.getsize(local_path);    
    percent_now = round(download_size*(100/view_unit)/file_size)
    if percent != percent_now :
        print percent_now * view_unit, "% (", download_size, ") bytes"
        
    percent = percent_now    
    fd.close()
 
def download(host, id, pw, ftp_image_dir, local_dir, file_name) :
    # 글로벌 변수 중 ftp_path, image_file_name, local_path에 값을 지정합니다.
    global ftp_path
    global image_file_name
    global local_path
    
    image_file_name = file_name
    ftp_path = ftp_image_dir
    local_path = "%s%s" % (local_dir, file_name)

    # 로컬 파일로 작성하려는 경로에 있는 파일을 삭제합니다.
    try :        
        os.remove(local_path)
    except :
        print "%s 파일이 없습니다."%local_path
        print "계속 진행합니다.\n"
        pass

    # 파일 내려받습니다.
    ftp_down(host, id, pw)
        
if __name__ == "__main__":
    host = <FTP 주소>
    id = <FTP 관리자 ID>
    pw = <FTP 관리자 암호>
    ftp_path = ""
    local_dir = "/bootflash/"                   # 로컬 디렉터리 위치
    image_file_name = "nxos.7.0.3.I4.1.bin"     # 이미지 파일명
    
    download(host, id, pw, ftp_path, local_dir, image_file_name)
