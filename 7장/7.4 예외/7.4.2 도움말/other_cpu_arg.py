#!/bin/env python
#-*- coding: utf-8 -*-

import argparse

def arg_parser(parser) :
    parser.add_argument('conf',nargs=1, help='모니터링 구성 [필수 입력 항목]')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    print parser.parse_args()

if __name__ == "__main__":
    parser = argparse.ArgumentParser('other_cpu.py')
    arg_parser(parser)
    if len(sys.argv) > 1 :
        option =  sys.argv[1]
        if option == "conf" and os.path.exists(cfg_path) :
            os.remove(cfg_path)
