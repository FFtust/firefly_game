#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' Utility entity '

__author__ = 'Leo lu'

import time
import os

def is_dir_exists(path, search_dir):
    if type(path) != str:
        return None
    if type(search_dir) != str:
        return None

    cwd = os.getcwd()
    os.chdir(path)
    dirs = os.listdir()
    os.chdir(cwd)
    for d in dirs:
        if d == search_dir:
            return True
    return False

# If path is "/a/b/" using absulute directory
# else if path is "./a/b" using relative directory
def make_dir(path):
    if type(path) != str:
        return False

    cwd = os.getcwd()
    if ('/' == path[0]):
        cur_path = "/"
    elif ('.' == path[0]):
        path = path.lstrip('.')
        cur_path = cwd

    dirs = path.strip('/').split('/')
    for d in dirs:
        if not is_dir_exists(cur_path, d):
            os.chdir(cur_path)
            os.mkdir(d)
        cur_path = cur_path + "/" + d

    os.chdir(cwd)
    return True

def walk_to_dir(path):
    if type(path) != str:
        return False

    if ('/' == path[0]):
        os.chdir('/')
    elif ('.' == path[0]):
        path = path.lstrip('.')

    dirs = path.strip('/').split('/')
    for d in dirs:
        if not is_dir_exists(".", d):
            return False
        os.chdir(d)

    return True

def caculate_32bit_xor_checksum(data):
    # print("****", data, type(data))
    # if type(data) != bytearray or type(data) != list:
    #    return None

    bytes_len = len(data)
    checksum = bytearray(4)
    checksum[0] = 0
    checksum[1] = 0
    checksum[2] = 0
    checksum[3] = 0
    for i in range(int(bytes_len/4)):
        checksum[0] = checksum[0] ^ data[i*4 + 0]
        checksum[1] = checksum[1] ^ data[i*4 + 1]
        checksum[2] = checksum[2] ^ data[i*4 + 2]
        checksum[3] = checksum[3] ^ data[i*4 + 3]

    if ( bytes_len%4 ):
        for i in range(bytes_len%4):
            checksum[0+i] = checksum[0+i] ^ data[4*int(bytes_len/4) + i]

    return checksum