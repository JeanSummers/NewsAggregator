@ECHO OFF

rem manage.py convenience script


set managePath="aggregator/manage.py"
set manageRun=python %managePath%

rem Production server ip and port here
rem local address must be set in config.bat
set apiIP=ENTER_IP_HERE
set apiPORT=ENTER_PORT_HERE

IF EXIST config.bat call config

IF "%1" == "run" (
    %manageRun% runserver
    GOTO:return
)

IF "%1" == "test" (
    rem No tests yet
    rem %manageRun% test "appname"
    ECHO TESTED
    GOTO:return
)

IF "%1" == "migrate" (
    %manageRun% makemigrations
    %manageRun% migrate
    GOTO:return
)

IF "%1" == "start" (
    env start 
    call %0 migrate && ^
call %0 test && ^
call %0 manage runserver %apiIP%:%apiPORT%

    GOTO:return
)

IF "%1" == "shell" (
    %manageRun% shell
    GOTO:return
)

if "%1" == "manage" (
    rem Pass rest arguments to manage.py
    %manageRun% %2 %3 %4 %5 %6 %7 %8 %9
    GOTO:return
)

if "%1" == "init" (
    copy "config.example.bat" ^
"config.bat"

    cd aggregator/aggregator/
 
    copy "settings_local.example.py" ^
"settings_local.py"

    cd ../..

    env install

    GOTO:return
)

ECHO Usage:
ECHO %0 run
ECHO     Fast server start
ECHO %0 start
ECHO     Migrate, tests and start
ECHO %0 test
ECHO     Run all tests
ECHO %0 migrate
ECHO     Make all migrations
ECHO %0 shell
ECHO     Opens django shell
ECHO %0 manage
ECHO     Call manage.py directly

:return