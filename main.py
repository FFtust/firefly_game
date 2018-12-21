# # coding:utf-8
from application.game import *
from application.game_adapter import *
from application.game_controller import *

import time
import random
import hardware

haloboard = hardware.haloboard("COM29")
haloboard.led.show_all(100, 0, 0)
time.sleep(1)
haloboard.led.show_all(100, 100, 0)
# codey = hardware.codey('COM28')

# # regisster screen update
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

# # function need to be complement here
# def screen_update_hardware(face):
#     print(face)
#     temp_face = [0] * FACE_COLUMN
#     for i in range(FACE_COLUMN):
#         temp_face[i] = face_info_invert(face[i])
#     codey.display.show_image(para_switch(temp_face))

# set_screen_update_function(screen_update_hardware)

# # application codes
# game = game_base()
# # 两个角色 为两个小点
# l_s = '00000000000000200000000000000000'
# r_s = '00000000000000002000000000000000'
# #背景图案
# b_s = '0000000000ff00000000ff0000000000'

# left_h = sprite_create(l_s)
# game.add_sprite(left_h)
# right_h = sprite_create(r_s)
# game.add_sprite(right_h)

# game.set_background(b_s)

# move_lock_flag = False
# speed = 20
# score = 0

# bg_change_count = 0

# # 速度控制
# def speed_control():
#     global speed
#     if isKeyPressed(Key_Up):
#         speed -= 1
#     if isKeyPressed(Key_Down):
#         speed += 1
    
#     if speed < 1:
#         speed = 1

# # 角色移动控制
# def move_control():
#     global speed, move_lock_flag
#     if isKeyPressed(Key_Left) and move_lock_flag == False:
#         left_h.set_position([-1, 0])
#     else:
#         left_h.home()
#     # B键按下， 右边角色右移， 否则回到原来位置
#     if isKeyPressed(Key_Right) and move_lock_flag == False:
#         right_h.set_position([1, 0])
#     else:
#         right_h.home()

# # 角色移动控制
# def move_control_2():
#     global speed, move_lock_flag
#     if codey.button_a.is_pressed() and move_lock_flag == False:
#         left_h.set_position([-1, 0])
#     else:
#         left_h.home()
#     # B键按下， 右边角色右移， 否则回到原来位置
#     if codey.button_b.is_pressed() and move_lock_flag == False:
#         right_h.set_position([1, 0])
#     else:
#         right_h.home()

# # 背景控制
# def background_control():
#     global bg_change_count, score
#     temp = game.get_background()
#     for i in range(16):
#         temp[i] <<= 1
#         temp[i] &= 0xff
#     temp[5] = 0xff
#     temp[10] = 0xff
#     if bg_change_count % 3 == 0:
#         score += 1
#         a = random.randint(6, 7)
#         b = random.randint(8, 9)
#         temp[a] |= 0x01
#         temp[b] |= 0x01
#     else:
#         pass
#     game.set_background(temp)
#     bg_change_count += 1

# def game_deinit():
#     global speed, score, move_lock_flag
#     score = 0
#     game.set_background(b_s)

# # C键开始
# def on_start(): 
#     global speed, score, move_lock_flag
#     count = 1
#     score = 0
#     game.game_start()
#     print("game start")
#     while True:
#         speed_control()
#         # move_control()
#         move_control_2()
#         if speed != 0:
#             if count % speed == 0:
#                 background_control()
#         else:
#             background_control()
#         # 如果角色碰到背景， 则游戏结束
#         if game.background_collision_check(right_h) or game.background_collision_check(left_h):
#             # game.game_over()
#             codey.speaker.play_melody('sad.wav')
#             game_deinit()
#             time.sleep(2)
#             # break

#         count += 1
#         time.sleep(0.025)

# # registerKeyEvent(Key_1, on_start, ())
# import threading
# th = threading.Thread(target = on_start, args = ())
# th.start()
# controllerStart()