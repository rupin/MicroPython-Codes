from machine import Pin
from machine import ADC
import time
samples=10

sensor=ADC(Pin(34))

#set the ADC to 3.3v range
sensor.atten(ADC.ATTN_11DB)

#set the ADC division to 4096
sensor.width(ADC.WIDTH_12BIT)

minimum=4096
maximum=0

while(1):
    sum=0
    for i in range(samples):        
        sensorValue=sensor.read()
        sum=sum+sensorValue
    avgvalue=sum/samples
    
    if(avgvalue > maximum):
        maximum=avgvalue
        print("Maximum Till now is :" + str(maximum))
    if(avgvalue< minimum):
        minimum=avgvalue
        print("Minimum Till now is :" + str(minimum))
        
    servoAngle=int(1.2 * avgvalue - 2520)
    print(servoAngle)
    
    
    #print(avgvalue)
    time.sleep(0.1)



