# import the time library
import time
# import the pin library
from machine import Pin
import random
# set the D4 pin to be an input with a pullup
switch=Pin(4,Pin.IN, Pin.PULL_UP)
# set the led pin d2 to be an output
led=Pin(2, Pin.OUT)

#set the led to off.
led.off()

number = random.randint(1,3)
#wait 5 seconds plus a random amount of time
time.sleep(5+number)
# turn the led on

#turn on the first neopixel led
np[0]=(128,0,0)
np.write()

time.sleep(0.5)

#turn on the second neopixel led
np[1]=(128,0,0)
np.write()

time.sleep(0.5)


start=time.ticks_us()
# keep a snapshot of the time here. this is the START time. 

# start a while loop to constantly check the switch being pressed
while(1):
    switchState=switch.value()
    
    
    #if the switch is pressed, the voltage on the pin will be 0v
    # else it will be 3.3v
    # when the switch is pressed, keep a snapshot of the time, this is the END time
    if(switchState==0):
        end=time.ticks_us()
        reactionTime=(end-start)/1000000
        print(reactionTime)
        
        if(reactionTime<0.5):
            print("Oh that was fast!")
        if(reactionTime>0.5 and reactionTime<1.5):
            print("Oh that was ok!")
        if(reactionTime>1.5 ):
            print("Do you need Coffee?")
        break

# subtract the START from the END, that is the reaction time