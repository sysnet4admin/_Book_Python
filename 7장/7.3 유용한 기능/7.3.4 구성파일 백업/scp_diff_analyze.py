#!/bin/env python
#-*- coding: utf-8 -*-

from scp_diff import *
import re

def get_diff_start_row(contents, row_info_str) :
    datas = row_info_str.split()     # 공백으로 분할
    row_info = datas[1]              # 두 번째 데이터에 줄 번호가 있음
    datas = row_info.split(",")      # 쉼표(,)로 분할
    return datas[0]                  # 첫 번째는 시작 줄, 두 번째는 마지막 줄

def get_diff_contents(contents, spliter1, spliter2) :
    contents_list = contents.split(spliter1)            # 첫 번째 파일의 줄 번호 제목으로 데이터 구분
    contents_list = contents_list[1].split(spliter2)    # 두 번째 파일의 줄 번호 제목으로 데이터 구분
    return (contents_list[0], contents_list[1])

def change_data(contents, changed_list, start_row) :
    ret_list = []
    
    for changed in changed_list :
        line_num = contents.split(changed)[0].count("\n")   # 변경 내용 앞에 줄 바꿈 문자가 몇 개인지
        line_num = int(start_row) + line_num - 1            # 실제 변경된 줄 번호0(부터 시작하므로 -1 적용)

        reason = changed[0]
        changed = changed[2: len(changed)]

        if reason == "+" :
            reason = "추가"
        elif reason == "-" :
            reason = "삭제"
        else :
            reason = "변경"
        ret_list.append((reason, line_num, changed))        # (변경된 원인, 변경된 줄 번호, 변경 내용)

    return ret_list

def make_changed_msg(list1, list2) :
    msg_list = []
    i = 0
    while i < min(len(list1), len(list2)) :
        (reason1, line_num1, changed1) = list1[i]
        (reason2, line_num2, changed2) = list2[i]
       
        msg_list.append("[변경] %i행->%i행, %s -> %s" % (
            line_num1, line_num2, changed1, changed2))
        i = i + 1
    return msg_list

def make_msg(list) :
    msg_list = []
    for (reason, line_num, changed) in list :
        if changed == "" :              # 공백 칸이 추가/삭제되는 경우는 남기지 않음
            continue
        msg_list.append("[%s] %i행, %s" % (reason, line_num, changed))
    return msg_list

def delete_time_change(changed_list):
    for i, data in enumerate(changed_list):
        if data.startswith("!Time: ") :
            changed_list.pop(i)         # 변경 내용 중에서 의미 없는 부분을 배제하기 위해 리스트에서 제거
    return changed_list

def analyze_diff(diff_result) :
    # 변경 내용이 단위별로 나타나므로 분할
    diff_list = diff_result.split("***************\n")

    analyze_list = []
    for diff_data in diff_list :
        diff_row_list = re.findall("[\*|-]{3,4} [0-9]*,?[0-9]* [\*|-]{3,4}", diff_data)
        if len(diff_row_list) == 0 :
            continue

        # diff_title1: 첫 번째 파일의 변경 범위를 알려주는 제목
        # diff_title2: 두 번째 파일의 변경 범위를 알려주는 제목
        diff_title1 = diff_row_list[0]
        diff_title2 = diff_row_list[1]

        # 첫 번째 파일과 두 번째 파일의 제목에서 각각 변경 시작 줄 번호를 찾음
        row1 = get_diff_start_row(diff_data, diff_title1)
        row2 = get_diff_start_row(diff_data, diff_title2)

        # 첫 번째 파일의 변경 내용과 두 번째 파일의 변경 내용을 추림
        (diff1, diff2) = get_diff_contents(diff_data, diff_title1, diff_title2)

        # 변경 내용 중 실제 변경된 줄만 리스트로 작성
        # change_list1이 change_list2 로 변경됨
        # 삭제는 첫 번째 파일에, 추가는 두 번째 파일에 변경 내용으로 기록됨
        changed_list1 = re.findall("! .*", diff1)
        changed_list2 = re.findall("! .*", diff2)
        changed_list1 = delete_time_change(changed_list1)
        changed_list2 = delete_time_change(changed_list2)
        
        delete_list = re.findall("- .*", diff1)
        add_list = re.findall("\+ .*", diff2)

        # 실제 변경/추가/삭제 중 어떤 변경이 이뤄졌는지
        # 파일의 몇 번째 줄이 어떤 내용으로 바뀌었는지
        # (reason, line_num, changed)의 튜플로 변경된 리스트 개수와 동일한 리스트로 반환
        list1 = change_data(diff1, changed_list1, row1)
        list2 = change_data(diff2, changed_list2, row2)
        delete_detail_list = change_data(diff1, delete_list, row1)
        add_detail_list = change_data(diff2, add_list, row2)
        
        # 메시지 작성
        # 변경됐다면 list1에서 list2로 어떻게 바뀌었는지 메시지 작성
        changed_msg_list = make_changed_msg(list1, list2)
        delete_msg_list = make_msg(delete_detail_list)
        add_msg_list = make_msg(add_detail_list)
        analyze_list = analyze_list + changed_msg_list + delete_msg_list + add_msg_list
    return analyze_list

if __name__ == "__main__":
    input_data = get_input_data()
    if input_data != None :
        (dir_path, start_date, end_date) = input_data
        scp_file_list = get_file_list(dir_path, start_date, end_date)
        if len(scp_file_list) == 0 :
            print "선택한 기간 동안 백업된 파일이 없습니다."
        elif len(scp_file_list) == 1 :
            print "선택한 기간 동안 백업된 파일이 1건이어서 변경 사항을 비교할 수 없습니다."
        else :
            i = 0
            while i < len(scp_file_list) - 1 :
                diff_file1 = scp_file_list[i]
                diff_file2 = scp_file_list[i+1]
                str_list1 = diff_file1.split("-running-config-")
                str_list2 = diff_file1.split("-running-config-")
                diff_date1 = str_list1[len(str_list1) - 1]
                diff_date2 = str_list1[len(str_list2) - 1]
                print "[%s-%s 비교]" % (diff_date1,diff_date2)
                cmd_result = diff(scp_file_list[i], scp_file_list [i+1])
                
                # 분석 결과를 출력하는 코드
                msg_list = analyze_diff(cmd_result)
                for msg in msg_list :
                    print msg
                print "=" * 80
                i = i + 1
