import tkinter as tk
import requests
import json

# Fungsi untuk mengambil data dari URL
def fetch_data():
    url = "https://raw.githubusercontent.com/YoshCasaster/verifikasi-sotp/refs/heads/main/otp_config.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

# Fungsi untuk mengirim permintaan
def send_request():
    target_number = entry_number.get()
    selected_service = service_var.get()
    
    # Mencari data untuk layanan yang dipilih
    service_data = next((item for item in services if item["name"] == selected_service), None)
    
    if service_data:
        url = service_data["url"]
        data = json.loads(service_data["data"].replace("target_number", target_number))
        headers = service_data["headers"]
        
        # Mengirim permintaan POST
        response = requests.post(url, headers=headers, json=data)
        
        # Menampilkan hasil
        if response.status_code == 200:
            result_label.config(text=f"OTP berhasil dikirim melalui {selected_service}!")
        else:
            result_label.config(text=f"Gagal mengirim OTP: {response.status_code} - {response.text}")
    else:
        result_label.config(text="Layanan tidak ditemukan.")

# Mendapatkan data dari URL
services = fetch_data()

# Membuat jendela utama
root = tk.Tk()
root.title("Pengirim OTP")

# Membuat label dan entry untuk nomor telepon
label_number = tk.Label(root, text="Masukkan Nomor Telepon:")
label_number.pack(pady=10)

entry_number = tk.Entry(root)
entry_number.pack(pady=10)

# Membuat dropdown untuk memilih layanan
service_var = tk.StringVar(root)
service_var.set(services[0]["name"])  # Set default value

service_menu = tk.OptionMenu(root, service_var, *[service["name"] for service in services])
service_menu.pack(pady=10)

# Tombol untuk mengirim permintaan
send_button = tk.Button(root, text="Kirim OTP", command=send_request)
send_button.pack(pady=20)

# Label untuk menampilkan hasil
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Menjalankan aplikasi
root.mainloop()