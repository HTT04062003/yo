#ifndef PATH_LINEAR_INTERPOLATION_H
#define PATH_LINEAR_INTERPOLATION_H
#include <stdint.h>
#include "scara_robot_parameter.h"
#define MAX_POINTS 1000
#define PATH_LINEAR_RESOLUTION 0.1
#define PATH_LINEAR_INTERPOLATION_CPLT 0
#define PATH_LINEAR_INTERPOLATION_NOT_CPLT 1
typedef struct {
    float t;
    float pos;
    float vel;
    float acc;
} TrajectoryPoint;

typedef struct {
    float q0, q1;        // v? trí b?t d?u và k?t thúc
	  float q_max;
	  float alpha;
	  float beta;
    float v_max;          // v?n t?c t?i da
    float a_max;          // gia t?c t?i da
    float jerk;          // jerk 
	  float t1;
	  float t2;
	  float t3;
	  float t4;
	  float te;
    float dt;            // chu k? l?y m?u
    float total_time;    // th?i gian t?ng (s? du?c tính t? d?ng)
    int x_sign;
	  int y_sign;
	  int z_sign;
	  int revolute_sign;
	  uint32_t Num_Of_Points;
} SCurveProfile;
typedef struct{
	int x_sign;
	int y_sign;
	int z_sign;
	int revolute_sign;
	}sign;
//
uint8_t generate_scurve_profile(Scara_Robot_Handle *Scara_Robot_Handler, SCurveProfile *profile);
//
void Scur_Profile_Init(void);
//
extern SCurveProfile SCURVE_PROFILE;
extern SCurveProfile THETA3_SCURVE_PROFILE;
#endif

