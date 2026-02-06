from machine import Pin
import time
# by default D2 is an input pin, convert it first to
# an output pin.
led1=Pin(2,Pin.OUT)
led2=Pin(4,Pin.OUT)

while(1):
    led1.on()
    time.sleep(0.25)
    
    led2.on()
    time.sleep(0.25)
    
    led1.off()
    time.sleep(0.25)
    
    led2.off()
    time.sleep(0.25)

# repeat the next two commands forever
    # turn on the led connected to Pin D2

    # turn off the led connected to Pin D2

