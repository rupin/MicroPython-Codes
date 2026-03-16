from ble_keyboard import BLEKeyboard
from machine import Pin
import time

# 1. Initialize the Bluetooth Keyboard
kb = BLEKeyboard("rupinkb1") # Name should be less then 10 characters

print("Waiting for Bluetooth connection...")
connection_ready = False
left=Pin(18, Pin.IN, Pin.PULL_UP)
right=Pin(19, Pin.IN, Pin.PULL_UP)

while(True):
    time.sleep_ms(1)
    if kb.is_connected():
        if not connection_ready:
            print("Connected! Waiting 2 seconds for OS security handshake...")
            time.sleep(2)            
            connection_ready = True
            
        leftVal=left.value()
        rightVal=right.value()
        
        
        
        if (leftVal==0): # this means the switch is pressed
            #print("Sending left key")
            kb.arrow_left()
            time.sleep_ms(1)
        if (rightVal==0): # this means the switch is pressed
            #print("Sending right key")
            kb.arrow_right()
            time.sleep_ms(1)
    else:
        connection_ready = False
    

