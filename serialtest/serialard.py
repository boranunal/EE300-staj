import serial
import time

arduino = serial.Serial(port='COM5', baudrate = 9600, timeout = 5)

while True:
    while(arduino.in_waiting):
        data = arduino.read()
        print()
    
    arduino.write(b'\x66')
    time.sleep(0.1)



