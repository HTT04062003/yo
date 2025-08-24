import sqlite3
from datetime import datetime
import requests
import queue
class myDataBase:
    def __init__(self):
        self.qr_queue = queue.Queue()
        self.running = True
    def send_qr_to_google_sheet(self, product_id):
        self.qr_queue.put(product_id)  # ✅ Thêm vào hàng đợi
        print(f"Đã thêm vào hàng đợi: {product_id}")

    def _process_queue(self):
        url = "https://script.google.com/macros/s/AKfycbw78nCXbF6j6PyQ-_exabkfW2edf0GoTTpI2aKCGinR5ugb_BqFNnb8i0F1UhB-ZJ7s/exec"
        while self.running:
            try:
                product_id = self.qr_queue.get(timeout=1)
                data = {"product_id": product_id}
                response = requests.post(url, json=data)
                print(f"Đã gửi {product_id}: {response.text}")
                self.qr_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print("Lỗi khi gửi:", e)
# Khởi tạo class
my_dataBase_obj = myDataBase()