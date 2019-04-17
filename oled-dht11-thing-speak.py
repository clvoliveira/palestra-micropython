# OLED -> ESP32
# CS   -> D5
# DC   -> D4
# RES  -> D15
# SDA  -> D23 (MOSI)
# SCK  -> D18 (SCK)
# Vdd  -> Vcc
# GND  -> GND

#DHT11 -> ESP32
# 2    -> D13

import ssd1306, time, dht, network, machine
from machine import Pin, SPI
from umqtt.simple import MQTTClient

print("Iniciando...")
sensor = dht.DHT11(Pin(13, Pin.IN, Pin.PULL_UP))
time.sleep(5.0)

spi = SPI(1, baudrate=8000000, sck=Pin(18), mosi=Pin(23), polarity=0, phase=0)
# dc, res, cs
oled = ssd1306.SSD1306_SPI(128, 64, spi, Pin(4), Pin(15), Pin(5))

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('COLOCAR_AP', 'COLOCAR_SENHA')
while wifi.isconnected() == False:
  machine.idle()
print('Conexao realizada.')
print(wifi.ifconfig())

SERVIDOR = "mqtt.thingspeak.com"
CHANNEL_ID = "34342"
WRITE_API_KEY = "RPVYR5VW7A0U6X9T"
cliente = MQTTClient("umqtt_client", SERVIDOR)
topico = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

try:
  while True:
    sensor.measure()
    temp = str(sensor.temperature())
    umid = str(sensor.humidity())
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)
    oled.text("Temperatura:", 5, 5)
    oled.text(temp + "'C", 5, 15)
    oled.text("Umidade:", 5, 35)
    oled.text(umid + "%", 5, 45)
    oled.show()
    conteudo = "field1=" + temp + "&field2=" + umid
    print ('Conectando a ThingSpeak...')
    cliente.connect()
    cliente.publish(topico, conteudo)
    cliente.disconnect()
    print ('Envio realizado.')
    time.sleep(600.0)
except KeyboardInterrupt:
  oled.fill(0)
  oled.show()
  spi.deinit()
  wifi.disconnect()
  print("Fim.")

