#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import Popen
from subprocess import os
from subprocess import PIPE

def megacli(args):
    os.chdir('/opt/lsi/MegaCLI')
    cmd = './MegaCli ' + args
    p = Popen(cmd, shell=True, stdout=PIPE)
    (ret, err) = p.communicate()
    return ret

def get_slot_list(raid_info) :
    rows = status.split('\n')
    slot_list = {}
    encl_id = ''
    slot_num = ''
    media_err = 0
    other_err = 0
    firmware_state = ''
    for row in rows :
        cols = row.split(':')
        if cols[0].find('Enclosure Device ID') >= 0 :
            encl_id = cols[1].strip()
        elif cols[0].find('Slot Number') >= 0 :
            # 화면에 표시할 때, 슬롯 번호를 기준으로 숫자 단위 정렬. 따라서 숫자로 변환
            slot_num = int(cols[1].strip())
        elif cols[0].find('Media Error Count') >= 0 :
            media_err = cols[1].strip()
        elif cols[0].find('Other Error Count') >= 0 :
            other_err = cols[1].strip()
        elif cols[0].find('Firmware state') >= 0 :
            firmware_state = cols[1].strip()
            slot_list[slot_num] = (encl_id, media_err, other_err, firmware_state)
        else :
            continue
    return slot_list

def set_off_line(device_id, slot_num) :
    ret = ""
    ret = ret + megacli('-PDOffline -PhysDrv [%s:%d] -aAll' % (device_id, slot_num))
    ret = ret + "\n" + megacli('-PDMarkMissing -PhysDrv [%s:%d] -aAll' % (device_id, slot_num))
    ret = ret + "\n" + megacli(' -PDGetMissing -aALL')
    return ret

def set_ready_remove(device_id, slot_num) :
    return megacli('-PDPrpRmv -PhysDrv [%s:%d] -aAll' % (device_id, slot_num))

if __name__ == "__main__":
    cmd_args = '-PDList -aAll | egrep '
    cmd_args = cmd_args + '"Enclosure Device ID:|Slot Number:|In quiry data:|Error Count:|state"'
    status = megacli(cmd_args)

    # 슬롯 정보를 화면에 출력
    slot_list = get_slot_list(status)
    print "="*50
    print "Slot\tDvice\tMedia\tOther\tFirmware"
    print "Num\tID\tError\tError\tState"
    print "="*50
    slot_num_list = slot_list.keys()    # 딕셔너리에서 키가 되는 슬롯 번호 리스트를 가져옵니다.
    slot_num_list.sort()                # 슬롯 번호 리스트를 정렬합니다.

    for slot_num in slot_num_list :     # 정렬된 슬롯 번호 순서대로 관련 데이터를 화면에 출력
        (encl_id, media_err, other_err, firmware_state) = slot_list[slot_num]
        print "%s\t%s\t%s\t%s\t%s" % (slot_num, encl_id, media_err, other_err, firmware_state)

    # 사용자에게 슬롯 번호를 입력받음
    slot_num = input("Select a slot to remove : ")

    # 선택한 레이드 정보 하나를 가져옴
    # 가져온 레이드 정보는 (드라이브 ID, 미디어 에러, 기타 에러, 펌웨어 상태) 튜플 형태임
    (dv_id, media_err, other_err, firmware_state) = slot_list[slot_num]
    print set_off_line(dv_id, slot_num)
    print set_ready_remove(dv_id, slot_num)
    print megacli(cmd_args)
