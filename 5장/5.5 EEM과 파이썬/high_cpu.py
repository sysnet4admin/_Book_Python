#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli
import time

def collecting_items(out_file):
    tmps = ["show system resources",
            "show process cpu sort | exclude 0.0",
            "show processes cpu history",
            "show system internal processes cpu",
            "show policy-map interface control-plane",
            "show hardware rate-limiter",
            "show hardware internal cpu-mac inband counters",
            "show hardware internal cpu-mac inband stats",
            "show system inband queuing status",
            "show system inband queuing statistics",
            "show system internal pktmgr internal vdc global-stats"]
    for tmp in tmps:
        str = cli(tmp)
        out_file.write(str)

def collect_log():
    now = time.localtime()
    st= "%04d%02d%02d_%02d%02d%02d_"%(now.tm_year, now.tm_mon, now.tm_mday,
                                     now.tm_hour, now.tm_min, now.tm_sec)
    tmp_file = "/bootflash/%sHighCPU.log"%st
    out_file = open(tmp_file, "w")
    collecting_items(out_file)
    out_file.close()

if __name__ == "__main__":
    collect_log()
