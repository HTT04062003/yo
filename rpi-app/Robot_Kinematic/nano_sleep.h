#ifndef NANO_SLEEP_H
#define NANO_SLEEP_H
#include <time.h>

long diff_ns(struct timespec start, struct timespec end);
void precise_delay(long remaining_ns);
#endif