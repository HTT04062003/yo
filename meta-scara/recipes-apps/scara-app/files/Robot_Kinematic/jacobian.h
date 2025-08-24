#ifndef JACOBIAN_H
#define JACOBIAN_H

void compute_joint_velocities(
    float theta1, float theta2,
    float vx, float vy,
    float theta1_dot_old, float theta2_dot_old, float theta3_dot_old,
    float* q1_dot_out, float* q2_dot_out, float* q3_dot_out);
#endif