@echo off
setlocal
cd /d "%~dp0"
py -3 -m venv .venv
if errorlevel 1 goto erreur
".venv\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto erreur
".venv\Scripts\python.exe" build_windows.py
if errorlevel 1 goto erreur
echo.
echo Morgue-3.1.12.exe est dans le dossier dist.
echo Fermez l ancien Morgue puis lancez ce nouveau fichier.
echo Placez-le dans votre dossier habituel de donnees Morgue.
pause
exit /b 0
:erreur
echo.
echo Construction interrompue. Consultez le message ci-dessus.
pause
exit /b 1
