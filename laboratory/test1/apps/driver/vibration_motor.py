from global_objects import vibration_motor_o
from utility.common import *
class vibration_motor(object):
    def __init__(self, vibration_motor_id = 0):
        self.vibration_motor_id = vibration_motor_id
        self.strength = 100
    # 0 - 10
    def set_strength(self, strength):
        if not type_check(strength, (int, float)):
            return
        strength = num_range_scale(strength, 0, 100)
        self.strength = int(strength)

    def on(self, strength = None):
        if strength == None:
            vibration_motor_o.set_strength(self.vibration_motor_id, self.strength)
            return 

        if not type_check(strength, (int, float)):
            return
        strength = num_range_scale(strength, 0, 100)
        self.strength = int(strength)
        vibration_motor_o.set_strength(self.vibration_motor_id, self.strength)


