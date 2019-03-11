#!/bin/env python
#-*- coding: utf-8 -*-

from syslog import syslog
import pexpect
import time
import os
from cli import cli

now = time.localtime()
cur_time= "%04d%02d%02d_%02d%02d%02d"%(now.tm_year, now.tm_mon, now.tm_mday,
                                       now.tm_hour, now.tm_min, now.tm_sec)
#### 백업 시스템 정보 (정확한 정보로 수정 필요)####
id='root'
pw='password'
ip=<백업 서버_IP>
########################
dir_name = cli('show switchname')[:-2]
backup_dir = '/var/log/'+'scp_backup_from-'+dir_name
backup_name ='n9k-running-config-%s'%cur_time

def exist_chk(method):
    try:
        f = open("/var/home/admin/.ssh/known_hosts",'r')
        data = f.read()
        if method=='ssh':
            if data.find('%s ecdsa-sha2-nistp256'%ip) == -1:
                return -1
        elif method=='scp':
            if data.find('%s ssh-rsa'%ip) == -1:
                return -1
    except:
        return -1

def mkdir_backup():
    cmd ="ssh %s@%s mkdir %s"%(id,ip,backup_dir)
    child = pexpect.spawn(cmd)
    if exist_chk('ssh'):
        child.expect("yes")
        child.sendline("yes\n")
    child.expect("assword:")
    child.sendline("%s\n"%pw)

def scp_backup():
    child = pexpect.spawn("/isan/bin/vsh")
    child.sendline("copy running-config scp://%s@%s/%s/%s"%(id,ip,backup_dir,backup_name))
    child.expect(":")
    child.sendline("management\n")
    if exist_chk('scp'):
        child.expect("yes")
        child.sendline("yes\n")
    child.expect("assword:")
    child.sendline("%s\n"%pw)
    syslog(3,"구성정보(%s)가 %s에 성공적으로 백업되었습니다"%(backup_name,ip))

if __name__ == "__main__":
    mkdir_backup()
    scp_backup()
