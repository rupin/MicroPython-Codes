from machine import Pin, ADC
import time
from simple_ble import BLEConnection
import random
from neopixel import NeoPixel

# define a pin on which i attach the neopixel
dataPin=18

#create a variable for number of pixels
pixels=16
np=NeoPixel(Pin(dataPin, Pin.OUT),pixels)
my_bluetooth = BLEConnection("ESP32_ReadRupin_Write")
print("Ready! Scan for 'ESP32_Read_Write'")
redValue=0
greenValue=0
blueValue=0
switchPosition="false"
# Add a timer to track when a connection actually started
connection_start_time = 0

while True:
    #my_bluetooth.check_timeout(timeout_ms=5000)
    if my_bluetooth.is_connected():       
        
        # --- ONLY DO THIS IF THE DEVICE STAYED CONNECTED ---
        if my_bluetooth.any():
            raw_data = my_bluetooth.read()
            messages = raw_data.split('\n')
            for msg in messages:
                clean_msg = msg.replace('\x00', '').strip()
                if clean_msg: 
                    raw_array = clean_msg.split(',')
                    print("Clean Array:", raw_array)
                    #data=raw_array[0].split()
                    
                    if (raw_array[0]=="R"):
                        redValue=int(raw_array[1])
                    if (raw_array[0]=="G"):
                        greenValue=int(raw_array[1])
                    if (raw_array[0]=="B"):
                        blueValue=int(raw_array[1])
                    if (raw_array[0]=="S"):
                        switchPosition=raw_array[1]
                    
#                    
                    if(switchPosition=="true"):
                        np.fill((redValue,greenValue,blueValue))
                        np.write()
                    if(switchPosition=="false"):
                        np.fill((0,0,0))
                        np.write()
                        
                    
                    
                    
        # Existing Send Logic
        x_val = random.randint(0,800)
        y_val = random.randint(0,800)
        data_to_send = [x_val, y_val]
        my_bluetooth.send_array(data_to_send)
        
    
        
    time.sleep(0.25) 

