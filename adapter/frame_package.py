# -*- coding: utf-8 -*-  
from struct import pack, unpack

COMMON_PROTOCOL_HEAD = 0xF3
COMMON_PROTOCOL_END = 0xF4

ONLINE_CMD_ID = 0x28
PROTOCOL_SUBSCRIBE_ID = 0x29

# script to prtocol frame
def create_frame(servive_id, exec_str, serial_num = 0):
    protocol_frame = bytearray()
    protocol_frame.append(COMMON_PROTOCOL_HEAD)
    
    # protocol_id + service_id + serial num(2) + strlen + '\0' 
    datalen = 1 + 1 + 2 + len(exec_str) + 1
    data_len_byte = datalen.to_bytes(2, "little")

    head_check = (data_len_byte[0] + data_len_byte[1] + COMMON_PROTOCOL_HEAD) & 0xFF

    # add head check
    protocol_frame.append(head_check)
    protocol_frame += data_len_byte

    data_sum = 0  
    # add protocol id
    protocol_frame.append(ONLINE_CMD_ID)
    data_sum += ONLINE_CMD_ID
    
    # add servive id
    protocol_frame.append(servive_id)
    data_sum += servive_id
    
    # add serial num, 2 bytes
    serial_num_bytes = serial_num.to_bytes(2, "little")
    protocol_frame += serial_num_bytes
    data_sum += serial_num_bytes[0]
    data_sum += serial_num_bytes[1]
    
    # add script bytes
    strbytes = bytes(exec_str, "utf8")
    protocol_frame += strbytes
    for i in range(len(strbytes)):
        data_sum += strbytes[i]
    # add string end code
    protocol_frame.append(0x00)

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
 

