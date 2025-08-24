#include "nano_sleep.h"
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <stdint.h>
#include <string.h>

#include <errno.h>

long diff_ns(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
}

void precise_delay(long remaining_ns) {
    if (remaining_ns > 0) {
        struct timespec ts = {
            .tv_sec = remaining_ns / 1000000000L,
            .tv_nsec = remaining_ns % 1000000000L
        };
        nanosleep(&ts, NULL);
    }
}
