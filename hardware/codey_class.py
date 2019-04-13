import time

from utils.common import *
import adapter.hd_adapter as hd_adapter

# define common commands
ONLINE_MODE_ID = 0x01
OFF_LINE_MODE_ID = 0x00

RUN_TO_ONLINE_MODE_COMMAND = [0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x01, 0x0e, 0xf4]
READ_MODE_COMMAND_ID = 0x0d
READ_MODE_COMMAND =  [0xf3, 0xf5, 0x02, 0x00, 0x0d, 0x80, 0x8D, 0xf4]
READ_VERSION_COMMAND_ID = 0x06
READ_VERSION_COMMAND = [0xF3, 0xF4, 0x01, 0x00, 0x06, 0x06, 0xF4]

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

class codey():
    def __init__(self, port_info):
        # do initialize
        self.adapter = hd_adapter.adapter([port_info])

        self.current_mode = None
        self.version = None
        self.adapter.common_link.register_process_function(READ_VERSION_COMMAND_ID, self.version_protocol_parse)
        self.adapter.common_link.register_process_function(READ_MODE_COMMAND_ID, self.mode_protocol_parse)

        if self.get_device_version(1) == None:
            warn_print(" can't get device version information ")

        self.rename_apis()
        self.__run_into_online_mode()
        self.__import_codey()

    # system process
    def __run_into_online_mode(self):
        self.adapter.write_bytes_directly(bytearray([0xf3, 0xf6, 0x03, 0x00, 0x0d, 0x00, 0x03, 0x10, 0xf4]))
        time.sleep(2)

    # import codey
    def __import_codey(self):
        self.adapter.write_str_directly("from codey import *", service_id = 0x02)

    # battery 
    def __battery_get_voltage(self):
        ret = self.adapter.read_async("battery.get_voltage")
        if ret == None:
            return 0
        else:
            return ret

    def __battery_get_percentage(self):
        ret = self.adapter.read_async("battery.get_percentage")
        if ret == None:
            return 0
        else:
            return ret

    # button
    def __button_a_is_pressed(self):
        ret = self.adapter.read_async("button_a.is_pressed")
        if ret == None:
            return False
        else:
            return bool(ret)

    def __button_b_is_pressed(self):
        ret = self.adapter.read_async("button_b.is_pressed")
        if ret == None:
            return False
        else:
            return bool(ret)

    def __button_c_is_pressed(self):
        ret = self.adapter.read_async("button_c.is_pressed")
        if ret == None:
            return False
        else:
            return bool(ret)
        
    # display 
    def __display_show_image(self, image):
        self.adapter.write_async("display.show_image", "('%s', )" %(image, ))

    def __display_show(self, var, pos_x = None, pos_y = None, wait = True):
        self.adapter.write_async("display.show", "('%s', %s, %s, %s)" %(var, pos_x, pos_y, wait))

    def __display_set_pixel(self, pos_x, pos_y, status):
        self.adapter.write_async("display.set_pixel", "(%s, %s, %s)" %(pos_x, pos_y, status))

    def __display_get_pixel(self, pos_x, pos_y):
        ret = self.adapter.read_async("display.get_pixel", "(%s, %s)" %(pos_x, pos_y))
        if ret == None:
            return False
        else:
            return bool(ret)

    def __display_toggle_pixel(self, pos_x, pos_y):
        self.adapter.write_async("display.toggle_pixel", "(%s, %s)" %(pos_x, pos_y))

    def __display_clear(self):
        self.adapter.write_async("display.clear",)

    #led
    def __led_show(self, r, g, b):
        self.adapter.write_async("led.show", "(%s, %s, %s)" %(r, g, b))

    def __led_set_red(self, val):
        self.adapter.write_async("led.set_red", "(%s)" %(val, ))

    def __led_set_green(self, val):
        self.adapter.write_async("led.set_green", "(%s)" %(val, ))

    def __led_set_blue(self, val):
        self.adapter.write_async("led.set_blue", "(%s)" %(val, ))

    def __led_off(self):
        self.adapter.write_async("led.off")

    # light_sensor
    def __light_sensor_get_value(self):
        ret = self.adapter.read_async("light_sensor.get_value")
        if ret == None:
            return 0
        else:
            return ret

    # light_sensor
    def __sound_sensor_get_loudness(self):
        ret = self.adapter.read_async("sound_sensor.get_loudness")
        if ret == None:
            return 0
        else:
            return ret

    # potentiometer
    def __potentiometer_get_value(self):
        ret = self.adapter.read_async("potentiometer.get_value")
        if ret == None:
            return 0
        else:
            return ret

    # speaker 
    def __speaker_stop_sounds(self):
        self.adapter.write_async("speaker.stop_sounds")

    def __speaker_set_volume(self, value):
        self.adapter.write_async("speaker.set_volume", '(%s)' %(value, ))

    def __speaker_get_volume(self):
        ret = self.adapter.read_async("speaker.get_volume")
        if ret == None:
            return 0
        else:
            return ret

    def __speaker_change_volume(self, value):
        self.adapter.write_async("speaker.change_volume", '(%s)' %(value, ))

    def __speaker_set_tempo(self, value):
        self.adapter.write_async("speaker.set_tempo", '(%s)' %(value, ))

    def __speaker_change_tempo(self, value):
        self.adapter.write_async("speaker.change_tempo", '(%s)' %(value, ))

    def __speaker_get_tempo(self):
        ret = self.adapter.read_async("speaker.get_tempo")
        if ret == None:
            return 0
        else:
            return ret

    def __speaker_play_melody(self, sound_name, wait = False, off_t = 0.05):
        self.adapter.write_async("speaker.play_melody", "('%s', %s, %s)" %(sound_name, wait, off_t), update_flag = True)

    def __speaker_play_melody_until_done(self, sound_name, wait = True, off_t = 0.05):
        self.adapter.write_async("speaker.play_melody_until_done", "('%s', %s, %s)" %(sound_name, wait, off_t), update_flag = True)

    def __speaker_play_note(self, note, beat = None):
        self.adapter.write_async("speaker.play_note", "(%s, %s)" %(note, beat), update_flag = True)


    def __speaker_play_tone(self, frequency, time_ms = None):
        self.adapter.write_async("speaker.play_tone", "(%s, %s)" %(frequency, time_ms), update_flag = True)

    def __speaker_rest(self, beat):
        self.adapter.write_async("speaker.play_tone", "(%s)" %(beat), update_flag = True)

    # motion sensor
    def __motion_sensor_get_roll(self):
        ret = self.adapter.read_async("motion_sensor.get_roll")
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_pitch(self):
        ret = self.adapter.read_async("motion_sensor.get_pitch")
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_yaw(self):
        ret = self.adapter.read_async("motion_sensor.get_yaw")
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_rotation(self, axis):
        ret = self.adapter.read_async("motion_sensor.get_rotation", '("%s")' %(axis, ))
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_reset_rotation(self, axis = "all"):
        if not (axis in  index_dict):
            return 0

        self.adapter.write_async("motion_sensor.reset_rotation", '("%s")' %(axis, ))


    def __motion_sensor_is_shaked(self):
        ret = self.adapter.read_async("motion_sensor.is_shaked")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_get_shake_strength(self):
        ret = self.adapter.read_async("motion_sensor.get_shake_strength")
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_is_tilted_left(self):
        ret = self.adapter.read_async("motion_sensor.is_tilted_left")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_is_tilted_right(self):
        ret = self.adapter.read_async("motion_sensor.is_tilted_right")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_is_ears_up(self):
        ret = self.adapter.read_async("motion_sensor.is_ears_up")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_is_ears_down(self):
        ret = self.adapter.read_async("motion_sensor.is_ears_down")
        if ret == None:
            return False
        else:
            return ret
    def __motion_sensor_is_display_up(self):
        ret = self.adapter.read_async("motion_sensor.is_display_up")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_is_display_down(self):
        ret = self.adapter.read_async("motion_sensor.is_display_down")
        if ret == None:
            return False
        else:
            return ret
    def __motion_sensor_is_upright(self):
        ret = self.adapter.read_async("motion_sensor.is_upright")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_get_acceleration(self, axis):
        index_dict = {'x':1, 'y':2, 'z':3}
        if not (axis in  index_dict):
            return 0

        ret = self.adapter.read_async("motion_sensor.get_acceleration__" + + str(index_dict[axis]), '("%s")' %(axis, ))
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_gyroscope(self, axis):
        index_dict = {'x':1, 'y':2, 'z':3}
        if not (axis in  index_dict):
            return 0

        ret = self.adapter.read_async("motion_sensor.get_gyroscope__" + str(index_dict[axis]), '("%s")' %(axis, ))
        if ret == None:
            return 0
        else:
            return ret

    def rename_apis(self):
        # button 
        self.button_a = api_format()
        self.button_a.is_pressed = self.__button_a_is_pressed

        self.button_b = api_format()
        self.button_b.is_pressed = self.__button_b_is_pressed

        self.button_c = api_format()
        self.button_c.is_pressed = self.__button_c_is_pressed

        # display
        self.display = api_format()
        self.display.show_image = self.__display_show_image
        self.display.show = self.__display_show
        self.display.set_pixel = self.__display_set_pixel
        self.display.get_pixel = self.__display_get_pixel
        self.display.toggle_pixel = self.__display_toggle_pixel
        self.display.clear = self.__display_clear

        #led
        self.led = api_format()
        self.led.show = self.__led_show
        self.led.set_red = self.__led_set_red
        self.led.set_green = self.__led_set_green
        self.led.set_blue = self.__led_set_blue
        self.led.off = self.__led_off

        # light_sensor
        self.light_sensor = api_format()
        self.light_sensor.get_value = self.__light_sensor_get_value

        # sound_sensor
        self.sound_sensor = api_format()
        self.sound_sensor.get_loudness = self.__sound_sensor_get_loudness

        # potentiometer
        self.potentiometer = api_format()
        self.potentiometer.get_value = self.__potentiometer_get_value

        # speaker 
        self.speaker = api_format()
        self.speaker.stop_sounds = self.__speaker_stop_sounds
        self.speaker.set_volume = self.__speaker_set_volume
        self.speaker.get_volume = self.__speaker_get_volume
        self.speaker.change_volume = self.__speaker_change_volume
        self.speaker.set_tempo = self.__speaker_set_tempo
        self.speaker.change_tempo = self.__speaker_change_tempo
        self.speaker.get_tempo = self.__speaker_get_tempo
        self.speaker.play_melody = self.__speaker_play_melody
        self.speaker.play_melody_until_done = self.__speaker_play_melody_until_done
        self.speaker.play_note = self.__speaker_play_note
        self.speaker.play_tone = self.__speaker_play_tone
        self.speaker.rest = self.__speaker_rest

        # motion sensor
        self.motion_sensor = api_format()
        self.motion_sensor.get_roll = self.__motion_sensor_get_roll
        self.motion_sensor.get_pitch = self.__motion_sensor_get_pitch
        self.motion_sensor.get_yaw =  self.__motion_sensor_get_yaw
        self.motion_sensor.get_rotation = self.__motion_sensor_get_rotation
        self.motion_sensor.reset_rotation = self.__motion_sensor_reset_rotation
        self.motion_sensor.is_shaked = self.__motion_sensor_is_shaked
        self.motion_sensor.get_shake_strength = self.__motion_sensor_get_shake_strength
        self.motion_sensor.is_tilted_left = self.__motion_sensor_is_tilted_left
        self.motion_sensor.is_tilted_right = self.__motion_sensor_is_tilted_right
        self.motion_sensor.is_ears_up = self.__motion_sensor_is_ears_up
        self.motion_sensor.is_ears_down = self.__motion_sensor_is_ears_down
        self.motion_sensor.is_display_up = self.__motion_sensor_is_display_up
        self.motion_sensor.is_display_down = self.__motion_sensor_is_display_down
        self.motion_sensor.is_upright = self.__motion_sensor_is_upright
        self.motion_sensor.get_acceleration = self.__motion_sensor_get_acceleration
        self.motion_sensor.get_gyroscope = self.__motion_sensor_get_gyroscope

    # other fiunctions
    def version_protocol_parse(self, frame):
        version_string = str(frame, "utf8")
        warn_print("version bytes is %s, string is %s" %(frame, version_string))
        self.version = version_string

    def mode_protocol_parse(self, frame):
        if frame[0] == 0x80:
            self.current_mode = frame[1]
            warn_print("mode bytes is %s, mode is %s" %(frame, self.current_mode))
        else:
            pass

    def get_device_version(self, max_time_s):
        self.version = None
        self.adapter.write_bytes_directly(bytearray(READ_VERSION_COMMAND))
        start = time.time()
        while self.version == None and time.time() - start < max_time_s:
            time.sleep(0.05)

        return self.version

    def get_device_current_mode(self, max_time_s):
        self.current_mode = None
        self.adapter.write_bytes_directly(bytearray(READ_MODE_COMMAND))
        start = time.time()
        while self.current_mode == None and time.time() - start < max_time_s:
            time.sleep(0.05)
        return self.current_mode
