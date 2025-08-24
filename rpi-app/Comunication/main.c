#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>
#include "my_usb_serial.h"
#include "can_interface.h"
#include "shared_mem.h"
#include "socket_server.h"
#include "comand_line.h"
#include "../Robot_Kinematic/inverse_kinematic.h"
#include "../Robot_Kinematic/jacobian.h"
#include "../Robot_Kinematic/nano_sleep.h"
#include "../Robot_Kinematic/p2p_interpolation.h"
#include "../Robot_Kinematic/path_linear_interpolation.h"
#include "../Robot_Kinematic/scara_robot_parameter.h"
#include "queue.h"
#include "thread.h"
#define MAX_BUF 1024
#define PORT 12345


/********** Private Variables ******************/
int client_fd = -1;
int max_fd;


fd_set read_fds;


/********** Main Function **********/
int main() {
    serial_fd = setup_serial("/dev/ttyUSB0");
    if (serial_fd < 0) {
        perror("UART init failed");
        return 1;
    }

    can_fd = setup_can("can0");
    if (can_fd < 0) {
        perror("CAN init failed");
        return 1;
    }

    shm_fd = init_shared_memory();
    if (shm_fd < 0) {
        perror("Shared memory init failed");
        return 1;
    }

    server_fd = setup_server(PORT);
    if (server_fd < 0) {
        perror("Socket server init failed");
        return 1;
    }

    // Start monitor and trigger threads
    pthread_create(&monitor_thread, NULL, monitor_status_thread_func, NULL);
    pthread_create(&trigger_thread, NULL, trigger_thread_func, NULL);

    // Init robot parameters
    printf("System ready. Waiting for data...\n");
    initQueue(&item);
    SCARA_ROBOT_PARAMETER.Current_EndPoint_Position.CurX = 400;
    SCARA_ROBOT_PARAMETER.Set_EndPoint_Position.SetX = 0;
    SCARA_ROBOT_PARAMETER.Set_EndPoint_Position.SetY = 400;
    SCARA_ROBOT_PARAMETER.state = ROBOT_STATE_IN_RANGE;

    CUBIC_EQUATION.Axis_Theta1.Accelerity_Max = 6;
    CUBIC_EQUATION.Axis_Theta1.Velocity_Max = 4.6;
    CUBIC_EQUATION.Axis_Theta2.Accelerity_Max = 6;
    CUBIC_EQUATION.Axis_Theta2.Velocity_Max = 4.6;
    CUBIC_EQUATION.Axis_Theta3.Accelerity_Max = 6;
    CUBIC_EQUATION.Axis_Theta3.Velocity_Max = 4.6;
    
    while (1) {
        FD_ZERO(&read_fds);
        FD_SET(server_fd, &read_fds);
        FD_SET(serial_fd, &read_fds);
        FD_SET(can_fd, &read_fds);
        max_fd = (serial_fd > server_fd) ? serial_fd : server_fd;
        max_fd = (can_fd > max_fd) ? can_fd : max_fd;
        if (client_fd > 0) {
            FD_SET(client_fd, &read_fds);
            if (client_fd > max_fd) max_fd = client_fd;
        }

        int ret = select(max_fd + 1, &read_fds, NULL, NULL, NULL);
        if (ret < 0) {
            perror("select");
            break;
        }

        if (FD_ISSET(server_fd, &read_fds)) {
            client_fd = accept(server_fd, NULL, NULL);
            if (client_fd >= 0) {
                printf("Client đã kết nối.\n");
            }
        }

        if (client_fd > 0 && FD_ISSET(client_fd, &read_fds)) {
            char cmd_buf[BUF_SIZE];
            int n = read(client_fd, cmd_buf, BUF_SIZE - 1);
            if (n <= 0) {
                close(client_fd);
                client_fd = -1;
                printf("Client đã ngắt kết nối.\n");
            } else {
                cmd_buf[n] = '\0';
                serial_send_string(serial_fd, cmd_buf);
                CMD_FROM_APP = readComand_From_App(cmd_buf);
            }
        }

        if (FD_ISSET(serial_fd, &read_fds)) {
            if (serial_buf_len < BUF_SIZE - 1) {
                int rx_len = read(serial_fd, serial_buf + serial_buf_len, BUF_SIZE - 1 - serial_buf_len);
                if (rx_len > 0) {
                    serial_buf_len += rx_len;

                    // Đảm bảo vẫn trong giới hạn
                    if (serial_buf_len < BUF_SIZE)
                        serial_buf[serial_buf_len] = '\0';
                    else {
                        serial_buf[BUF_SIZE - 1] = '\0'; // ép null terminate
                        serial_buf_len = BUF_SIZE - 1;   // giới hạn lại
                    }

                    char *newline = strchr((const char *)serial_buf, '\n');
                    if (newline) {
                        *newline = '\0';

                        if (parse_data((const char *)serial_buf) == UPDATE_DATA) {
                            //printf("Parsed: X=%.1f, Y=%.1f, Z=%.1f\n", shared_xyz->cur_x, shared_xyz->cur_y, shared_xyz->cur_z);
                            if (!is_sending && client_fd > 0) {
                                    send_all(client_fd, cmd_update_data_to_app, strlen(cmd_update_data_to_app));
                                }
                        } else {
                            printf("Serial: %s\n", serial_buf);
                        }

                        serial_buf_len = 0;
                        memset(serial_buf, 0, BUF_SIZE);
                    }
                }
            }
            else {
                fprintf(stderr, "Buffer overflow risk. Flushing serial_buf\n");
                serial_buf_len = 0;
                memset(serial_buf, 0, BUF_SIZE);
            }
        }

        if (FD_ISSET(can_fd, &read_fds)) {
            receive_can_frame(can_fd, client_fd);
            if (cmd_from_can_bus == CMD_ADD_NEW_ITEM_FROM_CAN_BUS) {
                
            }
        }
    }

    if (client_fd > 0) close(client_fd);
    close(serial_fd);
    close(server_fd);
    close(can_fd);
    cleanup_shared_memory();

    return 0;
}
