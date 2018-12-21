import time
import makeblock


def reboot_init():
    if makeblock.LED_MATRIX_ENABLE:
        from driver.led import led
        led = led()
        led.off_all()
        del led

    if makeblock.MUSIC_ENABLE:
        makeblock.music().stop()

    if makeblock.VIBRATION_MOTOR_ENABLE:
        from driver.vibration_motor import vibration_motor
        vibration_motor = vibration_motor()
        vibration_motor.on(0)
        del vibration_motor

    if makeblock.PIN_ENABLE:
        from driver.pin import pin
        pin0 = pin(0)
        pin1 = pin(1)
        pin2 = pin(2)
        pin3 = pin(3)
        pin0.is_touched()
        pin1.is_touched()
        pin2.is_touched()
        pin3.is_touched()
        del pin0
        del pin1
        del pin2
        del pin3

if __name__ == '__main__':
    reboot_init()