import network
import socket
import json

class AppInventorLink:
    def __init__(self):
        self.server = None
        self.callback = None

    def start_ap(self, ssid, password=""):
        # Set up the ESP32 as an Access Point (Hotspot)
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        
        # Configure Wi-Fi security
        if password:
            ap.config(essid=ssid, password=password, authmode=3) # WPA2
        else:
            ap.config(essid=ssid, authmode=0) # Open network
            
        ip = ap.ifconfig()[0]
        print("Access Point Created!")
        print("SSID:", ssid)
        print("Gateway IP Address:", ip) # Usually 192.168.4.1
        
        # Setup a non-blocking web server on port 80
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', 80))
        self.server.listen(5)
        self.server.setblocking(False)

    def on_request(self, func):
        # Attach the student's logic function
        self.callback = func

    def _parse_query_string(self, qs):
        # Helper function to turn "action=on&pin=2" into {"action": "on", "pin": "2"}
        params = {}
        if not qs: return params
        for pair in qs.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
        return params

    def process(self):
        try:
            # Check for incoming app requests
            conn, addr = self.server.accept()
            conn.settimeout(1.0)
            request = conn.recv(1024).decode('utf-8')
            
            if not request:
                conn.close()
                return
                
            # Parse the HTTP request line (e.g., "GET /?action=led_on HTTP/1.1")
            first_line = request.split('\r\n')[0].split(' ')
            if len(first_line) > 1:
                path = first_line[1]
                
                # Extract query string if it exists
                qs = ""
                if '?' in path:
                    path, qs = path.split('?', 1)
                
                # Convert query string to a dictionary
                params = self._parse_query_string(qs)
                
                response_data = "{}"
                if self.callback:
                    # Pass parameters to student's code and get their response
                    result = self.callback(params)
                    
                    # Convert student's dictionary response to JSON text
                    if isinstance(result, dict):
                        response_data = json.dumps(result)
                    else:
                        response_data = str(result)
                
                # Send HTTP response back to the app
                http_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + response_data
                conn.send(http_response.encode())
                
            conn.close()
        except OSError:
            # No incoming connection, continue loop seamlessly
            pass

