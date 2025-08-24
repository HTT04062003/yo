SUMMARY = "SCARA Robot base image"
LICENSE = "MIT"

inherit core-image

IMAGE_FEATURES += "ssh-server-openssh"

IMAGE_INSTALL += " \
    packagegroup-core-boot \
    packagegroup-core-ssh-openssh \
    python3 \
    python3-tkinter \
    libx11 \
    libxext \
    libxrender \
    libxft \
    xserver-xorg \
    xinit \
"

