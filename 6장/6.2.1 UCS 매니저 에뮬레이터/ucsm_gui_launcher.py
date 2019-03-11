#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch

def ucsm_gui_launch(ucsm_ip,user,password):
    handle = UcsHandle(ucsm_ip,user,password)
    handle.login()
    ucs_gui_launch(handle)
    handle.logout()

if __name__ == "__main__":
    ucsm_gui_launch('192.168.56.250','ucspe','ucspe')
