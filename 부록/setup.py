#!/bin/env python
#-*- coding: utf-8 -*-
    
from distutils.core import setup
import py2exe
from glob import glob
import os

file_list = {}
options={
    "bundle_files":1,                                   # 컴파일된 파이썬 코드와 관련 패키지 라이브러리를 하나로 묶어서 배포하기 위한 옵션으로 64비트에서는 사용하지 못하는 옵션입니다.
    "dll_excludes":["MSVCP90.dll", "w9xpopen.exe"],     # 설치 과정에서 포함하지 않을 dll을 정의합니다.
    "includes" : ["sip", "_cffi_backend"],              # 포함할 라이브러리를 지정합니다. sip는 PyQt4 코드를 배포할 때 사용합니다. _cffi_backend는 paramiko 모듈이 사용하는 라이브러리입니다. (ssh_check_type.py 모듈에서 paramiko 모듈을 임포트하고 있음)
    "packages": [ "packaging", "xml", "ucsmsdk", "paramiko"],   # 함께 배포될 패키지를 정의합니다.packaging은 배포 시 사용되는 패키지입니다. xml, ucsmsdk은 코드에서 사용한 vKVM 접속과 관련된 패키지입니다.
# paramiko: SSH 접속 테스트를 위한 패키지
}
datas=[
    ("", ["./grey.png", "./green.png", "./orange.png", "./red.png", "./blank.png", "./environment.cfg"])
]

def get_file_list(path) :           # 하위 파일 리스트를 모두 찾습니다.
    global file_list
    if os.path.isdir(path) :
        for path in glob(path + "/*") :
            get_file_list(path)
    else :
        dirname = os.path.dirname(path).replace("c:/", "")
        path = path.replace("\\", "/")
        if file_list.get(dirname) == None :
            file_list[dirname] = [path]
        else :
            file_list[dirname].append(path)

def append_kvm_files() :
    global datas
    get_file_list("./kvm")
    keys = file_list.keys()
    keys.sort()
    for dirname in keys :
        datas.append((dirname, file_list[dirname]))     # kvm의 파일을 모두 찾아서 datas에 포함시킴
append_kvm_files()
setup(
    options = {"py2exe" : options},                     # options : 설치 옵션을 정의
    data_files = datas,                                 # datas: EXE 실행 파일을 만들 때 함께 복사할 파일
    windows=["vkvm_launch_dialog.py"],                  # 윈도우 형태의 실행 파일을 작성할 파이썬 코드
)
