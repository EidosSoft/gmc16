import sys

class GMC16:
    def __init__(self):
        self.mem = bytearray(65536)   # 64KB памяти
        self.regs = [0] * 8           # R0..R7
        self.pc = 0
        self.flags = 0                # биты: 0-Z, 1-C, 2-E, 3-L
        self.halted = False
        self._input_buffer = ""

    def _get_flag(self, bit):
        return (self.flags >> bit) & 1

    def _set_flag(self, bit, val):
        if val:
            self.flags |= (1 << bit)
        else:
            self.flags &= ~(1 << bit)

    def load_binary(self, data, base_addr=0x4000):
        for i, b in enumerate(data):
            self.mem[base_addr + i] = b & 0xFF
        self.pc = base_addr

    def _read_char(self):
        if sys.platform == 'win32':
            import msvcrt
            return msvcrt.getch().decode('utf-8', errors='ignore')
        else:
            import termios, tty
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return ch

    def run(self, max_steps=100000):
        step = 0
        while not self.halted and step < max_steps:
            try:
                cmd = self.mem[self.pc:self.pc+5]
                if len(cmd) < 5:
                    raise Exception("PC out of range")
                self.pc += 5
                self._execute(cmd)
                step += 1
            except Exception as e:
                print(f"\nОшибка на шаге {step}: {e}")
                break
        if self.halted:
            print("\n[Программа завершена (HLT)]")
        print(f"\n[Статистика: {step} шагов, PC=0x{self.pc:04X}, R0={self.regs[0]}]")

    def _execute(self, cmd):
        opcode = cmd[0] & 0x1F
        reg_dst = (cmd[1] >> 4) & 0x0F
        reg_src = cmd[1] & 0x0F
        imm16 = cmd[2] | (cmd[3] << 8)

        # MOV
        if opcode == 0x0A:   # 10
            if reg_src == 0 and imm16 != 0:
                self.regs[reg_dst] = imm16
            else:
                self.regs[reg_dst] = self.regs[reg_src]

        # ADD
        elif opcode == 0x06:   # 6
            res = self.regs[reg_dst] + self.regs[reg_src]
            self._set_flag(0, (res & 0xFFFF) == 0)
            self._set_flag(1, res > 0xFFFF)
            self.regs[reg_dst] = res & 0xFFFF

        # SUB
        elif opcode == 0x12:   # 18
            a = self.regs[reg_dst]
            b = self.regs[reg_src]
            res = a - b
            self._set_flag(0, (res & 0xFFFF) == 0)
            self._set_flag(1, a < b)
            self.regs[reg_dst] = res & 0xFFFF

        # AND
        elif opcode == 0x02:   # 2
            self.regs[reg_dst] &= self.regs[reg_src]

        # LOAD (абсолютная адресация)
        elif opcode == 0x1A:   # 26
            addr = imm16
            if addr == 0xFFF1:          # порт ввода
                print("\n[Введите символ] ", end='')
                ch = self._read_char()
                if ch:
                    self.regs[reg_dst] = ord(ch[0])
                else:
                    self.regs[reg_dst] = 0
                print()
            else:
                if addr + 1 >= len(self.mem):
                    raise Exception(f"LOAD out of range: {addr}")
                low = self.mem[addr]
                high = self.mem[addr+1]
                self.regs[reg_dst] = low | (high << 8)

        # STORE (абсолютная адресация)
        elif opcode == 0x1E:   # 30
            addr = imm16
            val = self.regs[reg_src]
            if addr == 0xFFF0:          # порт вывода
                print(chr(val & 0xFF), end='', flush=True)
            else:
                if addr + 1 >= len(self.mem):
                    raise Exception(f"STORE out of range: {addr}")
                self.mem[addr] = val & 0xFF
                self.mem[addr+1] = (val >> 8) & 0xFF

        # CMP
        elif opcode == 0x0E:   # 14
            a = self.regs[reg_dst]
            b = self.regs[reg_src]
            diff = a - b
            self._set_flag(0, (diff & 0xFFFF) == 0)
            self._set_flag(2, (diff & 0xFFFF) == 0)
            self._set_flag(3, (diff & 0x8000) != 0)

        # JMP
        elif opcode == 0x16:   # 22
            self.pc = imm16

        # JEQ
        elif opcode == 0x15:   # 21
            if self._get_flag(2):
                self.pc = imm16

        # JNE
        elif opcode == 0x17:   # 23
            if not self._get_flag(2):
                self.pc = imm16

        # JLT
        elif opcode == 0x18:   # 24
            if self._get_flag(3):
                self.pc = imm16

        # JGE
        elif opcode == 0x19:   # 25
            if not self._get_flag(3):
                self.pc = imm16

        # HLT
        elif opcode == 0x1F:   # 31
            self.halted = True

        else:
            raise Exception(f"Неизвестный опкод: {opcode}")
