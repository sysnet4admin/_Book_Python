#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.utils.ccoimage import get_ucs_cco_image_list
from ucsmsdk.utils.ccoimage import get_ucs_cco_image
from subprocess import os

def ucs_cco_image_search(cco_id,cco_password,keyword):
    global indexes
    global image_list

    # 이미지 리스트를 받아온 원본
    image_list = get_ucs_cco_image_list(cco_id,cco_password)
    
    # 이미지 리스트 중에 image_name이 포함된 줄만 추출
    i = 0
    str_img_list = []
    for number in image_list:
        str_img = str(image_list[i])
        idx = str_img.find("image_name")
        str_img = str_img[idx : str_img.find("\n", idx)].split()[1]
        str_img_list.append(str_img)
        i=i+1
   
    # 이미지를 검색해 다시 추출함
    indexes = [i for i, item in enumerate(str_img_list) if item.find(keyword)>=0]

    # 검색된 이미지 리스트
    i = 0
    print "=-"*20
    print "번호\t\t이미지 이름"
    print "-="*20
    for idx in indexes:
        print("%d") %i, str_img_list[idx]
        i=i+1    
        
def ucs_cco_image_download(selected_number):
    download_number = indexes[selected_number]
    get_ucs_cco_image(image=image_list[download_number], file_dir="/root/ccoimage")

if __name__ == "__main__":
    print "=-"*30
    print "UCS 이미지를 내려받으려면 시스코 홈페이지에 로그인해야 합니다."
    print "-="*30
    cco_id = raw_input("로그인 ID를 입력하세요 : ")
    cco_password = raw_input("로그인 암호를 입력하세요 : ")
    keyword = raw_input("검색할 이미지 이름 또는 버전을 입력하세요 (예 : 3.1.1e) : ")
    print "검색 중입니다."
    ucs_cco_image_search(cco_id,cco_password,keyword)
    selected_number= input("내려받을 이미지 번호를 선택하세요 : ")
    try:
       os.mkdir('/root/ccoimage')       # 디렉터리 생성 / 디렉터리가 있다면 생성되지 않음
    finally:
       print "내려받는 중입니다."
       ucs_cco_image_download(selected_number)  # 디렉터리의 존재와 관계없이 실행됨
