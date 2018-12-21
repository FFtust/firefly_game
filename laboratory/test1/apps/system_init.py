import time
import _thread
import utility.utility as utility

import makeblock

from global_objects import *


def sys_init():
    if makeblock.NEURONS_ENGINE_ENABLE:
        import neurons_protocol.neurons_protocol_parse as neurons_protocol_parse
        neurons_protocol_o = neurons_protocol_parse.neurons_protocol()
        neurons_protocol_o.bind_to_phy(communication_o.PHY_UART1_ID)
        neurons_protocol_o.start()

    time.sleep(0.1)
    print("system init successed")



if __name__ == '__main__':
    sys_init()

