import bluetooth
import time
from micropython import const
import ubinascii

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), const(0x0002) | const(0x0010))
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), const(0x0004) | const(0x0008))
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX))

class BLEConnection:
    def __init__(self, base_name="ESP32_"):
        self._ble = bluetooth.BLE()
        self._ble.active(False)
        self._ble.active(True)
            
        mac_bytes = self._ble.config('mac')[1]
        hex_mac = ubinascii.hexlify(mac_bytes).decode().upper()
        self.device_name = base_name + hex_mac[-4:]
        self._ble.config(gap_name=self.device_name)
        
        self._ble.irq(self._irq)
        ((self._tx, self._rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        
        self._connections = set()
        self._rx_buffer = bytearray() 
        
        # Track the time of the last received message
        self._last_msg_time = 0 
        
        self._payload = bytearray()
        self._payload.append(0x02)
        self._payload.append(0x01)
        self._payload.append(0x06)
        name_bytes = self.device_name.encode('utf-8')
        self._payload.append(len(name_bytes) + 1)
        self._payload.append(0x09)
        self._payload.extend(name_bytes)

        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            # data contains: conn_handle, addr_type, addr
            conn_handle, addr_type, addr = data
            self._connections.add(conn_handle)
            
            # Reset the timeout timer
            self._last_msg_time = time.ticks_ms()
            
            # Extract and print the connecting device's MAC address
            mac_addr = ":".join(["{:02X}".format(b) for b in addr])
            print("Connected! Device MAC:", mac_addr)
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("Disconnected. Restarting advertising...")
            self._advertise()
            
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if conn_handle in self._connections and value_handle == self._rx:
                self._rx_buffer += self._ble.gatts_read(self._rx)
                # Update the timer every time data is written
                self._last_msg_time = time.ticks_ms()

    def check_timeout(self, timeout_ms=2000):
        # Force a disconnect if no data has been received within timeout_ms
        if self._connections and time.ticks_diff(time.ticks_ms(), self._last_msg_time) > timeout_ms:
            print("Connection timed out (no messages for {}ms). Forcing disconnect...".format(timeout_ms))
            for conn_handle in list(self._connections):
                try:
                    self._ble.gap_disconnect(conn_handle)
                except OSError:
                    pass
            self._connections.clear()
            self._advertise()
                
    def is_connected(self):
        return len(self._connections) > 0

    def send_array(self, data_list):
        if not self.is_connected():
            return
            
        str_data = ",".join(str(item) for item in data_list) + "\n"
        
        for conn_handle in list(self._connections):
            try:
                self._ble.gatts_notify(conn_handle, self._tx, str_data.encode())
            except OSError:
                pass 

    def any(self):
        return len(self._rx_buffer) > 0

    def read(self):
        if not self.any():
            return ""
        raw_bytes = self._rx_buffer
        self._rx_buffer = bytearray() 
        return raw_bytes.decode('utf-8').replace('\x00', '').strip()

    def _advertise(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload, connectable=True)

