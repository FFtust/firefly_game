import sys
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import *

# keyBoard
Key_Escape = Qt.Key_Escape
Key_Tab = Qt.Key_Tab
Key_Backtab = Qt.Key_Backtab
Key_Backspace = Qt.Key_Backspace
Key_Return = Qt.Key_Return
Key_Enter = Qt.Key_Enter
Key_Insert = Qt.Key_Insert
Key_Delete = Qt.Key_Delete
Key_Pause = Qt.Key_Pause
Key_Print = Qt.Key_Print
Key_SysReq = Qt.Key_SysReq
Key_Clear = Qt.Key_Clear
Key_Home = Qt.Key_Home
Key_End = Qt.Key_End
Key_Left = Qt.Key_Left
Key_Up = Qt.Key_Up
Key_Right = Qt.Key_Right
Key_Down = Qt.Key_Down
Key_PageUp = Qt.Key_PageUp
Key_PageDown = Qt.Key_PageDown
Key_Shift = Qt.Key_Shift
Key_Control = Qt.Key_Control
Key_Meta = Qt.Key_Meta
Key_Alt = Qt.Key_Alt
Key_AltGr = Qt.Key_AltGr
Key_CapsLock = Qt.Key_CapsLock
Key_NumLock = Qt.Key_NumLock
Key_ScrollLock = Qt.Key_ScrollLock
Key_F1 = Qt.Key_F1
Key_F2 = Qt.Key_F2
Key_F3 = Qt.Key_F3
Key_F4 = Qt.Key_F4
Key_F5 = Qt.Key_F5
Key_F6 = Qt.Key_F6
Key_F7 = Qt.Key_F7
Key_F8 = Qt.Key_F8
Key_F9 = Qt.Key_F9
Key_F10 = Qt.Key_F10
Key_F11 = Qt.Key_F11
Key_F12 = Qt.Key_F12
Key_0 = Qt.Key_0
Key_1 = Qt.Key_1
Key_2 = Qt.Key_2
Key_3 = Qt.Key_3
Key_4 = Qt.Key_4
Key_5 = Qt.Key_5
Key_6 = Qt.Key_6
Key_7 = Qt.Key_7
Key_8 = Qt.Key_8
Key_9 = Qt.Key_9
Key_A = Qt.Key_A
Key_B = Qt.Key_B
Key_C = Qt.Key_C
Key_D = Qt.Key_D
Key_E = Qt.Key_E
Key_F = Qt.Key_F
Key_G = Qt.Key_G
Key_H = Qt.Key_H
Key_I = Qt.Key_I
Key_J = Qt.Key_J
Key_K = Qt.Key_K
Key_L = Qt.Key_L
Key_M = Qt.Key_M
Key_N = Qt.Key_N
Key_O = Qt.Key_O
Key_P = Qt.Key_P
Key_Q = Qt.Key_Q
Key_R = Qt.Key_R
Key_S = Qt.Key_S
Key_T = Qt.Key_T
Key_U = Qt.Key_U
Key_V = Qt.Key_V
Key_W = Qt.Key_W
Key_X = Qt.Key_X
Key_Y = Qt.Key_Y
Key_Z = Qt.Key_Z

eventTable = {}
KeyStatus_table = {}
def registerKeyEvent(event, cb, para = ()):
    global eventTable
    eventTable[event] = (cb, para)

def unregisterKeyEvent(event):
    global eventTable
    eventTable.pop(event)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        self.setWindowTitle('游戏控制台')
        self.show()


    # 检测键盘回车按键
    def keyPressEvent(self, event):
        global eventTable, KeyStatus_table
        # print("按下：" + str(event.key()))
        for key in eventTable:
            if event.key() == key:
                eventTable[key][0](*eventTable[key][1])
        KeyStatus_table[event.key()] = True

    # 检测键盘回车按键
    def keyReleaseEvent(self, event):
        global eventTable, KeyStatus_table
        # print("弹起：" + str(event.key()))
        KeyStatus_table[event.key()] = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("鼠标左键点击")
        elif event.button() == Qt.RightButton:
            print("鼠标右键点击")
        elif event.button() == Qt.MidButton:
            print("鼠标中键点击")
 
def isKeyPressed(key):
    global KeyStatus_table
    if key in KeyStatus_table:
        return KeyStatus_table[key]
    else:
        return False

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Window()
#     sys.exit(app.exec_())

def controllerStart():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())