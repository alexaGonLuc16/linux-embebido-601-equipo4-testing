#primero van las librerías estandar
import time

#segundo van librerías de terceros
import serial

#módulos o librerías locales


PORT = '/dev/ttyACM1'
BAUDRATE = 115200

arduino = serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=2.)

time.sleep(2)
arduino.write(b'hola')
time.sleep(.5)
received = arduino.readline()
print(received)
time.sleep(.5)
received = arduino.readline()
print(received)

for i in range(1, 4):
    to_send = f"Prueba {i}"
    arduino.write(to_send.encode(encoding="utf-8"))
    print(f"Enviado: {to_send}")
    time.sleep(.5)
    received = arduino.readline()
    print(f"Recibido: {received}")