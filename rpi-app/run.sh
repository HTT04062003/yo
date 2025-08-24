#!/bin/bash
cd "$(dirname "$0")"
PYTHON_PORT=12345

# Hiện thông tin debug
set -x

# Hàm dọn dẹp khi thoát hoặc lỗi
cleanup() {
    echo ""
    echo "Stopping all processes..."

    if ps -p $C_PID > /dev/null 2>&1; then
        echo "Killing C process (PID $C_PID)..."
        kill $C_PID
    fi

    if ps -p $PY_PID > /dev/null 2>&1; then
        echo "Killing Python process (PID $PY_PID)..."
        kill $PY_PID
    fi

    echo "Shutting down CAN interface..."
    ip link set can0 down

    echo "All processes stopped."
    exit 0
}

# Gán cleanup cho Ctrl+C
trap cleanup SIGINT

# Khởi tạo giao diện CAN
echo "Setting up CAN interface..."
ip link set can0 down 2>/dev/null  # chắc chắn can0 được giải phóng
ip link set can0 up type can bitrate 500000
if [ $? -ne 0 ]; then
    echo "Failed to bring up CAN interface. Exiting."
    exit 1
fi

# Giải phóng cổng đang bị chiếm (nếu có)
EXISTING_PID=$(lsof -t -i :$PYTHON_PORT)
if [ ! -z "$EXISTING_PID" ]; then
    echo "Port $PYTHON_PORT is currently in use by PID $EXISTING_PID. Killing it..."
    kill -9 $EXISTING_PID
    sleep 1
else
    echo "Port $PYTHON_PORT is free."
fi

# Chạy chương trình C ở nền
echo "Running C binary..."
./Comunication/comunication_process &
C_PID=$!

# Chạy Python script và lưu log
echo "Starting Python script..."
python3 app/mainapp.py > /var/log/python_log.txt 2>&1 &
PY_PID=$!

# Đợi một trong hai tiến trình kết thúc
wait -n

# Cleanup toàn bộ khi 1 tiến trình chết
cleanup
