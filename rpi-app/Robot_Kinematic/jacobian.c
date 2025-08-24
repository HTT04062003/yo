#include "jacobian.h"
#include <math.h>
#include <stdio.h>
#include <stdbool.h>

#define EPSILON 1e-6

// Các thông số cơ khí robot SCARA
float L1 = 225.0f;  // chiều dài tay 1
float L2 = 175.0f;  // chiều dài tay 2

// Hàm tính tốc độ khớp từ vận tốc đầu công cụ
void compute_joint_velocities(
    float theta1, float theta2,
    float vx, float vy,
    float theta1_dot_old, float theta2_dot_old, float theta3_dot_old,
    float* q1_dot_out, float* q2_dot_out, float* q3_dot_out)
{
    float s1 = sinf(theta1);
    float c1 = cosf(theta1);
    float s12 = sinf(theta1 + theta2);
    float c12 = cosf(theta1 + theta2);

    // Ma trận Jacobian
    float J11 = -L1 * s1 - L2 * s12;
    float J12 = -L2 * s12;
    float J21 =  L1 * c1 + L2 * c12;
    float J22 =  L2 * c12;

    // Định thức
    float det_J = J11 * J22 - J12 * J21;

    if (fabsf(det_J) < EPSILON || isnan(det_J))
    {
        //printf("[Warning] Singularity detected! theta1=%.3f, theta2=%.3f, det_J=%.6f\n", theta1, theta2, det_J);
        //printf("          Using previous joint velocities.\n");
        *q1_dot_out = theta1_dot_old;
        *q2_dot_out = theta2_dot_old;
        *q3_dot_out = theta3_dot_old;
        return;
    }

    // Nghịch đảo ma trận Jacobian 2x2
    float invJ11 =  J22 / det_J;
    float invJ12 = -J12 / det_J;
    float invJ21 = -J21 / det_J;
    float invJ22 =  J11 / det_J;

    // Tính tốc độ khớp
    float q1_dot = invJ11 * vx + invJ12 * vy;
    float q2_dot = invJ21 * vx + invJ22 * vy;
    float q3_dot = -(q1_dot + q2_dot); // Nếu q3 là khớp quay phụ thuộc

    // Gán kết quả ra ngoài
    *q1_dot_out = q1_dot;
    *q2_dot_out = q2_dot;
    *q3_dot_out = q3_dot;
}
