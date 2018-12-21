from global_objects import button_o

class button(object):
    def __init__(self, button_id = 0):
        self.button_id = button_id

    def is_pressed(self):
        if button_o.is_pressed(int(self.button_id)):
            return True
        else:
            return False
