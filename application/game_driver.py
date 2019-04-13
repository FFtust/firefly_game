# # coding:utf-8
from firefly_online.application.game import *
from firefly_online.application.game_adapter import *
from firefly_online.application.game_controller import *


global func_list

# regisster screen update
# this is for the mismatching axis definition
def face_info_invert(dat):
    tempdata = 0
    tempdata += (dat & 0x80) >> 7
    tempdata += (dat & 0x40) >> 5
    tempdata += (dat & 0x20) >> 3
    tempdata += (dat & 0x10) >> 1
    tempdata += (dat & 0x08) << 1
    tempdata += (dat & 0x04) << 3
    tempdata += (dat & 0x02) << 5
    tempdata += (dat & 0x01) << 7
    return tempdata

def para_join(x, y):
    if type(x) == int:
        hx = hex(x)
        if len(hx) == 3:
            hx = '0' + hx[2]
        else:
            hx = hx[2:]
    else:
        hx = x

    if type(y) == int:
        hy = hex(y)
        if len(hy) == 3:
            hy = '0' + hy[2]
        else:
            hy = hy[2:]
    else:
        hy = y
    return hx + hy

def para_switch(para):
    if len(para) == 1:
        a = hex(para[0])
        if len(a) == 3:
            a = '0' + a[2]
        else:
            a = a[2:]
    else:
        a = reduce(para_join, list(para))

    return a

# function need to be complement here
def screen_update_hardware(face):
    global func_list
    temp_face = [0] * FACE_COLUMN
    for i in range(FACE_COLUMN):
        temp_face[i] = face_info_invert(face[i])

    for item in func_list:
        item(para_switch(temp_face))


def set_game_driver(func):
    global func_list
    func_list = func
    set_screen_update_function(screen_update_hardware)
