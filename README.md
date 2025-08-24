# 🤖 SCARA Robot Control System
Dự án này xây dựng một hệ thống điều khiển robot SCARA bao gồm:

- **Firmware STM32**: điều khiển động cơ servo, nội suy quỹ đạo (linear, circular, trapezoidal, S-curve), PID, giao tiếp CAN/UART.  
- **Raspberry Pi Application**: giao diện GUI (Python Tkinter) để điều khiển robot và giám sát trạng thái.  
- **Yocto Project Layer**: tích hợp ứng dụng vào hệ điều hành nhúng (core-image-scara) chạy trên Raspberry Pi.  
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

## 🛠️ Hướng dẫn build

### 1. Build firmware STM32
- Mở `stm32-firmware/` bằng STM32CubeIDE hoặc Keil.  
- Build và flash xuống STM32F407.  

### 2. Build image Yocto cho Raspberry Pi
```bash
# Clone repo
git clone https://github.com/HTT04062003/yo/scara-robot-project.git
cd scara-robot-project/yocto

# Source môi trường Yocto
source poky/oe-init-build-env build


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
