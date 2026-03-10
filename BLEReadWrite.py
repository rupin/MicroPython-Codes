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

            if message: # Extra safety check to ignore empty strings
                raw_array = message.split(',')
                clean_array = [item.split('\x00')[0] for item in raw_array]
                print("Clean Array:", clean_array)
                
        # --- Existing Send Logic ---
        x_val=random.randint(0,800)
        y_val=random.randint(0,800)
        
        data_to_send = [x_val, y_val]
        my_bluetooth.send_array(data_to_send)
        
    time.sleep(0.5) 
