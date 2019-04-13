import time

from firefly_online.utils.common import *
import firefly_online.adapter.hd_adapter as hd_adapter

codey_adapter = hd_adapter.adapter()

# system process
def __run_into_online_mode():
    codey_adapter.write_bytes_directly(bytearray([0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x03, 0x10, 0xf4]))
    time.sleep(3)

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

# import codey
def __import_codey():
    codey_adapter.write_str_directly("from codey import *")

# battery 
def __battery_get_voltage():
    ret = codey_adapter.read_async("battery.get_voltage")
    if ret == None:
        return 0
    else:
        return ret

def __battery_get_percentage():
    ret = codey_adapter.read_async("battery.get_percentage")
    if ret == None:
        return 0
    else:
        return ret

# button
def __button_a_is_pressed():
    ret = codey_adapter.read_async("button_a.is_pressed")
    if ret == None:
        return False
    else:
        return bool(ret)

def __button_b_is_pressed():
    ret = codey_adapter.read_async("button_b.is_pressed")
    if ret == None:
        return False
    else:
        return bool(ret)

def __button_c_is_pressed():
    ret = codey_adapter.read_async("button_c.is_pressed")
    if ret == None:
        return False
    else:
        return bool(ret)
    
# display 
def __display_show_image(image):
    codey_adapter.write_async("display.show_image", "('%s', )" %(image, ))

def __display_show(var, pos_x = None, pos_y = None, wait = True):
    codey_adapter.write_async("display.show", "('%s', %s, %s, %s)" %(var, pos_x, pos_y, wait))

def __display_set_pixel(pos_x, pos_y, status):
    codey_adapter.write_async("display.set_pixel", "(%s, %s, %s)" %(pos_x, pos_y, status))

def __display_get_pixel(pos_x, pos_y):
    ret = codey_adapter.read_async("display.get_pixel", "(%s, %s)" %(pos_x, pos_y))
    if ret == None:
        return False
    else:
        return bool(ret)

def __display_toggle_pixel(pos_x, pos_y):
    codey_adapter.write_async("display.toggle_pixel", "(%s, %s)" %(pos_x, pos_y))

def __display_clear():
    codey_adapter.write_async("display.clear",)

#led
def __led_show(r, g, b):
    codey_adapter.write_async("led.show", "(%s, %s, %s)" %(r, g, b))

def __led_set_red(val):
    codey_adapter.write_async("led.set_red", "(%s)" %(val, ))

def __led_set_green(val):
    codey_adapter.write_async("led.set_green", "(%s)" %(val, ))

def __led_set_blue(val):
    codey_adapter.write_async("led.set_blue", "(%s)" %(val, ))

def __led_off():
    codey_adapter.write_async("led.off")

# light_sensor
def __light_sensor_get_value():
    ret = codey_adapter.read_async("light_sensor.get_value")
    if ret == None:
        return 0
    else:
        return ret

# light_sensor
def __sound_sensor_get_loudness():
    ret = codey_adapter.read_async("sound_sensor.get_loudness")
    if ret == None:
        return 0
    else:
        return ret

# potentiometer
def __potentiometer_get_value():
    ret = codey_adapter.read_async("potentiometer.get_value")
    if ret == None:
        return 0
    else:
        return ret

# speaker 
def __speaker_stop_sounds():
    codey_adapter.write_async("speaker.stop_sounds")

def __speaker_set_volume(value):
    codey_adapter.write_async("speaker.set_volume", '(%s)' %(value, ))

def __speaker_get_volume():
    ret = codey_adapter.read_async("speaker.get_volume")
    if ret == None:
        return 0
    else:
        return ret

def __speaker_change_volume(value):
    codey_adapter.write_async("speaker.change_volume", '(%s)' %(value, ))

def __speaker_set_tempo( value):
    codey_adapter.write_async("speaker.set_tempo", '(%s)' %(value, ))

def __speaker_change_tempo(value):
    codey_adapter.write_async("speaker.change_tempo", '(%s)' %(value, ))

def __speaker_get_tempo():
    ret = codey_adapter.read_async("speaker.get_tempo")
    if ret == None:
        return 0
    else:
        return ret

def __speaker_play_melody(sound_name, wait = False, off_t = 0.05):
    codey_adapter.write_async("speaker.play_melody", "('%s', %s, %s)" %(sound_name, wait, off_t), update_flag = True)

def __speaker_play_melody_until_done(sound_name, wait = True, off_t = 0.05):
    codey_adapter.write_async("speaker.play_melody_until_done", "('%s', %s, %s)" %(sound_name, wait, off_t), update_flag = True)

def __speaker_play_note(note, beat = None):
    codey_adapter.write_async("speaker.play_note", "(%s, %s)" %(note, beat), update_flag = True)


def __speaker_play_tone(frequency, time_ms = None):
    codey_adapter.write_async("speaker.play_tone", "(%s, %s)" %(frequency, time_ms), update_flag = True)

def __speaker_rest(beat):
    codey_adapter.write_async("speaker.play_tone", "(%s)" %(beat), update_flag = True)

# motion sensor
def __motion_sensor_get_roll():
    ret = codey_adapter.read_async("motion_sensor.get_roll")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_pitch():
    ret = codey_adapter.read_async("motion_sensor.get_pitch")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_yaw():
    ret = codey_adapter.read_async("motion_sensor.get_yaw")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_rotation(axis):
    ret = codey_adapter.read_async("motion_sensor.get_rotation", '("%s")' %(axis, ))
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_reset_rotation(axis = "all"):
    if not (axis in  index_dict):
        return 0

    codey_adapter.write_async("motion_sensor.reset_rotation", '("%s")' %(axis, ))


def __motion_sensor_is_shaked():
    ret = codey_adapter.read_async("motion_sensor.is_shaked")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_get_shake_strength():
    ret = codey_adapter.read_async("motion_sensor.get_shake_strength")
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_is_tilted_left():
    ret = codey_adapter.read_async("motion_sensor.is_tilted_left")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_is_tilted_right():
    ret = codey_adapter.read_async("motion_sensor.is_tilted_right")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_is_ears_up():
    ret = codey_adapter.read_async("motion_sensor.is_ears_up")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_is_ears_down():
    ret = codey_adapter.read_async("motion_sensor.is_ears_down")
    if ret == None:
        return False
    else:
        return ret
def __motion_sensor_is_display_up():
    ret = codey_adapter.read_async("motion_sensor.is_display_up")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_is_display_down():
    ret = codey_adapter.read_async("motion_sensor.is_display_down")
    if ret == None:
        return False
    else:
        return ret
def __motion_sensor_is_upright():
    ret = codey_adapter.read_async("motion_sensor.is_upright")
    if ret == None:
        return False
    else:
        return ret

def __motion_sensor_get_acceleration(axis):
    index_dict = {'x':1, 'y':2, 'z':3}
    if not (axis in  index_dict):
        return 0

    ret = codey_adapter.read_async("motion_sensor.get_acceleration__" + + str(index_dict[axis]), '("%s")' %(axis, ))
    if ret == None:
        return 0
    else:
        return ret

def __motion_sensor_get_gyroscope(axis):
    index_dict = {'x':1, 'y':2, 'z':3}
    if not (axis in  index_dict):
        return 0

    ret = codey_adapter.read_async("motion_sensor.get_gyroscope__" + str(index_dict[axis]), '("%s")' %(axis, ))
    if ret == None:
        return 0
    else:
        return ret

# button 
button_a = api_format()
button_a.is_pressed = __button_a_is_pressed

button_b = api_format()
button_b.is_pressed = __button_b_is_pressed

button_c = api_format()
button_c.is_pressed = __button_c_is_pressed


# display
display = api_format()
display.show_image = __display_show_image
display.show = __display_show
display.set_pixel = __display_set_pixel
display.get_pixel = __display_get_pixel
display.toggle_pixel = __display_toggle_pixel
display.clear = __display_clear

#led
led = api_format()
led.show = __led_show
led.set_red = __led_set_red
led.set_green = __led_set_green
led.set_blue = __led_set_blue
led.off = __led_off

# light_sensor
light_sensor = api_format()
light_sensor.get_value = __light_sensor_get_value

# sound_sensor
sound_sensor = api_format()
sound_sensor.get_loudness = __sound_sensor_get_loudness

# potentiometer
potentiometer = api_format()
potentiometer.get_value = __potentiometer_get_value

# speaker 
speaker = api_format()
speaker.stop_sounds = __speaker_stop_sounds
speaker.set_volume = __speaker_set_volume
speaker.get_volume = __speaker_get_volume
speaker.change_volume = __speaker_change_volume
speaker.set_tempo = __speaker_set_tempo
speaker.change_tempo = __speaker_change_tempo
speaker.get_tempo = __speaker_get_tempo
speaker.play_melody = __speaker_play_melody
speaker.play_melody_until_done = __speaker_play_melody_until_done
speaker.play_note = __speaker_play_note
speaker.play_tone = __speaker_play_tone
speaker.rest = __speaker_rest

# motion sensor
motion_sensor = api_format()
motion_sensor.get_roll = __motion_sensor_get_roll
motion_sensor.get_pitch = __motion_sensor_get_pitch
motion_sensor.get_yaw =  __motion_sensor_get_yaw
motion_sensor.get_rotation = __motion_sensor_get_rotation
motion_sensor.reset_rotation = __motion_sensor_reset_rotation
motion_sensor.is_shaked = __motion_sensor_is_shaked
motion_sensor.get_shake_strength = __motion_sensor_get_shake_strength
motion_sensor.is_tilted_left = __motion_sensor_is_tilted_left
motion_sensor.is_tilted_right = __motion_sensor_is_tilted_right
motion_sensor.is_ears_up = __motion_sensor_is_ears_up
motion_sensor.is_ears_down = __motion_sensor_is_ears_down
motion_sensor.is_display_up = __motion_sensor_is_display_up
motion_sensor.is_display_down = __motion_sensor_is_display_down
motion_sensor.is_upright = __motion_sensor_is_upright
motion_sensor.get_acceleration = __motion_sensor_get_acceleration
motion_sensor.get_gyroscope = __motion_sensor_get_gyroscope


# do initialize
__run_into_online_mode()
__import_codey()
# frame = create_frame(0x01, "subscribe.add_item(1, codey.button_a.is_pressed, ())")   
# common_link.phy.write(frame)
# frame = create_frame(0x01, "subscribe.add_item(2, codey.button_b.is_pressed, ())")   
# common_link.phy.write(frame)
# frame = create_frame(0x01, "subscribe.add_item(3, codey.button_c.is_pressed, ())")   
# common_link.phy.write(frame)
print("online start")