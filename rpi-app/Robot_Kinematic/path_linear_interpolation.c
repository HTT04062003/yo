#include "path_linear_interpolation.h"
#include <math.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include "nano_sleep.h"
#include "inverse_kinematic.h"
#include "jacobian.h"
#include "../Comunication/my_usb_serial.h"
#include "../Comunication/comand_line.h"
#include "../Comunication/thread.h"
#include <unistd.h>  // cần thiết cho usleep
sign profile_sign;
#define pi 3.1428
#define DT 0.01 //10ms
#define PATH_LINEAR_INTERPOLATION_PERIOD_NS 10000000L  // 10ms = 10,000,000 ns
SCurveProfile SCURVE_PROFILE = {0};
void  calc_Distance(Scara_Robot_Handle *Scara_Robot_Handler, SCurveProfile *profile){
	float q_max;
	profile->x_sign = (Scara_Robot_Handler->Set_EndPoint_Position.SetX >= Scara_Robot_Handler->Current_EndPoint_Position.CurX) ? 1 : -1;
    profile->y_sign = (Scara_Robot_Handler->Set_EndPoint_Position.SetY >= Scara_Robot_Handler->Current_EndPoint_Position.CurY) ? 1 : -1;
    profile->z_sign = (Scara_Robot_Handler->Set_EndPoint_Position.SetZ >= Scara_Robot_Handler->Current_EndPoint_Position.CurZ) ? 1 : -1;
    float dx = Scara_Robot_Handler->Set_EndPoint_Position.SetX - Scara_Robot_Handler->Current_EndPoint_Position.CurX;
    float dy = Scara_Robot_Handler->Set_EndPoint_Position.SetY - Scara_Robot_Handler->Current_EndPoint_Position.CurY;
    float dz = Scara_Robot_Handler->Set_EndPoint_Position.SetZ - Scara_Robot_Handler->Current_EndPoint_Position.CurZ;
	
	q_max = sqrt(dx*dx + dy*dy + dz*dz);
	profile->q_max = q_max;
	profile->Num_Of_Points = profile->q_max/PATH_LINEAR_RESOLUTION;
	}
// Tính quãng du?ng cho profile S-curve
float calc_scurve_time(SCurveProfile *profile) {
   if(profile->v_max >= sqrt(profile->q_max * profile->a_max/2.0)) profile->v_max = sqrt(profile->q_max * profile->a_max/2.0);
	profile->t1 = profile->v_max/profile->a_max;
	profile->t2 = 2 * profile->t1;
	profile->t3 = profile->q_max/profile->v_max;
	profile->t4 = profile->t3 + profile->t1;
	profile->te =  profile->t3 + profile->t2;
	profile->jerk = profile->a_max/profile->t1;
	
}
void calc_3d_vector(Scara_Robot_Handle *Scara_Robot_Handler, SCurveProfile *profile) {
    float p_x = Scara_Robot_Handler->Set_EndPoint_Position.SetX;
    float p_y = Scara_Robot_Handler->Set_EndPoint_Position.SetY;
    float p_z = Scara_Robot_Handler->Set_EndPoint_Position.SetZ;
    float p_x_old = Scara_Robot_Handler->Current_EndPoint_Position.CurX;
    float p_y_old = Scara_Robot_Handler->Current_EndPoint_Position.CurY;
    float p_z_old = Scara_Robot_Handler->Current_EndPoint_Position.CurZ;

    float dx = p_x - p_x_old;
    float dy = p_y - p_y_old;
    float dz = p_z - p_z_old;

    // Góc alpha: hướng trong mặt phẳng XY
    profile->alpha = atan2f(dy, dx);  // an toàn với dx = 0

    // Độ dài chiếu vector chuyển động lên mặt phẳng XY
    float planar_length = sqrtf(dx * dx + dy * dy);

    // Góc beta: hướng so với mặt phẳng XY (theo phương Z)
    profile->beta = atan2f(planar_length, dz);  // không cần cộng pi
}
uint8_t generate_scurve_profile(Scara_Robot_Handle *Scara_Robot_Handler, SCurveProfile *profile) {
    profile->a_max = 250;
	profile->v_max = 250;
	calc_Distance(Scara_Robot_Handler, profile);
	calc_3d_vector(Scara_Robot_Handler, profile);
	
	calc_scurve_time(profile);
	//printf("Te = %f, Q_max = %f\n", profile->te, profile->q_max);
	profile->dt = DT;
	float sin_alpha = sin(fabs(profile->alpha));
	float cos_alpha = cos(profile->alpha);
	float sin_beta = sin(profile->beta);
	float cos_beta = cos(profile->beta);
	float q_x_old = Scara_Robot_Handler->Current_EndPoint_Position.CurX;
	float q_y_old = Scara_Robot_Handler->Current_EndPoint_Position.CurY;
	float q_z_old = Scara_Robot_Handler->Current_EndPoint_Position.CurZ;
	float e_old = Scara_Robot_Handler->Set_Revolute.E;
	Scara_Robot_Handler->Set_Revolute.E = Scara_Robot_Handler->Current_Revolute.curE;
	float t = 0.0f;
	float q = 0;
	float q_dot = 0;
	float q_2dot = 0;
    float q_x;
	float q_y;
	float q_z;
    float q_x_dot;
    float q_y_dot;
    float q_z_dot;
	float q1_dot;
	float q2_dot;
	float q3_dot;
    float theta1_dot_old = 0;
    float theta2_dot_old = 0;
    float theta3_dot_old = 0;
	float tmp1 = profile->t1 * profile->t1 * profile->t1;//t1^3
	float tmp2 = profile->t1 * profile->t1;//t1^2
	float tmp3 = profile->jerk * tmp1; // jerk*t1^3
	float tmp4 = profile->jerk * tmp2; // jerk*t1^2
	float tmp5 = profile->a_max * tmp2; // a_max * t1^2
	float tmp6 = profile->v_max * (profile->t3 - profile->t2); // v_max*(t3 - t2)
	float tmp7 = profile->jerk * (profile->t4 - profile->t3)*(profile->t4 - profile->t3)/2;
	SCARA_ROBOT_PARAMETER.state = ROBOT_STATE_BUSY;
	float data[8];
	while(t <= profile->te){
		struct timespec t_start, t_end;
        clock_gettime(CLOCK_MONOTONIC, &t_start);
		if( t <= profile->t1){
			q = profile->jerk * t*t*t / 6;
			q_dot = profile->jerk * t*t / 2;
			q_2dot = profile->jerk * t;
			}
		else if( t <= profile->t2){
			q = tmp3/6 + tmp4/2 * (t - profile->t1)
			    + profile->a_max * (t - profile->t1)*(t - profile->t1)/2
			    - profile->jerk * (t - profile->t1)*(t - profile->t1)*(t - profile->t1) / 6;
			q_dot = tmp4/2 + profile->a_max * (t - profile->t1)
			        - profile->jerk * (t - profile->t1)*(t - profile->t1) / 2;
			q_2dot = profile->a_max - profile->jerk * (t - profile->t1);
			}
	  else if(t <= profile->t3){
		  q = tmp5 + profile->v_max * (t - profile->t2);
			q_dot = profile->v_max;
			q_2dot = 0;
		}
		else if(t <= profile->t4){
			q = tmp5 + tmp6 + profile->v_max * (t - profile->t3)
			    - profile->jerk * (t - profile->t3)*(t - profile->t3)*(t - profile->t3) / 6;
			q_dot = profile->v_max - profile->jerk * (t - profile->t3)*(t - profile->t3) / 2;
			q_2dot = -profile->jerk * (t - profile->t3);
			}
		else if(t <= profile->te){
			q = profile->q_max - profile->jerk * (profile->te- t)*(profile->te- t)*(profile->te- t) / 6;
			q_dot = profile->v_max - tmp7 - profile->a_max * (t - profile->t4)
			        + profile->jerk * (t - profile->t4)*(t - profile->t4) / 2;
			q_2dot = -profile->a_max + profile->jerk * (t - profile->t4);
			}
        //
		q_x = q_x_old + profile->x_sign * q * sin_beta * fabs(cos_alpha);
		q_y = q_y_old + profile->y_sign * q * sin_beta * sin_alpha;
        q_z = q_z_old + profile->z_sign * q * fabs(cos_beta);
        //
        q_x_dot = profile->x_sign * q_dot * sin_beta * fabs(cos_alpha);
        q_y_dot = profile->y_sign * q_dot * sin_beta * sin_alpha;
        q_z_dot = profile->z_sign * q_dot * fabs(cos_beta);
        //
		SCARA_ROBOT_PARAMETER.Set_EndPoint_Position.SetX = q_x;
		SCARA_ROBOT_PARAMETER.Set_EndPoint_Position.SetY = q_y;
		SCARA_ROBOT_PARAMETER.Set_EndPoint_Position.SetZ = q_z;
        Scara_Robot_Invert_Kinematics(Scara_Robot_Handler);
        compute_joint_velocities(Scara_Robot_Handler->Set_Revolute.SetTheta1, Scara_Robot_Handler->Set_Revolute.SetTheta2, q_x_dot, q_x_dot, theta1_dot_old, theta2_dot_old, theta3_dot_old, &q1_dot, &q2_dot, &q3_dot);
	    theta1_dot_old = q1_dot;
		theta2_dot_old = q2_dot;
		theta3_dot_old = q3_dot;
		//Send To Slave
		if(SCARA_ROBOT_PARAMETER.state == ROBOT_STATE_OUT_OF_RANGE){
           return PATH_LINEAR_INTERPOLATION_NOT_CPLT;
		}
        
        data[0] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta1;
        data[1] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta2;
        data[2] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta3;
        data[3] = SCARA_ROBOT_PARAMETER.Set_Revolute.SetD4;
        data[4] = q1_dot;
        data[5] = q2_dot ;
        data[6] = q3_dot;
        data[7] = q_z_dot*60;
        send_float_packet(serial_fd, COMAND_SET_SERVO,data);
        clock_gettime(CLOCK_MONOTONIC, &t_end);

        long elapsed_ns = diff_ns(t_start, t_end);
        long remaining_ns = PATH_LINEAR_INTERPOLATION_PERIOD_NS - elapsed_ns;
        precise_delay(remaining_ns);
        //printf("X=%f,Y=%f,Z=%f,T1=%f,T2=%f,T3=%f,D4=%f,O1=%f,O2=%f, O3=%f\n",
		//         q_x, q_y, q_z,
		//		 SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta1,
		//		 SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta2,
		//		 SCARA_ROBOT_PARAMETER.Set_Revolute.SetTheta3,
		//		 q_z,
		//		 q1_dot, q2_dot, q3_dot
		 //        );
		t+= profile->dt;
	 }
	usleep(50000);
	Scara_Robot_Handler->Set_Revolute.E = e_old;
	Scara_Robot_Invert_Kinematics(Scara_Robot_Handler);
    data[2] = Scara_Robot_Handler->Set_Revolute.SetTheta3;
	data[6] = 1.0;
	send_float_packet(serial_fd, COMAND_MOVE_THETA3, data);
    printf("DONE\n");
	
	SCARA_ROBOT_PARAMETER.state = ROBOT_STATE_READY;
	return PATH_LINEAR_INTERPOLATION_CPLT;
}