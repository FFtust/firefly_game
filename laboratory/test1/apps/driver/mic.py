from global_objects import mic_o

class mic(object):
    def __init__(self):
        pass

    # "maximum" , "average"
    def get_loudness(self, value_type = "maximum"):
        if value_type != "maximum" and value_type != "average":
            return 0
        return mic_o.get_loudness(value_type)