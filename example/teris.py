from application.game import game_base
from application.game import sprite_create
from application.game import *
from application.game_controller import *

import hardware.codey as codey 
import time
import random

score = 0
game = game_base()
a_s = '10101010000000000000000000000000'
b_s = '10380000000000000000000000000000'
c_s = '30300000000000000000000000000000'
d_s = '10180800000000000000000000000000'
e_s = '30101000000000000000000000000000'
f_s = '08181000000000000000000000000000'
sprite_num = 6
sprites = [a_s, b_s, c_s, d_s, e_s, f_s]
current_script = None
move_lock_flag = False

move_flag = 0

def line_remove_process():
    global score
    screen = game.get_screen()
    background = game.get_background()
    removed_flag = False
    i = 0
    while i < 16:
        if screen[i] & 0xff == 0xff:
            score += 1
            removed_flag = True
            del background[i]
            background.insert(0, 0x00)
        i += 1
    if removed_flag:
        codey.speaker.play_melody("start")
    game.set_background(background)

down_speed = 10

def move_control():
    global down_speed, current_script, move_lock_flag
    if current_script == None :
        time.sleep(0.2)
        return
    if isKeyPressed(Key_Right) and move_lock_flag == False:
        current_script.up()
        if game.background_collision_check(current_script):
            current_script.down()

    elif isKeyPressed(Key_Left) and move_lock_flag == False:
        current_script.down()
        if game.background_collision_check(current_script):
            current_script.up()

    elif isKeyPressed(Key_Up) and move_lock_flag == False:
        current_script.rotate()

    elif isKeyPressed(Key_Down) and move_lock_flag == False:
        down_speed = 2
        

    temp = current_script.meet_border_check()
    if temp == UP_MEET:
        current_script.down()
        while current_script.meet_border_check() == UP_MEET:
            current_script.down()
    elif temp == DOWN_MEET:
        current_script.up()
        while current_script.meet_border_check() == DOWN_MEET:
            current_script.up()

def move_control2():
    global down_speed, current_script, move_lock_flag, move_flag
    if current_script == None :
        time.sleep(0.2)
        return
    if move_flag == 1 and move_lock_flag == False:
        current_script.up()
        if game.background_collision_check(current_script):
            current_script.down()
        move_flag = 0

    elif move_flag == 2 and move_lock_flag == False:
        current_script.down()
        if game.background_collision_check(current_script):
            current_script.up()
        move_flag = 0

    elif move_flag == 3 and move_lock_flag == False:
        current_script.rotate()
        move_flag = 0

    elif move_flag == 4 and move_lock_flag == False:
        down_speed = 2
        move_flag = 0
        

    temp = current_script.meet_border_check()
    if temp == UP_MEET:
        current_script.down()
        while current_script.meet_border_check() == UP_MEET:
            current_script.down()
    elif temp == DOWN_MEET:
        current_script.up()
        while current_script.meet_border_check() == DOWN_MEET:
            current_script.up()

def work():
    global current_script, down_speed, score, move_lock_flag
    game.game_start()
    game.set_background([0] * 16)
    while True:
        index = random.randint(0, sprite_num - 1)
        current_script = sprite_create(sprites[index])
        game.add_sprite(current_script)
        current_script.left(2)
        if game.background_collision_check(current_script):
            game.del_sprite(current_script)
            current_script = None
            codey.speaker.play_melody("wrong")
            game.game_over()
            codey.display.show(score)
            score = 0
            break
        count = 1
        down_speed = 10
        while True:
            if count % down_speed == 0:
                current_script.right()
            
            if current_script.meet_border_check() == RIGHT_MEET:
                move_lock_flag = True
                current_script.left()
                codey.speaker.play_melody("score")
                break

            if game.background_collision_check(current_script):
                move_lock_flag = True
                current_script.left()
                codey.speaker.play_melody("score")
                break

            move_control2()

            time.sleep(0.05)
            count += 1
        time.sleep(0.1)
        game.set_background(game.get_screen())
        current_script.hide()
        time.sleep(0.1)
        line_remove_process()
        game.del_sprite(current_script)
        move_lock_flag = False

def main():
    while True:
        work()
        time.sleep(2)

def move_right():
    global move_flag
    move_flag = 1

def move_left():
    global move_flag
    move_flag = 2

def move_up():
    global move_flag
    move_flag = 3

def move_down():
    global move_flag
    move_flag = 4
registerKeyEvent(Key_Right, move_right, ())
registerKeyEvent(Key_Left, move_left, ())
registerKeyEvent(Key_Up, move_up, ())
registerKeyEvent(Key_Down, move_down, ())

# on_button_callback3()
# registerKeyEvent(Key_1, on_button_callback3, ())
import threading
th = threading.Thread(target = main, args = ())
th.start()
controllerStart()
