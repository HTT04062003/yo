#ifndef CAN_INTERFACE_H
#define CAN_INTERFACE_H

#include <stdint.h>
#define CMD_ADD_NEW_ITEM_FROM_CAN_BUS 0x101
#define CMD_UPDATE_ENCODER_VALUE_FROM_CANBUS 0x100
#define CMD_SESOR_2_FROM_CAN_BUS 0x102
#define CMD_RUN_BT_FROM_CAN_BUS 0x123
#define MAX_ENCODER_COUNT 10000000
#define PULSE_PER_ROUND 1066
#define R 16
int setup_can(const char *ifname);
void send_can_frame(int can_sock, uint32_t id, const uint8_t *data, uint8_t len);
void receive_can_frame(int can_sock, int cliend_fd); 
extern uint16_t cmd_from_can_bus;
extern uint8_t flag_on_sensor2_signal;
extern float value;
extern uint32_t counted_encoder_pulse;
extern int can_fd;
extern uint32_t encoder_now;   // giá trị hiện tại (giả sử được cập nhật bởi ISR hoặc polling)
extern uint32_t encoder_last;  // giá trị lần trước (cập nhật mỗi 10ms)
extern int32_t encoder_delta;  // số xung đi được trong 10ms
#endif
