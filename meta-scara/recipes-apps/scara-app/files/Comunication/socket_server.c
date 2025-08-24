#include "socket_server.h"
#include "my_usb_serial.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>

#define MAX_BUFFER 1024
int server_fd;
bool is_sending = false;
int setup_server(int port) {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        return -1;
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in server_addr = {
        .sin_family = AF_INET,
        .sin_port = htons(port),
        .sin_addr.s_addr = INADDR_ANY
    };

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        close(server_fd);
        return -1;
    }

    if (listen(server_fd, 5) < 0) {
        perror("listen");
        close(server_fd);
        return -1;
    }

    return server_fd;
}

int accept_client(int server_fd) {
    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);
    return accept(server_fd, (struct sockaddr *)&client_addr, &addr_len);
}

int send_all(int fd, const char *data, size_t len) {
    is_sending = true;

    size_t total_sent = 0;
    while (total_sent < len) {
        ssize_t sent = write(fd, data + total_sent, len - total_sent);
        if (sent < 0) {
            if (errno == EINTR) continue;
            perror("write");
            is_sending = false;
            return -1;
        }
        total_sent += sent;
    }

    is_sending = false;
    return 0;
}