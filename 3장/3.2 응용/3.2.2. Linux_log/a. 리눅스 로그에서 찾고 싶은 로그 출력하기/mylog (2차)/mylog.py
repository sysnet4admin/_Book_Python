#!/bin/env python
#-*- coding: utf-8 -*-

def printlog(logfile, search_word):
    f = open(logfile)
    logdata = f.read()
    f.close()

    index = logdata.find(search_word)

    if index  >= 0 :
        print "-" * 70
        print "Log file : ", logfile
        print "Find this word : ", search_word
        print "-" * 70
        
        # 함수를 호출할 때의 변수명( index)은 실제 함수의 변수명(start_index)과 달라도 됩니다.
        print get_log_data(logdata, index)        
        print "-" * 70

# 함수 추가(찾으려는 단어가 포함된 문장 한 줄을 뽑아내도록 추가할 부분)
def get_log_data(logdata, start_index) :
    # 찾은 단어의 위치보다 앞에 있는 줄 바꿈 문자 찾기
    enter_index = max(0, logdata.rfind("\n", 0, start_index))
    
    enter_index2 = logdata.find("\n", start_index, len(logdata))
    return logdata[enter_index : enter_index2]
