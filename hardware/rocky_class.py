import time

from utils.common import *

# define online apis, each name of the apis is the same with offline
class api_format():
    def __init__(self):
        self.version = "v1.0"

class rocky():
    def __init__(self, device):
        self.rename_apis()
        self.adapter = device.adapter
        # do initialize
        self.__import_rocky()

    # import rocky
    def __import_rocky(self):
        self.adapter.write_str_directly("from rocky import *", service_id = 0x02)

    def __rocky_stop(self):
        self.adapter.write_async("stop")

    def __rocky_forward(self, speed, t = None, straight = False, index = 1):
        self.adapter.write_async("forward", "(%s, %s, %s, %s)" %(speed, t, straight, index))

    def __rocky_backward(self, speed, t = None, straight = False, index = 1):
        self.adapter.write_async("backward", "(%s, %s, %s, %s)" %(speed, t, straight, index))

    def __rocky_turn_left(self, speed, t = None, index = 1):
        self.adapter.write_async("turn_left", "(%s, %s, %s)" %(speed, t, index))

    def __rocky_turn_right(self, speed, t = None, index = 1):
        self.adapter.write_async("turn_right", "(%s, %s, %s)" %(speed, t, index))

    def __rocky_drive(self, left_power, right_power, index = 1):
        self.adapter.write_async("drive", "(%s, %s, %s)" %(left_power, right_power, index))

    def __rocky_turn_left_by_degree(self, angle, speed = 40, index = 1):
        self.adapter.write_async("turn_left_by_degree", "(%s, %s, %s)" %(angle, speed, index))

    def __rocky_turn_right_by_degree(self, angle, speed = 40, index = 1):
        self.adapter.write_async("turn_right_by_degree", "(%s, %s, %s)" %(angle, speed, index))
    
    # ir color sensor 
    def __get_red(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_red", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret

    def __get_green(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_green", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret
       
    def __get_blue(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_blue", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret

    def __is_color(self, color_str, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.is_color", "(%s, %s)" %(color_str, index))
        if ret == None:
            return False
        else:
            return ret

    def __get_light_strength(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_light_strength", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret

    def __get_greyness(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_greyness", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret 

    def __get_reflected_light(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_reflected_light", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret

    def __get_reflected_infrared(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.get_reflected_infrared", "(%s)" %(index, ))
        if ret == None:
            return 0
        else:
            return ret

    def __is_obstacle_ahead(self, index = 1):
        ret = self.adapter.read_async("color_ir_sensor.is_obstacle_ahead", "(%s)" %(index, ))
        if ret == None:
            return False
        else:
            return ret

    def __set_led_color(self, color_name, index = 1):
        self.adapter.write_async("color_ir_sensor.set_led_color", "(%s, %s)" %(color_name, index ))

    def rename_apis(self):
        self.stop = self.__rocky_stop
        self.forward = self.__rocky_forward
        self.backward = self.__rocky_backward
        self.turn_left = self.__rocky_turn_left
        self.turn_right = self.__rocky_turn_right
        self.drive = self.__rocky_drive
        self.turn_left_by_degree = self.__rocky_turn_left_by_degree
        self.turn_right_by_degree = self.__rocky_turn_right_by_degree

        self.color_ir_sensor = api_format()
        self.color_ir_sensor.get_reflected_light = self.__get_reflected_light
        self.color_ir_sensor.get_greyness = self.__get_greyness




