import makeblock
from global_objects import speech_recognition_o
from utility.common import *
from global_objects import *
import json
import time

LAN_DEFAULT        = speech_recognition_o.LAN_DEFAULT
LAN_CHINESE        = speech_recognition_o.LAN_CHINESE
LAN_ENGLISH        = speech_recognition_o.LAN_ENGLISH
LAN_GERMAN         = speech_recognition_o.LAN_GERMAN
LAN_FRENCH         = speech_recognition_o.LAN_FRENCH
LAN_SPANISH        = speech_recognition_o.LAN_SPANISH
LAN_ID_MAX         = speech_recognition_o.LAN_ID_MAX
SERVER_BAIDU       = speech_recognition_o.SERVER_BAIDU
SERVER_MICROSOFT   = speech_recognition_o.SERVER_MICROSOFT
SERVER_AMAZON      = speech_recognition_o.SERVER_AMAZON
SERVER_ID_MAX      = speech_recognition_o.SERVER_ID_MAX

# microsoft as default server
current_server = SERVER_MICROSOFT
current_language = LAN_CHINESE

def start(server = SERVER_MICROSOFT, language = LAN_CHINESE, time_s = 5, wait_flag = True):
    global current_server
    global current_language
    
    time.sleep(0.1)
    # check if wifi is connected
    if not wifi_o.is_sta_connected():
        return

    time_s = int(num_range_scale(time_s, 1, 10))

    if server > SERVER_ID_MAX or server < SERVER_BAIDU:
        server = SERVER_MICROSOFT

    if language > LAN_ID_MAX or language < LAN_DEFAULT:
        server = LAN_CHINESE

    # this api will blocked until receiving the response of speech recognition 
    speech_recognition_o.start(int(server), int(language), int(time_s), int(wait_flag))
    
    current_server = server
    current_language = language

def set_token(server, token):
    if server > SERVER_ID_MAX or server < SERVER_BAIDU:
        server = SERVER_MICROSOFT

    speech_recognition_o.set_token(int(server), str(token))

def set_account(server, account, password):
    if server > SERVER_ID_MAX or server < SERVER_BAIDU:
        server = SERVER_MICROSOFT

    speech_recognition_o.set_account(int(server), str(account), str(password))

def set_token_url(server, url):
    if server > SERVER_ID_MAX or server < SERVER_BAIDU:
        server = SERVER_MICROSOFT

    speech_recognition_o.set_token_url(int(server), str(token))

def set_recognition_url(server, url):
    if server > SERVER_ID_MAX or server < SERVER_BAIDU:
        server = SERVER_MICROSOFT

    speech_recognition_o.set_recognition_url(int(server), str(url))

def set_wait_time(time_s):
    if type_check(time_s, (int, float)):
        time_s = 30
    time_s = int(num_range_scale(time_s, 5, 50))

    speech_recognition_o.set_wait_time(time_s * 1000)

def get_all_respond():
    return speech_recognition_o.get_all_respond()

def get_error_code():
    global current_server
    respond = speech_recognition_o.get_all_respond()
    if(respond == ""):
        return 3334
    if (respond == "error"):
        return 3335

    info = json.loads(respond)
    if current_server == SERVER_BAIDU:
        if 'err_no' in info:
            if type(info['err_no']) == int:
                return info['err_no']
    elif current_server == SERVER_MICROSOFT:
        if 'code' in info:
            if type(info['code']) == int:
                return info['code']
    else:
        return 3333

def get_error_message():
    global current_server
    respond = speech_recognition_o.get_all_respond()
    if(respond == ""):
        return "response timeout"
    if (respond == "error"):
        return "http client error"

    info = json.loads(respond)
    if current_server == SERVER_BAIDU:
        if 'err_msg' in info:
            return info['err_msg']
    elif current_server == SERVER_MICROSOFT:
        if 'data' in info:
            data_region = info['data']
            if 'RecognitionStatus' in data_region:
                return data_region['RecognitionStatus']            
    else:   
        return "unknow error"

def get_result_code():
    global current_server
    global current_language
    respond = speech_recognition_o.get_all_respond()
    if(respond == ""):
        return ""
    info = json.loads(respond)
    if current_server == SERVER_BAIDU:
        if 'err_no' in info:
            if info['err_no'] == 0:
                if 'result' in info:
                    return info['result'][0]
    elif current_server == SERVER_MICROSOFT:
        if 'data' in info:
            data_region = info['data']
            if 'DisplayText' in data_region:
                if current_language != LAN_CHINESE:
                    return data_region['DisplayText'].lower()
                else:
                    return data_region['DisplayText'] 

    return ""

def get_sn_code():
    respond = speech_recognition_o.get_all_respond()
    if(respond == ""):
        return 0
    info = json.loads(respond)
    if 'sn' in info:
        return info['sn']
    else:
        return 0