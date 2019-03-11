#!/bin/env python
#-*- coding: utf-8 -*-

from xlsxwriter import *

# 엑셀 파일 생성
workbook = Workbook('test.xlsx')

# 엑셀 시트(sheet) 추가
worksheet = workbook.add_worksheet()
data = "1 2 3 4 5"

columns = data.split()
for col_idx, col in enumerate(columns) :
    worksheet.write(0, col_idx, col)

workbook.close()
