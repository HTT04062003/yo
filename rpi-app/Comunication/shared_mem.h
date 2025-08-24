#ifndef SHARED_MEM_H
#define SHARED_MEM_H

typedef struct {
    float cur_x, cur_y, cur_z;
    float cur_Theta1, cur_Theta2, cur_Theta3, cur_Theta4;
    float F1, F2, F3, F4;
    float curE;
}SharedData;

int init_shared_memory();
void update_shared_data(const SharedData *new_data);
void cleanup_shared_memory();

extern SharedData *shared_xyz;
extern int shm_fd;
#endif