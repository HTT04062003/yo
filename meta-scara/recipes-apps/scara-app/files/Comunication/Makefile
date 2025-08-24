CFLAGS += -Wall -g -I. -I./Robot_Kinematic
LDFLAGS += -lm -lrt
TARGET = comunication_process

SRC = main.c \
      my_usb_serial.c \
      can_interface.c \
      shared_mem.c \
      comand_line.c \
      socket_server.c \
      queue.c \
      thread.c \
      Robot_Kinematic/forward_kinematic.c \
      Robot_Kinematic/inverse_kinematic.c \
      Robot_Kinematic/jacobian.c \
      Robot_Kinematic/nano_sleep.c \
      Robot_Kinematic/p2p_interpolation.c \
      Robot_Kinematic/path_linear_interpolation.c \
      Robot_Kinematic/scara_robot_parameter.c

# Convert to flat object names
OBJ = $(patsubst %.c, %.o, $(SRC))
OBJ := $(subst /,_,$(OBJ))

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Rule to compile with renamed object files
define COMPILE_TEMPLATE
$(subst /,_,$(1:.c=.o)): $(1)
	$$(CC) $$(CFLAGS) -c $$< -o $$@
endef

$(foreach src,$(SRC),$(eval $(call COMPILE_TEMPLATE,$(src))))

clean:
	rm -f $(OBJ) $(TARGET)
