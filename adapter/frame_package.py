# -*- coding: utf-8 -*-  
from struct import pack, unpack
from firefly_online.config import *
from firefly_online.utils.common import *

COMMON_PROTOCOL_HEAD = 0xF3
COMMON_PROTOCOL_END = 0xF4

ONLINE_CMD_ID = 0x28
PROTOCOL_SUBSCRIBE_ID = 0x29

def __string0_package(string):
    ret_frame = bytearray()
    strbytes = bytes(string, "utf8")
    ret_frame += strbytes
    # add string end code
    ret_frame.append(0x00)    
    
    return ret_frame

def __string_package(string):
    ret_frame = bytearray()
    l = len(string) & 0xff
    # add string len, one byte
    ret_frame.append(l) 
    strbytes = bytes(string, "utf8")
    if len(strbytes) > 255:
        ret_frame += strbytes[0 : 256]
    else:
        ret_frame += strbytes
    
    return ret_frame
 
def __bigstring_package(string):
    ret_frame = bytearray()
    l = len(string)
    l_bytes = int_to_byte_2(l)
    # add string len, two bytes
    ret_frame += l_bytes
    strbytes = bytes(string, "utf8")
    ret_frame += strbytes
    
    return ret_frame

# script to prtocol frame
def create_frame(servive_id, exec_str, serial_num = 0):
    protocol_frame = bytearray()
    protocol_frame.append(COMMON_PROTOCOL_HEAD)
    
    if SERVICE_ID_ENABLE:
        service_byte_len = 1
    else:
        service_byte_len = 0


    if SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_BIGSTRING:
        # protocol_id + service_id + serial num + strlen(2)
        datalen = 1 + service_byte_len + SERIAL_NUM_LEN + 2 + len(exec_str)

    elif SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_STRING:
        # protocol_id + service_id + serial num + strlen
        datalen = 1 + service_byte_len + SERIAL_NUM_LEN + 1 + len(exec_str)       
    elif SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_STRING0:
        # protocol_id + service_id + serial num + '\0'
        datalen = 1 + service_byte_len + SERIAL_NUM_LEN + len(exec_str) + 1  

    data_len_byte = datalen.to_bytes(2, "little")

    head_check = (data_len_byte[0] + data_len_byte[1] + COMMON_PROTOCOL_HEAD) & 0xFF

    # add head check
    protocol_frame.append(head_check)
    protocol_frame += data_len_byte

    data_sum = 0  
    # add protocol id
    protocol_frame.append(ONLINE_CMD_ID)
    data_sum += ONLINE_CMD_ID
    
    if SERVICE_ID_ENABLE:
        # add servive id
        protocol_frame.append(servive_id)
        data_sum += servive_id
    
    # add serial num, 2 bytes
    if SERIAL_NUM_LEN == 2:
        serial_num_bytes = serial_num.to_bytes(2, "little")
        protocol_frame += serial_num_bytes
        data_sum += serial_num_bytes[0]
        data_sum += serial_num_bytes[1]
    elif SERIAL_NUM_LEN == 1:
        protocol_frame.append(serial_num)
        data_sum += serial_num

    # add script bytes
    if SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_BIGSTRING:
        strbytes = __bigstring_package(exec_str)  
    elif SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_STRING:
        strbytes = __string_package(exec_str) 
    elif SCRIPT_PACKAGE_TYPE == SCRIPT_PACKAGE_TYPE_STRING0:
        strbytes = __string0_package(exec_str)
        
    protocol_frame += strbytes
    for i in range(len(strbytes)):
        data_sum += strbytes[i]

    data_sum = data_sum & 0xFF
    protocol_frame.append(data_sum)   
    protocol_frame.append(COMMON_PROTOCOL_END)  
    
    # print("whole frame", protocol_frame)
    
    return protocol_frame

def print_frame(frame):
    out_str = ""
    for i in range(len(frame)):
        temp = ('%2x' %frame[i])
        temp = temp.replace(" ", "0")
        out_str += temp
        out_str += " "
    print(out_str)

    out_str = ""
    for i in range(len(frame)):
        temp = ('%2x' %frame[i])
        temp = temp.replace(" ", "0")
        temp = "0x" + temp.replace(" ", "0") + ','
        out_str += temp
        out_str += " "

    print(out_str)
 

