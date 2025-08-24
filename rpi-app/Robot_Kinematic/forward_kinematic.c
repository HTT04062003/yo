#include "forward_kinematic.h"
#include <math.h>

/*
	*@:Forward Kinematic 
 */
void Scara_Robot_Forward_Kinematics(Scara_Robot_Handle *Scara_Robot_Handler){
	Scara_Robot_Handler->Current_EndPoint_Position.CurX = L1*cos(Scara_Robot_Handler->Current_Revolute.CurTheta1) + L2*cos(Scara_Robot_Handler->Current_Revolute.CurTheta1 + Scara_Robot_Handler->Current_Revolute.CurTheta2);
	Scara_Robot_Handler->Current_EndPoint_Position.CurY = L1*sin(Scara_Robot_Handler->Current_Revolute.CurTheta1) + L2*sin(Scara_Robot_Handler->Current_Revolute.CurTheta1 + Scara_Robot_Handler->Current_Revolute.CurTheta2);
	Scara_Robot_Handler->Current_EndPoint_Position.CurZ = d0 - Scara_Robot_Handler->Current_Revolute.CurD4;
	Scara_Robot_Handler->Current_Revolute.curE = Scara_Robot_Handler->Current_Revolute.CurTheta1 + Scara_Robot_Handler->Current_Revolute.CurTheta2 + Scara_Robot_Handler->Current_Revolute.CurTheta3;
//	Scara_Robot_Handler->Set_EndPoint_Position.SetX = Scara_Robot_Handler->Current_EndPoint_Position.CurX;
//	Scara_Robot_Handler->Set_EndPoint_Position.SetY = Scara_Robot_Handler->Current_EndPoint_Position.CurY;
//	Scara_Robot_Handler->Set_EndPoint_Position.SetZ = Scara_Robot_Handler->Current_EndPoint_Position.CurZ;
}
