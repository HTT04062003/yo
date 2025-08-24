import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import thư viện Pillow
from numeric_keypad import show_keyboard
from tkinter  import filedialog
import json
import os
from socketTCP import socket_client
from gcode_read import gCodeRead_Obj
from create_table_point import table_point
from tkinter import messagebox
#

# Biến global cho keyboard_frame
keyboard_frame = None
#
print_icon_image_path = "print_icon.png"
setting_icon_image_path = "setting_icon.png"
hotend_temp_icon_image_path = "hotend_temp_icon.png"
hedbed_temp_icon_image_path = "hedbed_temp_icon.png"
fanSpeed_icon_iamge_path = "fanSpeed_icon.png"
doC_icon_iamge_path = "doC.png"
time_icon_image_path = "tim_icon.png"
X_icon_iamge_path = "X_icon.png"
Y_icon_image_path = "Y_icon.png"
Z_icon_iamge_path = "Z_icon.png"
#
class MainMenu:
    def __init__(self, root):
        #define
        self.mainMenu = 1
        self.settingMenu = 2
        self.axisResolutionMenu = 3
        self.PIDParameterMenu = 4
        self.manControlMenu = 5
        self.create_table_menu = 6
        self.jogging_menu = 7
        
        #Tao mot bien chua gia tri menu hien tai
        self.currentMenu = self.mainMenu
        self.menu_pre = self.mainMenu
        # Tạo một frame chứa main Menu
        self.frame = tk.Frame(root, bg="#0F0A3F")
        
        self.frame.pack(fill=tk.BOTH, expand=True)  # Đặt `pack` để frame chiếm toàn bộ diện tích
        #******************************************Padding Frame***************************************************************************************#
        self.padding_frame = tk.Frame(self.frame, bg= "#0F0A3F", width=1000, height=600)
        self.padding_frame_2 = tk.Frame(self.padding_frame, bg= "#0F0A3F", width=1000, height=600)
        #/****************************************Extrude Menu Frame*********************************************************************************/#
        
        self.child_frame = tk.Frame(self.frame, bg= "#2e2e2e", width= 430, height=290)
        self.child_frame.place(x= 580, y = 10)
        self.keyBoard_frame = tk.Frame(self.frame,bg = "#2e2e2e", width=400, height=400)
        self.jogging_frame = tk.Frame(self.frame, bg= "#0F0A3F", width=1000, height=600)
        self.question_frame = tk.Frame(self.frame, bg = "white", width=400, height = 300)
        #Global Variable
        #Khoi tao doi tuong table_point
        self.create_table_obj = table_point(root)
        # Biến toàn cục để theo dõi thời gian
        self.seconds = 0
        self.running = False  # Biến trạng thái để kiểm tra đồng hồ đang chạy hay không
        self.Theta1 = 0.0
        self.Theta2 = 0.0
        self.Theta3 = 0.0
        self.Theta4 = 0.0
        self.Theta1_Speed = 0.0
        self.Theta2_Speed = 0.0
        self.Theta3_Speed = 0.0
        self.Theta4_Speed = 0.0
        self.E = 0.0
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.Kp_THotend = 0
        self.Ki_THotend = 0
        self.Kd_THotend = 0
        self.Kb_THotend = 0
        self.Kp_THedbed = 0
        self.Ki_Thedbed = 0
        self.Kd_THedbed = 0
        self.Kb_tHedbed = 0
        self.BLUX = 0
        self.BLUY = 0
        self.BLUZ = 0
        self.BLUE = 0
        self.setHotendTemp = 0
        self.setHedbedTemp = 0
        self.setFanSpeed = 0
        self.setX = 0
        self.setY = 0
        self.setZ = 0
        self.setE = 0
        self.setF = 0
        
        
        
        
        # Gọi hàm tạo các phần tử bên trong menu
        self.create_main_mernu_widgets()
        self.create_setting_menu_widget()

    def create_main_mernu_widgets(self):
        # Tạo các nút và Entry trong menu
        
        # Nút Settings
        # Nút bóng (shadow) lệch xuống dưới và sang phải
        self.shadow_setting_button = tk.Button(self.frame, text="⚙️ Setting", font=("Arial", 12), 
                                    bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_setting_button.place(x = 9, y = 9)  # Lệch vị trí để tạo hiệu ứng bóng
        self.setting_button = tk.Button(self.frame, text="⚙️ Setting", font=("Arial", 12), command=self.toggle_settings, bg="gray", fg="black", width=10, height=3,  highlightbackground="white", highlightthickness=1)
        self.setting_button.place(x=5, y = 5)
       
        #**************************************************Button connect****************************************************************************#
        self.shadow_connect_to_slave_button = tk.Button(self.frame, text="⚙️ Setting", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_connect_to_slave_button.place(x = 134, y = 9)
        self.button_connect_to_slave = tk.Button(self.frame, text= "Connect", font= ("Arial", 12),bg="gray", fg="black", width=10, height=3 ,
                                             highlightbackground="white", highlightthickness=1   )
        self.button_connect_to_slave.place(x = 130, y = 5)
        #**********************************Button Open Jogging Menu***********#
        self.shadow_open_jogging_menu_button = tk.Button(self.frame, text="⚙️ Setting", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_open_jogging_menu_button.place(x = 259, y = 9)
        self.open_jogging_menu_button = tk.Button(self.frame, text= "Jogging", font= ("Arial", 12),bg="gray", fg="black", width=10, height=3                          
                                             ,highlightbackground="white", highlightthickness=1     ,command= self.show_jogging_menu)
        self.open_jogging_menu_button.place(x = 255, y = 5)
        #*************************Button Open Menu Create Point Menu********#
        self.shadow_open_create_point_menu_button = tk.Button(self.frame,  text="Create Points", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_open_create_point_menu_button.place(x = 384, y = 9)
        self.open_create_point_menu_button = tk.Button(self.frame, text= "Create Points", font= ("Arial", 12),bg="gray", fg="black", width=10, height=3                          
                                             ,highlightbackground="white", highlightthickness=1     ,command= self.show_table_points_menu)
        self.open_create_point_menu_button.place(x = 380, y = 5)
        #******************************comboBox Servo Man Control*********#
        self.comboBox_MAN_Control_label = tk.Label(self.frame,width=8, heigh = 12, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_MAN_Control_label.place(x = 485, y = 85)
        self.comboBox_MAN_Control_label = tk.Label(self.frame, text = "State", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.comboBox_MAN_Control_label.place(x = 500, y = 90)
        self.state_servo_1_label = tk.Label(self.frame, bd = 1,width = 2, height=1, bg = "green",heigh = 1, relief="flat", highlightthickness=1)
        self.state_servo_1_label.place(x = 510, y = 125)

        self.state_servo_2_label = tk.Label(self.frame, bd = 1,width = 2, height=1, bg = "green",heigh = 1, relief="flat", highlightthickness=1)
        self.state_servo_2_label.place(x = 510, y = 165)
        self.state_servo_3_label = tk.Label(self.frame, bd = 1,width = 2, height=1, bg = "green",heigh = 1, relief="flat", highlightthickness=1)
        self.state_servo_3_label.place(x = 510, y = 205)

        self.state_servo_4_label = tk.Label(self.frame, bd = 1,width = 2, height=1, bg = "green",heigh = 1, relief="flat", highlightthickness=1)
        self.state_servo_4_label.place(x = 510, y = 245)
        #*****************************Servo ON Button********#
        self.RUN_button = tk.Button(self.frame, text= " VALVE ON", font= ("Arial", 12),bg="green", fg="white", width=10, height=3 ,  relief="flat", highlightthickness=1, bd = 1                       
                                                  ,command= self.on_press_button_start)
        self.RUN_button.place(x = 580, y = 300)
        self.STOP_button = tk.Button(self.frame, text= " VALVE_OFF ", font= ("Arial", 12),bg="red", fg="white", width=10, height=3 ,  relief="flat", highlightthickness=1, bd = 1                       
                                                  ,command= self.on_press_button_stop)
        self.STOP_button.place(x = 710, y = 300)
        self.PAUSE_button = tk.Button(self.frame, text= " PAUSE ", font= ("Arial", 12),bg="yellow", fg="black", width=10, height=3 ,  relief="flat", highlightthickness=1, bd = 1                       
                                                  ,command= self.on_press_button_pause)
        self.PAUSE_button.place(x = 840, y = 300)

        self.canvas_ON_SERVO = tk.Canvas(self.frame, width=130, heigh = 60, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_ON_SERVO.place(x = 640, y = 385)
        self.button_ON_SERVO = self.canvas_ON_SERVO.create_oval(0, 0, 130, 60,fill= "green", outline = "white", width=2)
        self.button_ON_SERVO_text = self.canvas_ON_SERVO.create_text(65, 30, text = "SERVO ON", font = ("Arial", 12), fill = "white")
        self.canvas_ON_SERVO.tag_bind(self.button_ON_SERVO , "<ButtonPress-1>", self.on_press_button_servo_on)
        self.canvas_ON_SERVO.tag_bind(self.button_ON_SERVO_text, "<ButtonPress-1>", self.on_press_button_servo_on)
        
        self.canvas_OFF_SERVO = tk.Canvas(self.frame, width=130, heigh = 60, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_OFF_SERVO.place(x = 780, y = 385)
        self.button_OFF_SERVO = self.canvas_OFF_SERVO.create_oval(0, 0, 130, 60,fill= "red", outline = "white", width=2)
        self.button_OFF_SERVO_text = self.canvas_OFF_SERVO.create_text(65, 30, text = "SERVO OFF", font = ("Arial", 12), fill = "white")
        self.canvas_OFF_SERVO.tag_bind(self.button_OFF_SERVO , "<ButtonPress-1>", self.on_press_button_servo_off)
        self.canvas_OFF_SERVO.tag_bind(self.button_OFF_SERVO_text, "<ButtonPress-1>", self.on_press_button_servo_off)
        
        self.auto_homing_button = tk.Button(self.frame, text= "AUTO HOME", font= ("Arial", 12),bg="yellow", fg="black", width=15, height=3 ,  relief="flat", highlightthickness=1, bd = 1                       
                                                  ,command= self.on_press_button_auto_home)
        self.auto_homing_button.place(x = 580, y = 460)

        self.reset_button = tk.Button(self.frame, text= "RESET", font= ("Arial", 12),bg="red", fg="black", width=15, height=3 ,  relief="flat", highlightthickness=1, bd = 1                       
                                                  ,command= self.show_table_points_menu)
        self.reset_button.place(x = 760, y = 460)
        #******************************comboBox Revolute Label********************#
        self.comboBox_Revolute_Label = tk.Label(self.frame,width=25, heigh = 12, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Revolute_Label.place(x = 5, y = 85)
        self.Revolute_Name_Box = tk.Label(self.frame, text = "Revolute", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Revolute_Name_Box.place(x = 80, y = 90)
        #********************************************************Tao icon hien thi bieu tuong hotend*************************************************#
    

        self.theta1_label = tk.Label(self.frame, text = "Theta1", font=("Arial", 14 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta1_label.place(x= 10, y = 125)
        # Tạo Entry để hiển thị số nhập
        self.theta1_value_box = tk.Entry(self.frame, font=("Arial", 14 ), width=12,  background="#2e2e2e", fg="white")
        self.theta1_value_box.place(x=70, y=125)
        # Gán giá trị cho luxBox
        self.theta1_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta1_value_box.insert(tk.END, f"{self.Theta1}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.rad_icon_label1 = tk.Label(self.frame, text = "rad",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.rad_icon_label1.place(x= 200, y = 125)
        #***************************************************************Tao icon cho Hedbed*****************************************************8*****#
        self.theta2_icon_label = tk.Label(self.frame,text = "Theta2", font=("Arial", 14 ), bd=0, relief="flat", highlightthickness=0)
        self.theta2_icon_label.place(x= 10, y = 165)
        # Tạo Entry để hiển thị số nhập
        self.theta2_value_box = tk.Entry(self.frame, font=("Arial", 14, ), width=12, background="#2e2e2e", fg="white")
        self.theta2_value_box.place(x=70, y=165)
        # Gán giá trị cho luxBox
        self.theta2_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta2_value_box.insert(tk.END, f"{self.Theta2}")  # Thêm giá trị mới vào cuối
        self.rad_icon_label2 = tk.Label(self.frame, text = "rad",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.rad_icon_label2.place(x= 200, y = 165)
        #*********************************Tao Box Theta3******************#
        self.theta3_icon_label = tk.Label(self.frame,text = "Theta3", font=("Arial", 14 ), bd=0, relief="flat", highlightthickness=0)
        self.theta3_icon_label.place(x= 10, y = 205)
        # Tạo Entry để hiển thị số nhập
        self.theta3_value_box = tk.Entry(self.frame, font=("Arial", 14, ), width=12, background="#2e2e2e", fg="white")
        self.theta3_value_box.place(x=70, y=205)
        # Gán giá trị cho luxBox
        self.theta3_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta3_value_box.insert(tk.END, f"{self.Theta3}")  # Thêm giá trị mới vào cuối

        #***************************************************Tao icon do C cho Hebded Temperature*****************************************************#
        self.rad_icon_label3 = tk.Label(self.frame, text = "rad",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.rad_icon_label3.place(x= 200, y = 205)
        #*********************************Theta4 Box***********************#
        self.theta4_icon_label = tk.Label(self.frame,text = "Theta4", font=("Arial", 14 ), bd=0, relief="flat", highlightthickness=0)
        self.theta4_icon_label.place(x= 10, y = 245)
        # Tạo Entry để hiển thị số nhập
        self.theta4_value_box = tk.Entry(self.frame, font=("Arial", 14, ), width=12, background="#2e2e2e", fg="white")
        self.theta4_value_box.place(x=70, y=245)
        # Gán giá trị cho luxBox
        self.theta4_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta4_value_box.insert(tk.END, f"{self.Theta4}")  # Thêm giá trị mới vào cuối

        #***************************************************Tao icon do C cho Hebded Temperature*****************************************************#
        self.mm_icon_label4 = tk.Label(self.frame, text = "mm",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.mm_icon_label4.place(x= 200, y = 245)
        #******************************comboBox Speed Label********************#
        self.comboBox_Speed_Label = tk.Label(self.frame,width=26, heigh = 12, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Speed_Label.place(x = 240, y = 85)
        self.Speed_Name_Box = tk.Label(self.frame, text = "Speed", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Speed_Name_Box.place(x = 320, y = 90)
        #********************************Theta1_Speed_Lebal*****************************#
        self.theta1_speed_label = tk.Label(self.frame, text = "Theta1", font=("Arial", 14 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta1_speed_label.place(x= 245, y = 125)
        # Tạo Entry để hiển thị số nhập
        self.theta1_speed_value_box = tk.Entry(self.frame, font=("Arial", 14 ), width=12,  background="#2e2e2e", fg="white")
        self.theta1_speed_value_box.place(x=305, y=125)
        # Gán giá trị cho luxBox
        self.theta1_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta1_speed_value_box.insert(tk.END, f"{self.Theta1_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.radPerSec_icon_label1 = tk.Label(self.frame, text = "rad/s",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.radPerSec_icon_label1.place(x= 435, y = 125)

        #********************************Theta2_Speed_Lebal*****************************#
        self.theta2_speed_label = tk.Label(self.frame, text = "Theta2", font=("Arial", 14 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta2_speed_label.place(x= 245, y = 165)
        # Tạo Entry để hiển thị số nhập
        self.theta2_speed_value_box = tk.Entry(self.frame, font=("Arial", 14 ), width=12,  background="#2e2e2e", fg="white")
        self.theta2_speed_value_box.place(x=305, y=165)
        # Gán giá trị cho luxBox
        self.theta2_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta2_speed_value_box.insert(tk.END, f"{self.Theta2_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.radPerSec_icon_label2 = tk.Label(self.frame, text = "rad/s",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.radPerSec_icon_label2.place(x= 435, y = 165)
    
        #********************************Theta3_Speed_Labal*****************************#
        self.theta3_speed_label = tk.Label(self.frame, text = "Theta3", font=("Arial", 14 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta3_speed_label.place(x= 245, y = 205)
        # Tạo Entry để hiển thị số nhập
        self.theta3_speed_value_box = tk.Entry(self.frame, font=("Arial", 14 ), width=12,  background="#2e2e2e", fg="white")
        self.theta3_speed_value_box.place(x=305, y=205)
        # Gán giá trị cho luxBox
        self.theta3_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta3_speed_value_box.insert(tk.END, f"{self.Theta3_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.radPerSec_icon_label3 = tk.Label(self.frame, text = "rad/s",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.radPerSec_icon_label3.place(x= 435, y = 205)
        #********************************Theta4_Speed_Labal*****************************#
        self.theta4_speed_label = tk.Label(self.frame, text = "Theta4", font=("Arial", 14 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta4_speed_label.place(x= 245, y = 245)
        # Tạo Entry để hiển thị số nhập
        self.theta4_speed_value_box = tk.Entry(self.frame, font=("Arial", 14 ), width=12,  background="#2e2e2e", fg="white")
        self.theta4_speed_value_box.place(x=305, y=245)
        # Gán giá trị cho luxBox
        self.theta4_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta4_speed_value_box.insert(tk.END, f"{self.Theta4_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.mmPerSec_icon_label3 = tk.Label(self.frame, text = "mm/s",font=("Arial", 14 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.mmPerSec_icon_label3.place(x= 435, y = 245)
        #***********************************Position comboBox*********************#
        self.comboBox_Position_Label = tk.Label(self.frame,width=25, heigh = 12, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Position_Label.place(x = 5, y = 300)
        self.Position_Name_Box = tk.Label(self.frame, text = "Position", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Position_Name_Box.place(x = 80, y = 305)
        #********************************************************************Tao Icon hien thi hop thoai X***************************************************#
        image = Image.open(X_icon_iamge_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((40, 40))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.X_icon = ImageTk.PhotoImage(image)

        self.X_icon_label = tk.Label(self.frame, image=self.X_icon, bd=0, relief="flat", highlightthickness=0)
        self.X_icon_label.place(x= 10, y = 335)
        self.mm_label1 = tk.Label(self.frame, text= "mm",font=("Arial", 14, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label1.place(x=140, y=345)
        self.X_mmBox = tk.Entry(self.frame, font=("Arial", 14, ), width=12, background="#2e2e2e", fg="white")
        self.X_mmBox.place(x=55, y=345)
        # Gán giá trị cho luxBox
        self.X_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.X_mmBox.insert(tk.END, f"{self.X}")  # Thêm giá trị mới vào cuối
        #*****************************************************Tao Icon hein thi hop thoai Y******************************************************************#
        image = Image.open(Y_icon_image_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((40, 40))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.Y_icon = ImageTk.PhotoImage(image)

        self.Y_icon_label = tk.Label(self.frame, image=self.Y_icon, bd=0, relief="flat", highlightthickness=0)
        self.Y_icon_label.place(x= 10, y = 375)
        self.mm_label2 = tk.Label(self.frame, text= "mm",font=("Arial", 14, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label2.place(x=140, y=385)
        self.Y_mmBox = tk.Entry(self.frame, font=("Arial", 14, ), width=12, background="#2e2e2e", fg="white")
        self.Y_mmBox.place(x=55, y=385)
        # Gán giá trị cho luxBox
        self.Y_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.Y_mmBox.insert(tk.END, f"{self.Y}")  # Thêm giá trị mới vào cuối
        #***************************************************Tao icon hien thi hop thoai Z********************************************************************#
        image = Image.open(Z_icon_iamge_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((40, 40))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.Z_icon = ImageTk.PhotoImage(image)

        self.Z_icon_label = tk.Label(self.frame, image=self.Z_icon, bd=0, relief="flat", highlightthickness=0)
        self.Z_icon_label.place(x= 10, y = 415)
        self.mm_label3 = tk.Label(self.frame, text= "mm",font=("Arial", 14, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label3.place(x=140, y=425)
        self.Z_mmBox = tk.Entry(self.frame, font=("Arial", 14, ), width=12, background="#2e2e2e", fg="white")
        self.Z_mmBox.place(x=55, y=425)
        #********************8***************************                                 *******************************************************************#
        # Gán giá trị cho luxBox
        self.Z_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.Z_mmBox.insert(tk.END, f"{self.Z}")  # Thêm giá trị mới vào cuối

        #*****************************************Text box *****************************************************#
        self.noteBox = tk.Entry(self.child_frame, width= 200, bg= "white")
        self.noteBox.place(x = 5, y = 5)
    
    def create_menu_pause_widgets(self):
        self.infoBox = tk.Label(self.padding_frame, text="Paused !!!", font=("Arial", 12), bd=0, relief="flat", highlightthickness=0,
                                bg= "white", fg="black")
        self.infoBox.place(x = 50, y = 50)
        self.continue_button = tk.Button(self.padding_frame, text="Continue", font=("Airal", 12), fg= "black", bg= "green",
                                         command= self.continue_button_callback)
        self.continue_button.place(x = 50, y=80)
   

    def create_setting_menu_widget(self):
        # Các nút trong setting_frame
        self.menu_motor_button = tk.Button(self.padding_frame, text="Axis Resolution", font=("Arial", 12), command=self.show_axis_resolution_menu, bg="black", fg="white", width=10, height=1)
        self.menu_motor_button.place(x=5, y=0)

        self.menu_hotend_button = tk.Button(self.padding_frame, text="PID_Setting", font=("Arial", 12), command=self.show_PID_Paremeter_menu, bg="black", fg="white", width=10, height=1)
        self.menu_hotend_button.place(x=5, y=30)

        self.close_setting_button = tk.Button(self.padding_frame, text="Close", font=("Arial", 12), command=self.off_setting_menu, bg="red", fg="white", width=10, height=1)
        self.close_setting_button.place(x=5, y=120)

        self.menu_manControl_button = tk.Button(self.padding_frame, text="MAN Control", font=("Arial", 12), command=self.show_manControl_menu, bg="black", fg="white", width=10, height=1)
        self.menu_manControl_button.place(x=5, y=60)

        self.extrude_option_button = tk.Button(self.padding_frame,text= "Extrude", font= ("Arial", 12), fg= "white", 
                                                                                             command=self.extrude_option_button_callback, bg = "black", bd = 0, width=10, height=1 )
        self.extrude_option_button.place(x = 5, y = 90)
    
    #********************Menu Jogging
    def create_jogging_menu_widget(self):
        
        self.joggingMenu_comboBox1_Label = tk.Label(self.jogging_frame,width=36, heigh = 14, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.joggingMenu_comboBox1_Label.place(x = 5, y = 5)
        self.joggingMenu_comboBox1_Name = tk.Label(self.jogging_frame, text = "Revolute", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.joggingMenu_comboBox1_Name.place(x = 120, y = 10)
        self.theta1_label = tk.Label(self.jogging_frame, text = "Theta1", font=("Arial", 20 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta1_label.place(x= 10, y = 45)
        # Tạo Entry để hiển thị số nhập
        self.theta1_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20 ), width=12,  background="#2e2e2e", fg="white",)
        self.theta1_value_box.place(x=100, y=45)
        self.theta1_value_box.bind("<FocusIn>", lambda event: show_keyboard(self.frame, self.theta1_value_box))
        # Gán giá trị cho luxBox
        self.theta1_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta1_value_box.insert(tk.END, f"{self.Theta1}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.rad_icon_label1 = tk.Label(self.jogging_frame, text = "rad",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.rad_icon_label1.place(x= 290, y = 45)
        #***************************************************************Tao icon cho Hedbed*****************************************************8*****#
        self.theta2_icon_label = tk.Label(self.jogging_frame,text = "Theta2", font=("Arial", 20 ), bd=0, relief="flat", highlightthickness=0)
        self.theta2_icon_label.place(x= 10, y = 95)
        # Tạo Entry để hiển thị số nhập
        self.theta2_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.theta2_value_box.place(x=100, y=95)
        # Gán giá trị cho luxBox
        self.theta2_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta2_value_box.insert(tk.END, f"{self.Theta2}")  # Thêm giá trị mới vào cuối
        self.rad_icon_label2 = tk.Label(self.jogging_frame, text = "rad",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.rad_icon_label2.place(x= 290, y = 95)
        #*********************************Tao Box Theta3******************#
        self.theta3_icon_label = tk.Label(self.jogging_frame,text = "Theta3", font=("Arial", 20 ), bd=0, relief="flat", highlightthickness=0)
        self.theta3_icon_label.place(x= 10, y = 145)
        # Tạo Entry để hiển thị số nhập
        self.theta3_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.theta3_value_box.place(x=100, y=145)
        # Gán giá trị cho luxBox
        self.theta3_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta3_value_box.insert(tk.END, f"{self.Theta3}")  # Thêm giá trị mới vào cuối

        #***************************************************Tao icon do C cho Hebded Temperature*****************************************************#
        self.rad_icon_label3 = tk.Label(self.jogging_frame, text = "rad",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.rad_icon_label3.place(x= 290, y = 145)
        #*********************************Theta4Box***********************#
        self.theta4_icon_label = tk.Label(self.jogging_frame,text = "Theta4", font=("Arial", 20 ), bd=0, relief="flat", highlightthickness=0)
        self.theta4_icon_label.place(x= 10, y = 195)
        # Tạo Entry để hiển thị số nhập
        self.theta4_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.theta4_value_box.place(x=100, y=195)
        # Gán giá trị cho luxBox
        self.theta4_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta4_value_box.insert(tk.END, f"{self.Theta4}")  # Thêm giá trị mới vào cuối

        #***************************************************Tao icon do C cho Hebded Temperature*****************************************************#
        self.mm_icon_label4 = tk.Label(self.jogging_frame, text = "mm",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.mm_icon_label4.place(x= 290, y = 195)
        #******************************comboBox Speed Label********************#
        self.comboBox_Speed_Label = tk.Label(self.jogging_frame,width=40, heigh = 14, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Speed_Label.place(x = 350, y = 10)
        self.Speed_Name_Box = tk.Label(self.jogging_frame, text = "Speed", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Speed_Name_Box.place(x = 450, y = 15)
        #********************************Theta1_Speed_Lebal*****************************#
        self.theta1_speed_label = tk.Label(self.jogging_frame, text = "Theta1", font=("Arial", 20 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta1_speed_label.place(x= 355, y = 45)
        # Tạo Entry để hiển thị số nhập
        self.theta1_speed_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20 ), width=12,  background="#2e2e2e", fg="white")
        self.theta1_speed_value_box.place(x=445, y=45)
        # Gán giá trị cho luxBox
        self.theta1_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta1_speed_value_box.insert(tk.END, f"{self.Theta1_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.radPerSec_icon_label1 = tk.Label(self.jogging_frame, text = "rad/s",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.radPerSec_icon_label1.place(x= 640, y = 45)

        #********************************Theta2_Speed_Lebal*****************************#
        self.theta2_speed_label = tk.Label(self.jogging_frame, text = "Theta2", font=("Arial", 20 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta2_speed_label.place(x= 355, y = 95)
        # Tạo Entry để hiển thị số nhập
        self.theta2_speed_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20 ), width=12,  background="#2e2e2e", fg="white")
        self.theta2_speed_value_box.place(x=445, y=95)
        # Gán giá trị cho luxBox
        self.theta2_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta2_speed_value_box.insert(tk.END, f"{self.Theta2_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.radPerSec_icon_label2 = tk.Label(self.jogging_frame, text = "rad/s",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.radPerSec_icon_label2.place(x= 640, y = 95)
    
        #********************************Theta3_Speed_Labal*****************************#
        self.theta3_speed_label = tk.Label(self.jogging_frame, text = "Theta3", font=("Arial", 20 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta3_speed_label.place(x= 355, y = 145)
        # Tạo Entry để hiển thị số nhập
        self.theta3_speed_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20 ), width=12,  background="#2e2e2e", fg="white")
        self.theta3_speed_value_box.place(x=445, y=145)
        # Gán giá trị cho luxBox
        self.theta3_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta3_speed_value_box.insert(tk.END, f"{self.Theta3_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.radPerSec_icon_label3 = tk.Label(self.jogging_frame, text = "rad/s",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.radPerSec_icon_label3.place(x= 640, y = 145)
        #********************************Theta4_Speed_Labal*****************************#
        self.theta4_speed_label = tk.Label(self.jogging_frame, text = "Theta4", font=("Arial", 20 ),heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.theta4_speed_label.place(x= 355, y = 195)
        # Tạo Entry để hiển thị số nhập
        self.theta4_speed_value_box = tk.Entry(self.jogging_frame, font=("Arial", 20 ), width=12,  background="#2e2e2e", fg="white")
        self.theta4_speed_value_box.place(x=445, y=195)
        # Gán giá trị cho luxBox
        self.theta4_speed_value_box.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.theta4_speed_value_box.insert(tk.END, f"{self.Theta4_Speed}")  # Thêm giá trị mới vào cuối
        #***************************************************************8**Tao icon do C**************************************************************#
        self.mmPerSec_icon_label3 = tk.Label(self.jogging_frame, text = "mm/s",font=("Arial", 20 ), fg = "white" , bg = "#0F0A3F",bd=0, relief="flat", highlightthickness=0)
        self.mmPerSec_icon_label3.place(x= 640, y = 195)
        #***********************************Position comboBox*********************#
        self.comboBox_Position_Label = tk.Label(self.jogging_frame,width=40, heigh = 12, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Position_Label.place(x = 350, y = 265)
        self.Position_Name_Box = tk.Label(self.jogging_frame, text = "Position", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Position_Name_Box.place(x = 450, y = 270)
        #********************************************************************Tao Icon hien thi hop thoai X***************************************************#
        image = Image.open(X_icon_iamge_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((50, 50))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.X_icon = ImageTk.PhotoImage(image)

        self.X_icon_label = tk.Label(self.jogging_frame, image=self.X_icon, bd=0, relief="flat", highlightthickness=0)
        self.X_icon_label.place(x= 355, y = 295)
        self.mm_label1 = tk.Label(self.jogging_frame, text= "mm",font=("Arial", 20, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label1.place(x=535, y=305)
        self.X_mmBox = tk.Entry(self.jogging_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.X_mmBox.place(x=410, y=305)
        # Gán giá trị cho luxBox
        self.X_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.X_mmBox.insert(tk.END, f"{self.X}")  # Thêm giá trị mới vào cuối
        #*****************************************************Tao Icon hein thi hop thoai Y******************************************************************#
        image = Image.open(Y_icon_image_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((50, 50))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.Y_icon = ImageTk.PhotoImage(image)

        self.Y_icon_label = tk.Label(self.jogging_frame, image=self.Y_icon, bd=0, relief="flat", highlightthickness=0)
        self.Y_icon_label.place(x= 355, y = 350)
        self.mm_label2 = tk.Label(self.jogging_frame, text= "mm",font=("Arial", 20, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label2.place(x=535, y=360)
        self.Y_mmBox = tk.Entry(self.jogging_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.Y_mmBox.place(x=410, y=360)
        # Gán giá trị cho luxBox
        self.Y_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.Y_mmBox.insert(tk.END, f"{self.Y}")  # Thêm giá trị mới vào cuối
        #***************************************************Tao icon hien thi hop thoai Z********************************************************************#
        image = Image.open(Z_icon_iamge_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((50, 50))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.Z_icon = ImageTk.PhotoImage(image)

        self.Z_icon_label = tk.Label(self.jogging_frame, image=self.Z_icon, bd=0, relief="flat", highlightthickness=0)
        self.Z_icon_label.place(x= 355, y = 410)
        self.mm_label3 = tk.Label(self.jogging_frame, text= "mm",font=("Arial", 20, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label3.place(x=535, y=420)
        self.Z_mmBox = tk.Entry(self.jogging_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.Z_mmBox.place(x=410, y=420)
        #********************8***************************                                 *******************************************************************#
        # Gán giá trị cho luxBox
        self.Z_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.Z_mmBox.insert(tk.END, f"{self.Z}")  # Thêm giá trị mới vào cuối
        #**********************Tao comboBox Jogging*******#
        self.comboBox_Jogging_Label = tk.Label(self.jogging_frame,width=22, heigh = 27, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Jogging_Label.place(x = 720, y = 10)
        self.Jogging_Name_Box = tk.Label(self.jogging_frame, text = "Jogging", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Jogging_Name_Box.place(x = 780, y = 15)


        #*************Tao Nut Up Theta1*************#
        self.canvas_up_theta1 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_theta1.place(x = 730, y = 45)
        self.button_up_theta1 = self.canvas_up_theta1.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_theta1_text = self.canvas_up_theta1.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_theta1.tag_bind(self.button_up_theta1, "<ButtonPress-1>", self.on_press_button_up_theta1)
        self.canvas_up_theta1.tag_bind(self.button_up_theta1_text, "<ButtonPress-1>", self.on_press_button_up_theta1)
        self.canvas_up_theta1.tag_bind(self.button_up_theta1, "<ButtonRelease-1>", self.on_release_button_up_theta1)
        self.canvas_up_theta1.tag_bind(self.button_up_theta1_text, "<ButtonRelease-1>", self.on_release_button_up_theta1)
        #*************Tao Nut Down Theta1*************#
        self.canvas_down_theta1 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_theta1.place(x = 830, y = 45)
        self.button_down_theta1 = self.canvas_down_theta1.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_theta1_text = self.canvas_down_theta1.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_theta1.tag_bind(self.button_down_theta1, "<ButtonPress-1>", self.on_press_button_down_theta1)
        self.canvas_down_theta1.tag_bind(self.button_down_theta1_text, "<ButtonPress-1>", self.on_press_button_down_theta1)
        self.canvas_down_theta1.tag_bind(self.button_down_theta1, "<ButtonRelease-1>", self.on_release_button_down_theta1)
        self.canvas_down_theta1.tag_bind(self.button_down_theta1_text, "<ButtonRelease-1>", self.on_release_button_down_theta1)
        #*************Tao Nut Up Theta2*************#
        self.canvas_up_theta2 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_theta2.place(x = 730, y = 95)
        self.button_up_theta2 = self.canvas_up_theta2.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_theta2_text = self.canvas_up_theta2.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_theta2.tag_bind(self.button_up_theta2, "<ButtonPress-1>", self.on_press_button_up_theta2)
        self.canvas_up_theta2.tag_bind(self.button_up_theta2_text, "<ButtonPress-1>", self.on_press_button_up_theta2)
        self.canvas_up_theta2.tag_bind(self.button_up_theta2, "<ButtonRelease-1>", self.on_release_button_up_theta2)
        self.canvas_up_theta2.tag_bind(self.button_up_theta2_text, "<ButtonRelease-1>", self.on_release_button_up_theta2)
        #*************Tao Nut Down Theta2*************#
        self.canvas_down_theta2 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_theta2.place(x = 830, y = 95)
        self.button_down_theta2 = self.canvas_down_theta2.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_theta2_text = self.canvas_down_theta2.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_theta2.tag_bind(self.button_down_theta2, "<ButtonPress-1>", self.on_press_button_down_theta2)
        self.canvas_down_theta2.tag_bind(self.button_down_theta2_text, "<ButtonPress-1>", self.on_press_button_down_theta2)
        self.canvas_down_theta2.tag_bind(self.button_down_theta2, "<ButtonRelease-1>", self.on_release_button_down_theta2)
        self.canvas_down_theta2.tag_bind(self.button_down_theta2_text, "<ButtonRelease-1>", self.on_release_button_down_theta2)
        #*************Tao Nut Up Theta3*************#
        self.canvas_up_theta3 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_theta3.place(x = 730, y = 145)
        self.button_up_theta3 = self.canvas_up_theta3.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_theta3_text = self.canvas_up_theta3.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_theta3.tag_bind(self.button_up_theta3, "<ButtonPress-1>", self.on_press_button_up_theta3)
        self.canvas_up_theta3.tag_bind(self.button_up_theta3_text, "<ButtonPress-1>", self.on_press_button_up_theta3)
        self.canvas_up_theta3.tag_bind(self.button_up_theta3, "<ButtonRelease-1>", self.on_release_button_up_theta3)
        self.canvas_up_theta3.tag_bind(self.button_up_theta3_text, "<ButtonRelease-1>", self.on_release_button_up_theta3)
        #*************Tao Nut Down Theta3*************#
        self.canvas_down_theta3 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_theta3.place(x = 830, y = 145)
        self.button_down_theta3 = self.canvas_down_theta3.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_theta3_text = self.canvas_down_theta3.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_theta3.tag_bind(self.button_down_theta3, "<ButtonPress-1>", self.on_press_button_down_theta3)
        self.canvas_down_theta3.tag_bind(self.button_down_theta3_text, "<ButtonPress-1>", self.on_press_button_down_theta3)
        self.canvas_down_theta3.tag_bind(self.button_down_theta3, "<ButtonRelease-1>", self.on_release_button_down_theta3)
        self.canvas_down_theta3.tag_bind(self.button_down_theta3_text, "<ButtonRelease-1>", self.on_release_button_down_theta3)
        #*************Tao Nut Up Theta4*************#
        self.canvas_up_theta4 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_theta4.place(x = 730, y = 195)
        self.button_up_theta4 = self.canvas_up_theta4.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_theta4_text = self.canvas_up_theta4.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_theta4.tag_bind(self.button_up_theta4, "<ButtonPress-1>", self.on_press_button_up_theta4)
        self.canvas_up_theta4.tag_bind(self.button_up_theta4_text, "<ButtonPress-1>", self.on_press_button_up_theta4)
        self.canvas_up_theta4.tag_bind(self.button_up_theta4, "<ButtonRelease-1>", self.on_release_button_up_theta4)
        self.canvas_up_theta4.tag_bind(self.button_up_theta4_text, "<ButtonRelease-1>", self.on_release_button_up_theta4)
        #*************Tao Nut Down Theta4*************#
        self.canvas_down_theta4 = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_theta4.place(x = 830, y = 195)
        self.button_down_theta4 = self.canvas_down_theta4.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_theta4_text = self.canvas_down_theta4.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_theta4.tag_bind(self.button_down_theta4, "<ButtonPress-1>", self.on_press_button_down_theta4)
        self.canvas_down_theta4.tag_bind(self.button_down_theta4_text, "<ButtonPress-1>", self.on_press_button_down_theta4)
        self.canvas_down_theta4.tag_bind(self.button_down_theta4, "<ButtonRelease-1>", self.on_release_button_down_theta4)
        self.canvas_down_theta4.tag_bind(self.button_down_theta4_text, "<ButtonRelease-1>", self.on_release_button_down_theta4)
        #*************Tao Nut Up X*************#
        self.canvas_up_X = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_X.place(x = 730, y = 300)
        self.button_up_X = self.canvas_up_X.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_X_text = self.canvas_up_X.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_X.tag_bind(self.button_up_X, "<ButtonPress-1>", self.on_press_button_up_X)
        self.canvas_up_X.tag_bind(self.button_up_X_text, "<ButtonPress-1>", self.on_press_button_up_X)
        self.canvas_up_X.tag_bind(self.button_up_X, "<ButtonRelease-1>", self.on_release_button_up_X)
        self.canvas_up_X.tag_bind(self.button_up_X_text, "<ButtonRelease-1>", self.on_release_button_up_X)
        #*************Tao Nut Down X*************#
        self.canvas_down_X = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_X.place(x = 830, y = 300)
        self.button_down_X = self.canvas_down_X.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_X_text = self.canvas_down_X.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_X.tag_bind(self.button_down_X, "<ButtonPress-1>", self.on_press_button_down_X)
        self.canvas_down_X.tag_bind(self.button_down_X_text, "<ButtonPress-1>", self.on_press_button_down_X)
        self.canvas_down_X.tag_bind(self.button_down_X, "<ButtonRelease-1>", self.on_release_button_down_X)
        self.canvas_down_X.tag_bind(self.button_down_X_text, "<ButtonRelease-1>", self.on_release_button_down_X)
        #*************Tao Nut Up Y*************#
        self.canvas_up_Y = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_Y.place(x = 730, y = 350)
        self.button_up_Y = self.canvas_up_Y.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_Y_text = self.canvas_up_Y.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_Y.tag_bind(self.button_up_Y, "<ButtonPress-1>", self.on_press_button_up_Y)
        self.canvas_up_Y.tag_bind(self.button_up_Y_text, "<ButtonPress-1>", self.on_press_button_up_Y)
        self.canvas_up_Y.tag_bind(self.button_up_Y, "<ButtonRelease-1>", self.on_release_button_up_Y)
        self.canvas_up_Y.tag_bind(self.button_up_Y_text, "<ButtonRelease-1>", self.on_release_button_up_Y)
        #*************Tao Nut Down Y*************#
        self.canvas_down_Y = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_Y.place(x = 830, y = 350)
        self.button_down_Y = self.canvas_down_Y.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_Y_text = self.canvas_down_Y.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_Y.tag_bind(self.button_down_Y, "<ButtonPress-1>", self.on_press_button_down_Y)
        self.canvas_down_Y.tag_bind(self.button_down_Y_text, "<ButtonPress-1>", self.on_press_button_down_Y)
        self.canvas_down_Y.tag_bind(self.button_down_Y, "<ButtonRelease-1>", self.on_release_button_down_Y)
        self.canvas_down_Y.tag_bind(self.button_down_Y_text, "<ButtonRelease-1>", self.on_release_button_down_Y)
        #*************Tao Nut Up Z*************#
        self.canvas_up_Z = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_up_Z.place(x = 730, y = 400)
        self.button_up_Z = self.canvas_up_Z.create_oval(0, 0, 80, 40,fill= "green", outline = "white", width=2)
        self.button_up_Z_text = self.canvas_up_Z.create_text(40, 20, text = "+", font = ("Arial", 20), fill = "white")
        self.canvas_up_Z.tag_bind(self.button_up_Z, "<ButtonPress-1>", self.on_press_button_up_Z)
        self.canvas_up_Z.tag_bind(self.button_up_Z_text, "<ButtonPress-1>", self.on_press_button_up_Z)
        self.canvas_up_Z.tag_bind(self.button_up_Z, "<ButtonRelease-1>", self.on_release_button_up_Z)
        self.canvas_up_Z.tag_bind(self.button_up_Z_text, "<ButtonRelease-1>", self.on_release_button_up_Z)
        #*************Tao Nut Down Z*************#
        self.canvas_down_Z = tk.Canvas(self.jogging_frame, width=80, heigh = 40, bg = "#0F0A3F", highlightthickness=0)
        self.canvas_down_Z.place(x = 830, y = 400)
        self.button_down_Z = self.canvas_down_Z.create_oval(0, 0, 80, 40,fill= "red", outline = "white", width=2)
        self.button_down_Z_text = self.canvas_down_Z.create_text(40, 20, text = "-", font = ("Arial", 20), fill = "white")
        self.canvas_down_Z.tag_bind(self.button_down_Z, "<ButtonPress-1>", self.on_press_button_down_Z)
        self.canvas_down_Z.tag_bind(self.button_down_Z_text, "<ButtonPress-1>", self.on_press_button_down_Z)
        self.canvas_down_Z.tag_bind(self.button_down_Z, "<ButtonRelease-1>", self.on_release_button_down_Z)
        self.canvas_down_Z.tag_bind(self.button_down_Z_text, "<ButtonRelease-1>", self.on_release_button_down_Z)
        
        self.button_set_home = tk.Button(self.jogging_frame, text = "Set Home", font = ("Arial", 20), bg = "Yellow", fg = "black")
        self.button_set_home.place(x = 10, y = 300)
        self.button_close_jogging_menu = tk.Button(self.jogging_frame, text = "Close", font = ("Arial", 20), bg = "red", fg = "white", width=8
                                                   ,command =  self.off_jogging_menu)
        self.button_close_jogging_menu.place(x = 10, y = 350)
    def create_table_points_menu_widgets(self):
        
        #**********************************Button Open Jogging Menu***********#
        self.shadow_open_jogging_menu_button = tk.Button(self.padding_frame, text="⚙️ Setting", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_open_jogging_menu_button.place(x = 759, y = 9)
        self.open_jogging_menu_button = tk.Button(self.padding_frame, text= "Jogging", font= ("Arial", 12),bg="#0F0A3F", fg="white", width=10, height=3                          
                                                  ,command= self.show_joggingMenu_in_table_points_menu)
        self.open_jogging_menu_button.place(x = 755, y = 5)
        #**********************************Button ADD NEW POINT***********#
        self.shadow_add_new_point_button = tk.Button(self.padding_frame, text="⚙️ Setting", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_add_new_point_button.place(x = 509, y = 9)
        self.add_new_point_button = tk.Button(self.padding_frame, text= "New Point", font= ("Arial", 12),bg="#0F0A3F", fg="white", width=10, height=3                          
                                                  ,command = self.add_new_point)
        self.add_new_point_button.place(x = 505, y = 5)
        #**********************************Button DELETE POINT***********#
        self.shadow_delete_point_button = tk.Button(self.padding_frame, text="⚙️ Setting", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_delete_point_button.place(x = 634, y = 9)
        self.add_delete_point_button = tk.Button(self.padding_frame, text= "Delete", font= ("Arial", 12),bg="#0F0A3F", fg="white", width=10, height=3                          
                                                  ,command= self.create_table_obj.delete_selected_row)
        self.add_delete_point_button.place(x = 630, y = 5)
        #**********************************Button APPLY POINT***********#
        self.shadow_apply_point_button = tk.Button(self.padding_frame, text="⚙️ Setting", font=("Arial", 12),bg="#556F78", fg="white", width=10, height=3, bd=0, relief="flat")
        self.shadow_apply_point_button.place(x = 884, y = 9)
        self.apply_point_button = tk.Button(self.padding_frame, text= "Apply", font= ("Arial", 12),bg="#0F0A3F", fg="white", width=10, height=3                          
                                                  ,command= self.update_selected_row)
        self.apply_point_button.place(x = 880, y = 5)
        #**********************************Button MOVE TO  POINT***********#
        
        self.move_to_point_button = tk.Button(self.padding_frame, text= "Move", font= ("Arial", 12),bg="gray", fg="black", width=10, height=2                         
                                             , highlightbackground="white", highlightthickness=2,command= self.move_to_point)
        self.move_to_point_button.place(x = 500, y = 420)
        #***********************************Button*******************************#
        self.close_table_point_menu_button = tk.Button(self.padding_frame, text= "Close", font= ("Arial", 12), fg= "white", 
                                                                                             command=self.off_table_point_menu, bg = "red", bd = 0, width=6, height=2)
        self.close_table_point_menu_button.place(x=650, y = 420)
        

        #***********************************Position comboBox*********************#
        self.comboBox_Position_Label = tk.Label(self.padding_frame,width=40, heigh = 12, bg="#0F0A3F", fg = "white", bd=1, relief="flat", highlightthickness=1)
        self.comboBox_Position_Label.place(x = 550, y = 165)
        self.Position_Name_Box = tk.Label(self.padding_frame, text = "Position", font=("Arial", 14 ), fg = "white", bg = "#0F0A3F",heigh = 1, bd=0, relief="flat", highlightthickness=0)
        self.Position_Name_Box.place(x = 550, y = 170)
        #********************************************************************Tao Icon hien thi hop thoai X***************************************************#
        image = Image.open(X_icon_iamge_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((50, 50))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.X_icon = ImageTk.PhotoImage(image)

        self.X_icon_label = tk.Label(self.padding_frame, image=self.X_icon, bd=0, relief="flat", highlightthickness=0)
        self.X_icon_label.place(x= 555, y = 195)
        self.mm_label1 = tk.Label(self.padding_frame, text= "mm",font=("Arial", 20, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label1.place(x=735, y=205)
        self.X_mmBox = tk.Entry(self.padding_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.X_mmBox.place(x=610, y=205)
        # Gán giá trị cho luxBox
        self.X_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.X_mmBox.insert(tk.END, f"{self.X}")  # Thêm giá trị mới vào cuối
        #*****************************************************Tao Icon hein thi hop thoai Y******************************************************************#
        image = Image.open(Y_icon_image_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((50, 50))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.Y_icon = ImageTk.PhotoImage(image)

        self.Y_icon_label = tk.Label(self.padding_frame, image=self.Y_icon, bd=0, relief="flat", highlightthickness=0)
        self.Y_icon_label.place(x= 555, y = 250)
        self.mm_label2 = tk.Label(self.padding_frame, text= "mm",font=("Arial", 20, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label2.place(x=735, y=260)
        self.Y_mmBox = tk.Entry(self.padding_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.Y_mmBox.place(x=610, y=260)
        # Gán giá trị cho luxBox
        self.Y_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.Y_mmBox.insert(tk.END, f"{self.Y}")  # Thêm giá trị mới vào cuối
        #***************************************************Tao icon hien thi hop thoai Z********************************************************************#
        image = Image.open(Z_icon_iamge_path)  # Đảm bảo rằng tệp hình ảnh đúng
        image = image.resize((50, 50))  # Thay đổi kích thước hình ảnh (tuỳ chọn)
        self.Z_icon = ImageTk.PhotoImage(image)

        self.Z_icon_label = tk.Label(self.padding_frame, image=self.Z_icon, bd=0, relief="flat", highlightthickness=0)
        self.Z_icon_label.place(x= 555, y = 310)
        self.mm_label3 = tk.Label(self.padding_frame, text= "mm",font=("Arial", 20, ), width=12, background="#0F0A3F", fg="white")
        self.mm_label3.place(x=735, y=320)
        self.Z_mmBox = tk.Entry(self.padding_frame, font=("Arial", 20, ), width=12, background="#2e2e2e", fg="white")
        self.Z_mmBox.place(x=610, y=320)
        #********************8***************************                                 *******************************************************************#
        # Gán giá trị cho luxBox
        self.Z_mmBox.delete(0, tk.END)  # Xóa tất cả nội dung hiện tại trong luxBox
        self.Z_mmBox.insert(tk.END, f"{self.Z}")  # Thêm giá trị mới vào cuối
        
        self.create_table_obj.show_table()
    def create_man_control_menu_widgets(self):
        self.hotend_temp_icon_label = tk.Label(self.padding_frame, image=self.hotend_temp_icon, bd=0, relief="flat", highlightthickness=0)
        self.hotend_temp_icon_label.place(x= 10, y = 10)
        # Tạo widget Scale (thước cuộn)
        self.hotend_temp_value_scale = tk.Scale(self.padding_frame, from_=0, to=500, orient="horizontal", command=self.on_hotend_temp_scale_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 630)
        self.hotend_temp_value_scale.set(self.setHotendTemp)
        self.hotend_temp_value_scale.place(x = 60, y = 10)
        #
        self.hedbed_temp_icon_label = tk.Label(self.padding_frame, image=self.hedbed_temp_icon, bd=0, relief="flat", highlightthickness=0)
        self.hedbed_temp_icon_label.place(x= 10, y = 80)
        self.hedbed_temp_value_scale = tk.Scale(self.padding_frame, from_=0, to=120, orient="horizontal", command=self.on_hedbed_temp_scale_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 630)
        self.hedbed_temp_value_scale.set(self.setHedbedTemp)
        self.hedbed_temp_value_scale.place(x= 60, y = 80)
        #
        self.fanSpeed_icon_label = tk.Label(self.frame, image=self.fanSpeed_icon, bd=0, relief="flat", highlightthickness=0)
        self.fanSpeed_icon_label.place(x= 10, y = 150)
        self.fan_speed_value_scale = tk.Scale(self.padding_frame, from_=0, to=100, orient="horizontal", command=self.on_fan_speed_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 630)
        
        self.fan_speed_value_scale.set(self.setFanSpeed)
        self.fan_speed_value_scale.place(x= 60, y = 150)
        #
        self.X_icon_label = tk.Label(self.padding_frame, image=self.X_icon, bd=0, relief="flat", highlightthickness=0)
        self.X_icon_label.place(x= 10, y = 220)
        self.X_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_X_value_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 630)
        self.setX = self.X
        self.X_value_scale.set(self.setX)
        self.X_value_scale.place(x= 60, y= 220)
        #
        self.Y_icon_label = tk.Label(self.padding_frame, image=self.Y_icon, bd=0, relief="flat", highlightthickness=0)
        self.Y_icon_label.place(x= 10, y = 290)
        self.Y_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Y_value_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 630)
        self.setY = self.Y
        self.Y_value_scale.set(self.setY)
        self.Y_value_scale.place(x= 60, y = 290)
        #
        self.Z_icon_label = tk.Label(self.padding_frame, image=self.Z_icon, bd=0, relief="flat", highlightthickness=0)
        self.Z_icon_label.place(x= 10, y = 360)
        self.Z_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Z_value_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 630)
        self.setZ = self.Z
        self.Z_value_scale.set(self.Z)
        self.Z_value_scale.place(x = 60, y = 360)
        #
        self.close_menu_man_control_button = tk.Button(self.padding_frame, text= "Close", font= ("Arial", 12), fg= "white", 
                                                                                             command=self.off_manControl_menu, bg = "red", bd = 0, width=5, height=1)
        self.close_menu_man_control_button.place(x=700, y = 10)
        #
        self.set_home_button = tk.Button(self.padding_frame, text="Home", font=("Arial", 12), bg = "green",
                                         command= self.set_home, width=5, height=1, fg= "black")
        self.set_home_button.place(x = 700, y = 50)
        
    
    def create_extrude_menu_widgets(self):
        self.Emm_Label = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="black", width=6, height=1,
                                  text="E (mm)", font=("Arial", 12), fg="white")
        self.Emm_Label.place(x = 10, y=10)
        self.Emm_value_scale = tk.Scale(self.padding_frame, from_=-10, to=50, resolution=0.5, orient="horizontal", command=self.on_E_mm_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Emm_value_scale.set(self.setE)
        self.Emm_value_scale.place(x = 80, y = 10)
        self.F_Label = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="black", width=8, height=1,
                                  text="F (mm/p)", font=("Arial", 12), fg="white")
        self.F_Label.place(x = 10, y = 80)
        self.F_value_scale = tk.Scale(self.padding_frame, from_=0, to=2000, resolution=1, orient="horizontal", command=self.on_F_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.F_value_scale.set(self.setF)
        self.F_value_scale.place(x = 80, y= 80)
        self.Extrude_button = tk.Button(self.padding_frame, text="Extrude", font=("Arial", 12), fg= "white", bg="green",
                                        command=self.extrude_button_callback)
        self.Extrude_button.place(x = 10, y= 150)
        self.close_extrude_menu_button = tk.Button(self.padding_frame, text="Close", font=("Arial", 12), fg="black", bg="red",
                                                   command=self.close_extrude_menu_button_callback)
        self.close_extrude_menu_button.place(x = 120, y = 150)
    def create_PID_Parameter_menu_widgets(self):
        self.label1 = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="#2e2e2e", width=50, height=17)
        self.label1.place(x=10, y=60)
        self.label2 = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="#2e2e2e", width=50, height=17)
        self.label2.place(x=425, y=60)
        self.label3 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="white", width=18, height=1,
                               text="Hotend PID Parameter", font=("Arial", 12), fg = "black")
        self.label3.place(x =115, y = 30)
        self.label4 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="white", width=18, height=1,
                               text="Hedbed PID Parameter", font=("Arial", 12), fg = "black")
        self.label4.place(x =545, y = 30)
        #
        self.label5 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Kp_T", font=("Arial", 12), fg = "white")
        self.label5.place(x =20, y = 70)

        self.Kp_T_Hotend_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Kp_THotend_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Kp_T_Hotend_value_scale.set(f"{self.Kp_THotend}")
        self.Kp_T_Hotend_value_scale.place(x = 65, y = 70)

        self.label6 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Ki_T", font=("Arial", 12), fg = "white")
        self.label6.place(x =20, y = 140)

        self.Ki_T_Hotend_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Ki_THoteng_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Ki_T_Hotend_value_scale.set(f"{self.Ki_THotend}")
        self.Ki_T_Hotend_value_scale.place(x = 65, y = 140)
        

        self.label7 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Kd_T", font=("Arial", 12), fg = "white")
        self.label7.place(x =20, y = 210)

        self.Kd_T_Hotend_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Kd_THotend_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Kd_T_Hotend_value_scale.set(f"{self.Kd_THotend}")
        self.Kd_T_Hotend_value_scale.place(x = 65, y = 210)

        self.label8 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Kb_T", font=("Arial", 12), fg = "white")
        self.label8.place(x =20, y = 280)

        self.Kb_T_Hotend_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Z_value_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Kb_T_Hotend_value_scale.place(x = 65, y = 280)
        #
        self.label9 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Kp_T", font=("Arial", 12), fg = "white")
        self.label9.place(x =435, y = 70)

        self.Kp_THedbed_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Kp_THedbed_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Kp_THedbed_value_scale.set(f"{self.Kp_THedbed}")
        self.Kp_THedbed_value_scale.place(x = 480, y = 70)

        self.label10 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Ki_T", font=("Arial", 12), fg = "white")
        self.label10.place(x =435, y = 140)

        self.Ki_THedbed_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Ki_THedbed_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Ki_THedbed_value_scale.set(f"{self.Ki_THedbed}")
        self.Ki_THedbed_value_scale.place(x = 480, y = 140)

        self.label11 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Kd_T", font=("Arial", 12), fg = "white")
        self.label11.place(x =435, y = 210)

        self.Kd_THedbed_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Kd_THedbed_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Kd_THedbed_value_scale.set(f"{self.Kd_THedbed}")
        self.Kd_THedbed_value_scale.place(x = 480, y = 210)

        self.label12 = tk.Label(self.padding_frame, bd=1, relief="flat", highlightthickness=1, bg="black", width=4, height=1,
                               text="Kb_T", font=("Arial", 12), fg = "white")
        self.label12.place(x =435, y = 280)

        self.Kb_THedbed_value_scale = tk.Scale(self.padding_frame, from_=-250, to=250, resolution=0.5, orient="horizontal", command=self.on_Z_value_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 340)
        self.Kb_THedbed_value_scale.place(x = 480, y = 280)


        self.close_PID_Parameter_Menu_button = tk.Button(self.padding_frame, text= "Close", font= ("Arial", 12), fg= "white", 
                                                                                             command=self.off_PID_Parameter_menu, bg = "red", bd = 0, width=5, height=1)
        self.close_PID_Parameter_Menu_button.place(x=10, y = 360)
        #
    def create_axis_resolution_menu_widgets(self):
        self.blux_label = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="#2e2e2e", width=8, height=1,
                                   text="BLU X", font=("Arial", 14), fg= "yellow")
        self.blux_label.place(x = 10, y = 10)
        self.blux_value_scale = tk.Scale(self.padding_frame, from_=-0.1, to=0.1, resolution=0.00001, orient="horizonta", command=self.on_BLUX_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 600)
        self.blux_value_scale.set(f"{self.BLUX}")
        self.blux_value_scale.place(x = 100, y = 10)

        self.bluy_label = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="#2e2e2e", width=8, height=1,
                                   text="BLU Y", font=("Arial", 14), fg= "yellow")
        self.bluy_label.place(x = 10, y = 80)
        self.bluy_value_scale = tk.Scale(self.padding_frame, from_=-0.1, to=0.1, resolution=0.00001, orient="horizonta", command=self.on_BLUY_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 600)
        self.bluy_value_scale.set(f"{self.BLUY}")
        self.bluy_value_scale.place(x = 100, y = 80)

        self.bluz_label = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="#2e2e2e", width=8, height=1,
                                   text="BLU Z", font=("Arial", 14), fg= "yellow")
        self.bluz_label.place(x = 10, y = 150)
        self.bluz_value_scale = tk.Scale(self.padding_frame, from_=-0.001, to=0.001, resolution=0.0000001, orient="horizonta", command=self.on_BLUZ_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 600)
        self.bluz_value_scale.set(f"{self.BLUZ}")
        self.bluz_value_scale.place(x = 100, y = 150)

        self.blue_label = tk.Label(self.padding_frame, bd=0, relief="flat", highlightthickness=0, bg="#2e2e2e", width=8, height=1,
                                   text="BLU E", font=("Arial", 14), fg= "yellow")
        self.blue_label.place(x = 10, y = 220)
        self.blue_value_scale = tk.Scale(self.padding_frame, from_=-0.1, to=0.1, resolution=0.001, orient="horizonta", command=self.on_BLUE_change, bg= "black", 
                              font=("Helvetica", 14), fg="white", width= 32, length= 600)
        self.blue_value_scale.set(f"{self.BLUE}")
        self.blue_value_scale.place(x = 100, y = 220)
        
        self.close_menu_axis_resolution_button = tk.Button(self.padding_frame, text="Close", font= ("Arial", 12), fg= "white",
                                                           bg="red", command=self.off_axis_resolution_menu)
        self.close_menu_axis_resolution_button.place(x=710, y =10)
    def create_question_menu_widgets(self, str):
        self.str_label = tk.Label(self.question_frame, bg = "white", bd = 0, highlightthickness=0,
                                  text = str, font = ("Arial", 20) )
        self.str_label.place(x = 50, y = 10)
        self.yes_button = tk.Button(self.question_frame, text = "Yes", font = ("Arial", 20), bg = "green", 
                                    command= self.on_press_button_yes)
        self.yes_button.place(x = 150, y = 100)
        self.no_button = tk.Button(self.question_frame, text = "No ", font = ("Arial", 20), bg = "red", 
                                    command= self.on_press_button_yes)
        self.no_button.place(x = 230, y = 100)
        
    #button_callback_functions
    def on_press_button_yes(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_auto_home)
        self.question_frame.destroy()
    def on_press_button_no(self):
        self.question_frame.destroy()
    def on_press_button_up_theta1(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta1_up)
    def on_release_button_up_theta1(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_theta1(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta1_down)
    def on_release_button_down_theta1(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_up_theta2(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta2_up)
    def on_release_button_up_theta2(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_theta2(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta2_down)
    def on_release_button_down_theta2(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)  
    def on_press_button_up_theta3(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta3_up)
    def on_release_button_up_theta3(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_theta3(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta3_down)
    def on_release_button_down_theta3(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_up_theta4(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta4_up)
    def on_release_button_up_theta4(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_theta4(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_theta4_down)
    def on_release_button_down_theta4(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_up_X(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_x_up)
    def on_release_button_up_X(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_X(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_x_down)
    def on_release_button_down_X(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)    
    def on_press_button_up_Y(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_y_up)
    def on_release_button_up_Y(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_Y(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_y_down)
    def on_release_button_down_Y(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_up_Z(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_z_up)
    def on_release_button_up_Z(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    def on_press_button_down_Z(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_jogging_z_down)
    def on_release_button_down_Z(self, event):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_no_op)
    #
    def on_press_button_auto_home(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_auto_home)
    #
    def on_press_button_start(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_val_on)
    #
    def on_press_button_stop(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_val_off)
    def on_press_button_pause(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_pause)
    def on_press_button_servo_on(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_servo_on)
    def on_press_button_servo_off(self):
        socket_client.my_socket_obj.send_data(socket_client.my_socket_obj.cmd_servo_off)
    def on_hotend_temp_scale_change(self, hotend_value):
        self.setHotendTemp = hotend_value
        
    def on_hedbed_temp_scale_change(self, hedbed_value):
        self.setHedbedTemp = hedbed_value
        
    def on_fan_speed_change(self, fanspeed_value):
        self.fanSpeedPower = fanspeed_value
        
    def on_X_value_change(self, X_value):
        self.setX = X_value
        
    def on_Y_value_change(self, Y_value):
        self.setY = Y_value
        
    def on_Z_value_change(self, Z_value):
        self.setZ = Z_value
        

    def on_Kp_THedbed_change(self, Kp_Hedbed_Val):
        self.Kp_THedbed = Kp_Hedbed_Val
        
    def on_Ki_THedbed_change(self, Ki_Hedbed_val):
        self.Ki_THedbed = Ki_Hedbed_val
    
    def on_Kd_THedbed_change(self, Kd_Hedbed_Val):
        self.Kd_THedbed = Kd_Hedbed_Val
        
    def on_Kp_THotend_change(self, Kp_Hotend_val):
        self.Kp_THotend = Kp_Hotend_val
        
    def on_Ki_THoteng_change(self, Ki_Hotend_Val):
        self.Ki_THotend = Ki_Hotend_Val
        
    def on_Kd_THotend_change(self, Kd_hotend_Val):
        self.Kd_THotend = Kd_hotend_Val
        
    def on_BLUX_change(self, BLUX_Val):
        self.BLUX = BLUX_Val
        
    def on_BLUY_change(self, BLUY_Val):
        self.BLUY = BLUY_Val
        
    def on_BLUZ_change(self, BLUZ_Val):
        self.BLUZ = BLUZ_Val
        
    def on_BLUE_change(self, BLUE_Val):
        self.BLUE = BLUE_Val
        
    def on_E_mm_change(self, E_Value):
        self.setE = E_Value
    def on_F_change(self, F_Value):
        self.setF = F_Value
    def toggle_settings(self):
        self.currentMenu = self.settingMenu
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.padding_frame = tk.Frame(self.frame)
        self.padding_frame.configure(width=130, height= 150, bg= "#2e2e2e")
        self.create_setting_menu_widget()
        self.padding_frame.place(x=5, y=80)
    # Hàm hiển thị màn hình điều khiển
    def off_setting_menu(self):
        self.currentMenu = self.mainMenu
        self.padding_frame.place_forget()
    def show_jogging_menu(self):
        
        if self.jogging_frame:
            self.jogging_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.jogging_frame = tk.Frame(self.frame)
        self.jogging_frame.configure(width=1050, height= 600, bg= "#0F0A3F")
        self.create_jogging_menu_widget()
        self.jogging_frame.place(x=5, y=5)
    def off_jogging_menu(self):
        self.create_main_mernu_widgets()
        self.jogging_frame.place_forget()
    def off_jogging_menu_in_create_table(self):
        self.create_table_obj.show_table()
        self.create_table_points_menu_widgets()
        self.jogging_frame.place_forget()
    def show_table_points_menu(self):
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.padding_frame = tk.Frame(self.frame)
        self.padding_frame.configure(width=1050, height= 600, bg= "#0F0A3F")
        self.create_table_points_menu_widgets()
        self.padding_frame.place(x=5, y=5)
    def off_table_point_menu(self):
        self.create_table_obj.hide_table()
        self.create_main_mernu_widgets()
        self.padding_frame.place_forget()
    def show_joggingMenu_in_table_points_menu(self):
        
        if self.jogging_frame:
            self.jogging_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.jogging_frame = tk.Frame(self.frame)
        self.jogging_frame.configure(width=1050, height= 600, bg= "#0F0A3F")
        
        self.create_table_obj.hide_table()
        self.create_jogging_menu_widget()
        self.button_close_jogging_menu.configure(command= self.off_jogging_menu_in_create_table)
        self.jogging_frame.place(x=5, y=5)
    def show_axis_resolution_menu(self):
        self.currentMenu = self.axisResolutionMenu
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.padding_frame = tk.Frame(self.frame)
        self.padding_frame.configure(width= 840, height= 480, bg= "#0F0A3F")
        self.create_axis_resolution_menu_widgets()
        self.padding_frame.place(x= 0, y = 0)
    def off_axis_resolution_menu(self):
        self.currentMenu = self.mainMenu
        self.padding_frame.place_forget()
   
    def show_manControl_menu(self):
        self.currentMenu =self.manControlMenu
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.padding_frame = tk.Frame(self.frame)
        self.padding_frame.configure(width= 840, height= 480, bg= "#0F0A3F")
        self.create_man_control_menu_widgets()
        self.padding_frame.place(x= 0, y = 0)
    
    def off_manControl_menu(self):
        self.currentMenu = self.mainMenu
        self.padding_frame.place_forget()
    
    def show_PID_Paremeter_menu(self):
        self.currentMenu == self.PIDParameterMenu
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.padding_frame = tk.Frame(self.frame)
        self.padding_frame.configure(width= 840, height= 480, bg= "#0F0A3F")
        self.create_PID_Parameter_menu_widgets()
        self.padding_frame.place(x= 0, y = 0)
    
    def off_PID_Parameter_menu(self):
        self.currentMenu = self.mainMenu
        self.padding_frame.place_forget()
    
    def extrude_option_button_callback(self):
        self.currentMenu == self.PIDParameterMenu
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
        # Tạo frame mới
        self.padding_frame = tk.Frame(self.frame)
        self.padding_frame.configure(width= 840, height= 480, bg= "#2e2e2e")
        self.create_extrude_menu_widgets()
        self.padding_frame.place(x= 10, y = 10)

    def close_extrude_menu_button_callback(self):
        self.padding_frame.place_forget()
    def extrude_button_callback(self):
        pass
    def theta1_value_change_keyboard(self):
        global keyboard_frame
        print("DA nhan")
        if keyboard_frame is not None:
            if keyboard_frame.winfo_ismapped():
                keyboard_frame.place_forget()
            else:
                keyboard_frame.place(x=300, y=300)  # Vị trí đặt bàn phím
        else:
            # Nếu keyboard_frame là None, tạo mới
            keyboard_frame = show_keyboard(self.frame, self.theta1_value_box)  # Hiển thị bàn phím nếu chưa có

    def blux_toggle_keyboard(self):
        global keyboard_frame
        if keyboard_frame is not None:
            if keyboard_frame.winfo_ismapped():
                keyboard_frame.place_forget()
            else:
                keyboard_frame.place(x=300, y=300)  # Vị trí đặt bàn phím
        else:
            # Nếu keyboard_frame là None, tạo mới
            keyboard_frame = show_keyboard(self.frame, self.bluxBox)  # Hiển thị bàn phím nếu chưa có

    def bluy_toggle_keyboard(self):
        global keyboard_frame
        if keyboard_frame is not None and keyboard_frame.winfo_ismapped():
            keyboard_frame.place_forget()  # Ẩn bàn phím nếu nó đang hiển thị
        else:
            keyboard_frame = show_keyboard(self.frame, self.bluyBox)  # Hiển thị bàn phím nếu chưa có

    def bluz_toggle_keyboard(self):
        global keyboard_frame
        if keyboard_frame is not None and keyboard_frame.winfo_ismapped():
            keyboard_frame.place_forget()  # Ẩn bàn phím nếu nó đang hiển thị
        else:
            keyboard_frame = show_keyboard(self.frame, self.bluzBox)  # Hiển thị bàn phím nếu chưa có      

    def blue_toggle_keyboard(self):
        global keyboard_frame
        if keyboard_frame is not None and keyboard_frame.winfo_ismapped():
            keyboard_frame.place_forget()  # Ẩn bàn phím nếu nó đang hiển thị
        else:
            keyboard_frame = show_keyboard(self.frame, self.blueBox)  # Hiển thị bàn phím nếu chưa có
    def set_home(self):
        pass
    def set_home_button_callback(self):
        pass
    # Hàm cập nhật đồng hồ
    def update_time(self):
        if self.running:  # Chỉ cập nhật khi đồng hồ đang chạy
            hours = self.seconds // 3600  # Tính số giờ
            minutes = (self.seconds % 3600) // 60  # Tính số phút
            secs = self.seconds % 60  # Tính số giây

            # Hiển thị thời gian dưới dạng HH:MM:SS
            time_str = f"{hours:02}:{minutes:02}:{secs:02}"
            self.timeBox.delete(0, tk.END)  # Xóa nội dung cũ
            self.timeBox.insert(tk.END, time_str)  # Chèn thời gian mới

            # Tăng số giây và gọi lại update_time sau 1 giây
            self.seconds += 1
            self.timeBox.after(1000, self.update_time)  # Cập nhật sau 1 giây

    # Hàm xử lý khi nhấn nút Start
    def start_button_callback(self):
        
        self.seconds = 0  # Reset lại thời gian về 0
        self.running = True  # Đánh dấu là đồng hồ đang chạy
        self.update_time()  # Bắt đầu hiển thị thời gian
        self.noteBox.delete(0, tk.END)
        self.noteBox.insert(tk.END, gCodeRead_Obj.gcode_commands[gCodeRead_Obj.current_command_index])
        gCodeRead_Obj.sendGcodeComand()

    # Hàm xử lý khi nhấn nút Pause
    def pause_button_callback(self):
        
        self.running = False  # Dừng đồng hồ khi nhấn Pause
        self.currentMenu = self.axisResolutionMenu
        if self.padding_frame:
            self.padding_frame.destroy()  # Xóa frame cũ
            # Tạo frame mới
            self.padding_frame = tk.Frame(self.frame)
            self.padding_frame.configure(width= 200, height= 200, bg= "white")
            self.create_menu_pause_widgets()
            self.padding_frame.place(x= 600, y = 60)
    def continue_button_callback(self):
        self.running = True
        self.update_time()
        self.currentMenu = self.mainMenu
        self.padding_frame.place_forget()
    def add_new_point(self):
         # Tự động tìm ID mới không trùng
        new_id = 0
        while new_id in self.create_table_obj.points:
            new_id += 1
        self.create_table_obj.save_point(new_id, self.X, self.Y, self.Z, self.E)
        
        self.create_table_obj.update_table()
    def update_selected_row(self):
        if self.create_table_obj.selected_id in self.create_table_obj.points:
            try:

                self.create_table_obj.points[self.create_table_obj.selected_id] = (self.X, self.Y, self.Z, self.E)
                self.create_table_obj.update_table()
                self.create_table_obj.apply_and_save()
                self.create_table_obj.send_cmd_aplly_point_to_slave(self.create_table_obj.selected_id)
            except ValueError:
                print("Giá trị nhập vào không hợp lệ.")
    def move_to_point(self):
        if self.create_table_obj.selected_id in self.create_table_obj.points:
            try:
                self.create_table_obj.move_to_points(self.create_table_obj.selected_id)
            except ValueError:
                print("Giá trị nhập vào không hợp lệ.")

    
        

 
