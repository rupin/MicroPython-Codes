# simple_ble.py - Two-Way Communication Library
import bluetooth
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3) # <--- Added Write Interrupt

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), const(0x0002) | const(0x0010))
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), const(0x0004) | const(0x0008))
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX))

class BLEConnection:
    def __init__(self, name="ESP32_Etch"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx, self._rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._rx_buffer = bytearray() # <--- Added Buffer to store incoming messages
        
        self._payload = bytearray()
        self._payload.append(0x02)
        self._payload.append(0x01)
        self._payload.append(0x06)
        name_bytes = name.encode('utf-8')
        self._payload.append(len(name_bytes) + 1)
        self._payload.append(0x09)
        self._payload.extend(name_bytes)
        
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            self._advertise()
            
        elif event == _IRQ_GATTS_WRITE: # <--- App has sent us data!
            conn_handle, value_handle = data
            if conn_handle in self._connections and value_handle == self._rx:
                # Read the data from the Bluetooth hardware and add to buffer
                self._rx_buffer += self._ble.gatts_read(self._rx)

    def is_connected(self):
        return len(self._connections) > 0

    def send_array(self, data_list):
        if not self.is_connected():
            return
        str_data = ",".join(str(item) for item in data_list) + "\n"
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx, str_data.encode())

    # --- NEW: Student-facing Read Functions ---
    def any(self):
        """Returns True if there is unread data from the phone."""
        return len(self._rx_buffer) > 0

    def read(self):
        """Reads the incoming message as a string and clears the buffer."""
        if not self.any():
            return ""
        
        # Decode the bytes to a string
        message = self._rx_buffer.decode('utf-8').strip()
        # Clear the buffer so we don't read it twice
        self._rx_buffer = bytearray() 
        return message

    def _advertise(self):
        self._ble.gap_advertise(100000, adv_data=self._payload)
