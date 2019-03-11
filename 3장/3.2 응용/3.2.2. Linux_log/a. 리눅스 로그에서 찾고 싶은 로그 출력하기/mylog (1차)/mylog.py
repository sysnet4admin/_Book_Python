#!/bin/env python
#-*- coding: utf-8 -*-

def printlog(logfile, search_word):
    f = open(logfile)       # 파일 열기
    logdata = f.read()      # 파일 읽기
    f.close()               # 파일 닫기

    index = logdata.find(search_word)

    if index >= 0 :
        print "-" * 70
        print "Log file : ", logfile
        print "Find this word : ", search_word
        print index
        print "-" * 70
