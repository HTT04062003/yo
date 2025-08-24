#include "my_usb_serial.h"
#include "socket_server.h"
#include "shared_mem.h"
#include <termios.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <errno.h>
#include "comand_line.h"
#include <stdlib.h>
#include <ctype.h>
#include "../Robot_Kinematic/scara_robot_parameter.h"
#include "../Robot_Kinematic/forward_kinematic.h"
#include "thread.h"
int serial_fd;
uint8_t serial_buf[BUF_SIZE];
int serial_buf_len = 0;

int setup_serial(const char *device) {
    int fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd < 0) return -1;

    struct termios tty;
    if (tcgetattr(fd, &tty) != 0) return -1;

    cfsetospeed(&tty, BAUDRATE);
    cfsetispeed(&tty, BAUDRATE);
    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;
    tty.c_iflag &= ~(IXON | IXOFF | IXANY);
    tty.c_cflag |= (CLOCAL | CREAD);
    tty.c_cflag &= ~(PARENB | PARODD | CSTOPB | CRTSCTS);
    tty.c_lflag = 0;
    tty.c_oflag = 0;
    tty.c_cc[VMIN] = 1;
    tty.c_cc[VTIME] = 1;

    if (tcsetattr(fd, TCSANOW, &tty) != 0) return -1;

    return fd;
}
uint8_t crc8(const uint8_t *data, uint32_t len) {
    uint8_t crc = 0x00;
    for (uint32_t i = 0; i < len; ++i) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; ++j) {
            if (crc & 0x80)
                crc = (crc << 1) ^ 0x07;
            else
                crc <<= 1;
        }
    }
    return crc;
}
void send_float_packet(int uart_fd, uint8_t header,float *data) {
    FloatPacket packet;
    packet.header = (uint8_t)header;
    memcpy(packet.f, data, sizeof(float) * 8);
    packet.crc = crc8((uint8_t *)&packet, sizeof(FloatPacket) - 2);  // không tính byte CRC
    packet.stop = '\n';
    // Gửi bằng write()
    // XÓA BUFFER TRUYỀN TRƯỚC KHI GỬI
    if (tcflush(uart_fd, TCOFLUSH) < 0) {
        perror("tcflush TCOFLUSH failed");
    }

    // Gửi gói tin
    int written = write(uart_fd, &packet, sizeof(FloatPacket));
    if (written < 0) {
        perror("UART write failed");
    }

    // Chờ gửi xong toàn bộ
    if (tcdrain(uart_fd) < 0) {
        perror("tcdrain failed");
    }
}

void receive_float_packet( int serial_fd, int client_fd) {
    
    int rx_len = read(serial_fd, serial_buf + serial_buf_len, PACKET_SIZE - serial_buf_len);
            if (rx_len > 0) {
                serial_buf_len += rx_len;

                if (serial_buf_len == PACKET_SIZE) {
                    // Kiểm tra header và stop
                    if (serial_buf[34] == '\n') {
                        // Tính CRC8 và so sánh
                        uint8_t crc = crc8(serial_buf, 33); // từ header đến f[7]
                        if (crc == serial_buf[33] && serial_buf[0] == RESPONSE_UPDATE_DATA_FROM_SLAVE) {
                            // Gói hợp lệ
                            static uint8_t cnt = 0;
                            cnt+=1;
                            FloatPacket *pkt = (FloatPacket *)serial_buf;
                            shared_xyz->cur_Theta1 = pkt->f[0];
                            shared_xyz->cur_Theta2 = pkt->f[1];
                            shared_xyz->cur_Theta3 = pkt->f[2];
                            shared_xyz->cur_Theta4 = pkt->f[3];
                            shared_xyz->F1 = pkt->f[4];
                            shared_xyz->F2 = pkt->f[5];
                            shared_xyz->F3 = pkt->f[6];
                            shared_xyz->F4 = pkt->f[7];
                            SCARA_ROBOT_PARAMETER.Current_Revolute.CurTheta1 = shared_xyz->cur_Theta1;
                            SCARA_ROBOT_PARAMETER.Current_Revolute.CurTheta2 = shared_xyz->cur_Theta2;
                            SCARA_ROBOT_PARAMETER.Current_Revolute.CurTheta3 = shared_xyz->cur_Theta3;
                            SCARA_ROBOT_PARAMETER.Current_Revolute.CurD4 = shared_xyz->cur_Theta4;
                            Scara_Robot_Forward_Kinematics(&SCARA_ROBOT_PARAMETER);
                            shared_xyz->cur_x = SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurX;
                            shared_xyz->cur_y = SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurY;
                            shared_xyz->cur_z = SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurZ;
                            shared_xyz->curE = SCARA_ROBOT_PARAMETER.Current_Revolute.curE;
                            
                            if(cnt == 4){
                               if (!is_sending && client_fd > 0) {
                                    send_all(client_fd, cmd_update_data_to_app, strlen(cmd_update_data_to_app));
                                }
                                cnt = 0;  
                            }
                        else if(crc == serial_buf[33] && serial_buf[0] == RESPONSE_MOVE_Z_PLT){
                            pthread_mutex_lock(&status_mutex);
                            if(robot_status == STATUS_PLACE){
                                robot_status = STATUS_MOVE_TO_PICK_POINT;
                            }
                            else if (robot_status == STATUS_PICK){
                                robot_status = STATUS_MOVE_TO_WAWEHOUSE;
                            }
                            pthread_mutex_unlock(&status_mutex);
                            }  
                        
                        }
                        else if(serial_buf[0] == RESPONSE_MOVE_THETA3_CPLT){
                             printf("MOVE CPLT\n");
                            //printf("Parsed: T1=%.5f, T2=%.5f, T3=%.5f, X = %.5f, Y = %.5f, Z = %.5f\n", 
                            //        pkt->f[0], pkt->f[1], pkt->f[2], SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurX, SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurY, SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurZ);
                        } else {
                            //fprintf(stderr, "CRC mismatch: expected %02X, got %02X\n", crc, serial_buf[33]);
                        }
                    } else {
                        fprintf(stderr, "Invalid packet (header=0x%02X, stop=0x%02X)\n",
                                serial_buf[0], serial_buf[34]);
                    }

                    // Reset buffer sau mỗi gói
                    serial_buf_len = 0;
                    memset(serial_buf, 0, BUF_SIZE);
                }
            }

    
}
int serial_send_string(int serial_fd, const char *str) {
    if (serial_fd < 0 || str == NULL) return -1;
    return write(serial_fd, str, strlen(str));
}

int parse_data(const char *str) {
    if (!shared_xyz || !str) return -1;

    const char *p = str;
    uint8_t cmd = 0;

    while (*p) {
        if (*p == 'U') {
            cmd = UPDATE_DATA;
            p++;
        }
        else if (*p == 'X') {
            shared_xyz->cur_x = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'Y') {
            shared_xyz->cur_y = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'Z') {
            shared_xyz->cur_z = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'H') {
            shared_xyz->cur_Theta1 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'B') {
            shared_xyz->cur_Theta2 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'N') {
            shared_xyz->cur_Theta3 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'M') {
            shared_xyz->cur_Theta4 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'J') {
            shared_xyz->F1 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'K') {
            shared_xyz->F2 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'L') {
            shared_xyz->F3 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'P') {
            shared_xyz->F4 = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else if (*p == 'E') {
            shared_xyz->curE = atof(++p);
            while (*p && (isdigit(*p) || *p == '.' || *p == '-')) p++;
        }
        else {
            p++;  // bỏ qua ký tự không hợp lệ
        }
    }

    return cmd;
}
void Send_Cmd_Move_Z_To_Slave(int uart_fd, float Set_Z, float Speed){
    float data[8];
        data[0] = 0;
        data[1] = 0;
        data[2] = 0;
        data[3] = Set_Z;
        data[4] = 0;
        data[5] = 0 ;
        data[6] = 0;
        data[7] = Speed;
    send_float_packet(uart_fd, COMAND_MOVE_Z, data);

    
}
void Send_Cmd_Set_Theta3_To_Slave(int uart_fd, float Set_Theta3, float Set_Speed){
    float data[8];
        data[0] = 0;
        data[1] = 0;
        data[3] = 0;
        data[2] = Set_Theta3;
        data[4] = 0;
        data[5] = 0 ;
        data[7] = 0;
        data[6] = Set_Speed;
    send_float_packet(uart_fd, COMAND_MOVE_THETA3, data);
}
