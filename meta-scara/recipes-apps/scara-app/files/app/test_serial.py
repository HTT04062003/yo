import tkinter as tk
import serial
import re
#
ser = None
# Cấu hình cổng USB nối tiếp
USB_PORT = "/dev/ttyUSB0"  # Thay bằng cổng USB thực tế của bạn
BAUD_RATE = 115200

last_X = 0
last_Y = 0
last_Z = 0
last_Theta1 = 0
last_Theta2 = 0
last_Theta3 = 0
last_Theta4 = 0
last_V1 = 0
last_V2 = 0
last_V3 = 0
last_V4 = 0
last_E = 0
class mySerial:
    def __init__(self):
        self.ser = None
        self.USB_PORT = USB_PORT
        self.BAUD_RATE = BAUD_RATE
        #define command
        self.cmd_connect_to_slave = "Q"
        self.cmd_start = "Start"
        self.cmd_stop = "Stop"
        self.cmd_pause = "Pause"
        self.cmd_servo_on = "S1"
        self.cmd_servo_off = "S2"
        self.cmd_auto_home = "J0"
        self.cmd_no_op = "N0"
        self.cmd_jogging_theta1_up = "J1U"
        self.cmd_jogging_theta1_down = "J1D"
        self.cmd_jogging_theta2_up = "J2U"
        self.cmd_jogging_theta2_down = "J2D"
        self.cmd_jogging_theta3_up = "J3U"
        self.cmd_jogging_theta3_down = "J3D"
        self.cmd_jogging_theta4_up = "J4U"
        self.cmd_jogging_theta4_down = "J4D"
        self.cmd_jogging_x_up = "JXU"
        self.cmd_jogging_x_down = "JXD"
        self.cmd_jogging_y_up = "JYU"
        self.cmd_jogging_y_down = "JYD"
        self.cmd_jogging_z_up = "JZU"
        self.cmd_jogging_z_down = "JZD"
        
        #Response from slave
        self.response_ready_to_receive_gcode = "G_CODE_NONE"
        self.response_busy = "BUSY"
        self.response_ready = "READY"
        self.response_homing_complete = "HOMECPLT"
        self.response_from_slave = None
        #define Connect State
        self.state_connected = True
        self.state_disconnected = False
        self.state = self.state_disconnected
        
        
    # Hàm gửi chuỗi xuống vi điều khiển
    def send_data(self,  data):
        if data:
            try:
                self.ser.reset_output_buffer()
                self.ser.write(f"{data}\n".encode('utf-8'))
                print(f"Gửi: {data}")
            except serial.SerialException as e:
                print(f"Lỗi gửi dữ liệu: {e}")

    def process_data(self, data):
        # Khởi tạo các giá trị mặc định
        global last_X, last_Y, last_Z, last_Theta1, last_Theta2, last_Theta3, last_Theta4, last_V1, last_V2, last_V3, last_V4, last_E
        X = last_X
        Y = last_Y
        Z = last_Z
        Theta1 = last_Theta1
        Theta2 = last_Theta2
        Theta3 = last_Theta3
        Theta4 = last_Theta4
        V1 = last_V1
        V2 = last_V2
        V3 = last_V3
        V4 = last_V4
        E = last_E
        # Xử lý các phản hồi sẵn sàng nhận G-code hoặc bận
        if data == self.response_ready_to_receive_gcode:
            self.response_from_slave = self.response_ready_to_receive_gcode
            print(f"Response From Slave: {self.response_ready_to_receive_gcode}")
        if data == self.response_busy:
            self.response_from_slave = self.response_busy
            print(f"Response From Slave: {self.response_busy}")
        if data == self.response_ready:
            self.response_from_slave = self.response_ready
        if data == self.response_homing_complete:
            self.response_from_slave = self.response_homing_complete
        # Tách chuỗi và xử lý các thành phần X, Y, Z
        if 'X' in data:
            X = self.extract_value(data, 'X')
        if 'Y' in data:
            Y = self.extract_value(data, 'Y')
        if 'Z' in data:
            Z = self.extract_value(data, 'Z')
        if 'H' in data:
            Theta1 = self.extract_value(data, 'H')
        if 'B' in data:
            Theta2 = self.extract_value(data, 'B')
        if 'N' in data:
            Theta3 = self.extract_value(data, 'N')
        if 'M' in data:
            Theta4 = self.extract_value(data, 'M')
        if 'J' in data:
            V1 = self.extract_value(data, 'J')
        if 'K' in data:
            V2 = self.extract_value(data, 'K')
        if 'L' in data:
            V3 = self.extract_value(data, 'L')
        if 'P' in data:
            V4 = self.extract_value(data, 'P')
        if 'E' in data:
            E = self.extract_value(data, 'E')
        #print(f"Received data: X={X}, Y={Y}, Z={Z}, Theta1={Theta1}, Theta2={Theta2}")
            
        last_X = X
        last_Y = Y
        last_Z = Z
        last_Theta1 = Theta1
        last_Theta2 = Theta2
        last_Theta3 = Theta3
        last_Theta4 = Theta4
        last_V1 = V1
        last_V2 = V2
        last_V3 = V3
        last_V4 = V4
        last_E = E
        return X, Y, Z, Theta1, Theta2, Theta3, Theta4, V1, V2, V3, V4, E

    def extract_value(self, data, param):
        """
        Hàm này dùng để tách giá trị sau ký tự param (X, Y, Z, H, B) từ chuỗi dữ liệu.
        """
        try:
            start = data.find(param) + 1  # Tìm vị trí của ký tự (X, Y, Z, H, B)
            end = start
            while end < len(data) and (data[end].isdigit() or data[end] == '.' or data[end] == '-' or data[end] == '+'):
                end += 1  # Tìm hết số thực sau ký tự (X, Y, Z, H, B)
            
            value = data[start:end]
            return float(value) if value else None
        except ValueError:
            return None



# Khởi tạo đối tượng mySerial
serial_obj = mySerial()  # Khởi tạo đối tượng mySerial để truy cập các phương thức của nó