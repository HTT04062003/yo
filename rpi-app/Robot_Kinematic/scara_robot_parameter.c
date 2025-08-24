#include "scara_robot_parameter.h"
/************************************Private Variable**************************************/
Scara_Robot_Handle SCARA_ROBOT_PARAMETER = {0};

uint8_t HOMING_MODE_THETA1 = MOTION_MODE_INITIAL;
uint8_t HOMING_MODE_THETA2 = MOTION_MODE_INITIAL;
uint8_t HOMING_MODE_THETA3 = MOTION_MODE_INITIAL;
uint8_t HOMING_MODE_D4 = MOTION_MODE_INITIAL;
uint8_t HOMING_MODE = HOMMING_STATE_NOT_CPLETE;
uint8_t MOTION_MODE = MOTION_MODE_NO_OP;

Point Table_Point[NUM_OF_POINTS] = {0};
uint32_t point_count = 0;