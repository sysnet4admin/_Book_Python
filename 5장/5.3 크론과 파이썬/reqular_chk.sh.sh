#!/usr/bin/env bash

echo -e "동작 시간과 런큐(run queue)를 확인"
uptime

echo -e "\nCPU 코어별 사용률 표시"
mpstat -P ALL

echo -e "\n메모리 사용률이 높은 프로세스 20개를 정렬"
ps aux --sort -pmem | head -n 20

echo -e "\n가상메모리 사용 현황"
vmstat -s

echo -e "\n네트워크 인터페이스별 사용량 및 에러"
netstat -i

echo -e "\n네트워크 프로토콜별 통계"
netstat -s

echo -e "\n디스크 마운트 상태 및 용량"
lsblk

echo -e "\n디스크 사용률 정보 표시"
iostat -x