#include <DHTesp.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define DHT_PIN  15
#define LED_PIN  2
#define PIR_PIN  12

#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASS ""

#define SERVER_GET  "https://postman-echo.com/get"
#define SERVER_POST "https://postman-echo.com/post"

DHTesp dht;
LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long lastDHTRead = 0;
bool lastMotionState = false;
int sendMethod = 0;  // cycles: 0=GET, 1=POST url-encoded, 2=POST JSON

// a) HTTP GET — data url-encoded in query string
void sendHTTPGet(float temp, float hum) {
  HTTPClient http;
  String url = String(SERVER_GET) + "?temp=" + String(temp, 1) + "&humid=" + String(hum, 1);
  http.begin(url.c_str());
  int code = http.GET();
  if (code > 0) {
    Serial.print("[HTTP-GET] Response: ");
    Serial.println(code);
    Serial.println(http.getString());
  } else {
    Serial.print("[HTTP-GET] Error: ");
    Serial.println(code);
  }
  http.end();
}

// b) HTTP POST — data url-encoded in body
void sendHTTPPostUrlEncoded(float temp, float hum) {
  HTTPClient http;
  http.begin(SERVER_POST);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  String body = "temp=" + String(temp, 1) + "&humid=" + String(hum, 1);
  int code = http.POST(body);
  if (code > 0) {
    Serial.print("[HTTP-POST-URL] Response: ");
    Serial.println(code);
    Serial.println(http.getString());
  } else {
    Serial.print("[HTTP-POST-URL] Error: ");
    Serial.println(code);
  }
  http.end();
}

// c) HTTP POST — data as JSON in body (using ArduinoJson)
void sendHTTPPostJSON(float temp, float hum) {
  HTTPClient http;
  http.begin(SERVER_POST);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<128> doc;
  doc["temp"] = temp;
  doc["humid"] = hum;
  String body;
  serializeJson(doc, body);

  int code = http.POST(body);
  if (code > 0) {
    Serial.print("[HTTP-POST-JSON] Response: ");
    Serial.println(code);
    Serial.println(http.getString());
  } else {
    Serial.print("[HTTP-POST-JSON] Error: ");
    Serial.println(code);
  }
  http.end();
}

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);

  dht.setup(DHT_PIN, DHTesp::DHT22);

  Wire.begin(21, 23);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("  IoT Monitor   ");
  lcd.setCursor(0, 1);
  lcd.print(" Connecting WiFi");

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("[WiFi] Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("\n[WiFi] Connected! IP: " + WiFi.localIP().toString());

  lcd.setCursor(0, 1);
  lcd.print(" Initializing.. ");

  Serial.println("[SYS] System initialized");
  delay(2000);
  lcd.clear();
}

void loop() {
  unsigned long now = millis();

  // Read DHT22 every 2 seconds
  if (now - lastDHTRead >= 2000) {
    lastDHTRead = now;

    TempAndHumidity data = dht.getTempAndHumidity();

    if (dht.getStatus() == 0) {
      lcd.setCursor(0, 0);
      lcd.print("Temp: ");
      lcd.print(data.temperature, 1);
      lcd.print(" C    ");

      lcd.setCursor(0, 1);
      lcd.print("Humi: ");
      lcd.print(data.humidity, 1);
      lcd.print(" %    ");

      Serial.printf("[DHT22] Temp: %.1f C | Humi: %.1f %%\n",
                    data.temperature, data.humidity);

      if (WiFi.status() == WL_CONNECTED) {
        switch (sendMethod) {
          case 0: sendHTTPGet(data.temperature, data.humidity);             break;
          case 1: sendHTTPPostUrlEncoded(data.temperature, data.humidity);  break;
          case 2: sendHTTPPostJSON(data.temperature, data.humidity);        break;
        }
        sendMethod = (sendMethod + 1) % 3;
      } else {
        Serial.println("[WiFi] Disconnected");
      }
    } else {
      Serial.println("[DHT22] ERROR: Failed to read sensor");
    }
  }

  // PIR — only log on state change
  bool motionDetected = digitalRead(PIR_PIN) == HIGH;

  if (motionDetected != lastMotionState) {
    lastMotionState = motionDetected;
    if (motionDetected) {
      Serial.println("[PIR] Motion detected! LED ON");
    } else {
      Serial.println("[PIR] No motion. LED OFF");
    }
  }

  digitalWrite(LED_PIN, motionDetected ? HIGH : LOW);

  delay(50);
}
