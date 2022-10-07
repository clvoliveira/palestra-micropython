import time
from machine import Pin
led=Pin(2, Pin.OUT)       # GPIO5 - D1 (ESP8266)
                          # GPIO2 - D2 (ESP32)
while True:
  led.value(1)            # Ligar
  time.sleep(0.5)
  led.value(0)            # Desligar
  time.sleep(0.5)

