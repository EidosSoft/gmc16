import os
import subprocess
import tkinter as tk
from tkinter import messagebox

class GMCLauncher:
    def __init__(self, root):
        self.root = root
        root.title("GMC-16 Launcher")
        root.geometry("400x300")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.emu_path = os.path.join(self.base_dir, "gmc16.exe")
        if not os.name == 'nt':
            self.emu_path = os.path.join(self.base_dir, "gmc16")

        self.examples_dir = os.path.join(self.base_dir, "examples")

        if not os.path.exists(self.emu_path):
            messagebox.showerror("Ошибка", "Исполняемый файл gmc16 не найден!\nЗапустите build_exe.bat или build_exe.sh")
            root.destroy()
            return

        if not os.path.exists(self.examples_dir):
            messagebox.showerror("Ошибка", "Папка examples не найдена")
            root.destroy()
            return

        self.files = [f for f in os.listdir(self.examples_dir) if f.endswith(".gmc")]
        if not self.files:
            messagebox.showwarning("Нет программ", "Нет .gmc файлов в папке examples/")
            root.destroy()
            return

        tk.Label(root, text="Выберите программу:").pack(pady=10)
        self.listbox = tk.Listbox(root, height=10)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        for f in self.files:
            self.listbox.insert(tk.END, f)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Запустить", command=self.run_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Выход", command=root.destroy).pack(side=tk.LEFT, padx=5)

    def run_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите программу")
            return
        filename = self.files[sel[0]]
        full_path = os.path.join(self.examples_dir, filename)
        subprocess.Popen([self.emu_path, full_path], shell=False)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GMCLauncher(root)
    root.mainloop()
