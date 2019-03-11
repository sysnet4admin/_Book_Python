#!/bin/env python
#-*- coding: utf-8 -*-

from cli import cli,clip

def eem_conf(interface):
    syslog_var1 = "configure terminal ; event manager applet Auto-Provisioning ;"
    syslog_var2 = "event syslog pattern 'Interface Ethernet%s is up in mode access'"%interface
    syslog_var_pattern = syslog_var1 + syslog_var2

    cli(syslog_var_pattern)
    cli("configure terminal ; event manager applet Auto-Provisioning ;                  \
         action 1.0 syslog priority notifications msg Run_Python_Auto_Provisioning")
    cli("configure terminal ; event manager applet Auto-Provisioning ;                  \
         action 2.0 cli python bootflash:scripts/auto_provisioning.py")
    cli("configure terminal ; event manager applet Auto-Provisioning ;                  \
         action 3.0 syslog priority notifications msg Finish_Python_Auto_Provisioning")

if __name__ == "__main__":
    interface='1/24'
    interface = raw_input("어떤 인터페이스로 nxos 이미지를 내려받으시겠습니까?[1/24]")
    if interface=='':
        interface='1/24'
    eem_conf(interface)
    clip("show running-config eem")
