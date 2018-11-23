import hardware
import time
import random
import math

codey = hardware.codey('COM29')
haloboard = hardware.haloboard('COM28')
# haloboard2 = hardware.haloboard_class.haloboard('COM27')
rocky = hardware.rocky(codey)
codey.speaker.play_melody('hello.wav')
while True:
    if haloboard.motion_sensor.is_tilted_left():
        codey.led.show(100, 0, 0)
        rocky.turn_left(20)
    elif haloboard.motion_sensor.is_tilted_right():
        codey.led.show(0, 100, 0)
        rocky.turn_right(20)
    elif haloboard.motion_sensor.is_arrow_up():
        codey.led.show(100, 100, 0)
        rocky.forward(20)
    elif haloboard.motion_sensor.is_arrow_down():
        codey.led.show(100, 100, 100)
        rocky.backward(20)
    else:
        rocky.stop()
        
    if haloboard.touchpad0.is_touched():
        codey.speaker.play_melody_until_done('hello.wav')
        time.sleep(0.5)
    elif haloboard.touchpad1.is_touched():
        codey.speaker.play_melody_until_done('score.wav')
        time.sleep(0.5)
    elif haloboard.touchpad2.is_touched():
        codey.speaker.play_melody_until_done('sad.wav')
        time.sleep(0.5)
    elif haloboard.touchpad3.is_touched():
        codey.speaker.play_melody_until_done('score.wav')
        time.sleep(0.5)


    time.sleep(0.04)
# time.sleep(1)
# haloboard.led.show_all(255, 0, 0)
# # haloboard1.led.show_all(255, 0, 0)
# # haloboard2.led.show_all(255, 0, 0)
# time.sleep(1)
# haloboard.led.show_all(0, 255, 0)
# haloboard1.led.show_all(0, 255, 0)
# haloboard2.led.show_all(0, 255, 0)

# while True:
#     if haloboard.motion_sensor.is_tilted_left():
#         haloboard1.led.show_all(100, 0, 0)
#         haloboard2.led.show_all(100, 0, 0)
#     elif haloboard.motion_sensor.is_tilted_right():
#         haloboard1.led.show_all(0, 0, 0)
#         haloboard2.led.show_all(0, 0, 0)

#     if haloboard1.motion_sensor.is_tilted_left():
#         haloboard1.led.show_all(100, 0, 0)
#     elif haloboard1.motion_sensor.is_tilted_right():
#         haloboard1.led.show_all(0, 0, 0)    


#     # value = math.fabs(math.sin(a / 40)) * 100
#     # haloboard.led.show_all(value, 0, 0)
#     # a = (a + 1)

#     if haloboard.button.is_pressed():
#         haloboard.led.show_all(0, 100, 0)
#     if haloboard1.button.is_pressed():
#         haloboard1.led.show_all(0, 100, 0)

#     # print(haloboard.led.show_all(haloboard.microphone.get_loudness(), 0 , 0))
#     # print(haloboard.touchpad1.get_value())
#     # else:
#         # haloboard.led.show_all(0, 0, 0)
#     # time.sleep(0.05)
#     # haloboard.led.show_all(0, 100, 0)
#     # time.sleep(0.05)
#     # haloboard.led.show_all(0, 0, 100)
#     time.sleep(0.025)

# print('Done')
# time.sleep(10)
# print('Done22')