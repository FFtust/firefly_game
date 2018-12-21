# define makeblock functions and variabled

def setup():
    pass

def get_sys_mode():
    pass

def get_firmware_version():
    pass

def restart():
    pass

def timer_t():
    pass

def reset_timer_t():
    pass

def sleep_special():
    pass

def get_print_flag():
    pass

def set_print_flag():
    pass

DRIVER_ENABLE = True
class sensors():
    def __init__(self):
        pass

BATTERY_ENABLE = True
class battery():
    def __init__(self):
        pass

PIN_ENABLE = True
class pin():
    def __init__(self):
        pass

BUTTON_ENABLE = True
class button():
    def __init__(self):
        pass

    def value(self, button_id):
        print('button - value is called')
        return 1

    def is_pressed(self, button_id):
        print('button - is_pressed is called')
        return 1

    def is_released(self, button_id):
        print('button - is_released is called')
        return 1

TOUCHPAD_ENABLE = True
class touchpad():
    def __init__(self):
        pass

GYRO_ENABLE = True
class gyro():
    def __init__(self):
        pass

LED_MATRIX_ENABLE = True
class led_matrix():
    def __init__(self):
        pass

    def set_single_led(self, led_id, r, g, b):
        print("led - set_single_led is called")

    def set_all_led(self, r, g, b):
        print("led - set_single_led is called")

    def set_colorful_led(self, datas, offset):
        print("led - set_colorful_led is called")

VIBRATION_MOTOR_ENABLE = True
class vibration_motor():
    def __init__(self):
        pass

CLOCK_ENABLE = True
class clock():
    def __init__(self):
        pass

MUSIC_ENABLE = True
class music():
    def __init__(self):
        pass

COMMUNICATION_ENABLE = False
class communication():
    def __init__(self):
        pass

BLE_ENABLE = False
NEURONS_ENGINE_ENABLE = True
STOP_PYTHON_THREAD_ENABLE = False

EVENT_ENABLE = True
class event():
    def __init__(self):
        self.TRIGGER_NEVER = 0
        self.TRIGGER_ALWAYS_WITH_NO_PARAMETER = 1
        self.TRIGGER_ONCE_BY_VALUE_TRUE = 2
        self.TRIGGER_CONTINUOUS_BY_VALUE_TRUE = 3
        self.TRIGGER_ONCE_BY_VALUE_LARGER = 4
        self.TRIGGER_CONTINUOUS_BY_VALUE_LARGER = 5
        self.TRIGGER_ONCE_BY_VALUE_SMALLER = 6
        self.TRIGGER_CONTINUOUS_BY_VALUE_SMALLER = 7
        self.TRIGGER_BY_STRING_MATCHING = 8
        self.TRIGGER_TYPE_MAX = 9

        self.EVE_SYSTEM_LAUNCH = 0
        self.EVE_TIME_OVER = 1
        self.EVE_MESSAGE = 2
        self.EVE_CLOUD_MESSAGE = 3
        self.EVE_MESH_MESSAGE = 4
        self.EVENT_BUTTON = 5
        self.EVENT_TOUCHPAD_0 = 6
        self.EVENT_TOUCHPAD_1 = 7
        self.EVENT_TOUCHPAD_2 = 8
        self.EVENT_TOUCHPAD_3 = 9
        self.EVENT_SHAKED = 10
        self.EVENT_TILT_LEFT = 11
        self.EVENT_TILT_RIGHT = 12
        self.EVENT_TILT_FORWARD = 13
        self.EVENT_TILT_BACKWARD = 14
        self.EVENT_MICROPHONE = 15
        self.EVENT_TYPE_MAX = 16

        self.EVE_MAX_NUM = 64

    def event_register(self, event_type, trigger_type, user_para):

        return 1

WIFI_ENABLE = True
class wifi():
    def __init__(self):
        self.WLAN_MODE_NULL = 0
        self.WLAN_MODE_STA = 1
        self.WLAN_MODE_AP = 2
        self.WLAN_MODE_APSTA = 3
        self.WLAN_MODE_MESH = 255

WIFI_MESH_ENABLE = True
class wifi_mesh():
    def __init__(self):
        pass

SPEECH_RECOGNITION_ENABLE = True
class speech_recognition():
    def __init__(self):
        self.LAN_DEFAULT = 0
        self.LAN_CHINESE = 1
        self.LAN_ENGLISH = 2
        self.LAN_GERMAN = 3
        self.LAN_FRENCH = 4
        self.LAN_SPANISH = 5
        self.LAN_ID_MAX = 6
        self.SERVER_BAIDU = 1
        self.SERVER_MICROSOFT = 2
        self.SERVER_AMAZON = 3
        self.SERVER_ID_MAX = 4

I2S_MIC_ENABLE = True
class i2s_mic():
    def __init__(self):
        pass
