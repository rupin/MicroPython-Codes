from machine import Pin
import time
switch1=Pin(4,Pin.IN,Pin.PULL_UP) #connect a switch to pin 4, add a pullup resistor
#switch2=Pin(5,Pin.IN,Pin.PULL_UP) #connect a switch to pin 4, add a pullup resistor
led=Pin(2, Pin.OUT) # use the led on the board. 
count=0
while(1):
    
    switchstate1=switch1.value()
    #switchstate2=switch2.value()
    time.sleep(0.1)
    #Check if the switch is pressed, if yes, turn on the LED
    if(switchstate1==0):
        count=count+1        
        
    if (count%2==0):
        led.on()
    if (count%2==1):
        led.off()
    
        
        
    #print(switchstate)
    time.sleep(0.01)
    








