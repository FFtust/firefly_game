import makeblock 

if makeblock.DRIVER_ENABLE:
    from makeblock import sensors
    senosors_o = sensors()

    # sensor objects
    if makeblock.BUTTON_ENABLE:
        from makeblock import button as button_t
        button_o = button_t()
    if makeblock.GYRO_ENABLE:
        from makeblock import gyro as gyro_t
        gyro_o = gyro_t()
    if makeblock.LED_MATRIX_ENABLE:
        from makeblock import led_matrix as led_matrix_t
        led_matrix_o = led_matrix_t()
    if makeblock.TOUCHPAD_ENABLE:
        from makeblock import touchpad as touchpad_t
        touchpad_o = touchpad_t()
    if makeblock.VIBRATION_MOTOR_ENABLE:
        from makeblock import vibration_motor as vibration_motor_t
        vibration_motor_o = vibration_motor_t()
    if makeblock.PIN_ENABLE:
        from makeblock import pin as pin_t
        pin_o = pin_t()
    if makeblock.BATTERY_ENABLE:
        from makeblock import battery as battery_t
        battery_o = battery_t()
    if makeblock.I2S_MIC_ENABLE:
        mic_o = makeblock.i2s_mic()

# event
if makeblock.EVENT_ENABLE:
    from makeblock import event as event_t
    event_o = event_t()

# music
if makeblock.MUSIC_ENABLE:
    from makeblock import music as music_t
    music_o = music_t()

# communication module objext
if makeblock.COMMUNICATION_ENABLE:
    from makeblock import communication
    communication_o = communication()
    
# stop script
if makeblock.STOP_PYTHON_THREAD_ENABLE:
    from makeblock import stop_script
    stop_script_o = stop_script()

# wifi
if makeblock.WIFI_ENABLE:
    wifi_o = makeblock.wifi()
    # mesh
    if makeblock.WIFI_MESH_ENABLE:
        mesh_o = makeblock.wifi_mesh()
    if makeblock.I2S_MIC_ENABLE:
        # speech_recognition
        speech_recognition_o = makeblock.speech_recognition()