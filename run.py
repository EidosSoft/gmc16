import sys
from cpu import GMC16

def load_text_file(filename, cpu, base_addr=0x4000):
    data = bytearray()
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # удаляем комментарии
            comment = line.find(';')
            if comment >= 0:
                line = line[:comment]
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"Строка {line_num}: нужно 5 чисел, найдено {len(parts)}")
            for p in parts:
                if p.lower().startswith('0x'):
                    val = int(p, 16)
                else:
                    val = int(p)
                if val < 0 or val > 255:
                    raise ValueError(f"Строка {line_num}: число {val} вне диапазона 0..255")
                data.append(val)
    cpu.load_binary(data, base_addr)
    print(f"Загружено {len(data)} байт в 0x{base_addr:04X}")

def main():
    if len(sys.argv) < 2:
        print("Использование: python run.py <файл.gmc>")
        print("Пример: python run.py examples/hello.gmc")
        sys.exit(1)

    cpu = GMC16()
    try:
        load_text_file(sys.argv[1], cpu)
        cpu.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
