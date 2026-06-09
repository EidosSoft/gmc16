#!/bin/bash
echo "Сборка gmc16..."
pip3 install pyinstaller
pyinstaller --onefile --console --name gmc16 run.py
if [ -f "dist/gmc16" ]; then
    cp dist/gmc16 .
    chmod +x gmc16
    echo "Готово: ./gmc16"
else
    echo "Ошибка сборки"
fi
