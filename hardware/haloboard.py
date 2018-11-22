import time

from utils.common import *
import adapter.hd_adapter as hd_adapter

# system process
def __run_into_online_mode(t = None):
    haloboard_adapter.write_bytes_directly(bytearray([0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x01, 0x0e, 0xf4]))
    if t == None:
        time.sleep(2)
    else:
        time.sleep(t)

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

# import firefly
def __import_firefly():
    haloboard_adapter.write_str_directly("from haloboard import *")

# button
def __button_is_pressed():
    ret = haloboard_adapter.read_async("button.is_pressed")
    if ret == None:
        return False
    else:
        return bool(ret)

#led
def __led_show_all(r, g, b):
    # haloboard_adapter.write_async("led.show_all", "(%s, %s, %s)" %(r, g, b))
    haloboard_adapter.write_imidiate_script("led.show_all", "(%s, %s, %s)" %(r, g, b))

def __led_show_single(index, r , g, b):
    # haloboard_adapter.write_async(("led.show_single", "(%s, %s, %s, %s)" %(index, r, g, b)))
    haloboard_adapter.write_imidiate_script(("led.show_single", "(%s, %s, %s, %s)" %(index, r, g, b)))

def __led_off_all():
    # haloboard_adapter.write_async("led.off_all")
    haloboard_adapter.write_imidiate_script("led.off_all")
    
def __led_off_single(index):
    # haloboard_adapter.write_async(("led.off_single", "(%s)" %(index,)))
    haloboard_adapter.write_imidiate_script(("led.off_single", "(%s)" %(index,)))

#vibration motor
def __vibration_motor_on(value):
    haloboard_adapter.write_async(("vibration_motor.on," "(%s)" %(value,)))

def __vibration_motor_set_strength(value):
    haloboard_adapter.write_async(("vibration_motor.set_strength", "(%s)" %(value,)))


# music
def __music_play_melody(name):
    haloboard_adapter.write_imidiate_script(("music.play_melody",  "('%s')" %(name,)))

def __music_play_melody_to_stop(name):
    haloboard_adapter.write_imidiate_script(("music.play_melody_to_stop('%s')" %(name,)))


def __music_play_tone(frequency, beat):
    haloboard_adapter.write_imidiate_script(("music.play_tone", "(%s, %s)" %(frequency, beat)))

def __music_stop_sounds():
    haloboard_adapter.write_imidiate_script("music.stop_sounds")

def __music_set_volume(volume):
    haloboard_adapter.write_async(("music.set_volume", "(%s)" %(volume, )))


def __music_get_volume():
    ret = haloboard_adapter.read_async("music.get_volume")
    if ret == None:
        return 0
    else:
        return ret

def __music_change_volume(change_value):
    haloboard_adapter.write_async(("music.change_volume", "(%s)" %(change_value, )))

# touchpad
def __tp0_is_touched():
    ret = haloboard_adapter.read_async("touchpad0.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp0_set_touch_threshold(value):
    haloboard_adapter.write_async(("touchpad0.set_touch_threshold", "(%s)" %(value, )))

def __tp0_get_value():
    ret = haloboard_adapter.read_async("touchpad0.get_value")
    if ret == None:
        return 0
    else:
        return ret

def __tp1_is_touched():
    ret = haloboard_adapter.read_async("touchpad1.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp1_set_touch_threshold(value):
    haloboard_adapter.write_async(("touchpad1.set_touch_threshold", "(%s)" %(value, )))

def __tp1_get_value():
    ret = haloboard_adapter.read_async("touchpad1.get_value")
    if ret == None:
        return 0
    else:
        return ret

def __tp2_is_touched():
    ret = haloboard_adapter.read_async("touchpad2.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp2_set_touch_threshold(value):
    haloboard_adapter.write_async(("touchpad2.set_touch_threshold", "(%s)" %(value, )))

def __tp2_get_value():
    ret = haloboard_adapter.read_async("touchpad2.get_value")
    if ret == None:
        return 0
    else:
        return ret

def __tp3_is_touched():
    ret = haloboard_adapter.read_async("touchpad3.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp3_set_touch_threshold(value):
    haloboard_adapter.write_async(("touchpad3.set_touch_threshold", "(%s)" %(value, )))

def __tp3_get_value():
    ret = haloboard_adapter.read_async("touchpad3.get_value")
    if ret == None:
        return 0
    else:
        return ret

# microphone
def __mic_get_loudness():
    ret = haloboard_adapter.read_async("microphone.get_loudness")
    if ret == None:
        return 0
    else:
        return ret

# wifi
def __wifi_start(ssid = "Maker-guest", password = "makeblock", mode = 1):
    haloboard_adapter.write_imidiate_script(("wifi.start", "(%s, %s, %s)" %(ssid, password, mode)))


def __wifi_is_connected():
    haloboard_adapter.write_imidiate_script("wifi.is_connected")


# speech recognition    
def __speech_recognition_start(server = 0, language = 0, time = 5):
    haloboard_adapter.write_imidiate_script("speech_recognition.start", "(%s, %s, %s)" %(server, language, time))


def __speech_recognition_get_result_code():
    haloboard_adapter.write_imidiate_script("speech_recognition.get_result_code")
    if ret == None:
        return ''
    else:
        return ret

# # motion sensor
def __motion_sensor_get_acceleration(axis):
    ret = haloboard_adapter.read_async("motion_sensor.get_acceleration", "('%s')" %(axis, ))
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_gyroscope(axis):
    ret = haloboard_adapter.read_async("motion_sensor.get_gyroscope", "('%s')" %(axis, ))
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_rotation(axis):
    ret = haloboard_adapter.read_async("motion_sensor.get_rotation", "('%s')" %(axis, ))
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_reset_rotation(axis = "all"):
    ret = haloboard_adapter.write_imidiate_script("motion_sensor.reset_rotation", "('%s')" %(axis, ))

def __motion_sensor_is_shaked():
    ret = haloboard_adapter.read_async("motion_sensor.get_rotation")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_get_shake_strength():
    ret = haloboard_adapter.read_async("motion_sensor.shake_strength")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_is_tilted_left():
    ret = haloboard_adapter.read_async("motion_sensor.is_tilted_left")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_is_tilted_right():
    ret = haloboard_adapter.read_async("motion_sensor.is_tilted_right")
    if ret == None:
        return False
    else:
        return ret
def __motion_sensor_is_arrow_up():
    ret = haloboard_adapter.read_async("motion_sensor.is_arrow_up")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_is_arrow_down():
    ret = haloboard_adapter.read_async("motion_sensor.is_arrow_down")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_get_pitch():
    ret = haloboard_adapter.read_async("motion_sensor.get_pitch")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_roll():
    ret = haloboard_adapter.read_async("motion_sensor.get_roll")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_yaw():
    ret = haloboard_adapter.read_async("motion_sensor.get_yaw")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_gesture():
    return ''


# api rename
button = api_format()
button.is_pressed = __button_is_pressed

led = api_format()
led.show_all = __led_show_all
led.show_single = __led_show_single
led.off_single = __led_off_single
led.off_all = __led_off_all

vibration_motor = api_format()
vibration_motor.set_strength = __vibration_motor_set_strength
vibration_motor.on = __vibration_motor_on

music = api_format()
music.play_melody = __music_play_melody
music.play_melody_to_stop = __music_play_melody_to_stop
music.play_tone = __music_play_tone
music.stop_sounds = __music_stop_sounds
music.set_volume = __music_set_volume
music.change_volume = __music_change_volume
music.get_volume = __music_get_volume

touchpad0 = api_format()
touchpad1 = api_format()
touchpad2 = api_format()
touchpad3 = api_format()

touchpad0.is_touched = __tp0_is_touched
touchpad0.set_touch_threshold = __tp0_set_touch_threshold
touchpad0.get_value = __tp0_get_value
touchpad1.is_touched = __tp1_is_touched
touchpad1.set_touch_threshold = __tp1_set_touch_threshold
touchpad1.get_value = __tp1_get_value
touchpad2.is_touched = __tp2_is_touched
touchpad2.set_touch_threshold = __tp2_set_touch_threshold
touchpad2.get_value = __tp2_get_value
touchpad3.is_touched = __tp3_is_touched
touchpad3.set_touch_threshold = __tp3_set_touch_threshold
touchpad3.get_value = __tp3_get_value

microphone = api_format()
microphone.get_loudness = __mic_get_loudness

motion_sensor = api_format()

motion_sensor.get_acceleration = __motion_sensor_get_acceleration
motion_sensor.get_gyroscope = __motion_sensor_get_gyroscope
motion_sensor.get_rotation = __motion_sensor_get_rotation
motion_sensor.reset_rotation = __motion_sensor_reset_rotation
motion_sensor.is_shaked = __motion_sensor_is_shaked
motion_sensor.get_shake_strength = __motion_sensor_get_shake_strength
motion_sensor.is_tilted_left = __motion_sensor_is_tilted_left
motion_sensor.is_tilted_right = __motion_sensor_is_tilted_right
motion_sensor.is_arrow_up = __motion_sensor_is_arrow_up
motion_sensor.is_arrow_down = __motion_sensor_is_arrow_down
motion_sensor.get_pitch = __motion_sensor_get_pitch
motion_sensor.get_roll = __motion_sensor_get_roll
motion_sensor.get_yaw = __motion_sensor_get_yaw
motion_sensor.get_gesture = __motion_sensor_get_gesture

haloboard_adapter = None
# do initialize
def start(port):
    haloboard_adapter = hd_adapter.adapter([port])
    __run_into_online_mode()
    __import_firefly()

