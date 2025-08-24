import tkinter as tk
from tkinter import ttk
from numeric_keypad import show_keyboard
from socketTCP import socket_client
import json
import os

# Biến global cho keyboard_frame
keyboard_frame = None
CONFIG_FILE = "config.json"

class table_point:
    def __init__(self, root):
        self.points = {}
        self.columns = ("ID", "X", "Y", "Z", "E")
        
        self.selected_id = None
        self.table_frame = tk.Frame(root)
        self.table = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", height=8)
        self.table_shown = False
        self.load_from_file()
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=80, anchor="center")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.scrollbar.configure(style="Vertical.TScrollbar")
        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Style
        style = ttk.Style()
        style.configure("Treeview", rowheight=50)
        style.configure("Vertical.TScrollbar", width=30, background="grey")

        # Touch scroll
        self.start_y = None
        self.table.bind("<ButtonPress-1>", self.on_touch_start)
        self.table.bind("<B1-Motion>", self.on_touch_move)

        # BIND sự kiện chọn hàng
        self.table.bind("<<TreeviewSelect>>", self.on_row_select)

        # Entry hiển thị dữ liệu hàng được chọn
        self.entry_frame = tk.Frame(root)
        self.entries = {}
        for idx, col in enumerate(self.columns):
            tk.Label(self.entry_frame, text=col).grid(row=0, column=idx)
            entry = tk.Entry(self.entry_frame, width=10)
            entry.grid(row=1, column=idx)
            self.entries[col] = entry

    def save_point(self, ID, x, y, z, e):
        self.points[ID] = (x, y, z, e)
        if self.table_shown:
            self.update_table()

    def update_table(self):
        self.table.delete(*self.table.get_children())
        for name, (x, y, z, e) in self.points.items():
            self.table.insert("", "end", values=(name, x, y, z, e))

    def show_table(self):
        if not self.table_shown:
            self.table_frame.place(x=5, y=5, width=480, height=420)
            self.entry_frame.place(x=5, y=430)
            self.update_table()
            self.table_shown = True

    def hide_table(self):
        if self.table_shown:
            self.table_frame.place_forget()
            self.entry_frame.place_forget()
            self.table_shown = False

    def on_touch_start(self, event):
        self.start_y = event.y

    def on_touch_move(self, event):
        if self.start_y is not None:
            dy = self.start_y - event.y
            self.start_y = event.y
            self.table.yview_scroll(int(dy / 2), "units")

    def on_row_select(self, event):
        selected = self.table.focus()
        if selected:
            values = self.table.item(selected, "values")
            self.selected_id = int(values[0])
            for i, col in enumerate(self.columns):
                self.entries[col].delete(0, tk.END)
                self.entries[col].insert(0, values[i])

    def delete_selected_row(self):
        selected_item = self.table.selection()
        if not selected_item:
            return

        for item in selected_item:
            values = self.table.item(item, "values")
            if not values:
                continue
            try:
                ID = int(values[0])
                if ID in self.points:
                    self.send_cmd_delete_point_to_slave(ID)
                    del self.points[ID]
            except ValueError:
                continue

        self.update_table()

    def send_cmd_aplly_point_to_slave(self, point_id):
        try:
            point_id = int(point_id)
        except ValueError:
            print("ID phải là số nguyên.")
            return

        if point_id not in self.points:
            print(f"ID {point_id} không tồn tại.")
            return

        try:
            x, y, z, e = map(float, self.points[point_id])
            message = f"S{point_id}x{x:.1f}y{y:.1f}z{z:.1f}w{e:.1f}"
        except Exception as exc:
            print("Lỗi khi định dạng tọa độ:", exc)
            return

        if socket_client.my_socket_obj.s:
            socket_client.my_socket_obj.send_data(message)
            print("Đã gửi:", message)
        else:
            print("Chưa kết nối Socket Server.")

    def send_cmd_delete_point_to_slave(self, point_id):
        try:
            point_id = int(point_id)
        except ValueError:
            print("ID phải là số nguyên.")
            return

        if point_id not in self.points:
            print(f"ID {point_id} không tồn tại.")
            return

        message = f"D{point_id}"
        if socket_client.my_socket_obj.s:
            socket_client.my_socket_obj.send_data(message)
            print("Đã gửi:", message)
        else:
            print("Chưa kết nối Socket Server.")

    def move_to_points(self, point_id):
        try:
            point_id = int(point_id)
        except ValueError:
            print("ID phải là số nguyên.")
            return

        if point_id not in self.points:
            print(f"ID {point_id} không tồn tại.")
            return

        message = f"m{point_id}"
        if socket_client.my_socket_obj.s:
            socket_client.my_socket_obj.send_data(message)
            print("Đã gửi:", message)
        else:
            print("Chưa kết nối Socket Server.")

    def send_all_points(self):
        for point_id in sorted(self.points.keys()):
            x, y, z, e = self.points[point_id]
            message = f"S{point_id}x{float(x):.1f}y{float(y):.1f}z{float(z):.1f}w{float(e):.1f}"
            if socket_client.my_socket_obj.s:
                socket_client.my_socket_obj.send_data(message)
                print("Đã gửi:", message)
            else:
                print("Chưa kết nối Socket Server.")

    def apply_and_save(self):
        try:
            save_data = {str(k): list(v) for k, v in self.points.items()}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(save_data, f, indent=4)
            print("Đã lưu vào config.json.")
        except Exception as e:
            print("Lỗi khi lưu:", e)

    def load_from_file(self):
        if not os.path.exists(CONFIG_FILE):
            print("File config.json không tồn tại.")
            return

        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)

            self.points = {
                int(k): tuple(v) for k, v in data.items()
                if isinstance(v, list) and len(v) == 4  # x, y, z, e
            }
            self.update_table()
            print("Đã tải dữ liệu từ config.json.")
        except Exception as e:
            print("Lỗi khi đọc file:", e)