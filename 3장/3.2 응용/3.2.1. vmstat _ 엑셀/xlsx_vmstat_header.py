#!/bin/env python
#-*- coding: utf-8 -*-

from subprocess import *
from xlsxwriter import *

cmd = "vmstat 1 5 | awk '{now=strftime(\"%Y-%m-%d %T \"); print now $0}'"
p = Popen(cmd, shell=True, stdout=PIPE)
(ret, err) = p.communicate()

workbook = Workbook('vmstat_merge_header.xlsx')
worksheet = workbook.add_worksheet()
rows = ret.split("\n")

for row_idx, row in enumerate(rows) :
    if row_idx == 0 :               # 첫 번째 헤더는 엑셀 파일에 쓰지 않음
        continue
    columns = row.split()
    for col_idx, col in enumerate(columns) :
        worksheet.write(row_idx, col_idx, col)

# 첫번째 헤더를 병합한 셀에 직접 작성
merge_format = workbook.add_format({ "bold" : 1, "align" : "center"})   # 포맷 설정
worksheet.merge_range("A1:B1", "datetime", merge_format)    # 하위 열 2개
worksheet.merge_range("C1:D1", "procs", merge_format)       # 하위 열 2개
worksheet.merge_range("E1:H1", "memory", merge_format)      # 하위 열 4개
worksheet.merge_range("I1:J1", "swap", merge_format)        # 하위 열 2개
worksheet.merge_range("K1:L1", "io", merge_format)          # 하위 열 2개
worksheet.merge_range("M1:N1", "system", merge_format)      # 하위 열 2개
worksheet.merge_range("O1:S1", "cpu", merge_format)         # 하위 열 5개

workbook.close()
print "vmstat_merge_header.xlsx 파일에 저장됐습니다."
