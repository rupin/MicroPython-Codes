def setColor(params):
    print("Data Recieved")
    print(params)    
    redValue=0
    greenValue=0
    blueValue=0
    if "R" in params:
        redValue=int(params.get("R"))
    if "G" in params:
        greenValue=int(params.get("G"))
    if "B" in params: 
        blueValue=int(params.get("B"))
    np.fill((redValue, greenValue, blueValue))
    np.write()


from applink import AppInventorLink
from machine import Pin
import time
from neopixel import NeoPixel
dataPin=18
pixels=16
#create the neopixel abstract variable
np=NeoPixel(Pin(dataPin, Pin.OUT),pixels)

np.fill((0,0,0))
np.write()

colorLamp = AppInventorLink()

# Start ESP32 in Access Point (Hotspot) mode
# The phone will connect to this Wi-Fi network
colorLamp.start_ap("colorLamp", "12345678")
colorLamp.on_request(setColor)

while(True):
    colorLamp.process()
    time.sleep_ms(100)
    




