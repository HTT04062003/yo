#ifndef THREAD_H
#define THREAD_H
//
#include <pthread.h>
#include <stdint.h>
//
#define STATUS_MOVE_TO_WAWEHOUSE 1
#define STATUS_MOVE_TO_PICK_POINT 2
#define STATUS_PICK 4
#define STATUS_PLACE 5
#define STATUS_READY_TO_PICK 6
#define STATUS_READY_TO_PLACE 7
#define STATUS_LINEAR_INTERPOLATION_NOT_CPLT 0
#define STATUS_LINEAR_INTERPOLATION_CPLT 1
#define STATUS_P2P_INTERPOLATION_NOT_CPLT 0
#define STATUS_P2P_INTERPOLATION_CLPT 2
#define STATUS_NO_INTERPOLATION 3
void* p2p_interpolation_thread_func(void *arg);
void* linear_interpolation_thread_func(void *arg) ;
void* monitor_status_thread_func(void *arg);
void* trigger_thread_func(void *arg);

extern pthread_mutex_t status_mutex;
extern pthread_mutex_t scara_param_mutex;
extern pthread_mutex_t linear_interp_mutex;
extern pthread_mutex_t p2p_interp_mutex ;
extern pthread_mutex_t trigger_mutex;

extern pthread_t p2p_interpolation_thread;
extern pthread_t linear_interpolation_thread;
extern pthread_t monitor_thread;
extern pthread_t trigger_thread;

extern int linear_interpolation_running;
extern int p2p_interpolation_running;
extern int robot_status;
extern int trigger_flag;
extern uint8_t interpolation_status;
#endif
