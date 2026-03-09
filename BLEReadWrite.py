from machine import Pin, ADC
import time
from simple_ble import BLEConnection
import random


my_bluetooth = BLEConnection("ESP32_Etch_Write")
print("Ready! Scan for 'ESP32_Etch'")

while True:
    if my_bluetooth.is_connected():
        
        # --- NEW: Check for incoming messages ---
        if my_bluetooth.any():
            message = my_bluetooth.read()
            print("Received from phone:", message)
            
            if message == "CLEAR":
                print("App cleared the screen. Maybe we should play a sound?")
            elif message == "RED":
                print("App changed color to red!")
                
        # --- Existing Send Logic ---
        x_val=random.randint(0,800)
        y_val=random.randint(0,800)
        
        # Put data in an array (list)
        data_to_send = [x_val, y_val]
        #data_to_send = [pot_x.read(), pot_y.read()]
        my_bluetooth.send_array(data_to_send)
        
        time.sleep(0.5) 

