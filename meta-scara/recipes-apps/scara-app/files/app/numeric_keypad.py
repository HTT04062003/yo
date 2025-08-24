import tkinter as tk

# Hàm thêm số hoặc dấu chấm vào entry
def add_digit(digit, entry, tmpEntry):
    current_value = entry.get()  # Lấy giá trị hiện tại trong entry

    if digit == '.' and '.' in current_value:
        return  # Không cho phép nhập dấu chấm khi đã có dấu chấm
    entry.delete(0, tk.END)  # Xóa giá trị cũ trong entry
    entry.insert(tk.END, current_value + digit)  # Thêm số hoặc dấu chấm vào cuối giá trị hiện tại
    tmpEntry.delete(0, tk.END)
    tmpEntry.insert(tk.END, current_value + digit)

# Hàm xử lý nút backspace
def backspace(entry, tmpEntry):
    current_value = entry.get()  # Lấy giá trị hiện tại trong entry
    if current_value:  # Kiểm tra nếu có giá trị
        entry.delete(len(current_value)-1, tk.END)  # Xóa ký tự cuối
        tmpEntry.delete(len(current_value)-1, tk.END)

# Hàm xử lý khi nhấn Enter
def enter_key(entry, keyboard_frame, valueBox_frame):
    print("Nút Enter được nhấn. Giá trị hiện tại trong Entry:", entry.get())
    keyboard_frame.place_forget()  # Ẩn bàn phím khi nhấn Enter
    valueBox_frame.place_forget()

# Hàm hiển thị bàn phím
def show_keyboard(root, entry):
    print("OK")
    # Tạo một frame cho bàn phím
    keyboard_frame = tk.Frame(root, bg="gray", width=300, height=200)
    keyboard_frame.place(x=10, y=300)  # Hiển thị bàn phím dưới cùng của cửa sổ chính
    valueBox_frame = tk.Frame(root, bg = "white",width=800, height=30)
    valueBox_frame.place(x = 10, y = 270)
    tmpEntry = tk.Entry(valueBox_frame, width=800, font = ("Airal", 14))
    tmpEntry.place(x = 0, y = 0)
    current_value = entry.get()  # Lấy giá trị hiện tại trong entry
    tmpEntry.delete(0, tk.END)
    tmpEntry.insert(tk.END, current_value)
    # Tạo các nút số từ 0 đến 9 và gán sự kiện cho chúng
    buttons = [
        ('1', 0, 0), ('2', 1, 0), ('3', 2, 0),('Q',3,0),('W', 4,0),('E', 5,0),('R', 6,0), ('T', 7,0), ('Y', 8,0), ('U', 9,0), ('I', 10, 0), ('O', 11,0), ('P', 12,0),
        ('4', 0, 1), ('5', 1, 1), ('6', 2, 1),('A', 3,1), ('S', 4,1), ('D', 5,1), ('F', 6,1), ('G', 7,1),('H', 8,1), ('J', 9,1), ('K', 10,1),('L', 11,1), (':', 12,1),
        ('7', 0, 2), ('8', 1, 2), ('9', 2, 2),('Z', 3,2), ('X', 4,2), ('C', 5,2), ('V', 6,2), ('B', 7,2), ('N', 8,2), ('M', 9,2), (';', 10,2), ('<', 11,2), ('>', 12,2),
        ('0', 1, 3),
        ('.', 2, 3),  # Nút dấu chấm
        ('←', 0, 3),  # Nút backspace
        ('OK', 0, 4),  # Nút OK
        ('Enter', 1, 4),  # Nút Enter
        (' ', 2,4)
    ]
    
    for (text, x, y) in buttons:
        if text == '←':  # Nút backspace
            button = tk.Button(keyboard_frame, text=text, font=("Arial", 14), width=3, height=1, command=lambda: backspace(entry))
        elif text == 'OK':  # Nút OK
            button = tk.Button(keyboard_frame, text=text, font=("Arial", 14), width=3, height=1, command=keyboard_frame.place_forget)
        elif text == 'Enter':  # Nút Enter
            button = tk.Button(keyboard_frame, text=text, font=("Arial", 14), width=3, height=1, command=lambda: enter_key(entry, keyboard_frame, valueBox_frame))
        elif text == ' ':
            button = tk.Button(keyboard_frame, text=text, font=("Arial", 14), width=3, height=1, command=lambda digit=text: add_digit(digit, entry, tmpEntry))
        else:  # Các nút số và dấu chấm
            button = tk.Button(keyboard_frame, text=text, font=("Arial", 14), width=3, height=1, command=lambda digit=text: add_digit(digit, entry, tmpEntry))
        button.grid(row=y, column=x, padx=2, pady=2)
    
    return keyboard_frame