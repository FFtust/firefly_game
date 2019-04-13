#import halo
import time
import hardware
halo = hardware.haloboard('COM29')

while True:
    a = halo.button.is_pressed()
    if a:
        halo.led.show_all(100, 0, 100)
        time.sleep(1)
        halo.led.show_all(0, 0, 0)
        time.sleep(1)
    time.sleep(0.05)