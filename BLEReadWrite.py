from machine import Pin, ADC
import time
from simple_ble import BLEConnection
import random


my_bluetooth = BLEConnection("ESP32_Read_Write")
print("Ready! Scan for 'ESP32_Read_Write'")

while True:
    if my_bluetooth.is_connected():
        
        # --- NEW: Check for incoming messages ---
        message = my_bluetooth.read()

        # Split by comma
        raw_array = message.split(',')

        # Clean out the \x00 character from each item in the list
        clean_array = [item.split('\x00')[0] for item in raw_array]
            
        print("Clean Array:", clean_array)
            
            
                
        # --- Existing Send Logic ---
        x_val=random.randint(0,800)
        y_val=random.randint(0,800)
        
        # Put data in an array (list)
        data_to_send = [x_val, y_val]
        #data_to_send = [pot_x.read(), pot_y.read()]
        my_bluetooth.send_array(data_to_send)
        
        time.sleep(0.5) 

