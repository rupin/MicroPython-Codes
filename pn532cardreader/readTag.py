import time
from pn532_i2c import PN532_I2C

# Initialize the reader using the custom library
reader = PN532_I2C(scl_pin=22, sda_pin=21)

if reader.sam_configure():
    print("PN532 is ready! Tap a tag...")
    
    while True:
        uid = reader.read_passive_target()
        
        if uid:
            # Convert the raw bytes into a formatted string (e.g., "04:3C:40...")
            uid_hex = ":".join(["{:02X}".format(b) for b in uid])
            print(f"Tag UID: {uid_hex}")
            
            # Wait 1 second so it doesn't read the same tag 100 times
            time.sleep(1) 
            
        time.sleep(0.1) # Short delay to prevent overwhelming the I2C bus
else:
    print("Failed to initialize PN532.")
