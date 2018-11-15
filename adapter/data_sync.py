import time
import threading
from utils.common import *
from config import BIGSTRING_ENABLE

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

class hardware_data():
    def __init__(self):
        self.sensor_data = {}
    
    def data_parse(self, frame):
        if BIGSTRING_ENABLE:
            json_item = eval(str(frame[3 :], "utf8"))
        else:
            json_item = eval(str(frame[1 : -1], "utf8"))
        # print(json_item)
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
        max_count = max_wait_time // 50
        count = 0
        while not (value_key in self.sensor_data):
            time.sleep(0.05)
            count += 1    
            if count > max_count:
                print('wait first update max time')
                break

    def get_whole_data(self):
        return self.sensor_data