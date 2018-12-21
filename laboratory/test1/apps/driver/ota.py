import makeblock

WIFI_MODE_STA = (1)
WIFI_MODE_AP = (2)

AP_SSID = 0
AP_PASSWORD = 1
STA_SSID = 2
STA_PASSWORD = 3
OTA_INFO_HOST = 4
OTA_INFO_URL = 5
OTA_BIN_HOST = 6
OTA_BIN_URL = 7

# ota
ota = makeblock.wifi_ota()

def ota_set_wifi_congfig_info(mode, config_option,data):
    if len(data) > 32:
        print("\n")
        print("data length error: %d\r\n" %len(data))
        return None

    if mode == WIFI_MODE_STA:
        if config_option == 0x01:
            ota.ota_config_set_wifi_info(STA_SSID, data)
        elif config_option == 0x02:
            ota.ota_config_set_wifi_info(STA_PASSWORD, data)
    elif mode == WIFI_MODE_AP:
        if config_option == 0x01:
            ota.ota_config_set_wifi_info(AP_SSID, data)
        elif config_option == 0x02:
            ota.ota_config_set_wifi_info(AP_PASSWORD, data)

def ota_set_wifi_ota_congfig_info(data):
    net_addr_type = data[1]
    # add codes to store url
    if net_addr_type == 1:
        ota.ota_config_set_wifi_info(OTA_INFO_HOST,data[3:])
    elif net_addr_type == 2:
        ota.ota_config_set_wifi_info(OTA_INFO_URL,data[3:])

def ota_set_wifi_start_ota_update():
    print("start ota update!!!")
    ota.ota_start()

