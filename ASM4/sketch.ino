#include <DHTesp.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

#define DHT_PIN   15
#define LED_PIN   2
#define PIR_PIN   12

DHTesp dht;
LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long lastDHTRead = 0;
bool lastMotionState = false;

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
    } else {
      Serial.println("[DHT22] ERROR: Failed to read sensor");
    }
  }

  // PIR — only log on state change to avoid Serial spam
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
