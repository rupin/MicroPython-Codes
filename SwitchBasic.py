from machine import Pin
import time

#switch=Pin(4,Pin.IN)
switch=Pin(4,Pin.IN, Pin.PULL_UP)
led=Pin(2, Pin.OUT)

#_______________________________________________________________________________________

while(1):
    switchState=switch.value()
    if(switchState==0):
        print("Switch Is Pressed")
        # write any statement here that can execute when switch is pressed
        led.on()
    if(switchState==1):
        print("Switch Is Not Pressed")
        # write any statement here that can execute when switch is *not* pressed
        led.off()
    time.sleep(0.1)