# main.py - Student Code
from machine import Pin, ADC
import time
from simple_ble import BLEConnection
import random

led=Pin(2, Pin.OUT)

led.on()
time.sleep(1)
led.off()
time.sleep(1)

# 1. Setup the Potentiometers (Volume Dials)
pot_x = ADC(Pin(34))
pot_y = ADC(Pin(35))

# Expand range to 0-4095
pot_x.atten(ADC.ATTN_11DB)
pot_y.atten(ADC.ATTN_11DB)

# 2. Start Bluetooth
print("Starting Bluetooth...")
my_bluetooth = BLEConnection("EtchASketch")
print("Ready! Scan for 'EtchASketch' on your app.")

while True:
    if my_bluetooth.is_connected():
        # Read the analog values
        #x_val = pot_x.read()
        #y_val = pot_y.read()
        
        x_val=random.randint(0,800)
        y_val=random.randint(0,800)
        
        # Put data in an array (list)
        data_to_send = [x_val, y_val]
        
        # Send it to the app
        my_bluetooth.send_array(data_to_send)
        print("Sent:", data_to_send)
        
        # Small delay so we don't crash the app with too much data
        time.sleep(0.5) 


