import time
import events.event_manager as event_manager
from global_objects import *
from makeblock import reset_timer_t

def event_sys_start():
    event_manager.event_system_start()

def main_loop():
    event_sys_start()
    # reserve 0.1s to start thread firstly
    time.sleep(0.1)
    # system start, trigger start event
    event_manager.event_trigger(event_o.EVE_SYSTEM_LAUNCH)

    # do something about system here
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main_loop()