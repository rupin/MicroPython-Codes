from machine import Pin
import time

in1=Pin(2,Pin.OUT)
in2=Pin(4,Pin.OUT)
in3=Pin(18,Pin.OUT)
in4=Pin(19, Pin.OUT)

delay=0.002 # this is 2 milliseconds
while(1):
    in1.on()  #1
    in2.off() #0
    in3.off() #0
    in4.off() #0
    time.sleep(delay)

    # one step is completed

    in1.off()  #0
    in2.on() #1
    in3.off() #0
    in4.off() #0
    time.sleep(delay)

    #second step is complete

    in1.off()  #0
    in2.off() #0
    in3.on() #1
    in4.off() #0
    time.sleep(delay)


    in1.off()  #0
    in2.off() #0
    in3.off() #0
    in4.on() #1
    time.sleep(delay)





