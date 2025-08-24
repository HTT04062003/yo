#include "comand_line.h"
#include "queue.h"
#include "can_interface.h"

#include "../Robot_Kinematic/scara_robot_parameter.h"
const char* cmd_auto_home = "J0\n";
const char* cmd_move_x_down = "JXD\n";
const char* cmd_move_x_up = "JXU\n";
const char* cmd_move_y_up = "JYU\n";
const char* cmd_move_y_down = "JYD\n";
const char* cmd_move_z_up = "JZU\n";
const char* cmd_move_z_down = "JZD\n";
const char* cmd_jogging_theta1_up = "J1U\n";
const char* cmd_jogging_theta1_down = "J1D\n";
const char* cmd_jogging_theta2_up = "J2U\n";
const char* cmd_jogging_theta2_down = "J2D\n";
const char* cmd_jogging_theta3_up = "J3U\n";
const char* cmd_jogging_theta3_down = "J3D\n";
const char* cmd_jogging_theta4_up = "J4U\n";
const char* cmd_jogging_theta4_down = "J4D\n";
const char* cmd_val_on = "VAL_ON\n";
const char* cmd_val_off = "VAL_OFF\n";
const char* cmd_move_z = "MOVE_Z";
const char* cmd_update_data_to_app = "UPDATE\n";
const char* cmd_add_new_item_to_app = "GETQR\n";
uint8_t CMD_FROM_APP = COMMAND_NO_OP;
uint8_t RESPONSE_FROM_APP = 0;
uint8_t select_id = 0;
uint8_t readComand_From_App(char *lineBuffer) {
	uint8_t cmd_type = 0;
    // Bi?n t?m d? gi? giá tr? s? khi g?p X, Y, F
    char *p = lineBuffer;
    uint8_t ID = 0;
	  uint8_t X, Y, Z;
    // Duy?t qua t?ng ký t? trong chu?i
    while (*p != '\0') {
        // Ki?m tra ký t? và tách giá tr? d?a trên các ký t? X, Y, F
        if (*p == 'X') {
            
				}else if(*p == 'J'){
					if((*(p+1) == '1') && (*(p+2) == 'U')) cmd_type = COMMAND_JOGGING_THETA1_UP;
					else if((*(p+1) == '1') && (*(p+2) == 'D')) cmd_type = COMMAND_JOGGING_THETA1_DOWN;
					else if((*(p+1) == '2') && (*(p+2) == 'U')) cmd_type = COMMAND_JOGGING_THETA2_UP;
					else if((*(p+1) == '2') && (*(p+2) == 'D')) cmd_type = COMMAND_JOGGING_THETA2_DOWN;
					else if((*(p+1) == '3') && (*(p+2) == 'U')) cmd_type = COMMAND_JOGGING_THETA3_UP;
					else if((*(p+1) == '3') && (*(p+2) == 'D')) cmd_type = COMMAND_JOGGING_THETA3_DOWN;
					else if((*(p+1) == '4') && (*(p+2) == 'U')) cmd_type = COMMAND_JOGGING_THETA4_UP;
					else if((*(p+1) == '4') && (*(p+2) == 'D')) cmd_type = COMMAND_JOGGING_THETA4_DOWN;
					else if((*(p+1) == 'X') && (*(p+2) == 'U')){
						cmd_type = COMAND_JOGGING_X_UP;
						
						}
					else if((*(p+1) == 'X') && (*(p+2) == 'D')){
						cmd_type = COMAND_JOGGING_X_DOWN;
						
						
						}
					else if((*(p+1) == 'Y') && (*(p+2) == 'U')){
						cmd_type = COMAND_JOGGING_Y_UP;
						
						}
					else if((*(p+1) == 'Y') && (*(p+2) == 'D')){
						cmd_type = COMAND_JOGGING_Y_DOWN;
						
						}
					else if((*(p+1) == 'Z') && (*(p+2) == 'U')){
						cmd_type = COMAND_JOGGING_Z_UP;
						
						}
					else if((*(p+1) == 'Z') && (*(p+2) == 'D')){
						cmd_type = COMAND_JOGGING_Z_DOWN;
						
						}
					else if(*(p+1) == '0') cmd_type = COMMAND_AUTO_HOME;
					else {
						cmd_type = COMMAND_NO_OP;
						
						}
				}else  if((*p == 'N') && (*(p + 1) == '0')) cmd_type = COMMAND_NO_OP;
				else if(*p == 'Q') cmd_type = COMMAND_CONNECT_FROM_MASTER;
				 else if(*p == 'S'){
					  select_id = atoi( p + 1);
					  Table_Point[select_id].ID = ID_EXIST;
					 }
				 else if(*p == 'D'){
					  ID = atoi( p + 1);
					  Table_Point[ID].ID = ID_NOT_EXIST;
					 }
				 else if(*p == 'x') Table_Point[select_id].x = atof( p + 1);
				 else if(*p == 'y') Table_Point[select_id].y = atof( p + 1);
				 else if(*p == 'z') Table_Point[select_id].z = atof( p + 1);
				 else if(*p == 'w') {
					 Table_Point[select_id].e = atof( p + 1); 
					
					}
				else if(*p == 'm'){
					select_id = atoi( p + 1);
					cmd_type = COMMAND_MOVE_TO_POINT;					
					}
				else if(*p == 'V'){
				    if((*(p+1) == 'O' && (*(p+2) == 'N'))) cmd_type = COMMAND_VAL_ON;
					else if((*(p+1) == 'O' && (*(p+2) == 'F'))) cmd_type = COMMAND_VAL_OFF;
				}
				else if(*p == 'A'){
                    new_id = atoi(p + 1);  // Sửa ở đây
					printf("New_ID = %d\n", new_id);
				    uint8_t data[8] = {0};
				    send_can_frame(can_fd, CMD_RUN_BT_FROM_CAN_BUS, data, 8);
				}
        // Tang con tr? d? ki?m tra ký t? ti?p theo
        p++;
    }
		
		return cmd_type;
}