#include "inverse_kinematic.h"
#include <math.h>

static uint8_t is_valid(float theta1, float theta2, float theta3);
static void set_angles(Scara_Robot_Handle *h, float t1, float t2, float t3);
static void Select_Angle(Scara_Robot_Handle *h,
                         float t1[2], float t2[2], float t3[2],
                         float CurTheta1, float CurTheta2, float CurTheta3
                         );

static uint8_t is_valid(float theta1, float theta2, float theta3) {
    return (theta1 >= THETA1_MIN && theta1 <= THETA1_MAX &&
            theta2 >= THETA2_MIN && theta2 <= THETA2_MAX 
            );
}

static void set_angles(Scara_Robot_Handle *h, float t1, float t2, float t3) {
    h->Set_Revolute.SetTheta1 = t1;
    h->Set_Revolute.SetTheta2 = t2;
    h->Set_Revolute.SetTheta3 = t3;
}
static void Select_Angle(Scara_Robot_Handle *h,
                         float t1[2], float t2[2], float t3[2],
                         float CurTheta1, float CurTheta2, float CurTheta3
                         ) {
    uint8_t valid_1 = is_valid(t1[0], t2[0], t3[0]);
    uint8_t valid_2 = is_valid(t1[1], t2[1], t3[1]);

    // Không nghi?m nào h?p l?
    if (!valid_1 && !valid_2){
        h->state = ROBOT_STATE_OUT_OF_RANGE;
       return;
    } 

    // Ch? nghi?m 1 h?p l?
    if (valid_1 && !valid_2) {
        h->state = ROBOT_STATE_IN_RANGE;
        set_angles(h, t1[0], t2[0], t3[0]);
        return;
    }

    // Ch? nghi?m 2 h?p l?
    if (!valid_1 && valid_2) {
        h->state = ROBOT_STATE_IN_RANGE;
        set_angles(h, t1[1], t2[1], t3[1]);
        return;
    }

    // C? hai nghi?m h?p l? -> ch?n nghi?m ít thay d?i hon
    float delta1 = fabsf(t1[0] - CurTheta1) + fabsf(t2[0] - CurTheta2) ;
    float delta2 = fabsf(t1[1] - CurTheta1) + fabsf(t2[1] - CurTheta2) ;

    uint8_t best_idx = (delta1 <= delta2) ? 0 : 1;

    set_angles(h, t1[best_idx], t2[best_idx], t3[best_idx]);
}
void Scara_Robot_Invert_Kinematics(Scara_Robot_Handle *Scara_Robot_Handler){

	float px = Scara_Robot_Handler->Set_EndPoint_Position.SetX;
    float py = Scara_Robot_Handler->Set_EndPoint_Position.SetY;
    float pz = Scara_Robot_Handler->Set_EndPoint_Position.SetZ;

    float c2, s2[2], t2[2];
    float phi, delta[2];
    float t1[2];
    float t3[2];

    // --- Tính c2 ---
    c2 = (px*px + py*py - L1*L1 - L2*L2) / (2.0f * L1 * L2);

    // Clamp c2 d? tránh sai s? float vu?t -1..1
    if (c2 > 1.0f) c2 = 1.0f;
    if (c2 < -1.0f) c2 = -1.0f;

    // --- Tính s2 ---
    s2[0] = sqrtf(1.0f - c2*c2);   // nhánh 1: elbow-up
    s2[1] = -s2[0];                // nhánh 2: elbow-down

    // --- Tính t2 ---
    t2[0] = atan2f(s2[0], c2);
    t2[1] = atan2f(s2[1], c2);

    // --- Tính phi ---
    phi = atan2f(py, px);

    // --- Tính delta, r?i tính t1 ---
    delta[0] = atan2f(L2 * s2[0], L1 + L2 * c2);
    delta[1] = atan2f(L2 * s2[1], L1 + L2 * c2);

    t1[0] = phi - delta[0];
    t1[1] = phi - delta[1];

    // --- Tính t3 (góc Z) n?u c?n ---
    t3[0] = Scara_Robot_Handler->Set_Revolute.E - (t1[0] + t2[0]);
    t3[1] = Scara_Robot_Handler->Set_Revolute.E  - (t1[1] + t2[1]);
    Scara_Robot_Handler->Set_Revolute.SetD4 = d0 - pz;
    // --- Ch?n nhánh t?i uu ---
    Select_Angle(Scara_Robot_Handler, 
                 t1, t2, t3,  
                 Scara_Robot_Handler->Current_Revolute.CurTheta1,
                 Scara_Robot_Handler->Current_Revolute.CurTheta2,
                 Scara_Robot_Handler->Current_Revolute.CurTheta3
                );
	}
