#ifndef MY_USB_SERIAL_H
#define MY_USB_SERIAL_H
#define BAUDRATE B115200
#define BUF_SIZE 256
#define PACKET_SIZE 35
#include <stdint.h>


typedef struct {
    uint8_t header;
    float f[8];
    uint8_t crc;
    uint8_t stop;
} __attribute__((packed)) FloatPacket;
int setup_serial(const char *device);
int serial_send_string(int serial_fd, const char *str);
int parse_data(const char *str);
void receive_float_packet( int serial_fd, int client_fd);
void send_float_packet(int uart_fd, uint8_t header,float *data);
void Send_Cmd_Move_Z_To_Slave(int uart_fd, float Set_Z, float Speed);
void Send_Cmd_Set_Theta3_To_Slave(int uart_fd, float Set_Theta3, float Set_Speed);
extern int serial_fd;
extern uint8_t serial_buf[BUF_SIZE];
extern int serial_buf_len;

#endif
