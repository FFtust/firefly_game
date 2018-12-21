from struct import pack, unpack
import time
import re
import os
import _thread

# cofig if use existed dictionaries
USE_DICT_CREATED_PRIVIOUSLY = True

POLLING_TIME_FOR_ASSIGNMENT_ID = 0.5 # unit: second
HEART_PACKAGE_THREAD_STACK_SIZE = 8 * 1024
HEART_PACKAGE_THREAD_PRIORITY  = 1

NO_VALID_FRAME    = 0
HEAD_START        = 1
CHECKSUM_SUCCESS  = 2
CHECKSUM_FAILURE  = 3
FRAME_DATA_END    = 4

lock = _thread.allocate_lock()

current_time = 0
previous_polling_time = 0
frame_status = NO_VALID_FRAME
default_link = None

online_neurons_module_request_dict = dict()
online_neurons_module_response_dict = dict()


if USE_DICT_CREATED_PRIVIOUSLY:
    from neurons_protocol.neurons_dicts import general_command_request_dict
    from neurons_protocol.neurons_dicts import general_command_response_dict
    from neurons_protocol.neurons_dicts import common_neurons_command_request_dict
    from neurons_protocol.neurons_dicts import common_neurons_command_response_dict
    from neurons_protocol.neurons_dicts import common_neurons_command_default_result_dict
else:
    general_command_request_dict = dict() 
    general_command_response_dict = dict()

    common_neurons_command_request_dict = dict()
    common_neurons_command_response_dict = dict()
    common_neurons_command_default_result_dict = dict()


online_neurons_module_inactive_block_dict = dict()
online_neurons_module_temporary_result_dict = dict()

def send_BYTE(data):
    data_bytes = bytearray()

    if type(data) == float:
        data = int(data)

    data_bytes.append(data & 0x7f)
    return data_bytes

def send_byte(data):
    data_bytes = bytearray()

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(1, "big")
    data1 = input_data_to_bytes[0] & 0x7f
    data2 = (input_data_to_bytes[0] >> 7) & 0x7f

    data_bytes.append(data1)
    data_bytes.append(data2)
    return data_bytes

def send_SHORT(data):
    data_bytes = bytearray()

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(2, "big")
    data1 = input_data_to_bytes[1] & 0x7f
    data2 = ((input_data_to_bytes[0] << 1) + (input_data_to_bytes[1] >> 7)) & 0x7f

    data_bytes.append(data1)
    data_bytes.append(data2)
    return data_bytes

def send_short(data):
    data_bytes = bytearray()

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(2, "big")
    data1 = input_data_to_bytes[1] & 0x7f
    data2 = ((input_data_to_bytes[0] << 1) + (input_data_to_bytes[1] >> 7)) & 0x7f
    data3 = (input_data_to_bytes[0] >> 6) & 0x7f

    data_bytes.append(data1)
    data_bytes.append(data2)
    data_bytes.append(data3)
    return data_bytes

def send_float(data):

    data_bytes = bytearray()
 
    float_bytes = pack('f', data)
    input_data_to_bytes = float_bytes
    data1 = input_data_to_bytes[0] & 0x7f
    data2 = ((input_data_to_bytes[1] << 1) + (input_data_to_bytes[0] >> 7)) & 0x7f
    data3 = ((input_data_to_bytes[2] << 2) + (input_data_to_bytes[1] >> 6)) & 0x7f
    data4 = ((input_data_to_bytes[3] << 3) + (input_data_to_bytes[2] >> 5)) & 0x7f
    data5 = (input_data_to_bytes[3] >> 4) & 0x7f

    data_bytes.append(data1)
    data_bytes.append(data2)
    data_bytes.append(data3)
    data_bytes.append(data4)
    data_bytes.append(data5)
    return data_bytes

def send_long(data):
    data_bytes = bytearray()

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(4, "big")
    data1 = input_data_to_bytes[3] & 0x7f
    data2 = ((input_data_to_bytes[2] << 1) + (input_data_to_bytes[3] >> 7)) & 0x7f
    data3 = ((input_data_to_bytes[1] << 2) + (input_data_to_bytes[2] >> 6)) & 0x7f
    data4 = ((input_data_to_bytes[0] << 3) + (input_data_to_bytes[1] >> 5)) & 0x7f
    data5 = (input_data_to_bytes[0] >> 4) & 0x7f

    data_bytes.append(data1)
    data_bytes.append(data2)
    data_bytes.append(data3)
    data_bytes.append(data4)
    data_bytes.append(data5)
    return data_bytes

def send_STR1(data):
    data_bytes = bytearray()
    data_bytes_BYTE = send_BYTE(len(data))
    for data_element in data_bytes_BYTE:
            data_bytes.append(data_element)

    for i in range(len(data)):
        print(type(data[i]))
        if(type(data[i]) == str):
            data_bytes.append(ord(data[i]))
        elif(type(data[i]) == int):
            data_bytes.append(data[i])

    return data_bytes


def send_STR2(data):
    data_bytes = bytearray()
    data_bytes_SHORT = send_SHORT(len(data))
    for data_element in data_bytes_SHORT:
            data_bytes.append(data_element)

    for i in range(len(data)):
        if(type(data[i]) == str):
            data_bytes.append(ord(data[i]))
        elif(type(data[i]) == int):
            data_bytes.append(data[i])

    return data_bytes

def read_BYTE(data):
    result = (data) & 0x7f;
    return result

def read_byte(data):
    data1 = (data[0]) & 0x7f
    temp = (data[1] << 7) & 0x80
    result = data1 | temp
    data_bytes = pack('B', result)
    result = unpack('b', data_bytes)
    result = result[0]
    return result

def read_SHORT(data):
    data1 = (data[0]) & 0x7f
    temp = (data[1] << 7) & 0x80
    data1 |= temp
    data2 = (data[1] >> 1) & 0x7f
    result = (data2 << 8 | data1) & 0xffff
    return result

def read_short(data):
    data1 = (data[0]) & 0x7f
    temp = (data[1] << 7) & 0x80
    data1 |= temp

    data2 = (data[1] >> 1) & 0x7f
    temp = (data[2] << 6)
    data2 = data2 | temp
    result = (data2 << 8 | data1) & 0xffff

    data_bytes = pack('H', result)
    result = unpack('h', data_bytes)
    result = result[0]
    return result

def read_long(data):
    data1 = (data[0]) & 0x7f
    temp = data[1] << 7;
    data1 |= temp;

    data2 = (data[1] >> 1) & 0x7f;
    temp = (data[2] << 6);
    data2 |= temp;

    data3 = (data[2] >> 2) & 0x7f;
    temp = (data[3] << 5);
    data3 |= temp;

    data4 =  (data[3] >> 3) & 0x7f;
    temp = (data[4] << 4);
    data4 |= temp;

    result = (data4 << 24 | data3 << 16 | data2 << 8 | data1) & 0xffffffff
    data_bytes = pack('L', result)
    result = unpack('l', data_bytes)
    result = result[0]
    return result

def read_float(data):
    data1 = (data[0]) & 0x7f
    temp = data[1] << 7;
    data1 |= temp;

    data2 = (data[1] >> 1) & 0x7f;
    temp = (data[2] << 6);
    data2 |= temp;

    data3 = (data[2] >> 2) & 0x7f;
    temp = (data[3] << 5);
    data3 |= temp;

    data4 =  (data[3] >> 3) & 0x7f;
    temp = (data[4] << 4);
    data4 |= temp;

    result = (data4 << 24 | data3 << 16 | data2 << 8 | data1) & 0xffffffff

    data_bytes = pack('L', result)
    result = unpack('f', data_bytes)
    result = result[0]
    return result

def request_data_conversion(data_type, data):
    data_bytes = bytearray()
    if(data_type == "BYTE"):
        return send_BYTE(data)

    elif(data_type == "byte"):
        return send_byte(data)

    elif(data_type == "SHORT"):
        return send_SHORT(data)

    elif(data_type == "short"):
        return send_short(data)

    elif(data_type == "float"):
        return send_float(data)

    elif(data_type == "long"):
        return send_long(data)

    elif(data_type == "STR1"):
        return send_STR1(data)

    elif(data_type == "STR2"):
        return send_STR2(data)

def response_data_conversion(data_type, para_stream_index, para_stream):
    if data_type == "BYTE":
        data = read_BYTE(para_stream[para_stream_index])
        para_stream_index = para_stream_index + 1
        return para_stream_index, data

    elif data_type == "byte":
        data = read_byte(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 2
        return para_stream_index, data

    elif data_type == "SHORT":
        data = read_SHORT(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 2
        return para_stream_index, data

    elif data_type == "short":
        data = read_short(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 3
        return para_stream_index, data

    elif data_type == "long":
        data = read_long(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 5
        return para_stream_index, data

    elif data_type == "float":
        data = read_float(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 5
        return para_stream_index, data

def conversion_str_to_data(data_type, str_data):
    data = None
    if data_type == "BYTE":
        data = int(str_data)

    elif data_type == "byte":
        data = int(str_data)

    elif data_type == "SHORT":
        data = int(str_data)

    elif data_type == "short":
        data = int(str_data)

    elif data_type == "long":
        data = long(str_data)

    elif data_type == "float":
        data = float(str_data)
    
    return data

def read_general_command_request_to_dict():
    global general_command_request_dict
    os.chdir("/lib")
    with open("request_general_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        while line:
            general_command_request_block_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)
            general_command_request_block_dict["type"] = int(line_elements[1],16);
            if(line_elements[2] != "None"):
                general_command_request_block_dict["subtype"] = int(line_elements[2],16);
            else:
                general_command_request_block_dict["subtype"] = None;
            para_num = 1
            while line_elements[para_num+2] != "" and \
                  line_elements[para_num+2] != "\r\n" and \
                  (para_num + 2) < elements_length:
                general_command_request_block_dict[para_num] = line_elements[para_num+2];
                para_num = para_num + 1
            general_command_request_block_dict["para_num"] = para_num - 1
            general_command_request_dict[line_elements[0]] = general_command_request_block_dict
           
            line = f.readline()
    f.close( )
    #print(general_command_request_dict)

def read_general_command_response_to_dict():
    global general_command_response_dict
    os.chdir("/lib")
    with open("response_general_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        while line:
            general_command_response_block_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)
            type_str = (int(line_elements[2],16)) & 0x7f
            if(line_elements[3] != "None"):
                type_str = type_str * 256 + int(line_elements[3],16)
            else:
                type_str = type_str * 256
            general_command_response_block_dict["name"] = line_elements[0]

            para_num = 1
            while line_elements[para_num+3] != "" and \
                  line_elements[para_num+3] != "\r\n" and \
                  (para_num + 3) < elements_length:
                general_command_response_block_dict[para_num] = line_elements[para_num+3];
                para_num = para_num + 1
            general_command_response_block_dict["para_num"] = para_num - 1
            general_command_response_dict[type_str] = general_command_response_block_dict
            line = f.readline()

    #print(general_command_response_dict)
    f.close( )

def read_common_neurons_command_request_to_dict():
    global common_neurons_command_request_dict
    os.chdir("/lib")
    with open("request_common_neurons_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        common_neurons_command_request_block_dict = dict()
        while line:
            common_neurons_command_request_function_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)

            type_str = (int(line_elements[1],16)) & 0x7f

            if(line_elements[2] != "None"):
                type_str = type_str * 256 + int(line_elements[2],16);
            else:
                type_str = type_str * 256 + 0;

            if type_str in common_neurons_command_request_dict:
                pass
            else:
                common_neurons_command_request_function_dict_list = dict()
                common_neurons_command_request_block_dict = dict()
                common_neurons_command_request_block_dict["name"] =  line_elements[0]

            common_neurons_command_request_function_dict["command_id"] = int(line_elements[4],16);
            
            para_num = 1
            while line_elements[para_num+4] != "" and \
                  line_elements[para_num+4] != "\r\n" and \
                  (para_num + 4) < elements_length:
                common_neurons_command_request_function_dict[para_num] = line_elements[para_num+4];
                para_num = para_num + 1
            common_neurons_command_request_function_dict["para_num"] = para_num - 1
            common_neurons_command_request_function_dict_list[line_elements[3]] = common_neurons_command_request_function_dict
            common_neurons_command_request_block_dict["function"] = common_neurons_command_request_function_dict_list
            common_neurons_command_request_dict[type_str] = common_neurons_command_request_block_dict
           
            line = f.readline()
    f.close( )
    #print(common_neurons_command_request_dict)

def read_common_neurons_command_response_to_dict():
    global common_neurons_command_response_dict
    global common_neurons_command_default_result_dict
    os.chdir("/lib")
    with open("response_common_neurons_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        while line:
            common_neurons_command_response_function_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)
            type_str = (int(line_elements[2],16)) & 0x7f
            if(line_elements[3] != "None"):
                type_str = type_str * 256 + int(line_elements[3],16);
            else:
                type_str = type_str * 256 + 0;

            if type_str in common_neurons_command_response_dict:
                common_neurons_command_default_function_result_list = []
                pass
            else:
                common_neurons_command_response_function_dict_list = dict()
                common_neurons_command_response_block_dict = dict()
                common_neurons_command_response_block_dict["name"] =  line_elements[0]

                common_neurons_command_default_function_result_list = []
                common_neurons_command_default_block_result_dict = dict()

            common_neurons_command_response_function_dict["command_name"] = line_elements[4];
            para_num = 1
            while line_elements[para_num+5] != "" and \
                  line_elements[para_num+5] != "\r\n" and \
                  (para_num + 5) < elements_length:
                str_para = line_elements[para_num+5];
                pos = str_para.rfind('/')
                if pos == -1:
                    para_type = str_para
                    para_default_value = 0
                else:
                    para_type = str_para[0:pos]
                    para_default_value_str = str_para.split('/')[-1]
                    para_default_value = conversion_str_to_data(para_type, para_default_value_str)
                common_neurons_command_response_function_dict[para_num] = line_elements[para_num+5];
                common_neurons_command_default_function_result_list.append(para_default_value)
                para_num = para_num + 1
            common_neurons_command_response_function_dict["para_num"] = para_num - 1
            common_neurons_command_response_function_dict_list[int(line_elements[5],16)] = common_neurons_command_response_function_dict
            common_neurons_command_response_block_dict["function"] = common_neurons_command_response_function_dict_list
            common_neurons_command_default_block_result_dict[line_elements[4]] = common_neurons_command_default_function_result_list
            common_neurons_command_response_dict[type_str] = common_neurons_command_response_block_dict
            common_neurons_command_default_result_dict[line_elements[0]] = common_neurons_command_default_block_result_dict
            line = f.readline()
    f.close( )
    # print(common_neurons_command_response_dict)

def calculation_block_id_and_subcommand_id(command_name, subcommand, block_index):
    global online_neurons_module_request_dict
    block_id = 0
    subcommand_id = 0
    if block_index == 0xff:
        block_id = 0xff
    else:
        function_block_dict = online_neurons_module_request_dict[command_name]
        device_id_list = function_block_dict["device_id"]
        if len(device_id_list) >= block_index:
            block_id = device_id_list[block_index-1]
        else:
            block_id = None
        function_dict = function_block_dict["function"]
        if subcommand in function_dict:
            subcommand_id = function_dict[subcommand]["command_id"]

    return block_id, subcommand_id

def fill_element_of_online_neurons_module_request_dict(device_id, type, subtype):
    global online_neurons_module_request_dict
    global online_neurons_module_inactive_block_dict
    str_block_type = type * 256 +  subtype

    if str_block_type in common_neurons_command_request_dict:
        block_dict = common_neurons_command_request_dict[str_block_type]
        block_name = block_dict["name"]
        if device_id in online_neurons_module_inactive_block_dict:
            online_neurons_module_inactive_block_dict[device_id]["name"] = block_name
            online_neurons_module_inactive_block_dict[device_id]["inactive"] = 0
            online_neurons_module_inactive_block_dict[device_id]["type"] = str_block_type
        else:
            online_neurons_module_inactive_block_info_dict = dict()
            online_neurons_module_inactive_block_info_dict["name"] = block_name
            online_neurons_module_inactive_block_info_dict["inactive"] = 0
            online_neurons_module_inactive_block_info_dict["type"] = str_block_type
            online_neurons_module_inactive_block_dict[device_id] = online_neurons_module_inactive_block_info_dict
        if block_name in online_neurons_module_request_dict:
            if device_id in online_neurons_module_request_dict[block_name]["device_id"]:
                pass
            else:
                online_neurons_module_request_dict[block_name]["device_id"].append(device_id)
                online_neurons_module_request_dict[block_name]["device_id"].sort()
        else:
            online_neurons_module_request_block_dict = dict()
            online_neurons_module_request_block_dict["device_id"] = []
            online_neurons_module_request_block_dict["type"] =  type
            online_neurons_module_request_block_dict["subtype"] =  subtype
            online_neurons_module_request_block_dict["device_id"].append(device_id)
            if "function" in block_dict:
                function_dict_list = block_dict["function"]
                online_neurons_module_request_block_dict["function"] = function_dict_list
                online_neurons_module_request_dict[block_name] = online_neurons_module_request_block_dict

def fill_element_of_online_neurons_module_response_dict(device_id, type, subtype):
    global online_neurons_module_response_dict
    global common_neurons_command_response_dict
    str_block_type = type * 256 +  subtype
    if str_block_type in online_neurons_module_response_dict:
        if device_id in online_neurons_module_response_dict[str_block_type]["device_id"]:
            pass
        else:
            online_neurons_module_response_dict[str_block_type]["device_id"].append(device_id)
            online_neurons_module_response_dict[str_block_type]["device_id"].sort()
            online_neurons_module_response_dict[str_block_type][device_id] = []


    elif str_block_type in common_neurons_command_response_dict:
        online_neurons_module_response_block_dict = dict()
        online_neurons_module_response_block_dict["device_id"] = []
        block_dict = common_neurons_command_response_dict[str_block_type]
        block_name = block_dict["name"]
        online_neurons_module_response_block_dict["name"] =  block_name
        online_neurons_module_response_block_dict["device_id"].append(device_id)
        online_neurons_module_response_block_dict[device_id] = []
        if "function" in block_dict:
            function_dict_list = block_dict["function"]
            online_neurons_module_response_block_dict["function"] = function_dict_list
            online_neurons_module_response_dict[str_block_type] = online_neurons_module_response_block_dict

def delete_online_neurons_module_request_dict(block_name, device_id):
    global online_neurons_module_request_dict
    if device_id in online_neurons_module_request_dict[block_name]["device_id"]:
        online_neurons_module_request_dict[block_name]["device_id"].remove(device_id)
        if len(online_neurons_module_request_dict[block_name]["device_id"]):
            pass
        else:
            del online_neurons_module_request_dict[block_name]

def delete_online_neurons_module_response_dict(block_type, device_id):
    global online_neurons_module_response_dict
    if block_type in online_neurons_module_response_dict:
        if device_id in online_neurons_module_response_dict[block_type]["device_id"]:
            online_neurons_module_response_dict[block_type]["device_id"].remove(device_id)
            if len(online_neurons_module_response_dict[block_type]["device_id"]):
                pass
            else:
                del online_neurons_module_response_dict[block_type]

def general_command_request(link, command_name, block_index, data_segment = []):
    global general_command_request_dict

    block_dict = general_command_request_dict[command_name]
    general_command_request_data = bytearray()

    block_id = block_index
    subcommand_id = 0x00
    general_command_request_data.append(block_id)

    # type data is added
    general_command_request_data.append(block_dict["type"])

    # subtype data is added
    if block_dict["subtype"] != None:
        general_command_request_data.append(block_dict["subtype"])

    arg_num = block_dict["para_num"]

    for i in range(arg_num):
        data_type = block_dict[i+1]
        if arg_num == 1:
            data_bytes = request_data_conversion(data_type, data_segment)
        else:
            data_bytes = request_data_conversion(data_type, data_segment[i])
        for data_element in data_bytes:
            general_command_request_data.append(data_element)

    # link.send(general_command_request_data)
    link(general_command_request_data)
    return block_id, subcommand_id

def general_command_response(data_stream):
    result = None
    data_stream_temp = data_stream
    device_id = data_stream_temp[0]
    block_type = data_stream_temp[1]
    str_block_type = block_type * 256
    result = []
    if str_block_type in general_command_response_dict:
        block_dict = general_command_response_dict[str_block_type]
        if block_dict["name"] == "assign_id":
            arg_num = block_dict["para_num"]
            para_stream = data_stream_temp[2:]
            para_stream_start = 0
            for i in range(arg_num):
                data_type = block_dict[i+1]
                try:
                    para_stream_start, data = response_data_conversion(data_type, para_stream_start, para_stream)
                    result.append(data)
                except:
                    pass
            fill_element_of_online_neurons_module_request_dict(device_id,result[0],result[1])
            fill_element_of_online_neurons_module_response_dict(device_id,result[0],result[1])

        elif block_dict["name"] == "query_version":
            pass
        else:
            pass
    return device_id, result

def common_neurons_command_request(link, command_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_request_dict

    block_dict = online_neurons_module_request_dict[command_name]
    online_neurons_module_request_data = bytearray()

    block_id, subcommand_id = calculation_block_id_and_subcommand_id(command_name, subcommand, block_index)
    if block_id == None:
        return block_id

    online_neurons_module_request_data.append(block_id)

    # type data is added
    online_neurons_module_request_data.append(block_dict["type"])

    # subtype data is added
    if block_dict["subtype"] != None:
        online_neurons_module_request_data.append(block_dict["subtype"])


    if command_name == "gyro_sensor":
        online_neurons_module_request_data.append(0x01)
        online_neurons_module_request_data.append(0x00)

    function_dict_list = block_dict["function"]
    function_dict = function_dict_list[subcommand]
    online_neurons_module_request_data.append(function_dict["command_id"])

    arg_num = function_dict["para_num"]
    for i in range(arg_num):
        data_type = function_dict[i+1]
        if arg_num == 1:
            data_bytes =  request_data_conversion(data_type, data_segment)
        else:
            data_bytes =  request_data_conversion(data_type, data_segment[i])
        for data_element in data_bytes:
            online_neurons_module_request_data.append(data_element)

    # link.send(online_neurons_module_request_data)
    link(online_neurons_module_request_data)
    return block_id, subcommand_id

def common_neurons_command_response(data_stream):
    global online_neurons_module_temporary_result_dict
    global online_neurons_module_response_dict
    global read_count
    global last_ticks
    data_stream_temp = data_stream
    block_id = data_stream_temp[0]
    str_block_type = data_stream_temp[1] * 256 + data_stream_temp[2]
    command_id = data_stream_temp[3]
    result_id = block_id * 256 + command_id
    result = []
    if str_block_type in online_neurons_module_response_dict:
        block_dict = online_neurons_module_response_dict[str_block_type]
        function_dict = block_dict["function"][command_id]
        para_stream = data_stream_temp[4:]
        para_stream_start = 0
        name = block_dict["name"]
        arg_num = function_dict["para_num"]
        for i in range(arg_num):
            
            data_type = function_dict[i+1]
            try:
                para_stream_start, data = response_data_conversion(data_type, para_stream_start, para_stream)
                result.append(data)
            except:
                pass

        if result_id in online_neurons_module_temporary_result_dict:
            online_neurons_module_temporary_result_dict[result_id]["result"] = result
        else:
            online_neurons_module_temporary_result = dict()
            online_neurons_module_temporary_result["result"] = result
            online_neurons_module_temporary_result_dict[result_id] = online_neurons_module_temporary_result

        if lock.locked():
            try:
                lock.release()
            except:
                pass

def activation_block_update():
    global online_neurons_module_inactive_block_dict
    global online_neurons_module_temporary_result_dict
    for device_id in online_neurons_module_inactive_block_dict:
        online_neurons_module_inactive_block_dict[device_id]["inactive"] += 1
        if online_neurons_module_inactive_block_dict[device_id]["inactive"] > 2:
            block_name = online_neurons_module_inactive_block_dict[device_id]["name"]
            block_type = online_neurons_module_inactive_block_dict[device_id]["type"]
            delete_online_neurons_module_request_dict(block_name, device_id)
            delete_online_neurons_module_response_dict(block_type, device_id)
            del online_neurons_module_inactive_block_dict[device_id]

            for result_id in online_neurons_module_temporary_result_dict:
                if ((result_id >> 8) & 0xff) == device_id:
                    del online_neurons_module_temporary_result_dict[result_id]

def get_default_result(block_name, subcommand):
    result = None
    global common_neurons_command_default_result_dict
    default_block_result_dict = []
    if block_name in common_neurons_command_default_result_dict:
        default_block_result_dict = common_neurons_command_default_result_dict[block_name]
        if subcommand in default_block_result_dict:
            result = default_block_result_dict[subcommand]
    return result

#this is subcommand not subtype
def request_distributor(link, block_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_request_dict
    if block_name in general_command_request_dict:
        return general_command_request(link, block_name, data_segment, block_index)
    elif block_name in online_neurons_module_request_dict:
        return common_neurons_command_request(link, block_name, subcommand, data_segment, block_index)

def response_distributor(frame):
    # global default_link
    # while True:
    #     frame = default_link.recv()
    #     if frame:
    if (frame[1] & 0x10) == 0x10:
        general_command_response(frame)
    else:
        common_neurons_command_response(frame)

def neurons_request(block_name, subcommand, data_segment = [], block_index = 0x01):
    global default_link
    return request_distributor(default_link, block_name, subcommand, data_segment, block_index)

def neurons_response():
    response_distributor()

def neurons_del_online_module_temporary_result(block_name, subcommand, block_index):
    global online_neurons_module_request_dict
    global online_neurons_module_temporary_result_dict
    block_id = None
    result_id = 0

    if block_name in online_neurons_module_request_dict:
        block_id, subcommand_id = calculation_block_id_and_subcommand_id(block_name, subcommand, block_index)
        if block_id == None:
            result_id = 0
        else:
            result_id = block_id * 256 + subcommand_id

    if result_id in online_neurons_module_temporary_result_dict:
        del online_neurons_module_temporary_result_dict[result_id]

    return result_id

def neurons_blocking_read(block_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_temporary_result_dict
    global online_neurons_module_response_dict
    result = None

    #delete online result 
    result_id = neurons_del_online_module_temporary_result(block_name, subcommand, block_index)

    last_ticks = time.ticks_ms()
    block_id = neurons_request(block_name, subcommand, data_segment, block_index)
    if block_id == None:
        result = get_default_result(block_name,subcommand)
        return result

    while True:
        lock.acquire(0)
        lock.acquire(1)
        if result_id in online_neurons_module_temporary_result_dict:
            result = online_neurons_module_temporary_result_dict[result_id]["result"]
            return result
        elif time.ticks_ms() - last_ticks > 1000:
            result = get_default_result(block_name,subcommand)
            return result

def neurons_async_read(block_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_temporary_result_dict
    global online_neurons_module_request_dict
    result = None

    if block_name in online_neurons_module_request_dict:
        block_id, subcommand_id = calculation_block_id_and_subcommand_id(block_name, subcommand, block_index)

        if block_id == None:
            result = get_default_result(block_name,subcommand)
            return result
        
        result_id = block_id * 256 + subcommand_id
        if result_id in online_neurons_module_temporary_result_dict:
            result = online_neurons_module_temporary_result_dict[result_id]["result"]
            return result
        else:
            result = get_default_result(block_name,subcommand)
            return result
    else:
        result = get_default_result(block_name,subcommand)
        return result

def neurons_async_read_test():
    global default_link
    online_neurons_module_request_data = bytearray()
    online_neurons_module_request_data.append(0x01)
    online_neurons_module_request_data.append(0x64)
    online_neurons_module_request_data.append(0x02)
    online_neurons_module_request_data.append(0x01)
    # default_link.send(online_neurons_module_request_data)
    default_link(online_neurons_module_request_data)

def neurons_heartbeat_thread():
    from makeblock import sleep_special
    global online_neurons_module_response_dict
    global online_neurons_module_request_dict
    global online_neurons_module_temporary_result_dict
    global default_link
        
    # default_link = link
    # _thread.start_new_thread(neurons_response, (), 3)
    neurons_request("assign_id", None, 0xff, (0x00))
    while True:
        activation_block_update()
        neurons_request("assign_id", None, 0xff, (0x00))
        if lock.locked():
            try:
                lock.release()
            except:
                pass
        # print(online_neurons_module_request_dict)
        # print(online_neurons_module_response_dict)
        # print(online_neurons_module_temporary_result_dict)
        # sleep_special use vTaskDelay() instead of mp_hal_delay_ms() 
        sleep_special(POLLING_TIME_FOR_ASSIGNMENT_ID)

def neurons_heartbeat_start():
    if USE_DICT_CREATED_PRIVIOUSLY:
        pass
    else:
        try:
            read_general_command_request_to_dict()
            read_general_command_response_to_dict()
            read_common_neurons_command_request_to_dict()
            read_common_neurons_command_response_to_dict()

        except Exception as e:
            print("neurons read csv error")
            print(e)

    _thread.stack_size(HEART_PACKAGE_THREAD_STACK_SIZE)
    _thread.start_new_thread(neurons_heartbeat_thread, (), HEART_PACKAGE_THREAD_PRIORITY)

def neuron_request_bind_phy(link):
    global default_link
    default_link = link
