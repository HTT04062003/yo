#ifndef SOCKET_SERVER_H
#define SOCKET_SERVER_H
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
int setup_server(int port);
int accept_client(int server_fd);
int handle_client(int client_fd, int serial_fd);
int send_all(int fd, const char *data, size_t len);
extern int server_fd;
extern bool is_sending;
#endif