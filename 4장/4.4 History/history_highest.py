#!/bin/env python
#-*- coding: utf-8 -*-

from history_all import *

def history_usage(history_list) :
    # (명령어, 사용 횟수)의 리스트 작성 - 가장 많이 사용된 명령어 순서로 만든 리스트
    cmd_list = []
    for h in history_list :
        cmd_list.append(h[1])   # h는 (시간, 명령어)의 튜플이므로 명령어는 h[1]입니다.

    # 중복된 내용을 제거한 명령어 리스트
    cmd_key_list = list(set(cmd_list))  # cmd_list에는 같은 명령어가 많으므로 중복 제거

    # 원본 cmd_list에서 명령어 개수 체크하기
    cnt_list = []
    for cmd in cmd_key_list :
        cnt_list.append(cmd_list.count(cmd))

    # 명령어 사용 횟수가 가장 많은 순서대로 재정렬
    usage_sort = []
    i = 0
    while len(cnt_list) > 0:
        max_cnt = max(cnt_list)
        max_index = cnt_list.index(max_cnt)
        cmd = cmd_key_list.pop(max_index)
        cnt = cnt_list.pop(max_index)
        usage_sort.append((cmd, cnt))

    return usage_sort

if __name__ == "__main__":
    accounts = get_accounts()
    for account in accounts :
        print "계정 :", account
        history_list = history(account)
        if len(history_list) == 0:
            print "\t기록된 이력 없음"          # 이력이 없을 때
        else :
            # history_usage 함수를 이용해 많이 사용한 순서의 명령어 리스트로 3건의 이력 정보 출력
            usage = history_usage(history_list)
            i = 0
            while i < min(3, len(usage)) :      # 이력이3 건보다 적으면 이력 수만큼 출력
                (cmd, cnt) = usage[i]
                if i == 0:
                    print "\t가장 많이 사용한 명령어 : %s (%d번)" % (cmd, cnt)
                else :
                    print "\t%d번째 많이 사용한 명령어 : %s (%d번)" % ((i + 1), cmd, cnt)
                i = i + 1
        print "-" * 70
