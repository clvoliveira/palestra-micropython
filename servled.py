import network
import socket 
import machine

html = """<!DOCTYPE html>
<html>
<head><title>ESP8266 LED ON/OFF</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.6/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container">
<form>
<h1>LED:</h1>
<p align="center">
<button name="LED" value="ON" type="submit" class="btn btn-success btn-lg">Ligar</button>&nbsp;&nbsp;
<button name="LED" value="OFF" type="submit" class="btn btn-danger btn-lg">Desligar</button><br />
</p>
</form>
</div>
</body>
</html>
"""

#Configuracao do pino
LED = machine.Pin(5, machine.Pin.OUT) # GPIO5 = D1

#Configuracao do Wi-Fi
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
  print('Conectando...')
  sta_if.active(True)
  sta_if.connect('COLOCAR_AP', 'COLOCAR_SENHA')
  while not sta_if.isconnected():
    pass
print('Configuracao:', sta_if.ifconfig())

#Configuracao do Socket e do Webserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print("Conexao de %s" % str(addr))
  request = conn.recv(1024)
  print("Conteudo = %s" % str(request))
  request = str(request)
  LEDON = request.find('/?LED=ON')
  LEDOFF = request.find('/?LED=OFF')
  print (LEDON, LEDOFF)
  if LEDON == 6:
    LED.value(1)
  if LEDOFF == 6:
    LED.value(0)
  response = html
  conn.send(response)
  conn.close()
  

