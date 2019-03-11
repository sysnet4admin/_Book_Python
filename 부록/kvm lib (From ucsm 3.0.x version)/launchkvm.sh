#!/bin/bash
# ================================================
# ================== KVM launcher ================
# ================================================

export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
export PATH=$PATH:.:./libs/avctVMWin32.jar:./libs/avctKVMIOWin32.jar
export CP=./libs/avctKVMIOLinux32.jar:./libs/avctKVMIOLinux64.jar:./libs/avctKVMIOWin32.jar:./libs/avctNuova.jar:./libs/avctVMLinux32.jar:./libs/avctVMLinux64.jar:./libs/avctVMWin32.jar:./libs/lzvcnt.jar 

USERNAME=
PASSWORD=
HOST=

usage()
{
    echo "Usage: $0 -u username -p password -h host_ip"
}

while getopts "u:p:h:" opt
do
    case "$opt" in
        u) USERNAME="$OPTARG";;
        p) PASSWORD="$OPTARG";;
        h) HOST="$OPTARG";;
        \?) usage;;
        *) usage;;
    esac
done

JAVA_VERSION=`java -version 2>&1 | grep "java version" | awk '{ print substr($3, 2, length($3)-2); }'`
JAVA_MAJOR=`echo $JAVA_VERSION | awk -F "." '{ print $1 }'`
JAVA_MINOR=`echo $JAVA_VERSION | awk -F "." '{ print $2 }'`

if [ $JAVA_MAJOR -gt 1 ] || [ $JAVA_MINOR -ge 6 ]
then
    if [ -z $USERNAME ] || [ -z $PASSWORD ] || [ -z $HOST  ]
    then
        java -Xms256M -Xmx512M -classpath $CP Launcher
    else
        java -Xms256M -Xmx512M -classpath $CP com.avocent.nuova.kvm.Main ip=$HOST user=$USERNAME passwd=$PASSWORD title="KVM on $HOST" apcp=1 version=2 kmport=2068 vport=2068 sslv3=1 autoEof=0 tempunpw=0 aimpresent=0 power=0 vm=1 chat=1 export=1 dvr=2 statusbar=ip,un,fr,bw,kp,enc,led custom=2
    fi
else
    echo "KVM requires Java Runtime Environment 1.6 or greater"
fi
