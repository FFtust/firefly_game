from struct import * 
import re
import time
import os
import _thread
import math
from global_objects import music_o
from utility.common import *

PLAY_MAX_TIME = 86400

MUSIC_FILE_FOLDER_PATH = "/music"
MUSIC_FILE_HEAD_READ_LEN = 1024
MUSIC_FILE_SRC_BLOCK_SIZE = 4096 * 1

SOUNDS_PLAYING_TASK_STACK_SIZE = 4096
SOUNDS_PLAYING_TASK_PRIORITY = 1

SOUNDS_TYPE_WAV = 1
SOUNDS_TYPE_TONE = 2

def __read_music_file(file_name, offset = 0, size = None):
    cur_path = os.getcwd()
    os.chdir(MUSIC_FILE_FOLDER_PATH)
    
    music_file_list = os.listdir()
    if not file_name in music_file_list:
        print("music not exist")
        os.chdir(cur_path)
        return None

    with open(file_name, "rb") as f:
        f.seek(offset)
        if size:
            music_data = f.read(size)
        elif size == None:
            music_data = f.read()

    os.chdir(cur_path)
    return  music_data

class speaker(object):
    def __init__(self):
        self.need_to_stop_flag = False
        self.music_playing_list = []
        self.play_sync_sema = _thread.allocate_lock()
        self.play_over_sema = _thread.allocate_lock()
        self.play_over_sema.acquire(False)
        self.play_sync_sema.acquire(False)
        self.tempo_value = 60
        # use internal ram
        _thread.start_new_thread(self.__music_play_task, ())

    @property
    def volume(self):
        return round(music_o.get_volume())

    @volume.setter
    def volume(self, value):
        if not type_check(value, (int, float)):
            return
        value = num_range_scale(value, 0, 100)
        music_o.set_volume(int(value)) 

    @property
    def tempo(self):
        return round(self.tempo_value)

    @tempo.setter
    def tempo(self, value):
        if not type_check(value, (int, float)):
            return
        value = num_range_scale(value, 6, 600)  
        self.tempo_value = int(value)

    def stop_sounds(self):
        self.music_playing_list = []
        self.need_to_stop_flag = True
        time.sleep(0.01)
        self.play_sync_sema.acquire(False)

    def play_melody_until_done(self, file_name):
        if not type_check(file_name, str):
            return

        if file_name[-4 : ] != ".wav":
            file_name = file_name + ".wav"

        self.stop_sounds()
        self.music_playing_list.append([SOUNDS_TYPE_WAV, file_name])
        self.__start_playing()
        # wait melody over
        self.play_over_sema.acquire(True)

    def play_melody(self, file_name):
        if not type_check(file_name, str):
            return
        
        if file_name[-4 : ] != ".wav":
            file_name = file_name + ".wav"

        self.stop_sounds()
        self.music_playing_list.append([SOUNDS_TYPE_WAV, file_name])
        self.__start_playing()

    def play_tone(self, frequency, time_ms = None):
        if not type_check(frequency, (int, float)):
            return
        
        self.stop_sounds()
        frequency = num_range_scale(frequency, 0, 1000)
        if frequency <= 0:
            return

        if time_ms == None:
            time_ms = PLAY_MAX_TIME
            self.music_playing_list.append([SOUNDS_TYPE_TONE, int(frequency), time_ms])
            self.__start_playing()

        elif type_check(time_ms, (int, float)):
            time_ms = num_range_scale(time_ms, 0)
            if time_ms <= 0:
                return
            # wait melody over
            self.music_playing_list.append([SOUNDS_TYPE_TONE, int(frequency), time_ms])
            self.__start_playing()
            self.play_over_sema.acquire(True)
        
    def play_note(self, note, beat = None):
        if type_check(note, (int, float)):
            if note <= 0:
                return
            note = num_range_scale(note, 48, 72) 

            freq = MIDI_NOTE_NUM0 * math.pow(NOTE_FREQUENCE_RATIO, note)

        elif type_check(note, str):
            if note in node_table:
                freq = node_table[note]
            else:
                return
        
        self.stop_sounds()

        if beat == None:
            beat = PLAY_MAX_TIME
            self.music_playing_list.append([SOUNDS_TYPE_TONE, int(freq), beat * (60 / self.tempo_value)])
            self.__start_playing()

        elif type_check(beat, (int, float)):
            beat = num_range_scale(beat, 0)
            if beat <= 0:
                return
            self.music_playing_list.append([SOUNDS_TYPE_TONE, int(freq), beat * (60 / self.tempo_value)])
            self.__start_playing()
            # wait melody over
            self.play_over_sema.acquire(True)

    def rest(self, beat):
        if not type_check(beat, (int, float)):
            return 
        time.sleep(beat * (60 / self.tempo_value))

    def __start_playing(self):
        self.need_to_stop_flag = False
        if self.play_sync_sema.locked():
            self.play_sync_sema.release()

    def __wait_over(self):
        pass

    def __music_play_task(self):
        while True:
            # block to wait playing event
            self.play_sync_sema.acquire(True)
            temp_play_list = self.music_playing_list.copy()
            if temp_play_list != []:
                if temp_play_list[0][0] == SOUNDS_TYPE_WAV:
                    self.__play_voice(temp_play_list[0][1])
                    if self.play_over_sema.locked():
                        self.play_over_sema.release()
                elif temp_play_list[0][0] == SOUNDS_TYPE_TONE:
                    self.__play_tone(temp_play_list[0][1], temp_play_list[0][2])
                    if self.play_over_sema.locked():
                        self.play_over_sema.release()

    def __play_voice(self, file_name):
        head_data = __read_music_file(file_name, 0, MUSIC_FILE_HEAD_READ_LEN)
        if head_data == None:
            return
        src_info = music_o.parse_wav_src(head_data)
        if src_info == None:
            return

        offset =  src_info[0]
        data_size = src_info[1]
        if offset and data_size:
            read_offset = 0
            while True:
                if self.need_to_stop_flag == True:
                    self.need_to_stop_flag = False
                    break
                elif data_size - read_offset >= MUSIC_FILE_SRC_BLOCK_SIZE:
                    data = __read_music_file(file_name, read_offset + offset, MUSIC_FILE_SRC_BLOCK_SIZE)
                    if data:
                        music_o.start()
                        music_o.play_src_data(data)
                        read_offset += MUSIC_FILE_SRC_BLOCK_SIZE
                    else:
                        break
                else:
                    data = __read_music_file(file_name, read_offset + offset, data_size - read_offset)
                    music_o.play_src_data(data)
                    time.sleep(0.1)
                    music_o.stop()
                    break
                time.sleep(0.05)

    def __play_tone(self, frequency, time_ms):
        music_o.start()
        music_o.play_frequency(frequency)
        count = (time_ms * 1000) // 50
        for i in range(count):
            time.sleep(0.05)
            if self.need_to_stop_flag == True:
                self.need_to_stop_flag = False
                break
        music_o.stop()
