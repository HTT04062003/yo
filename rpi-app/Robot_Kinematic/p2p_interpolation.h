#ifndef P2P_INTERPOLATION_H
#define P2P_INTERPOLATION_H
#include "scara_robot_parameter.h"
typedef struct{
	float a3;
	float a2;
	float a1;
	float a0;
	float Velocity_Max;
	float Accelerity_Max;
	float Current_Velocity;
	}cubic_equation_Parameter;
typedef struct{
	cubic_equation_Parameter Axis_Theta1;
	cubic_equation_Parameter Axis_Theta2;
	cubic_equation_Parameter Axis_Theta3;
	cubic_equation_Parameter Axis_D4;
	cubic_equation_Parameter End_Points;
	float  t_f;
	float t;
}Point_To_Point_Interpolation_Parameter_TypeDef;
void Trajectory_Planing(Scara_Robot_Handle *Scara_Robot_Handler, Point_To_Point_Interpolation_Parameter_TypeDef *cubic_equation);
void MOVE_EndPoint_P2P_Interpolation_With_Cubic_Trajectory_Planning(Scara_Robot_Handle *Scara_Robot_Handler, Point_To_Point_Interpolation_Parameter_TypeDef *cubic_equation, float setX, float setY, float setZ);
void Test();
extern Point_To_Point_Interpolation_Parameter_TypeDef CUBIC_EQUATION;

#endif