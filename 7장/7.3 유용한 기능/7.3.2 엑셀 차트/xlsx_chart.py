#!/bin/env python
#-*- coding: utf-8 -*-

from xlsxwriter.workbook import Workbook

def get_fan_logs() :
    data = [
        ['Count', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'],
        [1, 42, 531, 424, 424, 424, 424, 424,424,424,424,6, 0, 27], 
        [2, 42, 531, 424, 424, 424,17, 424,424,424,424,6, 0, 27], 
        [3, 42, 531, 424, 424, 424, 424, 424,424,424,424,6, 0, 27], 
        [4, 42, 424, 424, 424, 424,17, 424,424,424,424,6, 0, 27], 
        [5, 42, 531, 424, 424, 424,17, 424,424,424,424,6, 0, 27], 
        [6, 42, 424, 424, 424, 424,17, 424,424,424,424,6, 0, 27], 
        [7, 42, 424, 424, 424, 424, 424, 424,424,424,424,6, 0, 27], 
        [8, 42, 531, 424, 424, 424, 424, 424,424,424,424,6, 0, 27], 
        [9, 42, 424, 424, 424, 424,17, 424,424,424,424,6, 0, 28], 
        [10, 42, 424, 424, 424, 424, 424, 424,424,424,424,6, 0, 28]
    ]
    return data

def write_chart_xlsx(file_path, data) :
    workbook = Workbook(file_path)                  # 엑셀 파일 생성
    worksheet = workbook.add_worksheet()

    chart = workbook.add_chart({'type': 'line'})    # 엑셀 파일에 라인 차트 추가

    i = 0
    while i < len(data) :                           # A1행부터 A12행(11줄)까지 데이터 작성
        worksheet.write_row('A%i'%(i+1), data[i])   # 행마다 A~N열까지 데이터 리스트 작성
        i = i + 1

    # 엑셀 파일에 추가한 데이터를 바탕으로 차트 작성
    XLS_COL_NUM = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q']
    i = 1
    while i < len(data[0]) :
        chart.add_series({
            'name' : 'Sheet1!$%s$1' % XLS_COL_NUM[i],
            'categories': ('=Sheet1!$A$2:$A$%d'% len(data)),
            'values': '=Sheet1!$%s$2:$%s$%d' % (XLS_COL_NUM[i], XLS_COL_NUM[i], len(data)),
            'marker': {'type': 'automatic'},
        })
        i = i + 1
        
    # 차트 제목 설정 (X축 이름)
    chart.set_x_axis({
        'name': 'Sheet1!$A$1'
    })

    worksheet.insert_chart('E13', chart)
    workbook.close()        # 닫기

if __name__ == "__main__":
    data = get_fan_logs()
    write_chart_xlsx('sample.xlsx', data)
    print "샘플 차트를 작성했습니다 : sample.xlsx"
