general_command_request_dict = \
{
  'assign_id': {'type': 16, 'subtype': None, 1: 'BYTE', 'para_num': 1}, 
  'reset_block': {'type': 17, 'subtype': None, 'para_num': 0}, 
  'query_version': {'type': 18, 'subtype': None, 'para_num': 0}, 
  'set_baud_rate': {'type': 19, 'subtype': None, 1: 'BYTE', 'para_num': 1},
  'test_traffic': {'type': 20, 'subtype': None, 1: 'BYTE', 2: 'BYTE', 3: 'BYTE', 4: 'BYTE', 5: 'BYTE', 'para_num': 5}, 
  'set_command_response': {'type': 97, 'subtype': 1, 1: 'BYTE', 'para_num': 1}, 
  'set_block_rgb_led': {'type': 97, 'subtype': 2, 1: 'byte', 2: 'byte', 3: 'byte', 'para_num': 3}, 
  'handshake': {'type': 97, 'subtype': 3, 'para_num': 0}
 }

general_command_response_dict = \
{
  4096: {'name': 'assign_id', 1: 'BYTE', 2: 'BYTE', 'para_num': 2}, 
  4608: {'name': 'query_version', 1: 'BYTE', 2: 'BYTE', 3: 'SHORT', 'para_num': 3}, 
  5376: {'name': 'universal_response', 1: 'BYTE', 'para_num': 1}
}

common_neurons_command_request_dict = \
{
 25090: {'name': 'dc_motor_driver', 'function': {'run': {'command_id': 1, 1: 'byte', 2: 'byte', 'para_num': 2}, 'run_motor1': {'command_id': 2, 1: 'byte', 'para_num': 1}, 'run_motor2': {'command_id': 3, 1: 'byte', 'para_num': 1}}}, 
 25602: {'name': 'button', 'function': {'is_pressed': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 26114: {'name': 'buzzer', 'function': {'tone': {'command_id': 1, 1: 'short', 2: 'BYTE', 'para_num': 2}}}, 
 25346: {'name': 'light_sensor', 'function': {'get_intensity': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25360: {'name': 'rocky', 'function': {'stop': {'command_id': 12, 'para_num': 0}, 'forword': {'command_id': 13, 1: 'BYTE', 'para_num': 1}, 'backword': {'command_id': 14, 1: 'BYTE', 'para_num': 1}, 'turn_right': {'command_id': 15, 1: 'BYTE', 'para_num': 1}, 'turn_left': {'command_id': 16, 1: 'BYTE', 'para_num': 1}, 'driver': {'command_id': 17, 1: 'BYTE', 2: 'BYTE', 3: 'BYTE', 4: 'BYTE', 'para_num': 4}, 'diff_turn_right': {'command_id': 18, 1: 'BYTE', 'para_num': 1}, 'diff_turn_left': {'command_id': 19, 1: 'BYTE', 'para_num': 1}, 'single_motor_run': {'command_id': 20, 1: 'BYTE', 2: 'BYTE', 3: 'BYTE', 'para_num': 3}}}, 
 25352: {'name': 'soil_moisture', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25345: {'name': 'temp_sensor', 'function': {'get_celsius': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25351: {'name': 'humiture_sensor', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25357: {'name': 'sound_sensor', 'function': {'get_loudness': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25607: {'name': 'joystick', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25601: {'name': 'knob', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25349: {'name': 'color_sensor', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25356: {'name': 'pir_sensor', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25348: {'name': 'dual_ir_detector', 'function': {'get_value': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25347: {'name': 'ultrasonic_sensor', 'function': {'get_centimeter': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25604: {'name': 'funny_touch', 'function': {'read': {'command_id': 1, 'para_num': 0}, 'set_report_mode': {'command_id': 127, 1: 'BYTE', 2: 'long', 'para_num': 2}}}, 
 25862: {'name': 'el_wire', 'function': {'set_all': {'command_id': 1, 1: 'BYTE', 'para_num': 1}, 'set_el1': {'command_id': 2, 1: 'BYTE', 'para_num': 1}, 'set_el2': {'command_id': 3, 1: 'BYTE', 'para_num': 1}, 'set_el3': {'command_id': 4, 1: 'BYTE', 'para_num': 1}, 'set_el4': {'command_id': 5, 1: 'BYTE', 'para_num': 1}}}, 
 25091: {'name': 'dual_servo', 'function': {'write': {'command_id': 1, 1: 'SHORT', 'para_num': 1}, 'write_servo1': {'command_id': 2, 1: 'SHORT', 'para_num': 1}, 'write_servo2': {'command_id': 3, 1: 'SHORT', 'para_num': 1}}}, 
 25858: {'name': 'rgb_led', 'function': {'set': {'command_id': 1, 1: 'SHORT', 2: 'SHORT', 3: 'SHORT', 'para_num': 3}, 'gradient_set': {'command_id': 2, 1: 'SHORT', 2: 'SHORT', 3: 'SHORT', 'para_num': 3}}}, 
 25859: {'name': 'rgb_strip', 'function': {'set': {'command_id': 1, 1: 'SHORT', 2: 'SHORT', 3: 'SHORT', 'para_num': 3}, 'set_mode': {'command_id': 2, 1: 'BYTE', 2: 'BYTE', 3: 'STR1', 'para_num': 3}}}, 
 25861: {'name': 'lcd_display', 'function': {'string': {'command_id': 1, 1: 'BYTE', 2: 'BYTE', 3: 'STR2', 'para_num': 3}, 'face': {'command_id': 2, 1: 'BYTE', 2: 'BYTE', 'para_num': 2}}}, 
 25860: {'name': 'full_color_led_matrix', 'function': {'set_all': {'command_id': 1, 1: 'long', 2: 'long', 3: 'SHORT', 4: 'SHORT', 5: 'SHORT', 'para_num': 5}, 'set_single': {'command_id': 2, 1: 'BYTE', 2: 'SHORT', 3: 'SHORT', 4: 'SHORT', 'para_num': 4}, 'set_panel': {'command_id': 3, 1: 'BYTE', 2: 'STR1', 'para_num': 2}, 'set_animation': {'command_id': 4, 1: 'BYTE', 2: 'STR1', 'para_num': 2}, 'show_animation': {'command_id': 5, 1: 'BYTE', 2: 'BYTE', 'para_num': 2}, 'string': {'command_id': 6, 1: 'SHORT', 2: 'SHORT', 3: 'SHORT', 4: 'STR1', 'para_num': 4}}}, 
 25350: {'name': 'gyro_sensor', 'function': {'is_shake': {'command_id': 1, 'para_num': 0}, 'get_acc_x': {'command_id': 2, 'para_num': 0}, 'get_acc_y': {'command_id': 3, 'para_num': 0}, 'get_acc_z': {'command_id': 4, 'para_num': 0}, 'get_gyr_x': {'command_id': 5, 'para_num': 0}, 'get_gyr_y': {'command_id': 6, 'para_num': 0}, 'get_gyr_z': {'command_id': 7, 'para_num': 0}, 'get_pitch': {'command_id': 8, 'para_num': 0}, 'get_rool': {'command_id': 9, 'para_num': 0}, 'get_yaw': {'command_id': 10, 'para_num': 0}}}
}

common_neurons_command_response_dict = \
{
 25602: {'name': 'button', 'function': {1: {'command_name': 'is_pressed', 1: 'BYTE', 'para_num': 1}}}, 
 25346: {'name': 'light_sensor', 'function': {1: {'command_name': 'get_intensity', 1: 'BYTE', 'para_num': 1}}}, 
 25352: {'name': 'soil_moisture', 'function': {1: {'command_name': 'get_value', 1: 'BYTE', 'para_num': 1}}}, 
 25345: {'name': 'temp_sensor', 'function': {1: {'command_name': 'get_celsius', 1: 'float', 'para_num': 1}}}, 
 25351: {'name': 'humiture_sensor', 'function': {1: {'command_name': 'get_value', 1: 'byte', 2: 'BYTE', 'para_num': 2}}}, 
 25357: {'name': 'sound_sensor', 'function': {1: {'command_name': 'get_loudness', 1: 'BYTE', 'para_num': 1}}}, 
 25607: {'name': 'joystick', 'function': {1: {'command_name': 'get_value', 1: 'byte', 2: 'byte', 'para_num': 2}}}, 
 25601: {'name': 'knob', 'function': {1: {'command_name': 'get_value', 1: 'BYTE', 'para_num': 1}}}, 
 25349: {'name': 'color_sensor', 'function': {1: {'command_name': 'get_value', 1: 'SHORT', 2: 'SHORT', 3: 'SHORT', 'para_num': 3}}}, 
 25356: {'name': 'pir_sensor', 'function': {1: {'command_name': 'get_value', 1: 'BYTE', 'para_num': 1}}}, 
 25348: {'name': 'dual_ir_detector', 'function': {1: {'command_name': 'get_value', 1: 'BYTE', 'para_num': 1}}}, 
 25347: {'name': 'ultrasonic_sensor', 'function': {1: {'command_name': 'get_centimeter', 1: 'float', 'para_num': 1}}}, 
 25604: {'name': 'funny_touch_1', 'function': {1: {'command_name': 'is_touch', 1: 'BYTE', 'para_num': 1}}}, 
 25350: {'name': 'gyro_sensor', 'function': {1: {'command_name': 'is_shake', 1: 'BYTE', 'para_num': 1}, 2: {'command_name': 'get_acc_x', 1: 'float', 'para_num': 1}, 3: {'command_name': 'get_acc_y', 1: 'float', 'para_num': 1}, 4: {'command_name': 'get_acc_z', 1: 'float', 'para_num': 1}, 5: {'command_name': 'get_gyr_x', 1: 'float', 'para_num': 1}, 6: {'command_name': 'get_gyr_y', 1: 'float', 'para_num': 1}, 7: {'command_name': 'get_gyr_z', 1: 'float', 'para_num': 1}, 8: {'command_name': 'get_pitch', 1: 'short', 'para_num': 1}, 9: {'command_name': 'get_rool', 1: 'short', 'para_num': 1}, 10: {'command_name': 'get_yaw', 1: 'short', 'para_num': 1}}}
 }

common_neurons_command_default_result_dict = \
{
 'button': {'is_pressed': [0]}, 
 'light_sensor': {'get_intensity': [0]}, 
 'soil_moisture': {'get_value': [0]}, 
 'temp_sensor': {'get_celsius': [0]}, 
 'humiture_sensor': {'get_value': [0, 0]}, 
 'sound_sensor': {'get_loudness': [0]}, 
 'joystick': {'get_value': [0, 0]}, 
 'knob': {'get_value': [0]}, 
 'color_sensor': {'get_value': [0, 0, 0]}, 
 'pir_sensor': {'get_value': [0]}, 
 'dual_ir_detector': {'get_value': [0]}, 
 'ultrasonic_sensor': {'get_centimeter': [0]}, 
 'funny_touch_1': {'is_touch': [0]}, 
 'gyro_sensor': {'is_shake': [0], 'get_acc_x': [0], 'get_acc_y': [0], 'get_acc_z': [0], 'get_gyr_x': [0], 'get_gyr_y': [0], 'get_gyr_z': [0], 'get_pitch': [0], 'get_rool': [0], 'get_yaw': [0]}
}