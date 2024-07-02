import serial
import time

    
#COMMANDS:
START_CHARGING = b'\x20'
PE_ON = b'\x01'
PE_OFF = b'\x11'
B_ON = b'\x02'
B_OFF = b'\x12'
C_ON = b'\x03'
C_OFF = b'\x13'
WAIT = b'\x0F'

def open_com_port():
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout = 5)
    return arduino
    
##########

def send_byte(byt,seriPort):
    seriPort.write(byt)
    wait_ACK(byt, seriPort)
    if(not seriPort.is_open):
        seriPort.close()
        time.sleep(0.5)
        seriPort = open_com_port()
    return seriPort
def wait(sec,seriPort):
    seriPort = send_byte(WAIT, seriPort)
    seriPort.write(bytes(sec, 'utf-8'))
    while(seriPort.in_waiting):
        msec = seriPort.readline();
        print(msec)
    time.sleep(int(sec))
    return seriPort
def wait_ACK(cmd,seriPort):
    time.sleep(0.5)
    if(not seriPort.in_waiting):
        send_byte(cmd, seriPort)
        print("resending")

arduino = open_com_port() 

time.sleep(1)

cmdFile = open('testCMD.txt','r')

cmds = cmdFile.readlines()
for cmd in cmds:
    print(cmd)
    cmd = cmd.strip()
    cmd = cmd.split()
    match cmd[0]:
        case 'START_CHARGING':
            arduino = send_byte(START_CHARGING, arduino)
        case 'PE_ON':
            arduino = send_byte(PE_ON, arduino)
        case 'PE_OFF':
            arduino = send_byte(PE_OFF, arduino)
        case 'B_ON':
            arduino = send_byte(B_ON,arduino)
        case 'B_OFF':
            arduino = send_byte(B_OFF, arduino)
        case 'C_ON':
            arduino = send_byte(C_ON, arduino)
        case 'C_OFF':
            arduino = send_byte(C_OFF, arduino)
        case 'WAIT':
            arduino = wait(cmd[1], arduino)
        case default:
            print("Command not found")
    
            
            



