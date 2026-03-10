from machine import Pin, ADC
import time
from simple_ble import BLEConnection
import random

my_bluetooth = BLEConnection("ESP32_Read_Write")
print("Ready! Scan for 'ESP32_Read_Write'")

# Add a timer to track when a connection actually started
connection_start_time = 0

while True:
    my_bluetooth.check_timeout(timeout_ms=5000)
    if my_bluetooth.is_connected():       
        
        # --- ONLY DO THIS IF THE DEVICE STAYED CONNECTED ---
        if my_bluetooth.any():
            raw_data = my_bluetooth.read()
            messages = raw_data.split('\n')
            for msg in messages:
                clean_msg = msg.replace('\x00', '').strip()
                if clean_msg: 
                    raw_array = clean_msg.split(',')
                    print("Clean Array:", raw_array)
                    
        # Existing Send Logic
        x_val = random.randint(0,800)
        y_val = random.randint(0,800)
        data_to_send = [x_val, y_val]
        my_bluetooth.send_array(data_to_send)
        
    
        
    time.sleep(0.25) 

