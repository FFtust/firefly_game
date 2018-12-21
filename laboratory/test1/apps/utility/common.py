import math
from struct import pack, unpack
########################################
node_table = \
{ \
  'C2': 65,
  'D2': 73,
  'E2': 82,
  'F2': 87,
  'G2': 98,
  'A2': 110,
  'B2': 123,
  'C3': 131,
  'D3': 147,
  'E3': 165,
  'F3': 175,
  'G3': 196,
  'A3': 220,
  'B3': 247,
  'C4': 262,
  'D4': 294,
  'E4': 330,
  'F4': 349,
  'G4': 392,
  'A4': 440,
  'B4': 494,
  'C5': 523,
  'D5': 587,
  'E5': 659,
  'F5': 698,
  'G5': 784,
  'A5': 880,
  'B5': 988,
  'C6': 1047,
  'D6': 1175,
  'E6': 1319,
  'F6': 1397,
  'G6': 1568,
  'A6': 1760,
  'B6': 1976,
  'C7': 2093,
  'D7': 2349,
  'E7': 2637,
  'F7': 2794,
  'G7': 3136,
  'A7': 3520,
  'B7': 3951,
  'C8': 4186,
  'D8': 4699,
}
MIDI_NOTE_NUM0 = 8.18
NOTE_FREQUENCE_RATIO = math.pow(2, (1 / 12))

# color table
color_table = {"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),\
               "yellow":(255,255,0), "purple":(255,0,255), "cyan":(0,255,255),\
               "white":(150,150,150), "orange":(255,50,0), "black":(0,0,0), "gray":(0,0,0) \
               }

led_ring_tble = ((0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), \
                 (255, 50, 0), (255, 50, 0), (255, 50, 0),\
                 (255, 0, 0), (255, 0, 0))

#for common use
## check the type
def type_check(para, types):
    ret = False
    if not ((type(types) == tuple) or (type(types) == list)): 
        if type(para) == types:
            ret = True
    else:
        for item in types:
            if type(para) == item:
                ret = True
                break
    return ret

# check the range of number
def num_range_scale(num, min_n = None, max_n = None, to_range = True):
    if min_n == None and max_n == None:
        return num
    
    if min_n != None:
        if to_range and num < min_n:
            num = min_n

    if max_n != None:
        if to_range and num > max_n:
            num = max_n
    return num

# debug
__PY_DEBUG = False 
def start_dbg_out():
    global __PY_DEBUG
    __PY_DEBUG = True

def stop_dbg_out():
    global __PY_DEBUG
    __PY_DEBUG = False

def print_dbg(*args):
    global __PY_DEBUG
    if __PY_DEBUG:
        print(*args)

# function type check
# warning!!!:  may not work
def __function_type():
    pass

def function_type_check(func):
    if type(func) == type(__function_type):
        return True
    else:
        return False

# bytes switch
def float_to_byte_4(data): 
    float_bytes = pack('f', data)
    return bytearray(float_bytes)

def int_to_byte_4(data):
    if type(data) == float:
        data = int(data)
    int_bytes = data.to_bytes(4, "little")
    return bytearray(int_bytes)

def int_to_byte_2(data):
    if type(data) == float:
        data = int(data)
    int_bytes = data.to_bytes(2, "little")
    return bytearray(int_bytes)

def byte_2_to_short(data):
    if len(data) != 2:
        return None
    result = unpack('h', bytearray(data))
    result = result[0]
    return bytearray(result)

def byte_4_to_float(data): 
    float_bytes = unpack('f', bytearray(data))
    result = result[0]
    return bytearray(result)

def byte_4_to_int(data):
    if len(data) != 4:
        return None
    result = unpack('l', bytearray(data))
    result = result[0]
    return bytearray(result)

# about driver
def touchpad_value_scale(tp_id, value):
    ret = 0
    if tp_id <= 2:
        ret = (750 - value) / 730
    else:
        ret = (900 - value) / 880
    
    if ret < 0:
        ret = 0.0
    else:
        ret = round(ret * 100.0, 1)
    return ret