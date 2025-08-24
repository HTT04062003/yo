# 🤖 SCARA Robot Control System
Dự án này xây dựng một hệ thống điều khiển robot SCARA bao gồm:

- **Firmware STM32**: điều khiển động cơ servo, nội suy quỹ đạo (linear, circular, trapezoidal, S-curve), PID, giao tiếp CAN/UART.  
- **Raspberry Pi Application**: giao diện GUI (Python Tkinter) để điều khiển robot và giám sát trạng thái.  
- **Yocto Project Layer**: tích hợp ứng dụng vào hệ điều hành nhúng (core-image-scara) chạy trên Raspberry Pi.  
---
## 📂 Cấu trúc dự án
  scara-robot-project/
  │
  ├── stm32-firmware/     
  │   ├── Core/    
  │   ├── Drivers/     
  │   ├── Inc/      
  │   ├── Src/            
  │   ├── Makefile / .project      
  │   └── README.md             
  │
  ├── rpi-app/                       # Code chạy trên Raspberry Pi
  │   ├── app/                       # Python GUI (Tkinter)
  │   │   ├── mainapp.py
  │   │   ├── gui/                   # Các màn hình GUI con
  │   │   └── utils/                 # Hàm tiện ích
  │   │
  │   ├── Comunication/              # Code C giao tiếp với STM32
  │   │   ├── comunication_process.c
  │   │   ├── uart.c / can.c / socket.c / shm.c
  │   │   └── Makefile
  │   │
  │   ├── run.sh                     # Script khởi động app
  │   └── README.md                  # Hướng dẫn build & chạy trên RPi
  │
  ├── meta-scara/                    # Custom Yocto Layer
  │   ├── recipes-apps/
  │   │   └── scara-app/
  │   │       ├── files/
  │   │       │   ├── run.sh
  │   │       │   └── scara.service
  │   │       └── scara-app.bb       # Recipe build app vào Yocto
  │   └── README.md                  # Hướng dẫn tích hợp layer
  ---
## 🚀 Tính năng
- **STM32**  
  - Điều khiển AC Servo bằng xung STEP/DIR.  
  - Nội suy tuyến tính, cung tròn với profile vận tốc Trapezoidal & S-curve.  
  - PID điều khiển động cơ & nhiệt độ (hotend).  
  - Giao tiếp CAN & UART với Raspberry Pi.  

- **Raspberry Pi**  
  - GUI trực quan viết bằng Python Tkinter.  
  - Chương trình C trung gian: nhận lệnh từ GUI, gửi/nhận dữ liệu từ STM32 qua CAN/UART, chia sẻ bằng socket & shared memory.  
  - Tự động khởi động khi bật nguồn (systemd service).  

- **Yocto Project**  
  - Custom layer `meta-scara`.  
  - Recipe `scara-app.bb` cài đặt binary và script khởi động.  
  - Tạo ra file image `.img` để flash trực tiếp vào Raspberry Pi.  

---
# SCARA Yocto Image

## 🔽 Download
[**SCARA Firmware v1.1 (ZIP)**](https://github.com/HTT04062003/yo/releases/download/v1.1/SCARA_FIRMWARE.zip)

[SCARA Yocto Image v1.0 (ZIP)](https://github.com/HTT04062003/yo/releases/download/v1.0/core-image-scara-raspberrypi4.zip)

[**TAP_BAN_VE_DIEN v1.1 (ZIP)**](https://github.com/HTT04062003/yo/releases/download/v1.2/TAP_BAN_VE_DIEN.pdf)
## 💡 Hướng dẫn sử dụng

1. Tải về file `.zip` và giải nén ra `.img`
2. Dùng phần mềm [balenaEtcher](https://www.balena.io/etcher/) để flash file `.img` vào thẻ nhớ SD
3. Cắm vào Raspberry Pi 4 và khởi động

## ℹ️ Thông tin thêm

- Build từ Yocto Project
- Tùy biến cho SCARA robot
