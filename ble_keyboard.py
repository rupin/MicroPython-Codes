import bluetooth, struct, time, json

_K = {
    'a':(4,0),'b':(5,0),'c':(6,0),'d':(7,0),'e':(8,0),'f':(9,0),'g':(10,0),'h':(11,0),'i':(12,0),
    'j':(13,0),'k':(14,0),'l':(15,0),'m':(16,0),'n':(17,0),'o':(18,0),'p':(19,0),'q':(20,0),
    'r':(21,0),'s':(22,0),'t':(23,0),'u':(24,0),'v':(25,0),'w':(26,0),'x':(27,0),'y':(28,0),'z':(29,0),
    'A':(4,2),'B':(5,2),'C':(6,2),'D':(7,2),'E':(8,2),'F':(9,2),'G':(10,2),'H':(11,2),'I':(12,2),
    'J':(13,2),'K':(14,2),'L':(15,2),'M':(16,2),'N':(17,2),'O':(18,2),'P':(19,2),'Q':(20,2),
    'R':(21,2),'S':(22,2),'T':(23,2),'U':(24,2),'V':(25,2),'W':(26,2),'X':(27,2),'Y':(28,2),'Z':(29,2),
    '1':(30,0),'2':(31,0),'3':(32,0),'4':(33,0),'5':(34,0),'6':(35,0),'7':(36,0),'8':(37,0),'9':(38,0),'0':(39,0),
    '!':(30,2),'@':(31,2),'#':(32,2),'$':(33,2),'%':(34,2),'^':(35,2),'&':(36,2),'*':(37,2),'(':(38,2),')':(39,2),
    '\n':(40,0),'\b':(42,0),'\t':(43,0),' ':(44,0),'-':(45,0),'=':(46,0),'[':(47,0),']':(48,0),
    '\\':(49,0),';':(51,0),"'":(52,0),'`':(53,0),',':(54,0),'.':(55,0),'/':(56,0),
    '_':(45,2),'+':(46,2),'{':(47,2),'}':(48,2),'|':(49,2),':':(51,2),'"':(52,2),'~':(53,2),
    '<':(54,2),'>':(55,2),'?':(56,2)
}

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
        
        # Load any saved pairing keys from previous sessions
        self._secrets = {}
        try:
            with open('ble_secrets.json', 'r') as f:
                saved = json.load(f)
                for k, v in saved.items():
                    self._secrets[k] = bytes(v) if v else None
        except:
            pass

        # Windows/Mac strict bonding requirement
        try:
            self._ble.config(gap_name=name, io=3, bond=True, le_secure=True)
        except:
            self._ble.config(gap_name=name)

        F_R = bluetooth.FLAG_READ
        F_R_N = bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
        F_R_W = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE
        
        bat_service = (bluetooth.UUID(0x180F), ((bluetooth.UUID(0x2A19), F_R_N),))
        dev_info = (bluetooth.UUID(0x180A), ((bluetooth.UUID(0x2A50), F_R),))
        hid_service = (bluetooth.UUID(0x1812), (
            (bluetooth.UUID(0x2A4A), F_R), (bluetooth.UUID(0x2A4B), F_R),
            (bluetooth.UUID(0x2A4D), F_R_N, ((bluetooth.UUID(0x2908), F_R),)),
            (bluetooth.UUID(0x2A4E), F_R_W),
        ))

        services = self._ble.gatts_register_services((bat_service, dev_info, hid_service))
        
        self._h_bat = services[0][0]
        self._ble.gatts_write(self._h_bat, b"\x64") 
        self._h_pnp = services[1][0]
        self._ble.gatts_write(self._h_pnp, b"\x02\x5e\x04\x01\x00\x00\x01") 
        
        self._h_info, self._h_map, self._h_rep, self._h_rep_ref, self._h_proto = services[2]
        self._ble.gatts_write(self._h_info, b"\x11\x01\x00\x02") 
        self._ble.gatts_write(self._h_map, _HID_MAP)
        self._ble.gatts_write(self._h_rep_ref, bytes([1, 1])) 
        self._ble.gatts_write(self._h_proto, b"\x01") 
        
        # Buffer to prevent keyboard typing crashes
        self._ble.gatts_set_buffer(self._h_rep, 20, True)

        adv = bytearray()
        adv.extend(b"\x02\x01\x06")
        adv.extend(b"\x03\x19\xc1\x03") 
        adv.extend(b"\x05\x03\x12\x18\x0f\x18") 
        adv.extend(bytes([len(name) + 1, 0x09]) + name.encode())
        self._adv_payload = bytes(adv)
        self._advertise()

    def _irq(self, event, data):
        if event == 1: # _IRQ_CENTRAL_CONNECT
            self._conn_handle, _, _ = data
            self._connected = True
            
        elif event == 2: # _IRQ_CENTRAL_DISCONNECT
            self._connected = False
            self._conn_handle = None
            self._advertise()
            
        elif event == 15: # _IRQ_ENCRYPTION_UPDATE
            pass # Windows reconnecting
            
        elif event == 17: # _IRQ_PASSKEY_ACTION
            try: self._ble.gap_passkey(data[0], data[1], 1)
            except: pass
            
        elif event == 29: # _IRQ_GET_SECRET (OS is asking for our saved keys)
            sec_type, index, key = data
            return self._secrets.get(f"{sec_type}_{index}_{key}", None)
            
        elif event == 30: # _IRQ_SET_SECRET (OS is giving us keys to save)
            sec_type, key, value = data
            self._secrets[f"{sec_type}_{0}_{key}"] = value
            # Save dictionary to flash memory so it survives reboots
            try:
                save_dict = {k: list(v) if v else None for k, v in self._secrets.items()}
                with open('ble_secrets.json', 'w') as f:
                    json.dump(save_dict, f)
            except:
                pass
            return True

    def _advertise(self):
        self._ble.gap_advertise(100_000, self._adv_payload)

    def is_connected(self):
        return self._connected

    def _send(self, payload):
        conn = self._conn_handle
        if not self._connected or conn is None: 
            return
            
        for _ in range(10):  
            try:
                self._ble.gatts_notify(conn, self._h_rep, payload)
                return
            except OSError as e:
                if e.args[0] == 12: time.sleep_ms(20) 
                else: return 

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

    def type_text(self, text):
        for c in text:
            if c == '\n':
                self.enter()
            elif c in _K:
                self.send_raw(_K[c][0], modifier=_K[c][1])
            time.sleep_ms(20)

