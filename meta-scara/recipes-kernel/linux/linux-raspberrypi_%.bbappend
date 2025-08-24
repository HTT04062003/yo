FILESEXTRAPATHS:prepend := "${THISDIR}/linux:"

SRC_URI += "file://can.cfg"

KERNEL_FEATURES:append = " features/can/can.scc"
