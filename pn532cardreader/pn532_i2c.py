"""
PN532 I2C Driver for ESP32 (MicroPython)
Handles raw hex framing, checksums, and I2C polling.
"""
from machine import Pin, I2C
import time

class PN532_I2C:
    def __init__(self, scl_pin=22, sda_pin=21, i2c_addr=0x24):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
        self.addr = i2c_addr
        time.sleep(0.5) 
        if self.addr not in self.i2c.scan():
            raise RuntimeError("PN532 not found. Check wiring and ensure CH1=ON, CH2=OFF.")

    def _write_frame(self, data):
        length = len(data) + 1  
        lcs = (~length + 1) & 0xFF
        frame = bytearray([0x00, 0x00, 0xFF, length, lcs, 0xD4])
        
        for b in data:
            frame.append(b)
            
        checksum = (0xD4 + sum(data)) & 0xFF
        dcs = (~checksum + 1) & 0xFF
        frame.append(dcs)
        frame.append(0x00)
        self.i2c.writeto(self.addr, frame)

    def _wait_ready(self, timeout=1.0):
        buf = bytearray(1)
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < (timeout * 1000):
            try:
                self.i2c.readfrom_into(self.addr, buf)
                if buf[0] == 0x01:
                    return True  
            except OSError:
                pass 
            time.sleep_ms(10) 
        return False 

    def _read_data(self, num_bytes):
        buf = bytearray(num_bytes + 1)
        self.i2c.readfrom_into(self.addr, buf)
        return buf[1:] 

    def send_command(self, cmd_data, timeout=1.0):
        self._write_frame(cmd_data)
        if not self._wait_ready(timeout):
            return None
            
        ack = self._read_data(6)
        if list(ack) != [0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00]:
            return None

        if not self._wait_ready(timeout):
            return None
            
        response = self._read_data(32)
        if response[0:3] != b'\x00\x00\xFF':
            return None
            
        data_length = response[3]
        actual_data_len = data_length - 2 
        return response[7 : 7 + actual_data_len]

    def sam_configure(self):
        res = self.send_command([0x14, 0x01, 0x14, 0x00])
        return res is not None

    def read_passive_target(self):
        res = self.send_command([0x4A, 0x01, 0x00], timeout=0.5)
        if res and len(res) > 5 and res[0] == 0x01: 
            uid_len = res[5]
            return res[6 : 6 + uid_len]
        return None
