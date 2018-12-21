from global_objects import wifi_o
import time

class wifi():
    def __init__(self):
        self.WLAN_MODE_NULL   = wifi_o.WLAN_MODE_NULL
        self.WLAN_MODE_STA    = wifi_o.WLAN_MODE_STA
        self.WLAN_MODE_AP     = wifi_o.WLAN_MODE_AP
        self.WLAN_MODE_APSTA  = wifi_o.WLAN_MODE_APSTA
        self.WLAN_MODE_MESH   = wifi_o.WLAN_MODE_MESH

        self.mode = self.WLAN_MODE_NULL
        self.connecting_ssid = ''
        self.connecting_pass = ''

    def is_connected(self):
        time.sleep(0.05)
        return wifi_o.is_sta_connected()

    def set_mode(mode):
        wifi_o.set_mode(mode)

    def connect(self):
        time.sleep(0.05)
        wifi_o.sta_connect()

    def disconnect(self):
        time.sleep(0.05)
        wifi_o.sta_disconnect()

    # only the two function below face to users
    def start(self, ssid, password, mode = wifi_o.WLAN_MODE_STA):
        ssid = str(ssid)
        password = str(password)
        if self.WLAN_MODE_STA == mode:
            wifi_o.set_mode(mode)
            wifi_o.sta_config(ssid, password)

            if (ssid != self.connecting_ssid) or (password != self.connecting_pass):
                self.connecting_ssid = ssid
                self.connecting_pass = password
                wifi_o.sta_disconnect()
                time.sleep(0.1)
                wifi_o.start()
                self.mode = mode
            else:
                if not wifi_o.is_sta_connected():
                    wifi_o.sta_connect()
        time.sleep(0.1)
