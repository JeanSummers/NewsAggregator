@ECHO OFF

rem venv managing script
rem Contains some simple commands 
rem for convenience reasons


set envName=venv

rem TODO: Add installation check
rem if directory exists
rem -r --reinstall flag
IF "%1" == "install" (
    ECHO   Installing virtualenv
    pip install virtualenv
    ECHO   Creating enviroment
    virtualenv %envName%
    ECHO   Activating enviroment
    %0 start
    ECHO   Installing requirements
    pip install -r requirements.txt
    GOTO:return
) 


IF "%1" == "start" (
    %envName%\Scripts\activate.bat
    GOTO:return
) 

IF "%1" == "exit" (
    %envName%\Scripts\deactivate.bat
    GOTO:return
) 

ECHO Usage:
ECHO %0 start
ECHO     Activates enviroment
ECHO %0 exit
ECHO     Deactivates enviroment
ECHO %0 install
ECHO     Installs virtual enviroment and
ECHO     all dependencies using pip

:return