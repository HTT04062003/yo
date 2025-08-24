#ifndef COMAND_LINE_H
#define COMAND_LINE_H
//
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
//
#define UPDATE_DATA 0xFF
#define COMMAND_NO_OP 0
#define COMMAND_CONNECT_FROM_MASTER 1
#define RESPONSE_UPDATE_DATA_FROM_SLAVE 2
#define RESPONSE_MOVE_Z_PLT 4
#define RESPONSE_MOVE_THETA3_CPLT 5
#define COMAND_SET_SERVO 3
#define COMAND_MOVE_X 23
#define COMAND_MOVE_Y 24
#define COMAND_MOVE_Z 25
#define COMAND_MOVE_THETA1 26
#define COMAND_MOVE_THETA2 27
#define COMAND_MOVE_THETA3 28
#define COMAND_MOVE_D4 29
#define COMAND_JOGGING_X_UP 30
#define COMAND_JOGGING_X_DOWN 31
#define COMAND_JOGGING_Y_UP 32
#define COMAND_JOGGING_Y_DOWN 33
#define COMAND_JOGGING_Z_UP 34
#define COMAND_JOGGING_Z_DOWN 35
#define COMMAND_JOGGING_THETA1_UP 36
#define COMMAND_JOGGING_THETA1_DOWN 37
#define COMMAND_JOGGING_THETA2_UP 38
#define COMMAND_JOGGING_THETA2_DOWN 39
#define COMMAND_JOGGING_THETA3_UP 40
#define COMMAND_JOGGING_THETA3_DOWN 41
#define COMMAND_JOGGING_THETA4_UP 42
#define COMMAND_JOGGING_THETA4_DOWN 43
#define COMMAND_SERVO_ON 44
#define COMMAND_SERVO_OFF 45
#define COMMAND_AUTO_HOME 46
#define COMMAND_WAIT_FOR_JOGGING 47
#define COMMAND_WAIT_FOR_NEXT_CMD 48
#define COMMAND_MOVE_TO_POINT 50
#define COMMAND_VAL_ON 51
#define COMMAND_VAL_OFF 52
extern const char* cmd_auto_home;
extern const char* cmd_move_x_down;
extern const char* cmd_move_x_up;
extern const char* cmd_move_y_up;
extern const char* cmd_move_y_down;
extern const char* cmd_move_z_up;
extern const char* cmd_move_z_down;
extern const char* cmd_jogging_theta1_up;
extern const char* cmd_jogging_theta1_down;
extern const char* cmd_jogging_theta2_up;
extern const char* cmd_jogging_theta2_down;
extern const char* cmd_jogging_theta3_up;
extern const char* cmd_jogging_theta3_down;
extern const char* cmd_jogging_theta4_up;
extern const char* cmd_jogging_theta4_down;
extern const char* cmd_val_on;
extern const char* cmd_val_off;
extern const char* cmd_update_data_to_app ;
extern const char* cmd_add_new_item_to_app;
extern uint8_t CMD_FROM_APP;
extern uint8_t RESPONSE_FROM_APP;
extern uint8_t select_id;
uint8_t readComand_From_App(char *lineBuffer);
#endif