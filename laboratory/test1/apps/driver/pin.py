from global_objects import pin_o
from utility.common import *

class pin(object):
    def __init__(self, pin_id = 0):
        self.pin_id = int(pin_id)

    def read_digital(self):
        return pin_o.digital_read(self.pin_id)

    def write_digital(self, value):
        if not type_check(value, (int, float, bool)):
            return
        value = int(value)
        value = num_range_scale(value, 0, 1)

        pin_o.digital_write(self.pin_id, value)

    def servo_write(self, value):
        if not type_check(value, (int, float)):
            return
        value = int(value)
        # 20000 is not a valid value
        value = num_range_scale(value, 0, 19999)

        pin_o.servo_write(self.pin_id, value)

    def read_analog(self):
        # only pin2 and pin3 support analog reading
        if self.pin_id <= 1:
            return 0
        # thereturn value is voltage of mv
        analog = pin_o.analog_read(self.pin_id)
        ret = int((analog / 3300) * 1023)
        return num_range_scale(ret, 0, 1023)

    def write_analog(self, value):
        if not type_check(value, (int, float)):
            return
        value = int(num_range_scale(value, 0, 1024))

        pin_o.analog_write(self.pin_id, value)

    def analog_set_frequency(self, frequency):
        if not type_check(frequency, (int, float)):
            return
        pin_o.analog_set_frequency(self.pin_id, frequency)

    def is_touched(self):
        if pin_o.is_touched(self.pin_id):
            return True
        else:
            return False

    def set_touchpad_threshold(self, value):
        if not type_check(value, (int, float)):
            return

        value = num_range_scale(value, 0, 1)

        pin_o.set_touch_threshold(self.pin_id, value)

    def get_touchpad_value(self):
        ret = pin_o.get_touch_value(self.pin_id)
        ret = touchpad_value_scale(self.pin_id, ret)
        return ret
