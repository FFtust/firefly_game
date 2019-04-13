import threading
import math
import time
from firefly_online.utils.common import *

from firefly_online.application.game_adapter import screen_update_hardware
from firefly_online.application.game_adapter import FACE_ROW, FACE_COLUMN, REFRESH_INTERVAL, SPRITE_NUM_MAX

GAME_NOT_START = 0
GAME_READY = 1
GAME_RUNING = 2
GAME_OVER = 3

NOT_MEET = 0x00
UP_MEET = 0x01
DOWN_MEET = 0x02
LEFT_MEET = 0x04
RIGHT_MEET = 0x08

ANGLE_TORADIAN = 57.3

# calculate the next coordinate after rotate
# angle must be multiple of 90
def calculate_coordinate_after_rotate(rotate_center, pre_coor, angle):
    temp = [0, 0]
    temp[0] = pre_coor[0] - rotate_center[0]
    temp[1] = pre_coor[1] - rotate_center[1]
    t_angle = (angle + 360) % 360
    t_angle = t_angle / ANGLE_TORADIAN
    a_coor = [0, 0]
    a_coor[0] = round(math.cos(t_angle)) * temp[0] - round(math.sin(t_angle)) * temp[1]
    a_coor[1] = round(math.sin(t_angle)) * temp[0] + round(math.cos(t_angle)) * temp[1]
    a_coor[0] = a_coor[0] + rotate_center[0]
    a_coor[1] = a_coor[1] + rotate_center[1]
    return a_coor.copy()

def script_string_to_list(script):
    try:
        sprite_info = []
        for i in range(FACE_COLUMN):
            dat = int(script[i * 2 :  (i + 1) * 2], 16)
            sprite_info.append(dat)
        return sprite_info.copy()
    except:
        print_dbg("script_string_to_list error")

def script_list_to_string(script):
    try:
        sprite_info = ""
        for i in range(FACE_COLUMN):
            temp = hex(script[i])
            if len(temp) == 3:
                temp = '0x0' + temp[-1]
            sprite_info += temp
        return sprite_info.copy()
    except:
        print_dbg("script_list_to_string error")    

class sprite_create():
    def __init__(self, sp_info):
        count = 0
        p_x_l = 0
        p_x_r = 0
        p_y_u = 0
        p_y_d = 0
        self.ope_sema = threading.Lock()
        self.sprite_info = []
        self.sprite_current = [[None] * FACE_COLUMN] * FACE_ROW

        for i in range(FACE_ROW):
            dat = int(sp_info[i * 2 :  (i + 1) * 2], 16)
            self.sprite_info.append(dat)
            if count == 0 and dat != 0:
                p_x_l = i
                count += 1
            elif count == 1 and dat == 0:
                p_x_r = i - 1
                count += 1
        if count == 1:
            p_x_r = FACE_COLUMN - 1 
 
        count = 0
        ret = 0
        # check the lfet_up point
        for i in range(FACE_ROW):
            for j in range(FACE_COLUMN):
                ret |= self.sprite_info[j] & (1 << i)
            if count == 0 and ret != 0:
                p_y_u = i
                count += 1
            elif count == 1 and ret == 0:
                p_y_d = i - 1
                count += 1
                break
            if count > 2:
                break
            ret = 0    

        if count == 1:
            p_y_d = FACE_ROW - 1 
        self.lu_coord = [p_x_l, p_y_u]
        self.rd_coord = [p_x_r, p_y_d]
        self.rotate_angle = 0
        self.position = [0, 0]
        self.show_flag = True
        self.meet_border_status = 0 # 0: not meet 1: up 2: down 3: left 4: right
# calculate rotate center and region *******************************************************************
        self.rotate_center = [0, 0]
        self.region_len = 0 

        for i in range(2):
            self.rotate_center[i] = self.rd_coord[i] - self.lu_coord[i] + 1
            if self.rotate_center[i] % 2 == 0:
                self.rotate_center[i] = (self.rd_coord[i] + self.lu_coord[i] + 1) // 2
            else:
                self.rotate_center[i] = (self.rd_coord[i] + self.lu_coord[i]) // 2


        if (self.rd_coord[0] - self.lu_coord[0]) == (self.rd_coord[1] - self.lu_coord[1]):
            self.region_len = (self.rd_coord[0] - self.lu_coord[0]) + 1
        else:
            self.region_len = max((self.rd_coord[0] - self.lu_coord[0]), (self.rd_coord[1] - self.lu_coord[1])) + 1
            if self.region_len % 2 == 0:
                self.region_len += 1


    def add_point(self):
        pass

    def del_point(self):
        pass 

# sprite control
    def left(self, num = 1):
        self.ope_sema.acquire(1)
        self.position = [num_range_check(self.position[0] - num, -31, 31), self.position[1]]
        self.ope_sema.release()

    def right(self, num = 1):
        self.ope_sema.acquire(1)
        self.position = [num_range_check(self.position[0] + num, -31, 31), self.position[1]]
        self.ope_sema.release()

    def down(self, num = 1):
        self.ope_sema.acquire(1)
        self.position = [self.position[0], num_range_check(self.position[1] - num, -31, 31)]
        self.ope_sema.release()

    def up(self, num = 1):
        self.ope_sema.acquire(1)
        self.position = [self.position[0], num_range_check(self.position[1] + num, -31, 31)]
        self.ope_sema.release()

    def home(self):
        self.ope_sema.acquire(1)
        self.position = [0, 0]
        self.ope_sema.release()    

    # rotate clockwisely 
    def rotate(self, angle = 90):
        self.ope_sema.acquire(1)
        if angle % 90 == 0:
            self.rotate_angle += angle
        self.ope_sema.release() 

    def rotate_to(self, angle):
        self.ope_sema.acquire(1)
        if angle % 90 == 0:
            self.rotate_angle = angle
        self.ope_sema.release() 

    def show(self):
        self.ope_sema.acquire(1)
        self.show_flag = True
        self.ope_sema.release() 

    def hide(self):
        self.ope_sema.acquire(1)
        self.show_flag = False
        self.ope_sema.release() 

    def set_position(self, pos):
        self.ope_sema.acquire(1)
        if type(pos) == list:
            if len(pos) == 2:
                self.position[0] = pos[0]
                self.position[1] = -pos[1]
        self.ope_sema.release() 

    def get_position(self):
        self.ope_sema.acquire(1)
        res = [0, 0]
        res[0] = self.position[0]
        res[1] = -self.position[1]
        self.ope_sema.release() 
        return res

    def get_rotate_angle(self):
        self.ope_sema.acquire(1)
        res =  self.self.rotate_angle
        self.ope_sema.release()
        return res

    def get_region(self):
        peak_coor = [[0, 0], [0, 0], [0, 0], [0, 0]]
        peak_coor[0] = self.lu_coord.copy()
        peak_coor[1][0] = self.rd_coord[0]
        peak_coor[1][1] = self.lu_coord[1]
        peak_coor[2] = self.rd_coord.copy()
        peak_coor[3][0] = self.lu_coord[0]
        peak_coor[3][1] = self.rd_coord[1]
        if (self.rotate_angle + 360) % 360 == 0:
            return self.lu_coord.copy(), self.rd_coord.copy()
        elif (self.rd_coord[0] - self.lu_coord[0]) == (self.rd_coord[1] - self.lu_coord[1]):
            return self.lu_coord.copy(), self.rd_coord.copy()
        else:
            time_num = ((self.rotate_angle + 360) % 360) // 90
        lu = calculate_coordinate_after_rotate(self.rotate_center, peak_coor[4 - time_num], self.rotate_angle)
        rd = calculate_coordinate_after_rotate(self.rotate_center, peak_coor[(6 - time_num) % 4], self.rotate_angle)

        return lu.copy(), rd.copy()

    def meet_border_check(self):
        # calculate the matrix after motion and rotation
        lu_c = [0, 0]
        rd_c = [0, 0]
        self.ope_sema.acquire(1)
        lu_c, rd_c = self.get_region()

        self.meet_border_status = NOT_MEET
        if self.position[0] + lu_c[0] < 0:
            self.meet_border_status = LEFT_MEET
        elif self.position[0] + rd_c[0] >= FACE_COLUMN:
            self.meet_border_status = RIGHT_MEET
        
        if lu_c[1] - self.position[1] < 0:
            self.meet_border_status |= UP_MEET
        elif rd_c[1] - self.position[1] >= FACE_ROW:
            self.meet_border_status |= DOWN_MEET
        self.ope_sema.release() 
        return self.meet_border_status
        

# function below shou not be called by users            
    def face_rotate_info(self):
        sr_line_num = 0
        sr_cross_num = 0
        ret_info = [0] * FACE_COLUMN
        self.ope_sema.acquire(1)
# calculate buffer after rotate ************************************************************************* 
        sr_line_num = self.rotate_center[1] - (self.region_len) // 2
        sr_cross_num = self.rotate_center[0] - (self.region_len) // 2

        while self.rotate_angle < 0:
            self.rotate_angle += 360

        if self.rotate_angle % 360 == 90:
            temp = 0
            for i in  range(self.region_len): # column
                for j in range(self.region_len): # line
                    if (self.sprite_info[sr_cross_num + j] & (1 << (sr_line_num + i))):
                        temp |=  (1 << (j + sr_line_num))
                ret_info[sr_cross_num + self.region_len - i - 1] = temp
                temp = 0

        elif self.rotate_angle % 360 == 180:
            for i in  range(self.region_len): 
                for j in range(self.region_len):
                    if (self.sprite_info[sr_cross_num + j] & (1 << (sr_line_num + i))):
                        ret_info[sr_cross_num + self.region_len - j - 1] |= 1 << (sr_line_num + self.region_len - i - 1)

        elif self.rotate_angle % 360 == 270:
            temp = 0
            for i in  range(self.region_len):
                for j in range(self.region_len):
                    if (self.sprite_info[sr_cross_num + self.region_len - j - 1] & (1 << (sr_line_num + i))):
                        temp |=  (1 << (j + sr_line_num))
                ret_info[sr_cross_num + i] = temp
                temp = 0
        else:
            ret_info = self.sprite_info.copy()

        self.sprite_current = [0] * FACE_COLUMN
        for i in range(FACE_COLUMN):
            if (i + self.position[0]) >= 0 and  (i + self.position[0]) <= FACE_COLUMN - 1:
                if self.position[1] > 0:
                    self.sprite_current[i + self.position[0]] = (ret_info[i] >> self.position[1])
                else:
                    self.sprite_current[i + self.position[0]] = (ret_info[i] << (-self.position[1]))
        self.ope_sema.release()

class game_base():
    def __init__(self):
        self.status = 0
        self.face_buffer = [0] * FACE_COLUMN
        self.back_ground = [0] * FACE_COLUMN
        self.back_ground_show = True
        self.sprite_list = []
        self.sema = threading.Lock()
        self.refresh_interval = REFRESH_INTERVAL

    def set_background(self, background):
        self.sema.acquire(1)
        if type(background) == list:
            s_list = background
        elif type(background) == str:
            s_list = script_string_to_list(background)
        if type(s_list) == list:
            if len(s_list) == FACE_COLUMN:
                self.back_ground = s_list.copy()
        self.sema.release()

    def set_background_with_point(self, point_pos):
        self.sema.acquire(1)
        if point_pos[1] > 0:
            self.back_ground[point_pos[0]] |= (1 << point_pos[1]) 
        else:
            self.back_ground[point_pos[0]] |= (1 >> (-point_pos[1])) 
        self.sema.release()

    def clear_background_with_point(self, point_pos):
        self.sema.acquire(1)
        if point_pos[1] > 0:
            self.back_ground[point_pos[0]] &= ~(1 << point_pos[1]) 
        else:
            self.back_ground[point_pos[0]] &= ~(1 >> (-point_pos[1])) 
        self.sema.release()

    def get_background(self):
        self.sema.acquire(1)
        res = self.back_ground.copy()
        self.sema.release()
        return res

    def set_background_with_line(self, data, line_index):
        if line_index >= FACE_ROW or line_index < 0:
            return 0

        self.sema.acquire(1)
        for i in range(FACE_COLUMN):
            if (1 << line_index) & (data):
                self.back_ground[i] |= (1 << line_index)
            else:
                self.back_ground[i] &= (~(1 << line_index))
        self.sema.release()

    def get_background_with_line(self, line_index):
        if line_index >= FACE_ROW or line_index < 0:
            return 0
        self.sema.acquire(1)
        temp = 0
        for i in range(FACE_COLUMN):
            temp |= ((1 << line_index) & (self.back_ground[i]))
        self.sema.release()
        return temp
           
    def set_background_with_column(self, data, column_index):
        if column_index >= FACE_COLUMN or column_index < 0:
            return 
        self.sema.acquire(1)
        self.back_ground[column_index] = data
        self.sema.release()

    def get_background_with_column(self, column_index):
        if column_index >= FACE_COLUMN or column_index < 0:
            return 0
        self.sema.acquire(1)
        res = self.back_ground[column_index].copy()
        self.sema.release()
        return res

    def show_background(self):
        self.sema.acquire(1)
        self.back_ground_show = True
        self.sema.release()

    def hide_background(self):
        self.sema.acquire(1)
        self.back_ground_show = False
        self.sema.release()

    def get_screen(self):
        self.screen_refresh()
        self.sema.acquire(1)
        res = self.face_buffer.copy()
        self.sema.release()
        return res

    def del_sprite(self, sp):
        self.sema.acquire(1)
        for i in range(len(self.sprite_list)):
            if self.sprite_list[i] == sp:
                del self.sprite_list[i]
        self.sema.release()

    def sprite_list_clean(self):
        self.sema.acquire(1)
        del self.sprite_list
        self.sprite_list = []
        self.sema.release()

    def add_sprite(self, sp):
        self.sema.acquire(1)
        self.sprite_list.append(sp)
        self.sema.release()

    def collision_check(self, script_1, script_2):
        self.sema.acquire(1)
        script_1.face_rotate_info()
        script_2.face_rotate_info()
        start_num = script_1.lu_coord[0] + script_1.position[0]
        for i in range(script_1.rd_coord[0] - script_1.lu_coord[0] + 1):
            if i + start_num < 0 or i + start_num >= FACE_COLUMN:
                continue
            if script_1.sprite_current[i + start_num] ^ script_2.sprite_current[i + start_num] \
             != script_1.sprite_current[i + start_num] | script_2.sprite_current[i + start_num]:
                self.sema.release()
                return True
        self.sema.release()
        return False

    def background_collision_check(self, script):
        self.sema.acquire(1)
        script.face_rotate_info()
        start_num = script.lu_coord[0] + script.position[0]
        for i in range(script.rd_coord[0] - script.lu_coord[0] + 1):
            if i + start_num < 0 or i + start_num >= FACE_COLUMN:
                continue
            if script.sprite_current[i + start_num] ^ self.back_ground[i + start_num] \
             != script.sprite_current[i + start_num] | self.back_ground[i + start_num]:
                self.sema.release()
                return True
        self.sema.release()
        return False

    def screen_refresh(self):
        self.sema.acquire(1)
        self.face_buffer = [0] * FACE_COLUMN
        for i in range(FACE_COLUMN):
            for item in self.sprite_list:
                if i == 0:
                    item.face_rotate_info()
                if item.show_flag == False:
                    continue
                self.face_buffer[i] |= item.sprite_current[i]
            if self.back_ground_show:
                self.face_buffer[i] |= self.back_ground[i]
        self.sema.release()
        screen_update_hardware(self.face_buffer)

    def set_refresh_interval(self, val):
        self.refresh_interval = val

    def get_refresh_interval(self, val):
        return self.refresh_interval
        
    def screen_refresh_auto(self):
        self.status = GAME_RUNING
        while True:
            if self.status == GAME_RUNING:
                self.screen_refresh()
                time.sleep(self.refresh_interval / 1000)
            else:
                time.sleep(0.2)

    def game_start(self):
        if self.status == GAME_NOT_START:
            self.reflesh_th = threading.Thread(target = self.screen_refresh_auto, args =())
            self.reflesh_th.start()
        self.status = GAME_RUNING

    def game_over(self):
        self.status = GAME_OVER