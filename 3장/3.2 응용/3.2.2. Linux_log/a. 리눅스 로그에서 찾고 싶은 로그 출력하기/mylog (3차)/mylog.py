#!/bin/env python
#-*- coding: utf-8 -*-

# 인자를 4개로 수정
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
        print get_log_data(logdata, index, pre_rowcount, next_rowcount)
        print "-" * 70
        
def get_log_data(logdata, start_index, pre_rowcount, next_rowcount) :
    enter_index = max(0, logdata.rfind("\n", 0, start_index))

    # 코드 수정 시작
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

    # 코드 수정 완료 
    return logdata[enter_index : enter_index2]
