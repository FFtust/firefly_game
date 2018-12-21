import makeblock
from mqtt import MQTTClient
import events.event_manager as event_manager
import _thread
from global_objects import *
import time
import json
import time

MQTT_DEBUG = False

cloud_message_enable = False; 
cloud_message_topic = "USER/YANMINGE/MESSAGE";

CLOUD_MESSAGE_THREAD_STACK_SIZE = 8 * 1024
CLOUD_MESSAGE_THREAD_PRIORITY  =  1

cloud_message_value_dict = dict()

cloud_message_client = MQTTClient(client_id="", server = "mq.makeblock.com", port = 1883, user = None, password = None, keepalive = 60, ssl = False)

def log(in_reconnect, e):
    if MQTT_DEBUG:
        if in_reconnect:
            print("cloud_message reconnect: %r" % e)
        else:
            print("cloud_message: %r" % e)

def on_message_come(topic, msg):
    global cloud_message_value_dict
    info = json.loads(msg)
    if 'message' in info:
        event_manager.event_trigger(event_o.EVE_CLOUD_MESSAGE, str(info['message'], "utf8"))
        if info['message'] in cloud_message_value_dict:
            cloud_message_value_dict[info['message']] = info['value']
        else:
            cloud_message_value_dict.update({info['message']: info['value']})

def get_info(msg):
    global cloud_message_value_dict
    if msg in cloud_message_value_dict:
        return cloud_message_value_dict[msg]
    else:
        return ""

def subscribe_message_received():
    global cloud_message_enable
    global cloud_message_topic
    while True:
        if cloud_message_enable == False and wifi_o.is_sta_connected():
            try:
                cloud_message_client.connect(clean_session = True)
                cloud_message_client.set_callback(on_message_come)
                cloud_message_client.subscribe(cloud_message_topic, qos = 0)
                cloud_message_enable = True
                cloud_message_client.set_reconnect_flag(False)
            except OSError as e:
                log(True, e)
                time.sleep(2)
                cloud_message_enable = False

        if cloud_message_enable:
            cloud_message_client.wait_msg()
            if cloud_message_client.get_reconnect_flag():
                # print("reconnect")
                cloud_message_enable = False

def start(topic_head = "USER/YANMINGE/MESSAGE", client_id = None, server = "mq.makeblock.com", port = 1883, user = None, password = None, keepalive = 60, ssl = False):
    global cloud_message_topic   
    cloud_message_client.__init__(client_id, server, port, user, password, keepalive, ssl)
    _thread.stack_size(CLOUD_MESSAGE_THREAD_STACK_SIZE)
    _thread.start_new_thread(subscribe_message_received, (), CLOUD_MESSAGE_THREAD_PRIORITY)
    cloud_message_topic = topic_head
    cloud_message_client.start_mqtt_check_keepalive()


def broadcast(message, value = ""):
    global cloud_message_enable
    global cloud_message_topic
    message_str = json.dumps({ 'message': message, 'value': value})
    if cloud_message_enable:
        cloud_message_client.publish(cloud_message_topic, message_str, retain = False, qos = 0)

