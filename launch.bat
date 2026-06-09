@echo off
title GMC-16 Launcher
echo ================================
echo      GMC-16 PROGRAM LAUNCHER
echo ================================
echo.

set "EXAMPLES_DIR=%~dp0examples"
set "EMU_EXE=%~dp0gmc16.exe"

if not exist "%EMU_EXE%" (
    echo Ошибка: gmc16.exe не найден в папке %~dp0
    echo Запустите build_exe.bat для сборки эмулятора.
    pause
    exit /b 1
)

setlocal enabledelayedexpansion
set count=0
for %%f in ("%EXAMPLES_DIR%\*.gmc") do (
    set /a count+=1
    set "file!count!=%%~nxf"
    set "path!count!=%%f"
)

if %count%==0 (
    echo Нет .gmc файлов в папке examples\
    pause
    exit /b 1
)

echo Доступные программы:
echo.
for /l %%i in (1,1,%count%) do (
    echo   %%i. !file%%i!
)
echo.
set /p choice="Введите номер программы (1-%count%): "

if %choice% geq 1 if %choice% leq %count% (
    call set "selected=%%path%choice%%%"
    echo.
    echo Запуск: !selected!
    "%EMU_EXE%" "!selected!"
) else (
    echo Неверный выбор.
    pause
)
