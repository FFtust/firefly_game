from firefly_online.application.game import game_base
from firefly_online.application.game import sprite_create
from firefly_online.application.game import *
from firefly_online.application.game_controller import *
from firefly_online.application.game_driver import set_game_driver

import firefly_online.hardware
import time
import random

codey = hardware.codey('COM28')

score = 0
game = game_base()
set_game_driver([codey.display.show_image])

# 飞机三种造型
plane_s = '000000000000c060c000000000000000'
plane_s1 = '000000000000c0e0c000000000000000'
plane_s2 = '00000000000080408000000000000000'

# 子弹造型
bullet_s =  "000000000000001c0000000000000000"

# 用于选择飞机造型
plane_id = 0

# 用于选择音效
music_id = 0
# 音效名变量
music_name = "shot"

# 用于子弹控制
bullet_run_count = 0
bullet_run_flag = False

# 游戏角色， 飞机 + 子弹
plane = None
bullet = None


# 背景控制函数， 即控制障碍物的运动
def background_control():
    global score
    temp = game.get_background()
    
    # 随着分数增高， 障碍物的数量将随之增多， 共三个等级
    if score < 50:
        a = random.randint(0, 15)
    elif score < 100:
        a = random.randint(0, 7)
        b = random.randint(8, 15)
    else:
        a = random.randint(0, 5)
        b = random.randint(6, 11)
        c = random.randint(7, 15)

    # 控制整个背景向下平移
    for i in range(16):
        temp[i] <<= 1
        temp[i] &= 0xff
        if score < 50:
            if i == a:
                temp[i] |= 0x01
        elif score < 100:
            if i == a or i == b:
                temp[i] |= 0x01
        else:
            if i == a or i == b or i == c:
                temp[i] |= 0x01            
    game.set_background(temp)

# 消除障碍物函数
def barrier_delete():
    global score, music_id
    # 获取子弹列坐标
    i = bullet.get_position()[0]
    # 消除子弹所在列的全部障碍物
    game.set_background_with_column(0x00, i + 7)

# 子弹移动控制函数
def bullet_move_control():
    global bullet_run_flag, bullet_run_count, score, music_name, music_id
    # 按C键发射子弹， 子弹开始移动
    if isKeyPressed(Key_Up):
        bullet_run_flag = True
    move_step = 5

    if bullet_run_flag:
        if bullet_run_count == 0:
            codey.speaker.play_melody(music_name)
            bullet.set_position([plane.get_position()[0], plane.get_position()[1] + 2]) 
            bullet.show()
            bullet_run_count += 1
            # 检查是否碰到障碍物
            if game.background_collision_check(bullet):
                score += 1
                barrier_delete()
        elif bullet_run_count < move_step:
            bullet.up()
            bullet_run_count += 1
            if game.background_collision_check(bullet):
                score += 1
                barrier_delete()
        else:
            # 移动完毕， 子弹回到原始位置， 并隐藏
            bullet.home()
            bullet.hide()
            bullet_run_count = 0
            bullet_run_flag = False

# 飞机移动控制函数
move_flag = 0
def plane_move_control2():
    global plane, move_flag
    if plane == None:
        return

    # A键左移， B键右移， 碰到边界则无法继续移动
    # 为了保证能达到左右边缘上的障碍物， 因此设定飞机最外侧一列能移动到屏幕外
    if move_flag == 1:
        if plane.meet_border_check() & LEFT_MEET:
             plane.right()
        plane.left()
        move_flag = 0
    elif move_flag == 2:
        if plane.meet_border_check() & RIGHT_MEET:
             plane.left()
        plane.right()
        move_flag = 0

def plane_move_control():
    global plane
    if plane == None:
        return

    # A键左移， B键右移， 碰到边界则无法继续移动
    # 为了保证能达到左右边缘上的障碍物， 因此设定飞机最外侧一列能移动到屏幕外
    if codey.button_a.is_pressed():
        if plane.meet_border_check() & LEFT_MEET:
             plane.right()
        plane.left()
    elif codey.button_b.is_pressed():
        if plane.meet_border_check() & RIGHT_MEET:
             plane.left()
        plane.right()

# 游戏控制状态机标志位
game_status = 0

# 游戏控制主函数
def main():
    global game_status, score, plane_id, plane, music_name, bullet, music_id
    count = 0

    while True:
        # 开机选择飞机造型及音效
        if game_status == 0:
            print(codey.button_a.is_pressed(), codey.button_b.is_pressed(), codey.button_c.is_pressed())
            if plane_id == 0:
                codey.display.show_image(plane_s)
            elif plane_id == 1:
                codey.display.show_image(plane_s1)
            else:
                codey.display.show_image(plane_s2)
            # 开始游戏
            if codey.button_c.is_pressed():
                codey.speaker.play_melody("start")
                game_status = 1
                score = 0

                # 创建角色
                if plane_id == 0:
                    plane = sprite_create(plane_s)
                elif plane_id == 1:
                    plane = sprite_create(plane_s1)
                else:
                    plane = sprite_create(plane_s2)

                bullet = sprite_create(bullet_s)
                game.add_sprite(plane)
                bullet.hide()
                game.add_sprite(bullet)
                
                # 游戏开始
                game.game_start()
                time.sleep(1)
            # 选择飞机
            elif codey.button_a.is_pressed():
                plane_id += 1
                if plane_id > 2:
                    plane_id = 0
                while codey.button_a.is_pressed():
                    time.sleep(0.05)
            # 选择音效
            elif codey.button_b.is_pressed():
                music_id += 1
                if music_id > 2:
                    music_id = 0

                if music_id == 0:
                    music_name = "shot"
                elif music_id == 1:
                    music_name = "laser"
                elif music_id == 2:
                    music_name = "score"
                codey.speaker.play_melody(music_name)
                while codey.button_b.is_pressed():
                    time.sleep(0.05)
            time.sleep(0.05)
        # 游戏运行控制
        elif game_status == 1:
            # 调整数字可以调整移动灵敏度
            if count % 3 == 0:
                plane_move_control2()
            # 子弹移动控制
            bullet_move_control()
            
            #障碍物移动控制， 速度随电位器变化而变化
            if count % (codey.potentiometer.get_value() // 6) == 0:
                background_control()

            # 飞机是否撞到障碍物检测
            if game.background_collision_check(plane):
                codey.speaker.play_melody('wrong')
                game_status = 2
                game.set_background("00000000000000000000000000000000")
                game.sprite_list_clean()

                palne = None
                bullet = None
                game.game_over()
            time.sleep(0.02)
        else:
            # 游戏结束， 显示分数， 并等待C键按下， 重新开始游戏
            codey.display.show(score)
            if codey.button_c.is_pressed():
                game_status = 0
            time.sleep(0.1)
        count += 1

# 开始运行
def move_right():
    global move_flag
    move_flag = 2

def move_left():
    global move_flag
    move_flag = 1

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
