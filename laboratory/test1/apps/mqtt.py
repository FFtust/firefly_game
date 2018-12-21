import time
import simple_mqtt

class MQTTClient(simple_mqtt.MQTTClient):

    reconnect_flag = False
    MQTT_DEBUG = False

    def log(self, in_reconnect, e):
        if self.MQTT_DEBUG:
            if in_reconnect:
                print("publish: %r" % e)
            else:
                print("wait_msg: %r" % e)

    def get_reconnect_flag(self):
        return self.reconnect_flag

    def set_reconnect_flag(self, flag):
        self.reconnect_flag = flag

    def publish(self, topic, msg, retain=False, qos=0):
        while True:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(True, e)
                super().disconnect()
                self.set_reconnect_flag(True)
                break

    def wait_msg(self):
        while True:
            try:
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
                super().disconnect()
                self.set_reconnect_flag(True)
                break
