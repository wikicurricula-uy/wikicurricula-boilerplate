@echo off

rem Fetch Ghana's data
py bot.py en 117

rem Wait for the first script to finish
echo Waiting for the first script to finish...
timeout /t 10 /nobreak

rem Run the translation script
py translate.py Ghana

rem Fetch Uruguay script
py bot.py es 77

rem Wait for the second script to finish
echo Waiting for the second script to finish...
timeout /t 10 /nobreak

rem Run the translation script again
py translate.py Uruguay
pause