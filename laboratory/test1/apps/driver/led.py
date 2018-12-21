from global_objects import led_matrix_o
from utility.common import *
import math
import time
import random

firefly_table = [[0, 0, 20, True, 0], [4, 0, 15, True, 0], [7, 0, 20, True, 0], [11, 0, 25, True, 0]]

def __rgb_value_check(r, g, b):
    if type_check(r, (int, float)) and \
       type_check(g, (int, float)) and \
       type_check(b, (int, float)):
        
        return True

def __rgb_value_scale(r, g, b):
    r = int(num_range_scale(r, 0, 255))
    g = int(num_range_scale(g, 0, 255))
    b = int(num_range_scale(b, 0, 255))
    return r, g, b

class led(object):
    def __init__(self):
        pass

    def show_single(self, led_id, r, g, b, percentage = 100):
        if not type_check(led_id, (int, float)):
            return
        if not type_check(percentage, (int, float)):
            return  
        if not __rgb_value_check(r, g, b):
            return 

        led_id -= 1
        if led_id < 0 or led_id >= 12:
            return 

        percentage = num_range_scale(percentage, 0, 100)
        r = r * (percentage / 100)
        g = g * (percentage / 100)
        b = b * (percentage / 100)
        
        r, g, b = __rgb_value_scale(r, g, b)
        led_matrix_o.set_single_led(led_id , r, g, b)

    def show_all(self, r, g, b, percentage = 100):
        if not type_check(percentage, (int, float)):
            return        
        if not __rgb_value_check(r, g, b):
            return 

        percentage = num_range_scale(percentage, 0, 100)
        r = r * (percentage / 100)
        g = g * (percentage / 100)
        b = b * (percentage / 100)

        r, g, b = __rgb_value_scale(r, g, b)

        led_matrix_o.set_all_led(r, g, b)

    def off_single(self, led_id):
        if not type_check(led_id, (int, float)):
            return

        led_id -= 1
        if led_id < 0 or led_id >= 12:
            return 
        led_matrix_o.set_single_led(int(led_id), 0, 0, 0)

    def off_all(self):
        led_matrix_o.clear() 

    def clear(self):
        self.clear_flag = True
        led_matrix_o.clear()
    
    def show_ring(self, color_str, offset = 0):
        if (not type_check(color_str, str)) or (not type_check(offset, (int, float))):
            return
        offset = int(offset)
        color = color_str.split(' ')
        if len(color) > 12:
            color = color[0 : 12]

        value = bytearray(36)
        index = 0
        for item in color:
            if item in color_table:
                value[index] = color_table[item][0]
                index += 1
                value[index] = color_table[item][1]
                index += 1
                value[index] = color_table[item][2]
                index += 1
        led_matrix_o.set_colorful_led(value, offset)

    def ring_graph(self, percentage):
        if not type_check(percentage, (int, float)):
            return
        percentage = int(num_range_scale(percentage, 0, 100))
        num = int((percentage / 100) * 12)
        
        if num == 0:
            self.off_all()
            return
        else:
            value = bytearray(36)

            for i in range(num):
                value[3*i] = led_ring_tble[i][0]
                value[3*i + 1] = led_ring_tble[i][1]
                value[3*i + 2] = led_ring_tble[i][2]
            
            led_matrix_o.set_colorful_led(value, 0)

    def meteor_effect(self):
        self.clear_flag = False

        for index in range(12):
            for count in range(8):
                led_matrix_o.set_single_led(((index + 4) + count) % 12, 1, 0, 6)
     
            led_matrix_o.set_single_led((index + 0) % 12, 10, 10, 10)
            led_matrix_o.set_single_led((index + 1) % 12, 20, 20, 20)
            led_matrix_o.set_single_led((index + 2) % 12, 30, 30, 30)
            led_matrix_o.set_single_led((index + 3) % 12, 120, 120, 120)
            time.sleep(0.05)
            if self.clear_flag:
                led_matrix_o.clear()
                break

    def rainbow_effect(self):
        self.clear_flag = False

        red = 0
        green = 0
        blue = 0
        for i in range(1001):
            red = int((math.sin(0.36 * i / 180.0 * math.pi) + 1) * 100)
            green = int((math.sin(0.72 * i / 180.0 * math.pi) + 1) * 100)
            blue = int((math.sin(1.08 * i / 180.0 * math.pi) + 1) * 100)
            led_matrix_o.set_all_led(red, green, blue)
            time.sleep(0.002)
            if self.clear_flag:
                led_matrix_o.clear()
                break

    def spoondrift_effect(self):
        self.clear_flag = False
        
        light = 1.5
        for index in range(24):
            for count in range(8):
                led_matrix_o.set_single_led(((index + 4) + count) % 12 , 10, 20, 120)
     
            led_matrix_o.set_single_led((index + 0) % 12, int(10 * light), int(20 * light), 120)
            led_matrix_o.set_single_led((index + 1) % 12, int(10 * light), int(20 * light), 120)
            led_matrix_o.set_single_led((index + 2) % 12, int(10 * (3.67 * (light - 1) + 1)), int(20 * (1.67 * (light - 1) + 1)), 120)
            led_matrix_o.set_single_led((index + 3) % 12, int(10 * (3.67 * (light - 1) + 1)), int(20 * (1.67 * (light - 1) + 1)), 120)
            
            light = math.sin((index / 24) * math.pi) * 3 + 1.5
            time.sleep(0.2)
            if self.clear_flag:
                led_matrix_o.clear()
                break

    def firefly_effect(self):
        global firefly_table
        self.clear_flag = False

        count = 0
        # here off all led is necessary
        led_matrix_o.set_all_led(0, 0, 0)
        while True:        
            for i in range(len(firefly_table)):
                led_matrix_o.set_single_led(firefly_table[i][0], 0, firefly_table[i][1], 0)

                if firefly_table[i][3] == True:
                    firefly_table[i][1] += 1
                    if firefly_table[i][1] >= firefly_table[i][2]:
                        firefly_table[i][3] = False
                else:
                    firefly_table[i][1] -= 1
                    
                    if firefly_table[i][1] == 0:
                        firefly_table[i][4] += 1
                        if firefly_table[i][4] == 3:
                            led_matrix_o.set_single_led(firefly_table[i][0], 0, 0, 0)
                            # create new one
                            firefly_id = random.randint(-4, 16)
                            step = random.randint(10, 25)
                            firefly_table[i][0] = firefly_id
                            firefly_table[i][1] = 1
                            firefly_table[i][2] = step
                            firefly_table[i][3] = True
                            firefly_table[i][4] = 0
                        else:
                            firefly_table[i][3] = True
                time.sleep(0.003)

            time.sleep(0.02)

            count += 1
            if count > 250:
                break

            if self.clear_flag:
                led_matrix_o.clear()
                break

    def show_animation(self, name_string):
        if name_string == 'spoondrift':
            self.spoondrift_effect()
        elif name_string == 'meteor':
            self.meteor_effect()
        elif name_string == 'rainbow':
            self.rainbow_effect()
        elif name_string == 'firefly':
            self.firefly_effect()
