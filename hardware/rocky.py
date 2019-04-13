import json
import time

from utilc.common import *
from hardware.codey import codey_adapter as rocky_adapter

# system process
def __run_into_online_mode():
    rocky_adapter.write_bytes_directly(bytearray([0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x03, 0x10, 0xf4]))

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

# import rocky
def __import_rocky():
    rocky_adapter.write_str_directly("from rocky import *", service_id = 0x02)

def __get_reflected_light():
    ret = rocky_adapter.read_async("color_ir_sensor.get_reflected_light")
    if ret == None:
        return 0
    else:
        print('g', ret)
        return ret

def __get_greyness():
    ret = rocky_adapter.read_async("color_ir_sensor.get_greyness")
    if ret == None:
        return 0
    else:
        return ret    

def __drive(left, right):
    rocky_adapter.write_async("drive", '(%d, %d)' %(left, right))

color_ir_sensor = api_format()
color_ir_sensor.get_reflected_light = __get_reflected_light
color_ir_sensor.get_greyness = __get_greyness

drive = __drive
# do initialize
__run_into_online_mode()
__import_rocky()

