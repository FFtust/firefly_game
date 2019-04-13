import time
import threading
from firefly_online.utils.common import *
from firefly_online.config import *

# config
DATA_UPDATE_SYNC_LOCK_ENABLE = False


# realization
PROTOCOL_SUBSCRIBE_ID = 0x29

class subscribe_item_structure():
    def __init__(self):
        self.value = None
        self.value_update_flag = False
        self.value_update_cb = None
        if DATA_UPDATE_SYNC_LOCK_ENABLE:
            self.value_update_sync_lock = threading.Lock()

def get_json_string(frame):
    if SERVICE_ID_ENABLE:
        service_len = 1
    else:
        service_len = 0

    if SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_BIGSTRING:
        json_string = str(frame[2 + service_len :], "utf8")
    elif SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_STRING:
        json_string = str(frame[1 + service_len :], "utf8")
    elif SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_STRING0:
        json_string = str(frame[service_len : -1], "utf8")

    return json_string

class hardware_data():
    def __init__(self):
        self.sensor_data = {}
    
    def data_parse(self, frame):
        json_item = eval(get_json_string(frame))
 
        print(frame, json_item)
        for key in json_item:
            if key in self.sensor_data:
                self.sensor_data[key].value = json_item[key]
            else:
                self.sensor_data[key] = subscribe_item_structure()
                self.sensor_data[key].value = json_item[key]

            self.value_update_flag = True
            if DATA_UPDATE_SYNC_LOCK_ENABLE:
                if self.sensor_data[key].value_update_sync_lock.locked():
                    self.sensor_data[key].value_update_sync_lock.release()
            # print("sensor value dict", self.sensor_data[key].value)


        # print("sensor value dict", self.sensor_data)

    def set_value_status(self, value_key, status):
        if value_key in self.sensor_data:
            self.sensor_data[value_key].value_update_flag = status

    def get_value_status(self, value_key):
        if value_key in self.sensor_data:
            return self.sensor_data[value_key].value_update_flag

    def wait_value_update(self, value_key):
        if DATA_UPDATE_SYNC_LOCK_ENABLE:
            self.sensor_data[key].value_update_sync_lock.acquire(1)
        else:
            while not self.sensor_data[value_key].value_update_flag:
                time.sleep(0.005)

    def wait_value_first_update(self, value_key, max_wait_time = 500):
        start = time.time()
        while (not (value_key in self.sensor_data)) and (time.time() - start) * 1000 < max_wait_time:
            time.sleep(0.05)

    def get_whole_data(self):
        return self.sensor_data