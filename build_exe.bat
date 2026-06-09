@echo off
echo Сборка gmc16.exe...
pip install pyinstaller
pyinstaller --onefile --console --name gmc16 run.py
if exist "dist\gmc16.exe" (
    copy /Y dist\gmc16.exe .
    echo Готово: gmc16.exe
) else (
    echo Ошибка сборки
)
pause
