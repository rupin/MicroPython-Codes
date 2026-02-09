from machine import Pin
import time

in1=Pin(2,Pin.OUT)
in2=Pin(4,Pin.OUT)
in3=Pin(18,Pin.OUT)
in4=Pin(19, Pin.OUT)

delay=2 # this is 2 milliseconds

stepPattern=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

for step in stepPattern:
    in1.value(step[0])
    in2.value(step[1])
    in3.value(step[2])
    in4.value(step[3])
    time.sleep_ms(delay)
    
