#include "p2p_interpolation.h"
#include <math.h>
#include <stdint.h>
#include "../Comunication/my_usb_serial.h"
#include <termios.h>
#include <time.h>
#include <errno.h>
#include "nano_sleep.h"
#include "inverse_kinematic.h"
#include "../Comunication/comand_line.h"
/******************************************************************8***** */
#define FRAME_SIZE 32
#define P2P_INTERPOLATION_PERIOD_NS 10000000L  // 10ms = 10,000,000 ns
/*******Private Variable************* */
Point_To_Point_Interpolation_Parameter_TypeDef CUBIC_EQUATION = {0};
/************************************ */

void Calculating_Cubic_Equation_Parameter(Point_To_Point_Interpolation_Parameter_TypeDef *cubic_equation, Scara_Robot_Handle *Scara_Robot_Handler)
{
    float T[4] = {0};  // T1, T2, T3
    float delta[4];
    float vmax[3], amax[3];
    float tmp1, tmp2;
    
    // Tính chênh l?ch góc/d?ch chuy?n c?a 4 tr?c
    delta[0] = fabs(Scara_Robot_Handler->Set_Revolute.SetTheta1 - Scara_Robot_Handler->Current_Revolute.CurTheta1);
    delta[1] = fabs(Scara_Robot_Handler->Set_Revolute.SetTheta2 - Scara_Robot_Handler->Current_Revolute.CurTheta2);
    delta[2] = fabs(Scara_Robot_Handler->Set_Revolute.SetTheta3 - Scara_Robot_Handler->Current_Revolute.CurTheta3);
    //delta[3] = fabs(Scara_Robot_Handler->Set_Revolute.SetD4      - Scara_Robot_Handler->Current_Revolute.CurD4);

    // Trích xu?t t?c d? & gia t?c t?i da t? c?u trúc
    vmax[0] = cubic_equation->Axis_Theta1.Velocity_Max;
    vmax[1] = cubic_equation->Axis_Theta2.Velocity_Max;
    vmax[2] = cubic_equation->Axis_Theta3.Velocity_Max;
    //vmax[3] = cubic_equation->Axis_D4.Velocity_Max;

    amax[0] = cubic_equation->Axis_Theta1.Accelerity_Max;
    amax[1] = cubic_equation->Axis_Theta2.Accelerity_Max;
    amax[2] = cubic_equation->Axis_Theta3.Accelerity_Max;
    //amax[3] = cubic_equation->Axis_D4.Accelerity_Max;

    // Tính th?i gian cho t?ng tr?c
    for (int i = 0; i < 3; ++i) {
        if (vmax[i] > 0.0f)
            tmp1 = (3.0f * delta[i]) / (2.0f * vmax[i]);
        else
            tmp1 = 0.0f;

        if (amax[i] > 0.0f)
            tmp2 = sqrtf((6.0f * delta[i]) / amax[i]);
        else
            tmp2 = 0.0f;

        T[i] = fmaxf(tmp1, tmp2);
    }

    // L?y th?i gian l?n nh?t d? d?ng b? chuy?n d?ng
    cubic_equation->t_f = fmaxf(fmaxf(T[0], T[1]), fmaxf(T[2], T[3]));

    // N?u t_f quá nh? thì gán t?i thi?u d? tránh chia 0
    if (cubic_equation->t_f < 1e-6f)
        cubic_equation->t_f = 1e-6f;

    // Macro cho tính toán h? s? n?i suy
    #define CALC_CUBIC_COEFF(axis, cur, set) \
        cubic_equation->axis.a0 = cur; \
        cubic_equation->axis.a1 = 0.0f; /* v_i = 0 */ \
        cubic_equation->axis.a2 = (3.0f * (set - cur)) / (cubic_equation->t_f * cubic_equation->t_f); \
        cubic_equation->axis.a3 = (-2.0f * (set - cur)) / (cubic_equation->t_f * cubic_equation->t_f * cubic_equation->t_f)

    // Gán h? s? cho t?ng tr?c
    CALC_CUBIC_COEFF(Axis_Theta1, Scara_Robot_Handler->Current_Revolute.CurTheta1, Scara_Robot_Handler->Set_Revolute.SetTheta1);
    CALC_CUBIC_COEFF(Axis_Theta2, Scara_Robot_Handler->Current_Revolute.CurTheta2, Scara_Robot_Handler->Set_Revolute.SetTheta2);
    CALC_CUBIC_COEFF(Axis_Theta3, Scara_Robot_Handler->Current_Revolute.CurTheta3, Scara_Robot_Handler->Set_Revolute.SetTheta3);
    //CALC_CUBIC_COEFF(Axis_D4,      Scara_Robot_Handler->Current_Revolute.CurD4,      Scara_Robot_Handler->Set_Revolute.SetD4);

    #undef CALC_CUBIC_COEFF
}
//
float Update_Revolute( cubic_equation_Parameter * cubic_equation, float t){
	return (cubic_equation->a0 + (cubic_equation->a1 * t) + (cubic_equation->a2 * t * t) + (cubic_equation->a3 * t * t * t));
}
//
float Update_Axis_Velocity( cubic_equation_Parameter * cubic_equation, float t){
	return (cubic_equation->a1 + (2.0 * cubic_equation->a2 * t) + ( 3.0 * cubic_equation->a3 * t * t));
}

void Trajectory_Planing(Scara_Robot_Handle *Scara_Robot_Handler, Point_To_Point_Interpolation_Parameter_TypeDef *cubic_equation){
	uint8_t DIR1 = 0;
	uint8_t DIR2 = 0;
	uint8_t DIR3 = 0;
	uint8_t DIR4  =0;
	float t1 = 0;
	float t2 = 0;
	float t3 = 0;
	float d4 = 0;
    Scara_Robot_Invert_Kinematics(Scara_Robot_Handler);
	if(Scara_Robot_Handler->Set_Revolute.SetTheta1 > Scara_Robot_Handler->Current_Revolute.CurTheta1)DIR1 = 1;
	if(Scara_Robot_Handler->Set_Revolute.SetTheta2 > Scara_Robot_Handler->Current_Revolute.CurTheta2)DIR2 = 1;
	cubic_equation->t = 0.0;
	Calculating_Cubic_Equation_Parameter(cubic_equation, Scara_Robot_Handler);
    printf("t_f = %f\n", cubic_equation->t_f);
    uint64_t cnt = 0;
	while(cubic_equation->t <= cubic_equation->t_f){
        struct timespec t_start, t_end;
        clock_gettime(CLOCK_MONOTONIC, &t_start);
        cubic_equation->t+=0.01;
		 t1 = Update_Revolute(&(cubic_equation->Axis_Theta1), cubic_equation->t);
		 if((t1 > Scara_Robot_Handler->Set_Revolute.SetTheta1) && (DIR1 == 1)) t1 = Scara_Robot_Handler->Set_Revolute.SetTheta1;
		 //
		 t2 = Update_Revolute(&(cubic_equation->Axis_Theta2), cubic_equation->t);
		 if((t2 > Scara_Robot_Handler->Set_Revolute.SetTheta2) && (DIR2 ==1)) t2 = Scara_Robot_Handler->Set_Revolute.SetTheta2;
		//
		 t3 = Update_Revolute(&(cubic_equation->Axis_Theta3), cubic_equation->t);
		 if(t3 > Scara_Robot_Handler->Set_Revolute.SetTheta3) t3 = Scara_Robot_Handler->Set_Revolute.SetTheta3;
		 
		//
		
		 cubic_equation->Axis_Theta1.Current_Velocity =  Update_Axis_Velocity(&(cubic_equation->Axis_Theta1), cubic_equation->t);
		cubic_equation->Axis_Theta2.Current_Velocity =  Update_Axis_Velocity(&(cubic_equation->Axis_Theta2), cubic_equation->t);
		cubic_equation->Axis_Theta3.Current_Velocity =  Update_Axis_Velocity(&(cubic_equation->Axis_Theta3), cubic_equation->t);
		//
        /*
		 Servo_Position_Control(&servo1, t1,  cubic_equation->Axis_Theta1.Current_Velocity);
		Servo_Position_Control(&servo2, t2,  cubic_equation->Axis_Theta2.Current_Velocity);
		Servo_Position_Control(&servo3, t3,  cubic_equation->Axis_Theta3.Current_Velocity);
		 HAL_Delay(9);
        */
        /*
        int written = write(uart_fd, data, FRAME_SIZE);
        if (written < 0) {
            perror("UART write failed");
        }

        // Đảm bảo UART đã gửi xong dữ liệu thật sự (blocking)
        tcdrain(uart_fd);
        */
       float data[8];
        data[0] = t1;
        data[1] = t2;
        data[2] = t3;
        data[3] = SCARA_ROBOT_PARAMETER.Current_Revolute.CurD4;
        data[4] = cubic_equation->Axis_Theta1.Current_Velocity;
        data[5] = cubic_equation->Axis_Theta2.Current_Velocity ;
        data[6] = cubic_equation->Axis_Theta3.Current_Velocity;
        data[7] = 0;
        send_float_packet(serial_fd, COMAND_SET_SERVO,data);
       clock_gettime(CLOCK_MONOTONIC, &t_end);

        long elapsed_ns = diff_ns(t_start, t_end);
        long remaining_ns = P2P_INTERPOLATION_PERIOD_NS - elapsed_ns;
        precise_delay(remaining_ns);
        cnt+=1;
        //printf("T1 = %f, T2 = %f, T3 = %f, F1 = %f, F2 = %f, F3 = %f, cnt = %d\n", t1, t2, t3, cubic_equation->Axis_Theta1.Current_Velocity, cubic_equation->Axis_Theta2.Current_Velocity,cubic_equation->Axis_Theta3.Current_Velocity, cnt );
	   }	
     
	}
void MOVE_EndPoint_P2P_Interpolation_With_Cubic_Trajectory_Planning(Scara_Robot_Handle *Scara_Robot_Handler, Point_To_Point_Interpolation_Parameter_TypeDef *cubic_equation, float setX, float setY, float setZ){
	Scara_Robot_Handler->Set_EndPoint_Position.SetX = setX;
	Scara_Robot_Handler->Set_EndPoint_Position.SetY = setY;
	Scara_Robot_Handler->Set_EndPoint_Position.SetZ = setZ;
	Scara_Robot_Invert_Kinematics(Scara_Robot_Handler);
	Trajectory_Planing(Scara_Robot_Handler, cubic_equation);
}
void Test(){
    uint64_t i = 0;
    while(i < 10){
        struct timespec t_start, t_end;
        clock_gettime(CLOCK_MONOTONIC, &t_start);
        float data[8];
        data[0] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta1;
        data[1] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta2;
        data[2] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta3;
        data[3] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetD4;
        data[4] = 1;
        data[5] = 1;
        data[6] = 1;
        data[7] = 1;
        send_float_packet(serial_fd, COMAND_SET_SERVO,data);
        clock_gettime(CLOCK_MONOTONIC, &t_end);

        long elapsed_ns = diff_ns(t_start, t_end);
        long remaining_ns = P2P_INTERPOLATION_PERIOD_NS - elapsed_ns;
        precise_delay(remaining_ns);
        //printf("OK\n");
        i++;
    }
}