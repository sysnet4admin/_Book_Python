#!/bin/env python
#-*- coding: utf-8 -*-

import threading
from time import sleep

def prime_factors(x):
    factor_list=[]
    div=2
    while div<=x:
        if x%div==0:        # 나눗셈을 해서 자기 자신으로밖에 나누어 떨어지지 않는 경우는 소수
            x/=div
            factor_list.append(div)
        else:
            div+=1          # 나눗셈 기준값 증가
    return factor_list

class ThreadRange ( threading.Thread ) :
    def run(self):
        for i in range(9999999):        # 소수를 구하는 범위를 설정합니다.
            sleep(0.001)                # CPU의 사용량을 조절합니다.
            print prime_factors(i)

for i in range(5):                      # 스레드를 5개 생성해 CPU 사용량을 더 높입니다.
    ThreadRange().start()
