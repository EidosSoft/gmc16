#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$SCRIPT_DIR/examples"
EMU_EXE="$SCRIPT_DIR/gmc16"

if [ ! -f "$EMU_EXE" ]; then
    echo "Ошибка: gmc16 не найден. Запустите build_exe.sh"
    exit 1
fi

files=("$EXAMPLES_DIR"/*.gmc)
count=${#files[@]}

if [ $count -eq 0 ]; then
    echo "Нет .gmc файлов в examples/"
    exit 1
fi

echo "================================"
echo "      GMC-16 LAUNCHER"
echo "================================"
echo ""

for i in "${!files[@]}"; do
    filename=$(basename "${files[$i]}")
    echo "  $((i+1)). $filename"
done

echo ""
read -p "Выберите номер (1-$count): " choice

if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "$count" ]; then
    selected="${files[$((choice-1))]}"
    echo "Запуск: $selected"
    "$EMU_EXE" "$selected"
else
    echo "Неверный выбор."
fi
