import time
from utility.common import *
from global_objects import *

from makeblock import timer_t
from makeblock import reset_timer_t
import makeblock

# driver
if makeblock.BATTERY_ENABLE:
    from driver.battery import battery
    battery = battery()

if makeblock.PIN_ENABLE:
    from driver.pin import pin
    pin0 = pin(0)
    pin1 = pin(1)
    pin2 = pin(2)
    pin3 = pin(3)

if makeblock.CLOCK_ENABLE:
    clock = makeblock.clock()
    print_dbg("clock enable")

if makeblock.GYRO_ENABLE:
    from driver.motion_sensor import motion_sensor
    motion_sensor = motion_sensor()
    print_dbg("gyro sensor enable")

if makeblock.BUTTON_ENABLE:
    from driver.button import button
    button = button()
    print_dbg("button enable")

if makeblock.LED_MATRIX_ENABLE:
    from driver.led import led
    led = led()
    print_dbg("led enable")

if makeblock.TOUCHPAD_ENABLE:
    from driver.touchpad import touchpad
    touchpad0 = touchpad(0)
    touchpad1 = touchpad(1)
    touchpad2 = touchpad(2)
    touchpad3 = touchpad(3)
    print_dbg("touchpad enable")

if makeblock.VIBRATION_MOTOR_ENABLE:
    from driver.vibration_motor import vibration_motor
    vibration_motor = vibration_motor()
    print_dbg("vibration motor enable")

# mesh
if makeblock.WIFI_MESH_ENABLE:
    import driver.mesh as mesh

# wifi
if makeblock.WIFI_ENABLE:
    from driver.wifi import wifi
    wifi = wifi()

#speech recognition
if makeblock.SPEECH_RECOGNITION_ENABLE:
    import driver.speech_recognition as speech_recognition

# music
if makeblock.MUSIC_ENABLE:
    import music.speaker as speaker_t
    speaker = speaker_t.speaker()
    print_dbg("music enable")

# i2c mic
if makeblock.I2S_MIC_ENABLE:
    from driver.mic import mic
    microphone = mic()
    print_dbg("microphone enable")
  
# cloud message
if makeblock.WIFI_ENABLE:
    import driver.cloud_message as cloud_message

# for timer
def get_timer():
    return timer_t()

def reset_timer():
    reset_timer_t()

# stop script
if makeblock.STOP_PYTHON_THREAD_ENABLE:
    stop_this_script = stop_script_o.stop_this_script
    stop_other_scripts = stop_script_o.stop_other_script
    stop_all_scripts = stop_script_o.stop_all_script

reset_timer()

