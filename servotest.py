# include the servo library
from servo import Servo
# include the time libarry
import time
# include the pin library
from machine import Pin
#initialise the pin to be an output-
#Servo is an output device
servopin=Pin(4, Pin.OUT)
# initialise the servo for use
pupilservo=Servo(servopin)

#write the angle to the servo
while (1):
    for i in range (0,180):
        pupilservo.write_angle(i)
        time.sleep(0.01)

    


