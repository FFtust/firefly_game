from utility.common import *
from global_objects import *
import makeblock

# event type definition
if makeblock.EVENT_ENABLE:
    import events.event_manager as event_manager
    print_dbg("event enable")

    def start(callback):
        event_manager.event_register(event_o.EVE_SYSTEM_LAUNCH, event_o.TRIGGER_ALWAYS_WITH_NO_PARAMETER, callback, None)

    def received(mstr):
        def decorator(callback):
            if type_check(mstr, str):
                mstr_str = str(mstr)
            event_manager.event_register(event_o.EVE_MESSAGE, event_o.TRIGGER_BY_STRING_MATCHING, callback, mstr_str)
        return decorator

    def cloud_message(mstr):
        def decorator(callback):
            if type_check(mstr, str):
                mstr_str = str(mstr)
            event_manager.event_register(event_o.EVE_CLOUD_MESSAGE, event_o.TRIGGER_BY_STRING_MATCHING, callback, mstr_str)
        return decorator

    def mesh_message(mstr):
        def decorator(callback):
            if type_check(mstr, str):
                mstr_str = str(mstr)
            event_manager.event_register(event_o.EVE_MESH_MESSAGE, event_o.TRIGGER_BY_STRING_MATCHING, callback, mstr_str)
        return decorator

    def greater_than(threshold, type):
        def decorator(callback):
            if not type_check(threshold, (int, float)):
                return
            threshold_data = threshold
            if threshold_data < 0:
                threshold_data = 0
            type_str = type
            if type_str == "microphone":
                event_manager.event_register(event_o.EVENT_MICROPHONE, event_o.TRIGGER_ONCE_BY_VALUE_LARGER, callback, threshold_data)
            elif type_str == "timer":
                event_manager.event_register(event_o.EVE_TIME_OVER, event_o.TRIGGER_ONCE_BY_VALUE_LARGER, callback, threshold_data)
        return decorator

    if makeblock.GYRO_ENABLE:
        def shaked(callback):              
            event_manager.event_register(event_o.EVENT_SHAKED, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def tilted_left(callback):
            event_manager.event_register(event_o.EVENT_TILT_LEFT, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def tilted_right(callback):
            event_manager.event_register(event_o.EVENT_TILT_RIGHT, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def arrow_down(callback):
            event_manager.event_register(event_o.EVENT_TILT_FORWARD, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def arrow_up(callback):
            event_manager.event_register(event_o.EVENT_TILT_BACKWARD, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

    if makeblock.BUTTON_ENABLE:
        def button_pressed(callback):
            event_manager.event_register(event_o.EVENT_BUTTON, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

    if makeblock.TOUCHPAD_ENABLE:
        def touchpad0_active(callback):
            event_manager.event_register(event_o.EVENT_TOUCHPAD_0, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def touchpad1_active(callback):
            event_manager.event_register(event_o.EVENT_TOUCHPAD_1, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def touchpad2_active(callback):
            event_manager.event_register(event_o.EVENT_TOUCHPAD_2, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)

        def touchpad3_active(callback):
            event_manager.event_register(event_o.EVENT_TOUCHPAD_3, event_o.TRIGGER_ONCE_BY_VALUE_TRUE, callback, None)