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
WAIT = b'\x0f'
STOP_client = b'\xff'
global arduino
arduino = serial.Serial(port='COM5', baudrate=9600, timeout = 5)
##########

def send_byte(byt):
    arduino.write(byt)
    wait_ACK(byt)
def wait(sec):
    send_byte(WAIT)
    arduino.write(bytes(sec, 'utf-8'))
    while(arduino.in_waiting):
        msec = arduino.readline();
        print(msec)
    time.sleep(int(sec))
def wait_ACK(cmd):
    global arduino
    if(not arduino.is_open):
        arduino.close()
        time.sleep(0.5)
        arduino = serial.Serial(port='COM5', baudrate=9600, timeout = 5)

    time.sleep(0.5)
    
    if(arduino.in_waiting):
        ack = arduino.read()
        print("ACK: ", ack)
    else:
        print("resending")
        send_byte(cmd)
        

time.sleep(1)

cmdFile = open('testCMD.txt','r')

cmds = cmdFile.readlines()
for cmd in cmds:
    print(cmd)
    cmd = cmd.strip()
    cmd = cmd.split()
    match cmd[0]:
        case 'START_CHARGING':
            send_byte(START_CHARGING)
        case 'PE_ON':
            send_byte(PE_ON)
        case 'PE_OFF':
            send_byte(PE_OFF)
        case 'B_ON':
            send_byte(B_ON)
        case 'B_OFF':
            send_byte(B_OFF)
        case 'C_ON':
            send_byte(C_ON)
        case 'C_OFF':
            send_byte(C_OFF)
        case 'WAIT':
            wait(cmd[1])
        case default:
            print("Command not found")
    
            
            



