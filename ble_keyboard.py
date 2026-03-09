import bluetooth, struct, time

_HID_MAP = bytes([
    0x05, 0x01, 0x09, 0x06, 0xA1, 0x01, 0x85, 0x01, 0x05, 0x07, 
    0x19, 0xE0, 0x29, 0xE7, 0x15, 0x00, 0x25, 0x01, 0x75, 0x01, 
    0x95, 0x08, 0x81, 0x02, 0x95, 0x01, 0x75, 0x08, 0x81, 0x01, 
    0x95, 0x06, 0x75, 0x08, 0x15, 0x00, 0x25, 0x65, 0x19, 0x00, 
    0x29, 0x65, 0x81, 0x00, 0xC0
])

class BLEKeyboard:
    def __init__(self, name="ESP32_KB"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._connected = False
        self._conn_handle = None
        
        # io=3 means "No Input No Output". This tells the PC to use "Just Works" 
        # silent pairing without asking you to type a PIN code.
        try:
            self._ble.config(gap_name=name, io=3) 
        except:
            self._ble.config(gap_name=name)

        F_R = bluetooth.FLAG_READ
        F_R_N = bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
        F_R_W = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE

        # 1. Device Information Service (Required by Windows/Mac for HID devices)
        dev_info = (
            bluetooth.UUID(0x180A), (
                (bluetooth.UUID(0x2A50), F_R), # PnP ID
            )
        )
        
        # 2. HID Service
        hid_service = (
            bluetooth.UUID(0x1812), (
                (bluetooth.UUID(0x2A4A), F_R),
                (bluetooth.UUID(0x2A4B), F_R),
                (bluetooth.UUID(0x2A4D), F_R_N, ((bluetooth.UUID(0x2908), F_R),)),
                (bluetooth.UUID(0x2A4E), F_R_W),
            )
        )
        
        services = self._ble.gatts_register_services((dev_info, hid_service))
        
        # Write standard PnP ID so the OS accepts it
        self._h_pnp = services[0][0]
        self._ble.gatts_write(self._h_pnp, b"\x02\x5e\x04\x01\x00\x00\x01") 
        
        # Setup HID characteristics
        self._h_info, self._h_map, self._h_rep, self._h_rep_ref, self._h_proto = services[1]
        self._ble.gatts_write(self._h_info, b"\x11\x01\x00\x02") 
        self._ble.gatts_write(self._h_map, _HID_MAP)
        self._ble.gatts_write(self._h_rep_ref, bytes([1, 1])) 
        self._ble.gatts_write(self._h_proto, b"\x01") 
        
        adv = bytearray()
        adv.extend(b"\x02\x01\x06")
        adv.extend(b"\x03\x19\xc1\x03")
        adv.extend(b"\x03\x03\x12\x18")
        adv.extend(bytes([len(name) + 1, 0x09]) + name.encode())
        self._adv_payload = bytes(adv)
        self._advertise()

    def _irq(self, event, data):
        if event == 1:
            self._conn_handle, _, _ = data
            self._connected = True
        elif event == 2:
            self._connected = False
            self._conn_handle = None
            self._advertise()
        elif event == 17: # _IRQ_PASSKEY_ACTION
            # The PC is requesting pairing. We must accept it to stay connected!
            conn_handle, action, passkey = data
            try:
                self._ble.gap_passkey(conn_handle, action, 1)
            except:
                pass

    def _advertise(self):
        self._ble.gap_advertise(100_000, self._adv_payload)

    def is_connected(self):
        return self._connected

    def _send(self, payload):
        if not self._connected: return
        for _ in range(10):  
            try:
                self._ble.gatts_notify(self._conn_handle, self._h_rep, payload)
                return
            except OSError as e:
                if e.args[0] == 12:  # ENOMEM
                    time.sleep_ms(20) 
                else:
                    raise

    def send_raw(self, keycode, modifier=0):
        self._send(struct.pack("8B", modifier, 0, keycode, 0, 0, 0, 0, 0))
        time.sleep_ms(15)
        self._send(b"\x00" * 8)
        time.sleep_ms(15)

    def enter(self): self.send_raw(0x28)
    def esc(self): self.send_raw(0x29)
    def backspace(self): self.send_raw(0x2A)
    def tab(self): self.send_raw(0x2B)
    def space(self): self.send_raw(0x2C)
    def arrow_right(self): self.send_raw(0x4F)
    def arrow_left(self): self.send_raw(0x50)
    def arrow_down(self): self.send_raw(0x51)
    def arrow_up(self): self.send_raw(0x52)
    def ctrl_c(self): self.send_raw(0x06, modifier=0x01)
    def ctrl_v(self): self.send_raw(0x19, modifier=0x01)
    def ctrl_z(self): self.send_raw(0x1D, modifier=0x01)
    def win(self): self.send_raw(0x00, modifier=0x08)     
    def win_d(self): self.send_raw(0x07, modifier=0x08)   
    def volume_up(self): self.send_raw(0x80)
    def volume_down(self): self.send_raw(0x81)
    
    def type_text(self, text):
        for c in text:
            if 'a' <= c <= 'z': self.send_raw(0x04 + ord(c) - ord('a'))
            elif 'A' <= c <= 'Z': self.send_raw(0x04 + ord(c) - ord('A'), modifier=0x02)
            elif '1' <= c <= '9': self.send_raw(0x1E + ord(c) - ord('1'))
            elif c == '0': self.send_raw(0x27)
            elif c == ' ': self.space()
            elif c == '\n': self.enter()
            time.sleep_ms(20)

