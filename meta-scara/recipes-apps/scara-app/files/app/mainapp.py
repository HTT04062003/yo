import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import thư viện Pillow
import serial
import re
import threading
from mainMenu import MainMenu
import queue
import time
from gcode_read import gCodeRead_Obj
from tkinter import messagebox
from socketTCP import socket_client
import mmap
import struct
import os
import sys
import cv2
from pyzbar import pyzbar
from dataBase import my_dataBase_obj
import queue
import numpy as np
from dataBase import my_dataBase_obj
SHM_NAME = "/shared_xyz"
SHM_SIZE = 48  # 12 floats * 4 bytes
image_label = None
tk_img = None
flag_add_new_item = threading.Event()
flag_add_new_item.set()
current_num_of_item = 0
def Get_Current_Num_Of_Item(s):
    match = re.search(r'G(-?\d+)', s)
    if match:
        num = int(match.group(1))
        return num
    return None
def open_shared_memory(name, size):
    fd = os.open(f"/dev/shm{name}", os.O_RDONLY)
    return mmap.mmap(fd, size, mmap.MAP_SHARED, mmap.PROT_READ)

def read_shared_data(mm):
    mm.seek(0)
    data = mm.read(SHM_SIZE)
    values = struct.unpack('12f', data)  # 12 float
    fields = [
        "cur_x", "cur_y", "cur_z",
        "cur_Theta1", "cur_Theta2", "cur_Theta3", "cur_Theta4",
        "F1", "F2", "F3", "F4",
        "curE"
    ]
    return dict(zip(fields, values))
def Update_MainMenu(Theta1_Val, Theta2_Val, Theta3_Val, Theta4_Val, X_Val, Y_Val, Z_Val, V1, V2, V3, V4):
    menu_frame.theta1_value_box.delete(0, tk.END)
    menu_frame.theta1_value_box.insert(tk.END, f"{Theta1_Val}")
    menu_frame.theta2_value_box.delete(0, tk.END)
    menu_frame.theta2_value_box.insert(tk.END, f"{Theta2_Val}")
    menu_frame.theta3_value_box.delete(0, tk.END)
    menu_frame.theta3_value_box.insert(tk.END, f"{Theta3_Val}")
    menu_frame.theta4_value_box.delete(0, tk.END)
    menu_frame.theta4_value_box.insert(tk.END, f"{Theta4_Val}")
    
    menu_frame.theta1_speed_value_box.delete(0, tk.END)
    menu_frame.theta1_speed_value_box.insert(tk.END, f"{V1}")
    menu_frame.theta2_speed_value_box.delete(0, tk.END)
    menu_frame.theta2_speed_value_box.insert(tk.END, f"{V2}")
    menu_frame.theta3_speed_value_box.delete(0, tk.END)
    menu_frame.theta3_speed_value_box.insert(tk.END, f"{V3}")
    menu_frame.theta4_speed_value_box.delete(0, tk.END)
    menu_frame.theta4_speed_value_box.insert(tk.END, f"{V4}")

    menu_frame.X_mmBox.delete(0, tk.END)
    menu_frame.X_mmBox.insert(tk.END, f"{X_Val}")
    menu_frame.Y_mmBox.delete(0, tk.END)
    menu_frame.Y_mmBox.insert(tk.END, f"{Y_Val}")
    menu_frame.Z_mmBox.delete(0, tk.END)
    menu_frame.Z_mmBox.insert(tk.END, f"{Z_Val}")


def receive_data():
    try:
        mm = open_shared_memory(SHM_NAME, SHM_SIZE)  # Mở shared memory một lần
        while True:
            data = socket_client.my_socket_obj.s.recv(1024)
            print(data)
            if not data:
                print("Server đã đóng kết nối.")
                break
            message = data.decode().strip()
            
            if message == socket_client.my_socket_obj.cmd_update_data:
                socket_client.my_socket_obj.cmd_from_server = socket_client.my_socket_obj.cmd_update_data

                # Đọc dữ liệu từ shared memory
                values = read_shared_data(mm)
                #print("Dữ liệu từ shared memory:", values)
                menu_frame.X = values["cur_x"]
                menu_frame.Y = values["cur_y"]
                menu_frame.Z = values["cur_z"]
                menu_frame.E = values["curE"]
                # Cập nhật GUI
                Update_MainMenu(
                    values["cur_Theta1"], values["cur_Theta2"],
                    values["cur_Theta3"], values["cur_Theta4"],
                    values["cur_x"], values["cur_y"], values["cur_z"],
                    values["F1"], values["F2"], values["F3"], values["F4"]
                )
            if message == socket_client.my_socket_obj.response_get_qr_code_item:
                print("ADD\n")
                flag_add_new_item.set()
    except Exception as e:
        print("Lỗi khi nhận dữ liệu:", e)

def on_press_button_connect():
    
    if menu_frame.question_frame :
            menu_frame.question_frame.destroy()  # Xóa frame cũ
    # Tạo frame mới
    menu_frame.question_frame = tk.Frame(menu_frame.frame)
    menu_frame.question_frame.configure(width=460, height= 200, bg= "white")
    menu_frame.create_question_menu_widgets("     Robot is ready.\nDo you want to Homing Robot ?")
    menu_frame.question_frame.place(x=300, y=200)
def connect_to_slave():
    
    socket_client.my_socket_obj.connect_to_server()

    if socket_client.my_socket_obj.s:
       # Khởi chạy thread nhận dữ liệu từ server
        threading.Thread(target=receive_data, daemon=True).start()
        threading.Thread(target=socket_client.my_socket_obj.send, daemon=True).start()
        menu_frame.create_table_obj.send_all_points()
        start_qr_thread()
        threading.Thread(target=my_dataBase_obj._process_queue, daemon=True).start()
        
def warehouse_pos(product_id):
    length_wh = 158
    dis_x = 0
    dis_y = 250

    if product_id % 3 != 0:
        center_x = (product_id % 3) * (length_wh / 3) - (length_wh / 6) + dis_x
        center_y = (int(product_id / 3) + 1) * (length_wh / 3) - (length_wh / 6) + dis_y
    else:
        center_x = length_wh - length_wh / 6 + dis_x
        center_y = (product_id / 3) * (length_wh / 3) - (length_wh / 6) + dis_y

    return round(center_x, 2), round(center_y, 2)
def adjust_gamma(image, gamma=5.0):  # gamma > 1 làm tối ảnh
    invGamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** invGamma * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)
def reduce_glare(frame):
    # Chuyển ảnh sang không gian HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Tách 3 kênh
    h, s, v = cv2.split(hsv)

    # Cắt độ sáng tối đa xuống thấp hơn để giảm chói
    v = np.clip(v, 0, 220)  # Giới hạn V ở mức tối đa 150 (thay vì 200 trước đó)

    # Hoặc giảm toàn bộ độ sáng (scale lại V)
    v = (v * 1.0).astype(np.uint8)  # Giảm toàn bộ độ sáng xuống 70%

    # Ghép lại ảnh HSV và chuyển về BGR
    hsv_reduced = cv2.merge((h, s, v))
    return cv2.cvtColor(hsv_reduced, cv2.COLOR_HSV2BGR)

def qr_scanner():
    cap = cv2.VideoCapture(0)
    print("📸 Đang bật camera, đưa mã QR vào khung hình...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # ⚡️ Giảm chói trước khi xử lý
        frame = reduce_glare(frame)

        # Chuyển sang xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Cân bằng histogram ảnh xám
        gray = cv2.equalizeHist(gray)

        # Quét QR từ ảnh xám
        qrcodes = pyzbar.decode(gray)

        for qrcode in qrcodes:
            (x, y, w, h) = qrcode.rect
            data = qrcode.data.decode("utf-8")

            # Vẽ khung và text lên ảnh gốc (màu)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 0, 255), 2)

            try:
                product_id = int(data)
                if product_id < 1 or product_id > 9:
                    raise ValueError("Out of range")

                center_x, center_y = warehouse_pos(product_id)
                cv2.putText(frame, f"({center_x},{center_y})", (x, y + h + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                try:
                    if flag_add_new_item.is_set():
                        socket_client.my_socket_obj.send_data(f"A{data}")
                        my_dataBase_obj.send_qr_to_google_sheet(product_id)
                        flag_add_new_item.clear()
                except Exception as e:
                    print("[QR Thread] Lỗi khi gọi send_data:", e)

            except ValueError:
                print(f"❌ Mã QR không hợp lệ hoặc không nằm trong [1..9]: {data}")

        # Gửi ảnh gốc đã vẽ lên GUI
        root.after(0, update_camera_frame, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
def update_camera_frame(frame):
    global tk_img, image_label
    # Chuyển ảnh sang định dạng hiển thị bằng Tkinter
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    pil_image = pil_image.resize((430, 290), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(pil_image)

    if image_label is None:
        image_label = tk.Label(menu_frame.child_frame, image=tk_img, bg="#2e2e2e")
        image_label.place(x=0, y=0)
    else:
        image_label.config(image=tk_img)
def start_qr_thread():
    threading.Thread(target=qr_scanner, daemon=True).start()
      
#**************************************MainForm********************************************#
# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng Dụng với Form Cài Đặt")
root.geometry("840x480")
root.configure(bg="#0F0A3F")


menu_frame = MainMenu(root)
messagebox.showinfo("Thông báo", "Vui lòng kết nối với robot !")
menu_frame.button_connect_to_slave.configure(command= connect_to_slave)
menu_frame.X_mmBox.delete(0, tk.END)
menu_frame.X_mmBox.insert(tk.END, menu_frame.X)
#menu_frame.button_connect_to_slave.configure(command= connect_to_slave)
menu_frame.noteBox.delete(0,tk.END)
menu_frame.noteBox.insert(tk.END, "Xin Chao")

# Chạy vòng lặp chính
root.mainloop()
