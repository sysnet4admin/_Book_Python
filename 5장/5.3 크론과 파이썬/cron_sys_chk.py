#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import *
import os

def dirc():
    if not os.path.exists('/tmp/history'):
        os.makedirs('/tmp/history')

def output(command):
    p = Popen(command, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    nx_ret = ret.split("\n")
    return nx_ret

def sche_conf(minute,hour,day):
    active_user = output('whoami')[0]
    cmd = "%s %s %s * * /root/run_reqular_chk.sh\n"%(minute,hour,day)
    with open("/var/spool/cron/%s"%active_user,"w") as out:
        out.write(cmd)
    call(['systemctl', 'restart','crond'])
    print "%s는 주기적으로 /root/reqular_chk.sh를 실행해 /tmp/history에 저장합니다."%active_user

def show_set():
    set_mon = 'Y'
    set_mon = raw_input("설정된 스케줄러를 확인하시겠습니까?[Y]")
    if set_mon== 'y' or set_mon == 'Y' or set_mon =='':
        print "설정된 crontab은 다음과 같습니다."
        print output('crontab -l')
        print "\n현재의 cron 데몬의 상태는 다음과 같습니다."
        sys_stat = output('systemctl status crond')
        for i in sys_stat:
            print i

if __name__ == '__main__':
    minute = raw_input("설정할 분을 입력하세요 [Tip '*'을 입력하면 매분 실행됩니다.] :")
    hour = raw_input("설정할 시를 입력하세요 [Tip '*'을 입력하면 매시 실행됩니다.] :")
    day = raw_input("설정할 일을 입력하세요 [Tip '*'을 입력하면 매일 실행됩니다.] :")
    dirc()
    sche_conf(minute,hour,day)
    show_set()
