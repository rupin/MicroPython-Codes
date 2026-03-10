from machine import Pin, ADC
import time
from simple_ble import BLEConnection
import random


my_bluetooth = BLEConnection("ESP32_Read_Write")
print("Ready! Scan for 'ESP32_Read_Write'")

while True:
    if my_bluetooth.is_connected():
        
        # --- FIX: Only read and print IF data has arrived ---
        if my_bluetooth.any():
            message = my_bluetooth.read()
            print(message)
            if message: # Extra safety check to ignore empty strings
                first_packet = message.split('\x00')[0]                
                raw_array = first_packet.split(',')
                print("Clean Array:", raw_array)
                
        # --- Existing Send Logic ---
        x_val=random.randint(0,400)
        y_val=random.randint(0,400)
        
        data_to_send = [x_val, y_val]
        my_bluetooth.send_array(data_to_send)
        
    time.sleep(0.25) 
