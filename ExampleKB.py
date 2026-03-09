from ble_keyboard import BLEKeyboard
from machine import Pin
import time

kb = BLEKeyboard("My_ESP32_Macropad")
btn = Pin(0, Pin.IN, Pin.PULL_UP)

print("Waiting for Bluetooth connection...")
time.sleep(5)
while True:
    if kb.is_connected():
        print("Button pressed!")
        
        # This will now type Z, X, C on new lines perfectly
        kb.type_text("Z\n")
        time.sleep_ms(50)
        kb.type_text("X\n")
        time.sleep_ms(50)
        kb.type_text("C\n")
        
        print("Waiting for you to release the button...")
        # CRITICAL: Do nothing until the button is released!
        while btn.value() == 0:
            time.sleep_ms(10)
            
        time.sleep_ms(50) # Debounce after release
        
    time.sleep_ms(20)

