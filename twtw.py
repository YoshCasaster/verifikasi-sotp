import tkinter as tk
from tkinter import messagebox
import time

class CodeEntryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Input Code")
        
        self.code_var = tk.StringVar()
        
        self.label = tk.Label(master, text="Masukkan Kode:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(master, textvariable=self.code_var)
        self.entry.pack(pady=10)
        
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_code)
        self.submit_button.pack(pady=10)
        
        self.codes = {
            "5menit": (300, None),  # 5 menit
            "1hari": (86400, None),  # 1 hari
            "1minggu": (604800, None)  # 1 minggu
        }
        
        self.current_code = None
        self.expiry_time = None
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def submit_code(self):
        code = self.code_var.get()
        if code in self.codes:
            self.current_code = code
            self.expiry_time = time.time() + self.codes[code][0]
            messagebox.showinfo("Success", f"Kode {code} berhasil diterima!")
            self.master.destroy()  # Tutup input code dan buka GUI utama
            self.open_main_gui()
        else:
            messagebox.showwarning("Error", "Kode tidak valid!")

    def open_main_gui(self):
        main_window = tk.Tk()
        main_window.title("Main GUI")
        
        self.check_expiry(main_window)
        
        main_window.mainloop()

    def check_expiry(self, main_window):
        if self.expiry_time and time.time() > self.expiry_time:
            messagebox.showwarning("Expired", "Waktu kode telah habis!")
            main_window.destroy()
            self.restart()
        else:
            main_label = tk.Label(main_window, text="Selamat datang di GUI Utama!")
            main_label.pack(pady=20)
            main_button = tk.Button(main_window, text="Keluar", command=main_window.quit)
            main_button.pack(pady=10)

            # Set timer untuk memeriksa waktu setiap detik
            main_window.after(1000, lambda: self.check_expiry(main_window))

    def restart(self):
        self.master = tk.Tk()
        self.__init__(self.master)  # Reset aplikasi
        self.master.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Apakah Anda yakin ingin keluar?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEntryApp(root)
    root.mainloop()