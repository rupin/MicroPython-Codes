📚 Codebase Feature Index
This repository contains a structured collection of MicroPython scripts designed for hardware education, prototyping, and experiential learning. The codebase is broken down into three main categories: Basic Electronics and Actuators, Bluetooth (BLE) Integration, and WiFi/App Connectivity.

In the basic hardware section, the code demonstrates core microcontroller concepts such as digital logic, analog readings, and motor control, making it easy for students to interface with LEDs, switches, capacitive touch sensors, servos, and stepper motors . The Bluetooth section abstracts complex BLE protocols into easy-to-use libraries, allowing the ESP32 to function as a wireless HID device (like a keyboard) or send/receive sensor streams to custom applications, such as an Etch-a-Sketch controller . Finally, the WiFi modules provide simplified local network classes that allow the ESP32 to host lightweight socket servers, specifically tailored to parse JSON data and link seamlessly with MIT App Inventor projects . Together, these scripts serve as a robust toolkit for building interactive, physical computing projects.

🔌 Basic Hardware & Sensors
Core microcontroller operations, sensor reading, and motor control.

blink.py / TwoLEDS.py: Introductory digital output scripts for toggling LEDs with adjustable time delays .

CycleNeopixel.py: Interfacing with WS2812B addressable RGB LEDs to cycle through colors .

SwitchBasic.py / readswitch.py: Digital input examples demonstrating how to read push buttons using internal pull-up resistors .

FlexSensor.py: Demonstrates reading analog voltages (ADC) from a flex sensor or variable resistor .

touchInputBasics.py: Implements capacitive touch sensing using the ESP32's built-in touch pads and thresholds .

reactionTime.py: A simple logic game utilizing the random library to measure human reaction time using LEDs and switches .

servotest.py / Servo.py: Implements Pulse Width Modulation (PWM) for precise angle control of hobby servo motors .

stepperBasic.py / StepperWithForLoop.py: Controls stepper motors by sequentially firing output pins, demonstrating basic and loop-based phase control .

📡 Bluetooth Low Energy (BLE) & HID
Wireless communication and Human Interface Device emulation.

simple_ble.py / BasicBLECode.py: A foundational BLE wrapper library and example code to easily broadcast and connect ESP32 devices to central devices without deep knowledge of the Bluetooth stack .

BLEReadWrite.py: Demonstrates two-way Bluetooth communication, allowing the microcontroller to both send sensor data and receive incoming commands .

ble_keyboard.py: A robust HID library that allows the ESP32 to emulate a standard Bluetooth keyboard and send keystrokes to a connected PC or mobile device .

ExampleKB.py / KeyboardWithSwitch.py: Implementation scripts using the ble_keyboard library to map physical buttons and capacitive touch inputs to specific computer keystrokes .

BluetoothEtchASketch.py: A practical project script that reads dual analog inputs (like potentiometers) and transmits the data over BLE, designed to pair with the included MIT App Inventor .aia file .

🌐 WiFi & MIT App Inventor Integration
Local networking, HTTP servers, and mobile app connectivity.

applink.py: A custom wrapper library that abstracts Python socket networking, making it trivial to host a local server and parse incoming JSON data from a mobile app .

basicWifi.py / WifiDemo.py: Boilerplate implementation codes showing how to instantiate the AppInventorLink, connect to a local WiFi network, and handle incoming requests .

colorLamp.py: A practical endpoint script designed to receive RGB color parameters sent from a mobile app over WiFi to control an LED lamp .
