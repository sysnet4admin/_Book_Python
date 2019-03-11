#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import os
from subprocess import Popen

def megacli(args):
    os.chdir('/opt/lsi/MegaCLI')
    cmd = './MegaCli ' + args
    Popen(cmd, shell=True)

def check_raid_info() :
    print "a. Check the Raid Adapter Time."
    print "b. Check the Raid Adapter Information."
    print "c. Save the Information of Adapter as a file."
    print "d. Save the Status of Battery as a file."

    # 문자를 입력받을 때는 다음과 같이 raw_input을 사용합니다.
    abc = raw_input("Select to execute[a-d] : ")

    while abc < "a" or abc > "d" :
        abc = raw_input("Wrong input. Select to execute[a-d] : ")

    if abc =='a' :
        megacli("-AdpGetTime -aAll")
    elif abc =='b' :
        megacli("-AdpAllInfo -aAll")
    elif abc =='c':
        megacli("-AdpAllInfo -aAll >> /tmp/Adapall.txt")
        print "Success to save : /tmp/Adpall.txt"
    elif abc =='d' :
        megacli("-AdpBbuCmd -GetBbuStatus -aAll >> /tmp/bbu.txt")
        print "Success to save : /tmp/bbu.txt"  
                        
def check_raid_disk() :
    print "a. Save the Physical Disk Status as a file."
    print "b. Save the Cache Policy as a file."

    # 숫자를 입력받을 때는 다음과 같이 input을 사용합니다.
    abc = raw_input("Select to execute[a-b] : ")
    if abc =='a' :
        megacli("-PDList aALL >> /tmp/pd.txt")
        print "Success to save : /tmp/pd.txt"
    elif abc =='b' :
        megacli("-LDGetProp -Cache -LALL -aAll >> /tmp/VD.txt")
        print "Success to save : /tmp/VD.txt"
      
def collect_raid_log() :
    print "a. Save the adapter event log as a file."
    print "b. Save the firmware event log as a file."
    abc = raw_input("Select to execute[a-b] : ")
    if abc =='a' :
        megacli("-AdpEventLog -GetEvents -f /tmp/eventlog.txt -aAll >> /dev/null")
        print "Success to save : /tmp/eventlog.txt"
    elif abc =='b' :
        megacli("-fwtermlog -dsply -aAll > /tmp/lsi-fwterm.log")
        print "Success to save : /tmp/lsi-fwterm.log"

if __name__ == "__main__":                                                              
    print "1. Check & Collect the General Raid Adapter Information."
    print "2. Collect the Raid Disk Information."
    print "3. Collect the Raid Event Log."

    inputValue = input("Select to execute[1-3] : ")
    while inputValue < 1 or inputValue > 3 :
        inputValue = input("Wrong input. Select to execute[1-3] :")

    if inputValue == 1:
        check_raid_info()
    elif inputValue == 2:
        check_raid_disk()
    elif inputValue == 3:
        collect_raid_log()
