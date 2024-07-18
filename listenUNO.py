import serial
from time import sleep
from subprocess import call
WLAN_DOWN = b'\x51'
WLAN_UP = b'\x52'
END_COM = b'\xc3'
suc = b'\x00'
unsuc = b'\xff'

arduino = serial.Serial(port = '/dev/ttyS0', baudrate=115200, timeout = 2)

if __name__ == '__main__':
    while(arduino.is_open):
        if(arduino.in_waiting):
            sleep(0.05)
            cmd = arduino.read()
            if cmd == WLAN_DOWN:
                call(['sh', 'killWLAN.sh'])
                arduino.write(suc)
            elif cmd == WLAN_UP:
                call(['sh', 'launchWLAN.sh'])
                arduino.write(suc)
            elif cmd == END_COM:
                arduino.write(END_COM)
                arduino.close()
            else:
                arduino.write(unsuc)
            
