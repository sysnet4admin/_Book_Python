#!/bin/env python
#-*- coding: utf-8 -*-

from syslog import syslog
import pexpect
import time
import os

def scp_backup():
    now = time.localtime()
    cur_time= "%04d%02d%02d_%02d%02d%02d"%(now.tm_year, now.tm_mon, now.tm_mday,
                                           now.tm_hour, now.tm_min, now.tm_sec)
    ip=<ip 주소>
    backup_name ='n9k-running-config-%s'%cur_time

    child = pexpect.spawn("/isan/bin/vsh")
    child.sendline("copy running-config scp://root@%s/%s"%(ip,backup_name))
    child.expect(":")
    child.sendline("management\n")
    if not os.path.isfile("/var/home/admin/.ssh/known_hosts"):
        child.expect("yes")
        child.sendline("yes\n")
    child.expect("assword:")
    child.sendline("<암호>\n")
    syslog(3,"구성정보(%s)가 %s에 성공적으로 백업되었습니다"%(backup_name,ip))

if __name__ == "__main__":
    scp_backup()

