from functools import reduce

# game cinfig
FACE_ROW = 8
FACE_COLUMN = 16
REFRESH_INTERVAL = 50
SPRITE_NUM_MAX = 20

def screen_update_hardware_default(face):
	   pass

def set_screen_update_function(func):
    global screen_update_hardware
    screen_update_hardware = func

def get_update_function():
	   global screen_update_hardware
	   return screen_update_hardware

screen_update_hardware = screen_update_hardware_default

# # function need to be complement here
# def screen_update_hardware(face):
#     temp_face = [0] * FACE_COLUMN
#     for i in range(FACE_COLUMN):
#         temp_face[i] = face_info_invert(face[i])
#     codey.display.show_image(para_switch(temp_face))
#     show_neurons_image(face)

# def para_join(x, y):
#     if type(x) == int:
#         hx = hex(x)
#         if len(hx) == 3:
#             hx = '0' + hx[2]
#         else:
#             hx = hx[2:]
#     else:
#         hx = x

#     if type(y) == int:
#         hy = hex(y)
#         if len(hy) == 3:
#             hy = '0' + hy[2]
#         else:
#             hy = hy[2:]
#     else:
#         hy = y
#     return hx + hy

# def para_switch(para):
#     if len(para) == 1:
#         a = hex(para[0])
#         if len(a) == 3:
#             a = '0' + a[2]
#         else:
#             a = a[2:]
#     else:
#         a = reduce(para_join, list(para))

#     return a

# def show_neurons_image(image):
#     face1 = []
#     face2 = []
#     for i in range(8):
#         for j in range(8):
#             if image[j] & (1 << i):
#                 face1.append(1)
#             else:
#                 face1.append(0)
    
#     for i in range(8):
#         for j in range(8):
#             if image[8 + j] & (1 << i):
#                 face2.append(1)
#             else:
#                 face2.append(0)

#     neurons.led_panel.show_image(face1, 1)
#     neurons.led_panel.show_image(face2, 2)
#     # neurons.led_panel.show_image(face2, 3)


# # this is for the mismatching axis definition
# def face_info_invert(dat):
#     tempdata = 0
#     tempdata += (dat & 0x80) >> 7
#     tempdata += (dat & 0x40) >> 5
#     tempdata += (dat & 0x20) >> 3
#     tempdata += (dat & 0x10) >> 1
#     tempdata += (dat & 0x08) << 1
#     tempdata += (dat & 0x04) << 3
#     tempdata += (dat & 0x02) << 5
#     tempdata += (dat & 0x01) << 7
#     return tempdata