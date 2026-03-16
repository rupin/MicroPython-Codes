from applink import AppInventorLink
from machine import Pin, ADC
import time

app = AppInventorLink()


# Start ESP32 in Access Point (Hotspot) mode
# The phone will connect to this Wi-Fi network
app.start_ap("WifiDemo", "12345678")

# Link the function so the library knows what to run
#app.on_request(handle_app_request)

# Main Loop
while True:
    app.process()
    time.sleep(0.1)

