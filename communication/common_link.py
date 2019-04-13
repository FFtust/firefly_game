#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import threading
import time
from utils.common import *

SERIAL_TIMEOUT = 1

# define physical channel functions
class phy_uart():
    def __init__(self, port, baudrate):
        self.ser = None
        self.com_port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(None, self.baudrate, timeout = SERIAL_TIMEOUT)
        self.write_lock = threading.Lock()

    def __del__(self):
        print('phy_uart del')
        if self.ser.is_open:
            self.close()

    def open(self):
        self.ser.port = self.com_port
        self.ser.baudrate = self.baudrate
        self.ser.write_timeout = SERIAL_TIMEOUT
        if not self.ser.is_open:
            self.ser.open()

    def close(self):
        if self.ser:
            if self.ser.is_open:
                self.ser.close()

    def write(self, frame):
        if not self.ser.is_open:
            return

        self.write_lock.acquire(1)
        print("phy write frame is", frame)
        self.ser.write(frame)
        self.write_lock.release()

    def read(self, bytes_num = 1):
        data = bytearray()
        if self.ser.is_open:
            data = self.ser.read(bytes_num)
        return data

# define functions about protocol
class common_link():
    # Frame header & end
    FRAME_HEADER = 0xF3
    FRAME_END = 0xF4
    FRAME_MAX_LEN = 1024
    MAX_FRAME_NUM = 64

    # FSM state
    S_HEAD = 0
    S_HEAD_CHECK = 1
    S_LEN_1 = 2
    S_LEN_2 = 3
    S_DATA = 4
    S_DATA_CHECK = 5
    S_END = 6

    def __init__(self, phy):
        self.phy = phy
        self.state = self.S_HEAD
        self.recv_buffer = bytearray()
        self.recv_len = 0
        self.head_checksum = 0
        self.len = 0
        self.frame_list = []
        self.recv_bin_sem = threading.Lock()
        self.recv_bin_sem.acquire()
        self.protocol_cb = {}

    def __del__(self):
        self.phy.__del__()
        print('common_link del')

    # Input a stream data, split stream to frame and save in frame_list
    def fsm(self, stream):
        # this variable indicate the number of datas should be read next time
        ret_num = 1
        for c in stream:
            receive_frame = None

            if len(self.recv_buffer) > self.FRAME_MAX_LEN:
                self.state = self.S_HEAD

            if (self.S_HEAD == self.state):
                if (self.FRAME_HEADER == c):
                    self.recv_buffer = bytearray()
                    self.recv_buffer.append(c)
                    self.state = self.S_HEAD_CHECK

            elif (self.S_HEAD_CHECK == self.state):
                self.recv_buffer.append(c)
                self.head_checksum = c
                self.state = self.S_LEN_1

            elif (self.S_LEN_1 == self.state):
                self.recv_buffer.append(c)
                self.len = c
                self.state = self.S_LEN_2

            elif (self.S_LEN_2 == self.state):
                self.recv_buffer.append(c)
                self.len += c * 0xFF
                head_checksum = (self.recv_buffer[0] + self.recv_buffer[2] + self.recv_buffer[3]) & 0xFF
                if (head_checksum == self.head_checksum):
                    self.state = self.S_DATA
                    self.recv_len = 0
                    # head check successed, read the reserved datas
                    # 2 = checksum(1) + 0xF4(1)
                    ret_num = self.len + 2

                else:
                    self.state = self.S_HEAD

            elif (self.S_DATA == self.state):
                self.recv_buffer.append(c)
                self.recv_len += 1
                if (self.len == self.recv_len):
                    self.state = self.S_DATA_CHECK

            elif (self.S_DATA_CHECK == self.state):
                self.recv_buffer.append(c)
                data_checksum = 0
                for i in self.recv_buffer[4:-1]:
                    data_checksum += i
                data_checksum = data_checksum & 0xFF
                if (data_checksum == self.recv_buffer[-1]):
                    self.state = self.S_END
                else:
                    self.state = self.S_HEAD

            elif (self.S_END == self.state):
                self.recv_buffer.append(c)
                if (self.FRAME_END == c):
                    receive_frame = self.recv_buffer[:]
                self.state = self.S_HEAD

            if receive_frame:
                # print(receive_frame)
                self.frame_list.append(receive_frame[4 : -2])

        if len(self.frame_list) > self.MAX_FRAME_NUM:
             self.frame_list.clear()

        if self.recv_bin_sem.locked():
             self.recv_bin_sem.release()

        return ret_num

    def work(self):
        self.phy.open()
        read_num = 1
        while True:
            try:
                stream = self.phy.read(read_num)
                if stream:
                    debug_print("read data is", stream)
                    read_num = self.fsm(stream)
            except:
                time.sleep(0.1)
                print('serial closed')

    def recv(self):
        self.recv_bin_sem.acquire()
        debug_print("received list is", self.frame_list)
        ret_list = []
        for l in self.frame_list:
            ret_list.append(l)
        self.frame_list.clear()
        return ret_list
    
    def register_process_function(self, id, cb):
        self.protocol_cb[id] = cb

    def received_frame_dispatch(self):
        while True:
            ret = self.recv()
            if ret:
                for item in ret:
                    if item[0] in self.protocol_cb:
                        self.protocol_cb[item[0]](item[1:])
    def start(self):
        self.thread_work = threading.Thread(target = self.work, args = ())
        self.thread_work.start()
        self.thread_dispatch = threading.Thread(target = self.received_frame_dispatch, args = ())
        self.thread_dispatch.start()

