#include "can_interface.h"
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include "queue.h"
#include "comand_line.h"
#include "thread.h"
#include "../Robot_Kinematic/scara_robot_parameter.h"
#include "socket_server.h"
#include "my_usb_serial.h"
uint16_t cmd_from_can_bus = 0;
uint8_t flag_on_sensor2_signal = 0;
float value;
uint32_t counted_encoder_pulse;
uint32_t encoder_now;   // giá trị hiện tại (giả sử được cập nhật bởi ISR hoặc polling)
uint32_t encoder_last = 0;  // giá trị lần trước (cập nhật mỗi 10ms)
int32_t encoder_delta = 0;  // số xung đi được trong 10ms

float distance_mm = 0;
int can_fd;
int setup_can(const char *ifname) {
    int sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (sock < 0) return -1;

    struct ifreq ifr;
    struct sockaddr_can addr;
    strcpy(ifr.ifr_name, ifname);
    if (ioctl(sock, SIOCGIFINDEX, &ifr) < 0) return -1;

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) return -1;

    return sock;
}

void send_can_frame(int can_sock, uint32_t id, const uint8_t *data, uint8_t len) {
    if (len > 8) {
        fprintf(stderr, "CAN data length must be <= 8\n");
        return;
    }

    struct can_frame frame;
    memset(&frame, 0, sizeof(frame));
    frame.can_id = id;
    frame.can_dlc = len;
    memcpy(frame.data, data, len);

    int nbytes = write(can_sock, &frame, sizeof(frame));
    if (nbytes != sizeof(frame)) {
        perror("CAN send failed");
    } else {
        printf("Sent CAN frame: ID=0x%X, LEN=%d\n", frame.can_id, frame.can_dlc);
    }
}
void receive_can_frame(int can_sock, int cliend_fd) {
    struct can_frame frame;
    int nbytes = read(can_sock, &frame, sizeof(frame));

    if (nbytes > 0) {
        if(frame.can_id == CMD_UPDATE_ENCODER_VALUE_FROM_CANBUS){
            memcpy(&encoder_now, frame.data, sizeof(uint32_t));
            if (encoder_now >= encoder_last)
            {
                // Không có tràn
                encoder_delta = encoder_now - encoder_last;
            }
            else
            {
                // Tràn: encoder_now nhỏ hơn encoder_last do reset về 0
                encoder_delta = (MAX_ENCODER_COUNT - encoder_last) + encoder_now;
            }
            float offset = encoder_delta * (3.1416f * 18.0f / 1066.0f);
            updateAllDataWithOffset(&item, offset);
            //printf("Value = %f\n", offset);
            encoder_last = encoder_now; // Cập nhật lần sau
        }
        else if(frame.can_id == CMD_ADD_NEW_ITEM_FROM_CAN_BUS){
            num_of_item+=1;
           // printf("Value = %d\n", num_of_item);
            cmd_from_can_bus = CMD_ADD_NEW_ITEM_FROM_CAN_BUS;
            //enqueue(&item, num_of_item, 0, 0);
            
        }
         else if(frame.can_id == CMD_SESOR_2_FROM_CAN_BUS){
            int Num_of_Point;
            float Y;
            int ID;
            if (!is_sending && cliend_fd > 0) {
                    send_all(cliend_fd,cmd_add_new_item_to_app , strlen(cmd_add_new_item_to_app));
                }
            if(new_id >= 1 && new_id < 10){
               uint8_t tmp[24];
                sprintf((char *)tmp, "i%d\n", new_id);
                //printf(tmp);
                new_id = 10;
                serial_send_string(serial_fd, tmp);
                
            }
            
            
        }
        //memcpy(&counted_encoder_pulse, frame.data, sizeof(uint32_t));
        //printf("Value = %d\n", counted_encoder_pulse);

        
        
        //uint8_t tmp[4];
        //memcpy(tmp, &counted_encoder_pulse, sizeof(float));
        //send_can_frame(can_sock, 0x123, tmp, 4);
    }
}
