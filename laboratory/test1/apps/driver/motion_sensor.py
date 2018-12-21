from global_objects import gyro_o
from utility.common import *
AXIS_X = 1
AXIS_Y = 2
AXIS_Z = 3

ANGLE_PITCH_ID = 1
ANGLE_ROLL_ID = 2
ANGLE_YAW_ID = 3

TILE_LEFT_ID = 1
TILE_RIGHT_ID = 2
TILE_FORWARD_ID = 3
TILE_BACKWARD_ID = 4

TILE_SCREEN_UP = 5
TILE_SCREEN_DOWN = 6

class motion_sensor(object):
    def __init__(self):
        pass

    def get_acceleration(self, axis):
        value = 0
        if type_check(axis, str):
            if axis == 'x':
                value = gyro_o.get_acc(AXIS_X)
            elif axis == 'y':
                value = gyro_o.get_acc(AXIS_Y)
            elif axis == 'z':
                value = -1 * gyro_o.get_acc(AXIS_Z)
        return  int(value * 98 * 2 / 32767.0) / 10

    def get_gyroscope(self, axis):
        value = 0
        if type_check(axis, str):
            if axis == 'x':
                value = -1 * gyro_o.get_gyro(AXIS_X)
            elif axis == 'y':
                value = -1 * gyro_o.get_gyro(AXIS_Y)
            elif axis == 'z':
                value = gyro_o.get_gyro(AXIS_Z)
        return int(value * 10) / 10

    def get_rotation(self, axis):
        value = 0
        if type_check(axis, str):
            if axis == 'x':
                value = -1 * gyro_o.get_rotate_angle(AXIS_X)
            elif axis == 'y':
                value = -1 * gyro_o.get_rotate_angle(AXIS_Y)
            elif axis == 'z':
                value = gyro_o.get_rotate_angle(AXIS_Z)
            else:
                return 0
        return value

    def reset_rotation(self, axis = "all"):
        if type_check(axis, str):
            if axis == 'x':
                value = gyro_o.reset_rotate_angle(AXIS_X)
            elif axis == 'y':
                value = gyro_o.reset_rotate_angle(AXIS_Y)
            elif axis == 'z':
                value = gyro_o.reset_rotate_angle(AXIS_Z)
            elif axis == "all":
                value = gyro_o.reset_rotate_angle(AXIS_X)
                value = gyro_o.reset_rotate_angle(AXIS_Y)
                value = gyro_o.reset_rotate_angle(AXIS_Z)

    def is_shaked(self):
        return bool(gyro_o.is_shaked())
    
    def get_shake_strength(self):
        return gyro_o.get_shaked_strength()  

    def is_tilted_left(self):
        return bool(gyro_o.get_tilt(TILE_LEFT_ID))

    def is_tilted_right(self):
        return bool(gyro_o.get_tilt(TILE_RIGHT_ID))

    def is_arrow_up(self):
        return bool(gyro_o.get_tilt(TILE_BACKWARD_ID))

    def is_arrow_down(self):
        return bool(gyro_o.get_tilt(TILE_FORWARD_ID))

    def is_led_ring_up(self):
        return bool(gyro_o.get_tilt(TILE_SCREEN_UP))

    def is_led_ring_down(self):
        return bool(gyro_o.get_tilt(TILE_SCREEN_DOWN))

    def get_pitch(self):
        return -1 * int(gyro_o.get_angle(ANGLE_PITCH_ID))

    def get_roll(self):
        return int(gyro_o.get_angle(ANGLE_ROLL_ID)) 

    def get_yaw(self):
        ret = gyro_o.get_angle(ANGLE_YAW_ID)
        while ret < 0:
            ret = ret + 360
        while ret > 360:
            ret = ret % 360 
        return round(int(ret))

    def get_gesture(self):
        return ""

