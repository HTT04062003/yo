#include "thread.h"
#include <unistd.h>
#include <stdio.h>
#include "../Robot_Kinematic/scara_robot_parameter.h"
#include "../Robot_Kinematic/path_linear_interpolation.h"
#include "../Robot_Kinematic/p2p_interpolation.h"
#include "my_usb_serial.h"
int robot_status = 0;
pthread_mutex_t status_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t scara_param_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_t linear_interpolation_thread;
pthread_t p2p_interpolation_thread;
pthread_t monitor_thread;
pthread_mutex_t linear_interp_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t p2p_interp_mutex = PTHREAD_MUTEX_INITIALIZER;
int p2p_interpolation_running = 0;
int linear_interpolation_running = 0;
// Cờ và thread kiểm tra biến
int trigger_flag = 0;
pthread_mutex_t trigger_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_t trigger_thread;
uint8_t interpolation_status = 0;
/********** Interpolation Thread Function **********/
void* p2p_interpolation_thread_func(void *arg) {
    printf("[ P2p Interpolation] Thread started\n");
    pthread_mutex_lock(&p2p_interp_mutex);
    p2p_interpolation_running = 1;
    interpolation_status = STATUS_P2P_INTERPOLATION_NOT_CPLT;
    pthread_mutex_unlock(&p2p_interp_mutex);

    pthread_mutex_lock(&status_mutex);
    robot_status = 1;  // Đang chạy
    pthread_mutex_unlock(&status_mutex);

    pthread_mutex_lock(&scara_param_mutex);
    //generate_scurve_profile(&SCARA_ROBOT_PARAMETER, &SCURVE_PROFILE);
    Trajectory_Planing(&SCARA_ROBOT_PARAMETER, &CUBIC_EQUATION);
    pthread_mutex_unlock(&scara_param_mutex);

    pthread_mutex_lock(&status_mutex);
    robot_status = 0;  // Đã hoàn thành
    pthread_mutex_unlock(&status_mutex);

    pthread_mutex_lock(&p2p_interp_mutex);
    p2p_interpolation_running = 0;
    interpolation_status = STATUS_P2P_INTERPOLATION_CLPT;
    pthread_mutex_unlock(&p2p_interp_mutex);

    printf("[P2p Interpolation] Thread ended\n");
    return NULL;
}

void* linear_interpolation_thread_func(void *arg) {
    printf("[Linear Interpolation] Thread started\n");
    pthread_mutex_lock(&linear_interp_mutex);
    linear_interpolation_running = 1;
    interpolation_status = STATUS_LINEAR_INTERPOLATION_NOT_CPLT;
    pthread_mutex_unlock(&linear_interp_mutex);

    pthread_mutex_lock(&status_mutex);
    robot_status = 1;  // Đang chạy
    pthread_mutex_unlock(&status_mutex);

    pthread_mutex_lock(&scara_param_mutex);
    //generate_scurve_profile(&SCARA_ROBOT_PARAMETER, &SCURVE_PROFILE);
    Trajectory_Planing(&SCARA_ROBOT_PARAMETER, &CUBIC_EQUATION);
    pthread_mutex_unlock(&scara_param_mutex);

    pthread_mutex_lock(&status_mutex);
    robot_status = 0;  // Đã hoàn thành
    pthread_mutex_unlock(&status_mutex);

    pthread_mutex_lock(&linear_interp_mutex);
    linear_interpolation_running = 0;
    interpolation_status = STATUS_LINEAR_INTERPOLATION_CPLT;
    pthread_mutex_unlock(&linear_interp_mutex);

    printf("[ Linear Interpolation] Thread ended\n");
    return NULL;
}
/********** Monitor Thread Function **********/
void* monitor_status_thread_func(void *arg) {
    int last_status = -1;
    while (1) {
        pthread_mutex_lock(&status_mutex);
        int current_status = robot_status;
        pthread_mutex_unlock(&status_mutex);
        
        if (current_status == STATUS_MOVE_TO_PICK_POINT) {
            pthread_mutex_lock(&linear_interp_mutex);
            if (!linear_interpolation_running) {
                pthread_create(&linear_interpolation_thread, NULL, linear_interpolation_thread_func, NULL);
            }
        
            pthread_mutex_unlock(&linear_interp_mutex);
            
        }
        else if(current_status == STATUS_MOVE_TO_WAWEHOUSE){
            pthread_mutex_lock(&linear_interp_mutex);
            if (!linear_interpolation_running) {
                pthread_create(&linear_interpolation_thread, NULL, linear_interpolation_thread_func, NULL);
            }
            pthread_mutex_unlock(&linear_interp_mutex);
        }
        if(interpolation_status == STATUS_LINEAR_INTERPOLATION_CPLT){
            printf("OK\n");
            
            interpolation_status = STATUS_NO_INTERPOLATION;
        }
        
    }
    return NULL;
}

/********** Trigger Thread Function **********/
void* trigger_thread_func(void *arg) {
    while (1) {
        pthread_mutex_lock(&trigger_mutex);
        if (trigger_flag) {
            trigger_flag = 0;
            pthread_mutex_unlock(&trigger_mutex);

            // Hành động khi cờ được bật
            printf("[Trigger] Đã phát hiện cờ. Thực hiện hành động!\n");

            // Ví dụ: gửi lệnh đến vi điều khiển
            // float data[8] = {0};
            // send_float_packet(serial_fd, CMD_TRIGGER_ACTION, data);
        } else {
            pthread_mutex_unlock(&trigger_mutex);
        }
        usleep(50000); // 50ms
    }
    return NULL;
}
