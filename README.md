# Codebase Index

This repository is a collection of MicroPython examples for the ESP32, organized as a practical teaching and prototyping resource. It begins with foundational scripts that introduce digital output, digital input, analog sensing, capacitive touch, and motor control. These files help learners understand how the ESP32 interacts with physical components such as LEDs, switches, flex sensors, servo motors, stepper motors, and NeoPixels. The code is written as small, focused examples, so each file demonstrates one clear hardware concept at a time.

A second major part of the repository focuses on wireless interaction through Bluetooth Low Energy. These files show how the ESP32 can send and receive data, act as a custom controller, and even behave like a Bluetooth keyboard. This makes the repository useful not only for electronics basics, but also for interactive installations, game inputs, and physical computing projects that communicate with phones or computers.

The WiFi section extends this idea further by linking the ESP32 to MIT App Inventor style apps over a local network. Together, the repository functions as a compact toolkit for learning embedded programming, building classroom demos, and developing interactive hardware projects.

---

## Basic Hardware and Sensor Control

These files cover the fundamentals of physical computing with MicroPython.

- `blink.py` – Basic LED blinking with timing delays.
- `TwoLEDS.py` – Controls two LEDs to demonstrate multiple digital outputs.
- `CycleNeopixel.py` – Cycles colors on a NeoPixel LED.
- `SwitchBasic.py` – Reads a switch input and uses internal pull-up logic.
- `readswitch.py` – Another switch-reading example for button interaction.
- `FlexSensor.py` – Reads analog values from a flex sensor using ADC.
- `touchInputBasics.py` – Demonstrates capacitive touch input on ESP32.
- `reactionTime.py` – A simple reaction game using timing, random delay, and input detection.
- `Servo.py` – A servo control library using PWM.
- `servotest.py` – Test script for moving a servo to different angles.
- `stepperBasic.py` – Basic stepper motor phase control.
- `StepperWithForLoop.py` – Stepper motor control using a loop-based structure.

---

## Bluetooth and BLE Features

These files focus on wireless communication and HID-style interaction.

- `simple_ble.py` – A lightweight BLE helper library for ESP32 communication.
- `BasicBLECode.py` – Starter BLE example for sending sensor-style data.
- `BLEReadWrite.py` – Demonstrates two-way BLE communication.
- `ble_keyboard.py` – Lets the ESP32 behave like a Bluetooth keyboard.
- `ExampleKB.py` – Example of keyboard-style BLE interaction.
- `KeyboardWithSwitch.py` – Triggers keyboard input from physical switches.
- `BluetoothEtchASketch.py` – Sends live control data over BLE for an Etch-a-Sketch style project.

---

## WiFi and App Connectivity

These files show how the ESP32 can connect to apps over WiFi.

- `applink.py` – A helper class for network communication and JSON handling.
- `basicWifi.py` – Basic WiFi communication example using the app link helper.
- `WifiDemo.py` – Demonstrates ESP32 communication over WiFi with app integration.
- `colorLamp.py` – Receives color values and applies them to a connected lighting-style project.

---

## Supporting Materials

The repository also includes supporting project resources beyond code.

- MIT App Inventor project files are included in the Bluetooth folder for companion app workflows.
- The `documentation` folder contains reference notes and library information for setup and teaching support.

---

## Feature Summary

This codebase can be understood through four main feature groups:

1. **Digital and analog I/O** – Reading switches, touch sensors, and analog sensors while controlling LEDs.
2. **Motion control** – Driving servo and stepper motors for mechanical interaction.
3. **Bluetooth interactivity** – Creating BLE-based data links and keyboard-style devices.
4. **WiFi app integration** – Connecting the ESP32 to mobile apps and passing structured data.

Because the examples are modular and short, the repository is especially useful for classrooms, workshops, and rapid prototyping.
