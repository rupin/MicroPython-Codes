# simple_ble.py - Student Library (Do not modify. Save to ESP32)
import bluetooth
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
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
        
        # Build the foolproof advertising payload we know works
        self._payload = bytearray()
        
        # 1. Flags (General Discoverable)
        self._payload.append(0x02) # Length 2
        self._payload.append(0x01) # Type: Flags
        self._payload.append(0x06) # Value: General Discoverable
        
        # 2. Local Name
        name_bytes = name.encode('utf-8')
        self._payload.append(len(name_bytes) + 1) # Length + 1 byte for type
        self._payload.append(0x09) # Type: Complete Local Name
        self._payload.extend(name_bytes)
        
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("App connected!")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("App disconnected. Advertising again...")
            self._advertise()



    def is_connected(self):
        return len(self._connections) > 0

    def send_array(self, data_list):
        """Converts [1024, 2048] to "1024,2048\n" and sends via BLE"""
        if not self.is_connected():
            return
            
        str_data = ",".join(str(item) for item in data_list) + "\n"
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx, str_data.encode())

    def _advertise(self):
        self._ble.gap_advertise(100000, adv_data=self._payload)

