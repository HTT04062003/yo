SUMMARY = "Communication Process Application"
DESCRIPTION = "App dùng CAN, socket, shared memory cho robot"
LICENSE = "CLOSED"
PR = "r0"

SRC_URI = " \
    file://Comunication/Makefile \
    file://Comunication/main.c \
    file://Comunication/my_usb_serial.c \
    file://Comunication/my_usb_serial.h \
    file://Comunication/can_interface.c \
    file://Comunication/can_interface.h \
    file://Comunication/shared_mem.c \
    file://Comunication/shared_mem.h \
    file://Comunication/comand_line.c \
    file://Comunication/comand_line.h \
    file://Comunication/socket_server.c \
    file://Comunication/socket_server.h \
    file://Comunication/queue.c \
    file://Comunication/queue.h \
    file://Comunication/thread.c \
    file://Comunication/thread.h \
    file://Robot_Kinematic/ \
    file://scara-app.service \
    file://run.sh \
"

S = "${WORKDIR}"

inherit systemd

SYSTEMD_SERVICE:${PN} = "scara-app.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"

do_compile() {
    cp -r ${S}/Robot_Kinematic ${S}/Comunication/
    oe_runmake -C ${S}/Comunication
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/Comunication/comunication_process ${D}${bindir}/comunication_process
    
    # Cài thư mục chứa run.sh
    install -d ${D}/usr/share/scara-app
    install -m 0755 ${S}/run.sh ${D}/usr/share/scara-app/run.sh

    # Cài file service vào systemd
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${S}/scara-app.service \
        ${D}${systemd_system_unitdir}/scara-app.service
}
