#!/bin/env python
#-*- coding: utf-8 -*-

def printlog(logfile, search_word, pre_rowcount, next_rowcount):
    f = open(logfile)
    logdata = f.read()
    f.close()
    
    index = logdata.find(search_word)

    if index >= 0 :
        print "-" * 70
        print "Log file : ", logfile
        print "Find this word : ", search_word
        print "-" * 70

        # 코드 수정 시작 (찾으려는 단어가 포함된 로그와 단어가 발견된 개수를 가져오도록 수정할 부분)
        (data, count) = get_log_data(logdata, search_word, index, pre_rowcount, next_rowcount)
        print data
        print "추출한 로그 개수 :", count
        # 코드 수정 완료
        
def get_log_data(logdata, search_word, start_index, pre_rowcount, next_rowcount) :
    # 코드 수정 시작
    count = 0
    ret = ""

    while start_index >= 0 :
    # 코드 수정 완료
        enter_index = max(0, logdata.rfind("\n", 0, start_index))
        for i in range(0, pre_rowcount):
            enter_index = max(0, logdata.rfind("\n", 0, enter_index))
            
        enter_index2 = logdata.find("\n", start_index, len(logdata))
        for i in range(0, next_rowcount):
            next_end_index2 = logdata.find("\n", enter_index2 + 1, len(logdata))
            if next_end_index2 == -1 :
                next_end_index2 = enter_index2
                break
            else :
                enter_index2 = next_end_index2

        # 코드 수정 시작
        ret = ret + logdata[enter_index : enter_index2]     # 로그 누적
        ret = ret + "\n" + ("-" * 70)                       # 구분하기 위해 엔터를 출력하고 '-'를 70번 출력

        # 한 번 출력한 로그의 마지막 줄 바꿈 위치(enter_index2) 뒤부터 찾고자 하는 단어를 찾습니다.
        # 따라서 index가 재조정되며 여러 번 반복한 다음에는 index가 -1이 되어 while 문을 종료합니다.
        start_index = logdata.find(search_word, enter_index2 + 1)
        count = count +1                                    # 로그를 찾은 횟수 갱신
        
    return (ret, count)
    # 코드 수정 완료
