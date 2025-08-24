from tkinter import filedialog
from test_serial import serial_obj
class gcodeRead:
    def __init__(self):
        self.current_command_index = 0  # Lưu trữ chỉ số lệnh hiện tại
        # Biến toàn cục để lưu trữ danh sách các lệnh G-code
        self.gcode_commands = []
    def readGcodeFile(self):
        file_path = filedialog.askopenfilename(filetypes=[("G-code files", "*.gcode"), ("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.gcode_commands = file.readlines()  # Đọc tất cả các lệnh G-code từ file
            print("File G-code đã được mở thành công.")
    def sendGcodeComand(self):
        if self.gcode_commands:
            command = self.gcode_commands[self.current_command_index].strip()
            print(f"Đang gửi lệnh: {command}")
            serial_obj.send_data(command)
    def sendNextGcodeComand(self):
        self.current_command_index+=1
        if self.current_command_index < len(self.gcode_commands):
                command = self.gcode_commands[self.current_command_index].strip()
                serial_obj.send_data(command)
        else:
            print("Tất cả các lệnh đã được gửi.")

gCodeRead_Obj = gcodeRead()
