@ECHO OFF

rem manage.py convenience script


set managePath="aggregator/manage.py"
set manageRun=python %managePath%

IF "%1" == "run" (
    %manageRun% runserver
    GOTO:return
)

IF "%1" == "test" (
    rem No tests yet
    rem %manageRun% test "appname"
    GOTO:return
)

IF "%1" == "migrate" (
    %manageRun% makemigrations
    %manageRun% migrate
    GOTO:return
)

IF "%1" == "start" (
    call %0 migrate && call %0 test && call %0 start
    GOTO:return
)

IF "%1" == "shell" (
    %manageRun% shell
    GOTO:return
)

if "%1" == "manage" (
    %manageRun% %2 %3 %4 %5 %6 %7 %8 %9
    GOTO:return
)

ECHO Usage:
ECHO %0 run
ECHO     Fast server start
ECHO %0 start
ECHO     Migrate, run tests and start
ECHO %0 test
ECHO     Run all tests
ECHO %0 migrate
ECHO     Make all migrations
ECHO %0 shell
ECHO     Opens django shell
ECHO %0 manage
ECHO     Call manage.py directly


:return