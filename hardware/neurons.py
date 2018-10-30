import json
import time

from utils.common import *
from hardware.codey import codey_adapter as neurons_adapter

# system process
def __run_into_online_mode():
    neurons_adapter.write_bytes_directly(bytearray([0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x03, 0x10, 0xf4]))

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

# import rocky
def __import_neurons():
    neurons_adapter.write_str_directly("from neurons import *")

def __led_panel_show_image(image, index):
    neurons_adapter.write_async("led_panel.show_image__" + str(index), '(%s, 0, %d)' %(image, index)) 

def __led_panel_clear(index):
    neurons_adapter.write_async("led_panel.clear", '(%d)' %(index, )) 

led_panel = api_format()
led_panel.show_image = __led_panel_show_image
led_panel.clear = __led_panel_clear

# do initialize
__run_into_online_mode()
__import_neurons()
