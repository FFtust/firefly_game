import _thread
import time
from utility.common import *
from global_objects import *
import makeblock

EVENT_THREAD_DEFAULT_STACK_SIZE = 1024 * 12
EVENT_THREAD_DEFAULT_PRIORITY = 1

EVENT_STATUS_FATAL_ERROR = -1
EVENT_STATUS_READY = 1

events_info = [None] * event_o.EVE_MAX_NUM

def T__is_event_id_valid(eve_id):
    if eve_id >= 0 and eve_id < event_o.EVE_MAX_NUM:
        return True
    else:
        return False

def __event_info_set(eve_id, value):
    global events_info
    if T__is_event_id_valid(eve_id):
        events_info[eve_id] = value

class event_class(object):
    def __init__(self, event_type, trigger_type, user_cb, user_para = 0, \
                 stack_size = EVENT_THREAD_DEFAULT_STACK_SIZE, priority = EVENT_THREAD_DEFAULT_PRIORITY):
        self.eve_id = event_o.event_register(event_type, trigger_type, user_para)
        if T__is_event_id_valid(self.eve_id):
            self.user_cb = user_cb
            self.user_para = user_para
            self.stack_size = stack_size
            self.priority = priority
            self.event_status = EVENT_STATUS_READY
        else:
            self.user_cb = None
            self.user_para = None
            self.stack_size = None
            self.priority = None
            self.event_status = EVENT_STATUS_FATAL_ERROR
            print_dbg("event register failed")

    def is_event_valid(self):
        if T__is_event_id_valid(self.eve_id) and self.event_status != EVENT_STATUS_FATAL_ERROR:
            return True
        else:
            return False

class event_operation(object):
    def __init__(self, event_class):
        self.eve_id = event_class.eve_id
        self.cb = event_class.user_cb
        self.stack_size = event_class.stack_size
        self.priority = event_class.priority

    def __event_cb_task(self):
        # only call this function once at the top of thread function
        if makeblock.STOP_PYTHON_THREAD_ENABLE:
            thread_id = stop_script_o.add_thread()
        while True:
            event_o.clear_sync(self.eve_id)
            KeyboardInterrupt_flag = False
            try:
                while True:
                    if T__is_event_id_valid(self.eve_id):
                        if makeblock.STOP_PYTHON_THREAD_ENABLE:
                            stop_script_o.set_thread_sta(thread_id, stop_script_o.THREAD_RESTARTED)
                        if event_o.wait_trigger(self.eve_id) == True:
                            # Call user callback function
                            if function_type_check(self.cb):
                                if makeblock.STOP_PYTHON_THREAD_ENABLE:
                                    stop_script_o.set_thread_sta(thread_id, stop_script_o.THREAD_EXECUTING)
                                self.cb()
                            event_o.clear_sync(self.eve_id)
                        else:
                            continue
                    else:
                        print_dbg("eve_id is null")
                        time.sleep(10)
            # if error occured in the callback, the sema RAM will be freed, 
            # but other function will still use this sema, then a fatal system error happend
            # catch the exception and make this task never out is a temporary solution
            except KeyboardInterrupt:
                # it's a proactive error, restart the thread only
                # we make tiis exception a reserved one
                if makeblock.STOP_PYTHON_THREAD_ENABLE:
                    stop_script_o.set_thread_sta(thread_id, stop_script_o.THREAD_RESTARTED)
                print("restart the thread proactively", "id is", self.eve_id)
                KeyboardInterrupt_flag = True

            # when error occured, set the item in event_sema_list to None, 
            # idicating that this callback had been destroyed
            if not KeyboardInterrupt_flag:
                if makeblock.STOP_PYTHON_THREAD_ENABLE:
                    stop_script_o.set_thread_sta(thread_id, stop_script_o.THREAD_FATAL_ERROR)
                
                if T__is_event_id_valid(self.eve_id):
                    __event_info_set(self.eve_id, None)
                print("event:", self.eve_id, "error occured:")
                print("free the memory of this callback")
                break

    def __event_execute_cb(self):
        _thread.stack_size(self.stack_size)
        _thread.start_new_thread(self.__event_cb_task, (), self.priority, 2)
  
    def event_listening_start(self):
        self.__event_execute_cb()

######################################################################################
def event_trigger(eve_type, parameter = None):
    event_o.trigger_by_type(eve_type, parameter)

def event_register(event_type, trigger_type, user_cb, user_para = 0, stack_size = EVENT_THREAD_DEFAULT_STACK_SIZE):
    global events_info
    event = event_class(event_type, trigger_type, user_cb, user_para, stack_size)
    if event.is_event_valid():
        __event_info_set(event.eve_id, event)
    elif T__is_event_id_valid(event.eve_id):
        __event_info_set(event.eve_id, None)
        print("event register failed, id is valid")
    else:
        print("event register failed")

def event_system_start():
    for item in events_info:
        if item != None:
            ope = event_operation(item)
            ope.event_listening_start()
    event_o.trigger_enable()

