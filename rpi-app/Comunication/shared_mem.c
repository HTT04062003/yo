#include "shared_mem.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define SHM_NAME "/shared_xyz"
int shm_fd;
SharedData *shared_xyz = NULL;  // Biến global trỏ vào shared memory


int init_shared_memory() {
    shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd < 0) {
        perror("shm_open");
        return -1;
    }

    if (ftruncate(shm_fd, sizeof(SharedData)) == -1) {
        perror("ftruncate");
        close(shm_fd);
        return -1;
    }

    shared_xyz = mmap(NULL, sizeof(SharedData), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shared_xyz == MAP_FAILED) {
        perror("mmap");
        close(shm_fd);
        return -1;
    }

    // Khởi tạo dữ liệu ban đầu nếu cần
    memset(shared_xyz, 0, sizeof(SharedData));
    return 0;
}

void update_shared_data(const SharedData *new_data) {
    if (shared_xyz && new_data) {
        memcpy(shared_xyz, new_data, sizeof(SharedData));
    }
}

void cleanup_shared_memory() {
    if (shared_xyz) {
        munmap(shared_xyz, sizeof(SharedData));
        shared_xyz = NULL;
    }

    if (shm_fd != -1) {
        close(shm_fd);
        shm_fd = -1;
    }

    shm_unlink(SHM_NAME);
}
