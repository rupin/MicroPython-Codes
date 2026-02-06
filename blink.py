from machine import Pin
import time
led=Pin(4,Pin.OUT)

times=5
counter=0
delay=0.5

while(delay>0):
    led.on()
    time.sleep_us(1136)
    led.off()
    time.sleep_us(1136)
    





