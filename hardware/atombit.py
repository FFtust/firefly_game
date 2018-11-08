import time

from utils.common import *
import adapter.hd_adapter as hd_adapter

atombit_adapter = hd_adapter.adapter()

# system process
def __run_into_online_mode():
    atombit_adapter.write_bytes_directly(bytearray([0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x01, 0x0e, 0xf4]))
    time.sleep(3)

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
    atombit_adapter.write_str_directly("from atombit import *")

# button
def __button_is_pressed():
    ret = atombit_adapter.read_async("button.is_pressed")
    if ret == None:
        return False
    else:
        return bool(ret)

#led
def __led_show_all(r, g, b):
    # atombit_adapter.write_async("led.show_all", "(%s, %s, %s)" %(r, g, b))
    atombit_adapter.write_imidiate_script("led.show_all", "(%s, %s, %s)" %(r, g, b))

def __led_show_single(index, r , g, b):
    # atombit_adapter.write_async(("led.show_single", "(%s, %s, %s, %s)" %(index, r, g, b)))
    atombit_adapter.write_imidiate_script(("led.show_single", "(%s, %s, %s, %s)" %(index, r, g, b)))

def __led_off_all():
    # atombit_adapter.write_async("led.off_all")
    atombit_adapter.write_imidiate_script("led.off_all")
    
def __led_off_single(index):
    # atombit_adapter.write_async(("led.off_single", "(%s)" %(index,)))
    atombit_adapter.write_imidiate_script(("led.off_single", "(%s)" %(index,)))

#vibration motor
def __vibration_motor_on(value):
    atombit_adapter.write_async(("vibration_motor.on," "(%s)" %(value,)))

def __vibration_motor_set_strength(value):
    atombit_adapter.write_async(("vibration_motor.set_strength", "(%s)" %(value,)))


# music
def __music_play_melody(name):
    atombit_adapter.write_imidiate_script(("music.play_melody",  "('%s')" %(name,)))

def __music_play_melody_to_stop(name):
    atombit_adapter.write_imidiate_script(("music.play_melody_to_stop('%s')" %(name,)))


def __music_play_tone(frequency, beat):
    atombit_adapter.write_imidiate_script(("music.play_tone", "(%s, %s)" %(frequency, beat)))

def __music_stop_sounds():
    atombit_adapter.write_imidiate_script("music.stop_sounds")

def __music_set_volume(volume):
    atombit_adapter.write_async(("music.set_volume", "(%s)" %(volume, )))


def __music_get_volume():
    ret = atombit_adapter.read_async("music.get_volume")
    if ret == None:
        return 0
    else:
        return ret

def __music_change_volume(change_value):
    atombit_adapter.write_async(("music.change_volume", "(%s)" %(change_value, )))

# touchpad
def __tp0_is_touched():
    ret = atombit_adapter.read_async("touchpad0.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp0_set_touch_threshold(value):
    atombit_adapter.write_async(("touchpad0.set_touch_threshold", "(%s)" %(value, )))

def __tp0_get_value():
    ret = atombit_adapter.read_async("touchpad0.get_value")
    if ret == None:
        return 0
    else:
        return ret

def __tp1_is_touched():
    ret = atombit_adapter.read_async("touchpad1.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp1_set_touch_threshold(value):
    atombit_adapter.write_async(("touchpad1.set_touch_threshold", "(%s)" %(value, )))

def __tp1_get_value():
    ret = atombit_adapter.read_async("touchpad1.get_value")
    if ret == None:
        return 0
    else:
        return ret

def __tp2_is_touched():
    ret = atombit_adapter.read_async("touchpad2.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp2_set_touch_threshold(value):
    atombit_adapter.write_async(("touchpad2.set_touch_threshold", "(%s)" %(value, )))

def __tp2_get_value():
    ret = atombit_adapter.read_async("touchpad2.get_value")
    if ret == None:
        return 0
    else:
        return ret

def __tp3_is_touched():
    ret = atombit_adapter.read_async("touchpad3.is_touched")
    if ret == None:
        return False
    else:
        return True

def __tp3_set_touch_threshold(value):
    atombit_adapter.write_async(("touchpad3.set_touch_threshold", "(%s)" %(value, )))

def __tp3_get_value():
    ret = atombit_adapter.read_async("touchpad3.get_value")
    if ret == None:
        return 0
    else:
        return ret

# microphone
def __mic_get_loudness():
    ret = atombit_adapter.read_async("microphone.get_loudness")
    if ret == None:
        return 0
    else:
        return ret

# wifi
def __wifi_start(ssid = "Maker-guest", password = "makeblock", mode = 1):
    atombit_adapter.write_imidiate_script(("wifi.start", "(%s, %s, %s)" %(ssid, password, mode)))


def __wifi_is_connected():
    atombit_adapter.write_imidiate_script("wifi.is_connected")


# speech recognition    
def __speech_recognition_start(server = 0, language = 0, time = 5):
    atombit_adapter.write_imidiate_script("speech_recognition.start", "(%d, %d, %d)" %(server, language, time))


def __speech_recognition_get_result_code():
    atombit_adapter.write_imidiate_script("speech_recognition.get_result_code")
    if ret == None:
        return ''
    else:
        return ret

# # motion sensor
# def __motion_sensor_get_acceleration(axis):
    

# get_gyroscope(axis):

# get_rotation(axis):

# reset_rotation(axis = "all"):

# is_shaked():
    
# get_shake_strength():
 
# is_tilted_left():

# is_tilted_right():

# is_arrow_up():

# is_arrow_down():

# get_pitch():

# get_roll():

# get_yaw():

# get_gesture()


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
# motion_sensor.get_acceleration(axis):

# get_gyroscope(axis):

# get_rotation(axis):

# reset_rotation(axis = "all"):

# is_shaked():
    
# get_shake_strength():
 
# is_tilted_left():

# is_tilted_right():

# is_arrow_up():

# is_arrow_down():

# get_pitch():

# get_roll():

# get_yaw():

# get_gesture()

# do initialize
__run_into_online_mode()
__import_firefly()

