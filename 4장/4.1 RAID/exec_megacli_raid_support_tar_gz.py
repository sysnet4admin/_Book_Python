#!/bin/env python
#-*- coding: utf-8 -*-

import tarfile
import os
import shutil
from exec_megacli_raid_infos import *

def make_tar(tar_name, files):
    tar = tarfile.open(tar_name, "w:gz")
    for name in files:
        tar.add(name)
    tar.close()

def collect_all_log() :
    print "Collecting logs .. "
    import time
    time.sleep(2)

    dirname = '/tmp/megacli'
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    megacli("-AdpGetTime -aAll >> %s/AdapTime.txt" % dirname )
    megacli("-AdpAllInfo -aAll >> %s/Adapall.txt" % dirname )
    megacli("-AdpBbuCmd -GetBbuStatus -aAll >> %s/bbu.txt" % dirname )
    megacli("-PDList aALL >> %s/pd.txt" % dirname )
    megacli("-LDGetProp -Cache -LALL -aAll >> %s/VD.txt" % dirname )
    megacli("-AdpEventLog -GetEvents -f %s/eventlog.txt -aAll >> /dev/null" % dirname )
    megacli("-fwtermlog -dsply -aAll  > %s/lsi-fwterm.log" % dirname )

    log_files =  [dirname + "/AdapTime.txt",
                  dirname + "/Adapall.txt",
                  dirname + "/bbu.txt",
                  dirname + "/pd.txt",
                  dirname + "/VD.txt",
                  dirname + "/eventlog.txt",
                  dirname + "/lsi-fwterm.log" ]
    time.sleep(5)
    make_tar("/tmp/MegaRaid.tar.gz",log_files )
    shutil.rmtree(dirname)
    print "Success to save : /tmp/MegaRaid.tar.gz"

if __name__ == "__main__":
    print "1. Check & Collect the General Raid Adapter Information."
    print "2. Collect the Raid Disk Information."
    print "3. Collect the Raid Event Log."
    print "4. Save the All Raid Logs as a tar.gz file."
    
    inputValue = input("Select to execute[1-4] : ")  
    if inputValue == 1: 
        check_raid_info() 
    elif inputValue == 2: 
        check_raid_disk() 
    elif inputValue == 3: 
        collect_raid_log() 
    elif inputValue == 4: 
        collect_all_log()