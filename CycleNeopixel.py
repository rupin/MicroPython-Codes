#lets import the libarries
from machine import Pin
import time

from neopixel import NeoPixel


# define a pin on which i attach the neopixel
dataPin=18

#create a variable for number of pixels
pixels=16


#initailise the switch and the neopixels

reedSwitch=Pin(4,PIN.IN, PIN.PULL_UP)

#create the neopixel abstract variable
np=NeoPixel(Pin(dataPin, Pin.OUT),pixels)

np.fill((0,0,0))
np.write()

last=0

while(1):
    reedSwitchValue=reedSwitch.value()
    if(reedSwitchValue==0):
        current=time.ticks_us()        
        timeDuration=(current-last)/1000000
        rpm=60/timeDuration
        
        last=current
        
        if(rpm>2):
        
    
    
    
    
    


# check for the reed switch to be triggered

# keep track of time as "last"

# check for the reed switch to be triggered again, keep track of time as "current"

#Subtract current from last, you get the duration of time, it takes the wheel to make one revolution.

# do some math to convert time to rpm.

# last=current