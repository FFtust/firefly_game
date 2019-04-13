import time

from firefly_online.utils.common import *
import firefly_online.adapter.hd_adapter as hd_adapter

READ_VERSION_COMMAND_ID = 0x06
READ_VERSION_COMMAND = [0xF3, 0xF4, 0x01, 0x00, 0x06, 0x06, 0xF4]

# define online apis, each name of the apis is the same with offline's
class api_format():
    def __init__(self):
        self.version = "v1.0"

class haloboard():
    def __init__(self, port_info):
        self.adapter = hd_adapter.adapter([port_info])

        self.current_mode = None
        self.version = None
        # self.adapter.common_link.register_process_function(READ_VERSION_COMMAND_ID, self.version_protocol_parse)

        self.remane_apis()
        self.__import_firefly()

    def __del__(self):
        print("haloboard del")
        self.adapter.__del__()

    # import firefly
    def __import_firefly(self):
        self.adapter.write_str_directly("from halo import *", service_id = 0x02)

    # button
    def __button_is_pressed(self):
        ret = self.adapter.read_async("button.is_pressed")
        if ret == None:
            return False
        else:
            return bool(ret)

    #led
    def __led_show_all(self, r, g, b):
        # self.adapter.write_async("led.show_all", "(%s, %s, %s)" %(r, g, b))
        self.adapter.write_imidiate_script("led.show_all", "(%s, %s, %s)" %(r, g, b))

    def __led_show_single(self, index, r , g, b):
        # self.adapter.write_async(("led.show_single", "(%s, %s, %s, %s)" %(index, r, g, b)))
        self.adapter.write_imidiate_script(("led.show_single", "(%s, %s, %s, %s)" %(index, r, g, b)))

    def __led_off_all(self):
        # self.adapter.write_async("led.off_all")
        self.adapter.write_imidiate_script("led.off_all")
    
    def __led_off_single(self, index):
        # self.adapter.write_async(("led.off_single", "(%s)" %(index,)))
        self.adapter.write_imidiate_script(("led.off_single", "(%s)" %(index,)))

    #vibration motor
    def __vibration_motor_on(self, value):
        self.adapter.write_async(("vibration_motor.on," "(%s)" %(value,)))

    def __vibration_motor_set_strength(self, value):
        self.adapter.write_async(("vibration_motor.set_strength", "(%s)" %(value,)))


    # music
    def __music_play_melody(self, name):
        self.adapter.write_imidiate_script(("music.play_melody",  "('%s')" %(name,)))

    def __music_play_melody_to_stop(self, name):
        self.adapter.write_imidiate_script(("music.play_melody_to_stop('%s')" %(name,)))


    def __music_play_tone(self, frequency, beat):
        self.adapter.write_imidiate_script(("music.play_tone", "(%s, %s)" %(frequency, beat)))

    def __music_stop_sounds(self):
        self.adapter.write_imidiate_script("music.stop_sounds")

    def __music_set_volume(self, volume):
        self.adapter.write_async(("music.set_volume", "(%s)" %(volume, )))


    def __music_get_volume(self):
        ret = self.adapter.read_async("music.get_volume")
        if ret == None:
            return 0
        else:
            return ret

    def __music_change_volume(self, change_value):
        self.adapter.write_async(("music.change_volume", "(%s)" %(change_value, )))

    # touchpad
    def __tp0_is_touched(self):
        ret = self.adapter.read_async("touchpad0.is_touched")
        if ret == None:
            return False
        else:
            return ret

    def __tp0_set_touch_threshold(self, value):
        self.adapter.write_async(("touchpad0.set_touch_threshold", "(%s)" %(value, )))

    def __tp0_get_value(self):
        ret = self.adapter.read_async("touchpad0.get_value")
        if ret == None:
            return 0
        else:
            return ret

    def __tp1_is_touched(self):
        ret = self.adapter.read_async("touchpad1.is_touched")
        if ret == None:
            return False
        else:
            return ret

    def __tp1_set_touch_threshold(self, value):
        self.adapter.write_async(("touchpad1.set_touch_threshold", "(%s)" %(value, )))

    def __tp1_get_value(self):
        ret = self.adapter.read_async("touchpad1.get_value")
        if ret == None:
            return 0
        else:
            return ret

    def __tp2_is_touched(self):
        ret = self.adapter.read_async("touchpad2.is_touched")
        if ret == None:
            return False
        else:
            return ret

    def __tp2_set_touch_threshold(self, value):
        self.adapter.write_async(("touchpad2.set_touch_threshold", "(%s)" %(value, )))

    def __tp2_get_value(self):
        ret = self.adapter.read_async("touchpad2.get_value")
        if ret == None:
            return 0
        else:
            return ret

    def __tp3_is_touched(self):
        ret = self.adapter.read_async("touchpad3.is_touched")
        if ret == None:
            return False
        else:
            return ret

    def __tp3_set_touch_threshold(self, value):
        self.adapter.write_async(("touchpad3.set_touch_threshold", "(%s)" %(value, )))

    def __tp3_get_value(self):
        ret = self.adapter.read_async("touchpad3.get_value")
        if ret == None:
            return 0
        else:
            return ret

    # microphone
    def __mic_get_loudness(self):
        ret = self.adapter.read_async("microphone.get_loudness")
        if ret == None:
            return 0
        else:
            return ret

    # wifi
    def __wifi_start(self, ssid = "Maker-guest", password = "makeblock", mode = 1):
        self.adapter.write_imidiate_script(("wifi.start", "(%s, %s, %s)" %(ssid, password, mode)))


    def __wifi_is_connected(self):
        self.adapter.write_imidiate_script("wifi.is_connected")


    # speech recognition    
    def __speech_recognition_start(self, server = 0, language = 0, time = 5):
        self.adapter.write_imidiate_script("speech_recognition.start", "(%s, %s, %s)" %(server, language, time))


    def __speech_recognition_get_result_code(self):
        self.adapter.write_imidiate_script("speech_recognition.get_result_code")
        if ret == None:
            return ''
        else:
            return ret

    # # motion sensor
    def __motion_sensor_get_acceleration(self, axis):
        ret = self.adapter.read_async("motion_sensor.get_acceleration", "('%s')" %(axis, ))
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_gyroscope(self, axis):
        ret = self.adapter.read_async("motion_sensor.get_gyroscope", "('%s')" %(axis, ))
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_rotation(self, axis):
        ret = self.adapter.read_async("motion_sensor.get_rotation", "('%s')" %(axis, ))
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_reset_rotation(self, axis = "all"):
        ret = self.adapter.write_imidiate_script("motion_sensor.reset_rotation", "('%s')" %(axis, ))

    def __motion_sensor_is_shaked(self):
        ret = self.adapter.read_async("motion_sensor.get_rotation")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_get_shake_strength(self):
        ret = self.adapter.read_async("motion_sensor.shake_strength")
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

    def __motion_sensor_is_arrow_up(self):
        ret = self.adapter.read_async("motion_sensor.is_arrow_up")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_is_arrow_down(self):
        ret = self.adapter.read_async("motion_sensor.is_arrow_down")
        if ret == None:
            return False
        else:
            return ret

    def __motion_sensor_get_pitch(self):
        ret = self.adapter.read_async("motion_sensor.get_pitch")
        if ret == None:
            return 0
        else:
            return ret

    def __motion_sensor_get_roll(self):
        ret = self.adapter.read_async("motion_sensor.get_roll")
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

    def __motion_sensor_get_gesture(self):
        return ''

    def remane_apis(self):
        # api rename
        self.button = api_format()
        self.button.is_pressed = self.__button_is_pressed

        self.led = api_format()
        self.led.show_all = self.__led_show_all
        self.led.show_single = self.__led_show_single
        self.led.off_single = self.__led_off_single
        self.led.off_all = self.__led_off_all

        self.vibration_motor = api_format()
        self.vibration_motor.set_strength = self.__vibration_motor_set_strength
        self.vibration_motor.on = self.__vibration_motor_on

        self.music = api_format()
        self.music.play_melody = self.__music_play_melody
        self.music.play_melody_to_stop = self.__music_play_melody_to_stop
        self.music.play_tone = self.__music_play_tone
        self.music.stop_sounds = self.__music_stop_sounds
        self.music.set_volume = self.__music_set_volume
        self.music.change_volume = self.__music_change_volume
        self.music.get_volume = self.__music_get_volume

        self.touchpad0 = api_format()
        self.touchpad1 = api_format()
        self.touchpad2 = api_format()
        self.touchpad3 = api_format()
        self.touchpad0.is_touched = self.__tp0_is_touched
        self.touchpad0.set_touch_threshold = self.__tp0_set_touch_threshold
        self.touchpad0.get_value = self.__tp0_get_value
        self.touchpad1.is_touched = self.__tp1_is_touched
        self.touchpad1.set_touch_threshold = self.__tp1_set_touch_threshold
        self.touchpad1.get_value = self.__tp1_get_value
        self.touchpad2.is_touched = self.__tp2_is_touched
        self.touchpad2.set_touch_threshold = self.__tp2_set_touch_threshold
        self.touchpad2.get_value = self.__tp2_get_value
        self.touchpad3.is_touched = self.__tp3_is_touched
        self.touchpad3.set_touch_threshold = self.__tp3_set_touch_threshold
        self.touchpad3.get_value = self.__tp3_get_value

        self.microphone = api_format()
        self.microphone.get_loudness = self.__mic_get_loudness

        self.motion_sensor = api_format()
        self.motion_sensor.get_acceleration = self.__motion_sensor_get_acceleration
        self.motion_sensor.get_gyroscope = self.__motion_sensor_get_gyroscope
        self.motion_sensor.get_rotation = self.__motion_sensor_get_rotation
        self.motion_sensor.reset_rotation = self.__motion_sensor_reset_rotation
        self.motion_sensor.is_shaked = self.__motion_sensor_is_shaked
        self.motion_sensor.get_shake_strength = self.__motion_sensor_get_shake_strength
        self.motion_sensor.is_tilted_left = self.__motion_sensor_is_tilted_left
        self.motion_sensor.is_tilted_right = self.__motion_sensor_is_tilted_right
        self.motion_sensor.is_arrow_up = self.__motion_sensor_is_arrow_up
        self.motion_sensor.is_arrow_down = self.__motion_sensor_is_arrow_down
        self.motion_sensor.get_pitch = self.__motion_sensor_get_pitch
        self.motion_sensor.get_roll = self.__motion_sensor_get_roll
        self.motion_sensor.get_yaw = self.__motion_sensor_get_yaw
        self.motion_sensor.get_gesture = self.__motion_sensor_get_gesture


    # other fiunctions
    def version_protocol_parse(self, frame):
        version_string = str(frame, "utf8")
        warn_print("version bytes is %s, string is %s" %(frame, version_string))
        self.version = version_string

    def get_device_version(self, max_time_s):
        self.version = None
        self.adapter.write_bytes_directly(bytearray(READ_VERSION_COMMAND))
        start = time.time()
        while self.version == None and time.time() - start < max_time_s:
            time.sleep(0.05)

        return self.version


