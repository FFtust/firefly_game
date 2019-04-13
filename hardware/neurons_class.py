import time
from firefly_online.utils.common import *

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

class neurons():
    def __init__(self, device):
        self.rename_apis()
        self.adapter = device.adapter
        # do initialize
        self.__import_neurons()

    # import rocky
    def __import_neurons(self):
        neurons_adapter.write_str_directly("from neurons import *")

    def __led_panel_show_image(self, image, index):
        neurons_adapter.write_async("led_panel.show_image__" + str(index), '(%s, 0, %d)' %(image, index)) 

    def __led_panel_clear(self, index):
        neurons_adapter.write_async("led_panel.clear", '(%d)' %(index, )) 

    def rename_apis(self):
        self.led_panel = api_format()
        self.led_panel.show_image = self.__led_panel_show_image
        self.led_panel.clear = self.__led_panel_clear


