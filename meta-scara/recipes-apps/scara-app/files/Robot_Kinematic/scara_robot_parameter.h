#ifndef SCARA_ROBOT_PARAMETER_H
#define SCARA_ROBOT_PARAMETER_H
#include <stdint.h>
#define INVERT_STATE_OUT_OF_RANGE 0
/************************************User Define*******************************************/
#define MOTION_MODE_NO_OP 0
#define MOTION_MODE_MOVE_X 1
#define MOTION_MODE_MOVE_Y 2
#define MOTION_MOVDE_MOVE_Z 3
#define MOTION_MODE_TRAJECTORY_PLANNING 4
#define MOTION_MODE_HOMING_THETA_1 5
#define MOTION_MODE_HOMING_THETA1_COMPLETE 9
#define MOTION_MODE_HOMING_THETA_2 6
#define MOTION_MODE_HOMING_THETA2_COMPLETE 10
#define MOTION_MODE_HOMING_THETA_3 7
#define MOTION_MODE_HOMING_THETA3_COMPLETE 11
#define MOTION_MODE_HOMING_D4 8
#define MOTION_MODE_HOMING_D4_COMPLETE 12
#define MOTION_MODE_INITIAL 13
#define HOMMING_STATE_NOT_CPLETE 14
#define HOMMING_STATE_CPLETE 15
#define ROBOT_STATE_OUT_OF_RANGE 16
#define ROBOT_STATE_IN_RANGE 17
#define ROBOT_STATE_READY 18
#define ROBOT_STATE_BUSY 19
#define THETA1_OFFSET -2.0
#define THETA2_OFFSET 2.1
#define THETA3_OFFSET -2.0
#define D4_OFFSET 20
#define THETA1_MIN -2.2689
#define THETA1_MAX 2.2689
#define THETA2_MIN -2.2689
#define THETA2_MAX 2.2689
#define D4_MAX 150
#define D4_MIN 0
#define ROBOT_RANGE_R_MAX 400
#define ROBOT_RANGE_R_MIN 130
//
#define NUM_OF_POINTS 128
#define MAX_NAME_LENGTH 10
#define ID_NOT_EXIST 0x00
#define ID_EXIST 0xFF
//
#define L1 (float)(225.0)
#define L2 (float)(175.0)
#define d0 (float)(173.1)
#define PI 3.14159265358979
#define TWO_PI (2 * PI)
#define NUM_VALUES 5000        // S? lu?ng giá tr? trong m?ng
#define START 0.0             // B?t d?u t? -1
#define END TWO_PI              // K?t thúc ? 1
#define COS_VALUE_START -1.0
#define COS_VALUE_END 1.0
#define v_f 0.0
#define v_i 0.0
//
typedef struct{
	float x;
	float y;
	float z;
	float e;
	uint8_t ID;
	}Point;
/************************************Struct Typedefine*************************************/
typedef struct{
	float CurX;
	float CurY;
	float CurZ;
	}Current_EndPoint_Position_TypeDef;
typedef struct{
	float SetX;
	float SetY;
	float SetZ;
	}Target_EndPoint_Position_TypeDef;
typedef struct{
	float CurTheta1;
	float CurTheta2;
	float CurTheta3;
	float CurD4;
	float curE;
	}Current_Revolute_Parameter_TypeDef;
typedef struct{
	float SetTheta1;
	float SetTheta2;
	float SetTheta3;
	float SetD4;
	float E;
	}Target_Revolute_Parameter_TypeDef;

typedef struct{
	Current_EndPoint_Position_TypeDef Current_EndPoint_Position;
  Current_Revolute_Parameter_TypeDef Current_Revolute;
	Target_EndPoint_Position_TypeDef Set_EndPoint_Position;
	Target_Revolute_Parameter_TypeDef Set_Revolute;
	uint8_t state;
	}Scara_Robot_Handle;
/******************************************************************************************/
extern Scara_Robot_Handle SCARA_ROBOT_PARAMETER;
//extern Point_To_Point_Interpolation_Parameter_TypeDef CUBIC_EQUATION;
extern	uint8_t HOMING_MODE_THETA1;
extern	uint8_t HOMING_MODE_THETA2;
extern	uint8_t HOMING_MODE_THETA3;
extern uint8_t HOMING_MODE_D4;
extern uint8_t MOTION_MODE;
extern uint8_t HOMING_MODE;
extern Point Table_Point[NUM_OF_POINTS];
extern	uint8_t select_id;
#endif