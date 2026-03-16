from machine import TouchPad, Pin
import time
threshold=100
capacitiveValue=0
#threshold = 150 # Threshold to be adjusted
touch_pin = TouchPad(Pin(4))
led=Pin(2,Pin.OUT)

while (True): # An Infinite loop
    capacitiveValue = touch_pin.read()
    print(capacitiveValue)
    #led.value(0)
    if capacitiveValue < threshold:
        #led.value(1)
        print("Touch Detected")




