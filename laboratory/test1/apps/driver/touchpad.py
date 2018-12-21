from global_objects import touchpad_o
from utility.common import *

class touchpad(object):
    def __init__(self, touchpad_id = 0):
        self.touchpad_id = touchpad_id

    def is_touched(self):
        if touchpad_o.is_pressed(self.touchpad_id):
            return True
        else:
            return False

    def set_touch_threshold(self, value):
        if not type_check(value, (int, float)):
            return
        value = num_range_scale(value, 0, 1)

        # add value limitation here
        touchpad_o.set_threshold(self.touchpad_id, value) 

    def get_value(self):
        ret = touchpad_o.value(self.touchpad_id)
        ret = touchpad_value_scale(self.touchpad_id, ret)

        return ret
            


