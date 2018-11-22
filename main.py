import hardware.haloboard as haloboard 
import time
import random
import math

time.sleep(1)
haloboard.led.show_all(255, 0, 0)
time.sleep(1)
haloboard.led.show_all(0, 255, 0)

a = 1
while True:
    value = math.fabs(math.sin(a / 40)) * 100
    haloboard.led.show_all(value, 0, 0)
    a = (a + 1)

    # if haloboard.button.is_pressed():
    #     haloboard.led.show_all(100, 0, 0)
    # else:
    #     haloboard.led.show_all(0, 100, 0)
    
    # print(haloboard.led.show_all(haloboard.microphone.get_loudness(), 0 , 0))
    # print(haloboard.touchpad1.get_value())
    # else:
        # haloboard.led.show_all(0, 0, 0)
    # time.sleep(0.05)
    # haloboard.led.show_all(0, 100, 0)
    # time.sleep(0.05)
    # haloboard.led.show_all(0, 0, 100)
    # time.sleep(0.05)
