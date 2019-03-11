@ECHO OFF
REM ================================================
REM ================== KVM launcher ================
REM ================================================

REM Linux jars included only to be consistent, won't actually be used for this .bat file
java -d64 -version > NUL 2>&1
if '%errorlevel%' == '0' (
set CP=.\libs\avctKVMIOLinux32.jar;.\libs\avctKVMIOLinux64.jar;.\libs\avctKVMIOWin64.jar;.\libs\avctNuova.jar;.\libs\avctVMLinux32.jar;.\libs\avctVMLinux64.jar;.\libs\avctVMWin64.jar;.\libs\lzvcnt.jar 
set LIBPATH=.
)
java -d32 -version > NUL 2>&1
if '%errorlevel%' == '0' (
set CP=.\libs\avctKVMIOLinux32.jar;.\libs\avctKVMIOLinux64.jar;.\libs\avctKVMIOWin32.jar;.\libs\avctNuova.jar;.\libs\avctVMLinux32.jar;.\libs\avctVMLinux64.jar;.\libs\avctVMWin32.jar;.\libs\lzvcnt.jar 
set LIBPATH=.\32BitLibs
)

SET KVML_USAGE=Usage: launchkvm.bat -u username -p password -h host_ip
SET USERNAME=
SET PASSWORD=
SET HOST=

:LOOPARGS
IF "%1" == "" goto :CONTINUEON
set ARG1=%1
REM position to next argument with SHIFT to get the associated value
SHIFT

REM if there is not a second argument in a pair then show usage and exit
IF "%1" == "" (
ECHO %KVML_USAGE%
goto :END
)

IF "%ARG1%" == "-p" (
SET PASSWORD=%1
goto :NEXTARG
)

IF "%ARG1%" == "-u" (
SET USERNAME=%1
goto :NEXTARG
)

IF "%ARG1%" == "-h" (
SET HOST=%1
goto :NEXTARG
)

ECHO %KVML_USAGE%
goto :END

:NEXTARG
REM position to next argument with SHIFT
SHIFT

REM if no more argument continue on to rest of bat script
IF "%1" == "" goto :CONTINUEON
goto :LOOPARGS
goto :END
:CONTINUEON

IF "%USERNAME%" == "" goto :LAUNCHER
IF "%PASSWORD%" == "" goto :LAUNCHER
IF "%HOST%" == "" goto :LAUNCHER

goto :CLI

:LAUNCHER
java -Xms256M -Xmx512M -Djava.library.path=%LIBPATH% -classpath %CP% Launcher
goto :END

:CLI
java -Xms256M -Xmx512M -Djava.library.path=%LIBPATH% -classpath %CP% com.avocent.nuova.kvm.Main ip=%HOST% user=%USERNAME% passwd=%PASSWORD% title="KVM on %HOST%" apcp=1 version=2 kmport=2068 vport=2068 sslv3=1 autoEof=0 tempunpw=0 aimpresent=0 power=0 vm=1 chat=1 export=1 dvr=2 statusbar=ip,un,fr,bw,kp,enc,led custom=2
goto :END

:END
