#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle
   
def change_lable(ucsm_ip,user,password):
    handle = UcsHandle(ucsm_ip,user,password)
    handle.login()
    print "\n-----------모든 블레이드 서버의 이름. 변경 전---------------"
    blades = handle.query_classid(class_id="computeBlade")
    for blade in blades:
        print "Blade-" + blade.slot_id + "     Lable:-" + blade.usr_lbl
        blade.usr_lbl = "Ironman" + blade.slot_id # 블레이드 이름 + 번호 
        handle.set_mo(blade)
        handle.commit()

    print "\n-----------모든 블레이드 서버의 이름. 변경 후---------------"
    blades = handle.query_classid(class_id="computeBlade")
    for blade in blades:
        print "Blade-" + blade.slot_id + "     Lable:-" + blade.usr_lbl
    handle.logout()
    
if __name__ == "__main__":
    ucsm_ip = raw_input("블레이드 이름을 변경할 UCS 매니저의 IP를 입력해 주세요 : ")
    change_lable(ucsm_ip,'ucspe','ucspe')


