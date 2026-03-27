from applink import AppInventorLink
from machine import Pin, ADC
import time

app = AppInventorLink()
led = Pin(2, Pin.OUT)
sensor = ADC(Pin(34))

# This function runs every time the app makes a request
def handle_app_request(params):
    print("App asked for:", params)
    
    # 1. Handle commands from the app (e.g., ?action=led_on)
    if params.get("action") == "true":
        led.value(1)
        return {"status": "LED is now ON"}
        
    elif params.get("action") == "false":
        led.value(0)
        return {"status": "LED is now OFF"}
        
    # 2. Handle data requests from the app (e.g., ?get=sensor)
    elif params.get("get") == "sensor":
        val = sensor.read()
        return {"sensor_value": val}
        
    # Default response if parameters don't match
    return {"status": "Connected to ESP32!"}

# Start ESP32 in Access Point (Hotspot) mode
# The phone will connect to this Wi-Fi network
app.start_ap("TinkerVillage_Bot", "12345678")

# Link the function so the library knows what to run
app.on_request(handle_app_request)

# Main Loop
while True:
    app.process()
    time.sleep(0.1)

