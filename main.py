import hardware.atombit as atombit 
import time
import random

time.sleep(1)
atombit.led.show_all(255, 0, 0)
time.sleep(1)
atombit.led.show_all(0, 255, 0)


while True:
    if atombit.button.is_pressed():
        atombit.led.show_all(100, 0, 0)
    else:
        atombit.led.show_all(0, 0, 0)

    # print(atombit.led.show_all(atombit.microphone.get_loudness(), 0 , 0))
    # print(atombit.touchpad1.get_value())
    # else:
        # atombit.led.show_all(0, 0, 0)
    # time.sleep(0.05)
    # atombit.led.show_all(0, 100, 0)
    # time.sleep(0.05)
    # atombit.led.show_all(0, 0, 100)
    time.sleep(0.05)
