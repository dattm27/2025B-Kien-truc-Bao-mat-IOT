# ASM4 — ESP32 IoT Sensor Monitor with HTTP Data Sending

An ESP32-based IoT project that collects temperature and humidity (DHT22), detects motion (PIR), displays data on an LCD, and sends sensor readings to a remote server via three HTTP methods.

---

## Hardware Components

| Component | Description | Pin |
|---|---|---|
| ESP32 DevKit C v4 | Microcontroller | — |
| DHT22 | Temperature & humidity sensor | GPIO 15 |
| PIR Motion Sensor | Motion detection | GPIO 12 |
| LCD 1602 (I2C) | 16x2 character display | SDA: GPIO 21, SCL: GPIO 23 |
| Red LED | Motion indicator | GPIO 2 |
| Resistor 1kΩ | LED current limiter | — |

## Wiring Diagram

```
ESP32               DHT22
3V3  ------------> VCC
GND  ------------> GND
GPIO15 ----------> SDA

ESP32               PIR Sensor
3V3  ------------> VCC
GND  ------------> GND
GPIO12 ----------> OUT

ESP32               LCD 1602 (I2C)
3V3  ------------> VCC
GND  ------------> GND
GPIO21 ----------> SDA
GPIO23 ----------> SCL

ESP32               LED
GPIO2 -----------> Anode (+)
                   Cathode (-) --> 1kΩ --> GND
```

---

## Software Features

### Sensor Reading
- **DHT22** — reads temperature (°C) and humidity (%) every 2 seconds
- **PIR** — continuously monitors motion; toggles LED and logs state changes

### LCD Display
- Row 0: `Temp: XX.X C`
- Row 1: `Humi: XX.X %`

### HTTP Data Transmission

On every successful DHT22 read, the device sends data to the server, cycling through three methods in order:

#### a) HTTP GET — URL-encoded query string
```
GET https://postman-echo.com/get?temp=24.7&humid=65.3
```

#### b) HTTP POST — URL-encoded body
```
POST https://postman-echo.com/post
Content-Type: application/x-www-form-urlencoded

temp=24.7&humid=65.3
```

#### c) HTTP POST — JSON body (via ArduinoJson)
```
POST https://postman-echo.com/post
Content-Type: application/json

{"temp":24.7,"humid":65.3}
```

---

## Libraries Required

| Library | Purpose |
|---|---|
| `DHTesp` | DHT22 sensor driver |
| `LiquidCrystal_I2C` | LCD I2C driver |
| `Wire` | I2C communication |
| `WiFi` | ESP32 WiFi (built-in) |
| `HTTPClient` | HTTP requests (built-in) |
| `ArduinoJson` | JSON serialization |

---

## Configuration

Edit the following defines at the top of `sketch.ino`:

```cpp
#define WIFI_SSID "Wokwi-GUEST"   // your WiFi SSID
#define WIFI_PASS ""               // your WiFi password
```

For Wokwi simulation use `"Wokwi-GUEST"` with an empty password.

---

## Simulation

This project is designed to run on [Wokwi](https://wokwi.com). The `diagram.json` file contains the full circuit layout and can be loaded directly in the Wokwi editor.

**Serial Monitor output example:**
```
[WiFi] Connecting......
[WiFi] Connected! IP: 10.0.0.2
[SYS] System initialized
[DHT22] Temp: 24.7 C | Humi: 65.3 %
[HTTP-GET] Response: 200
{ "args": { "temp": "24.7", "humid": "65.3" }, ... }
[DHT22] Temp: 24.8 C | Humi: 65.1 %
[HTTP-POST-URL] Response: 200
{ "form": { "temp": "24.8", "humid": "65.1" }, ... }
[DHT22] Temp: 24.7 C | Humi: 65.2 %
[HTTP-POST-JSON] Response: 200
{ "data": { "temp": 24.7, "humid": 65.2 }, ... }
[PIR] Motion detected! LED ON
[PIR] No motion. LED OFF
```

---

## Project Structure

```
ASM4/
├── sketch.ino       # Main Arduino sketch
├── diagram.json     # Wokwi circuit diagram
└── README.md        # This file
```
