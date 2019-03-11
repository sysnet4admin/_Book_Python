#!/bin/env python
#-*- coding: utf-8 -*-

import ftp
import sys
from cli import *
import time 

def boot_image(host, id, pw, image_path) :
    cli("configure terminal ; interface ethernet 1/24 ; description python auto_provisioning")
    cli("configure terminal ; interface ethernet 1/24 ; switchport ; switchport mode trunk ; \
    switchport trunk allowed vlan 500")

    print "Auto_provision을 위한 준비를 하고 있습니다."
    tm = 0
    while tm < 30:
	sys.stdout.write(".")
	sys.stdout.flush()        
	time.sleep(1)
	tm +=1
    cli("ping %s count 1"%host) 
    print "\n"

    file_index = image_path.rfind("/") + 1
    image_file_name = image_path[file_index: len(image_path)]
    ftp_image_dir = image_path[0: file_index]
    local_dir = "/bootflash/"
    ftp.download(host, id, pw, ftp_image_dir, local_dir, image_file_name )

    cli("configure terminal ; no event manager applet Auto-Provisioning")
    cli("configure terminal ; interface ethernet 1/24 ; no description ; no switchport")
    cli("configure terminal ; boot nxos bootflash:///%s" % image_file_name)
    print "다음에 부팅될 nxos 버전 :", cli("show running-config | include nxos")

if __name__ == "__main__":
    host = <FTP 주소>
    id = <FTP 관리자 ID>
    pw = <FTP 관리자 암호>
    image_path = "nxos.7.0.3.I4.1.bin"    # 이미지 파일명
    
    if len(sys.argv) > 4 :
        host = sys.argv[1]
        id = sys.argv[2]
        pw = sys.argv[3]
        image_path = sys.argv[4]

    boot_image(host, id, pw, image_path)
