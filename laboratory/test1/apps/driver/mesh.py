import events.event_manager as event_manager
from global_objects import *
import json
import time

mesh_message_value_dict = dict()

def start(type = "node", mesh_id = (0x77,0x77,0x77,0x77,0x77,0x77), router_ssid = "hello", 
          router_password = "12345678", max_connection = 5, channel = 6):
    
    mesh_o.init()
    mesh_o.config(type = type, mesh_id = mesh_id, router_ssid = router_ssid, router_password = router_password,
                  max_connection = max_connection, channel = channel)
    mesh_o.start()

def get_number_of_nodes():
    return mesh_o.get_number_of_nodes()

# mesh boardcast
def on_mesh_message_come(msg):
    global mesh_message_value_dict
    info = json.loads(msg)

    if 'message' in info:
        event_manager.event_trigger(event_o.EVE_MESH_MESSAGE, str(info['message'], "utf8"))
        if info['message'] in mesh_message_value_dict:
            # indicate that the value is new
            mesh_message_value_dict[info['message']] = [info['value'], True]
        else:
            # indicate that the value is new
            mesh_message_value_dict.update({info['message']: [info['value'], True]})

def get_info(msg):
    global mesh_message_value_dict
    if msg in mesh_message_value_dict:
        ret = mesh_message_value_dict[msg][0]
        # indicate that the value is old
        mesh_message_value_dict[msg][1] = False
        return ret
    else:
        return ""

def get_info_status(msg):
    global mesh_message_value_dict
    if msg in mesh_message_value_dict:
        ret = mesh_message_value_dict[msg][1]
        return ret
    else:
        return False

# for online mode
serial_num = 0
def get_all_info_status():
    global mesh_message_value_dict, serial_num
    ret = [serial_num]
    for key in mesh_message_value_dict:
        if mesh_message_value_dict[key][1]:
            ret.append(key)
            mesh_message_value_dict[key][1] = False

    if len(ret) == 1:
        return []
    else:
        serial_num = (serial_num + 1) % 10
        return ret

def get_info_once(msg):
    global mesh_message_value_dict
    if msg in mesh_message_value_dict:
        if mesh_message_value_dict[msg][1]:
            mesh_message_value_dict[msg][1] = False
            ret = mesh_message_value_dict[msg][0]
        else:
            ret = None
        return ret
    else:
        return None

def broadcast(message, value = ""):
    message_str = json.dumps({'message': message, 'value': value})
    message_frame = build_message_frame(message_str)
    communication_o.send_with_protocol(communication_o.PHY_MESH_ID, communication_o.COMMON_PROTOCOL_GROUP_ID, message_frame)
    time.sleep(0.05)
    # event_manager.event_trigger(event_o.EVE_MESH_MESSAGE, message)
