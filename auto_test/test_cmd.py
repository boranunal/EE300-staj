import serial
from time import sleep
from sys import exit
from glob import glob
import serial.tools.list_ports
    
#COMMANDS:
POWER_OFF = b'\x20'
POWER_ON = b'\x21'
START_CHARGING = b'\x22'
PE_ON = b'\x01'
PE_OFF = b'\x11'
B_ON = b'\x02'
B_OFF = b'\x12'
C_ON = b'\x03'
C_OFF = b'\x13'
RFID = b'\x33'
WLAN_DOWN = b'\x51'
WLAN_UP = b'\x52'
WAIT = b'\x0f'
WAIT_MS = b'\x1f'
END = b'\xff'


##########

def send_byte(byt):
    arduino.write(byt)
    sleep(0.5)
    print(byt)

def byte_count(cmds):
    count = 0
    for cmd in cmds:
        cmd = cmd.strip()
        cmd = cmd.split()
        cmd[0] = cmd[0].upper()
        if (cmd[0] == "WAIT" or cmd[0] == "WAIT_MS"):
            count = count + 5
        else:
            count = count + 1
    return count
def makeByteArr(cmds):
    ret = bytes(0)
    for cmd in cmds:
        print(cmd)
        cmd = cmd.strip()
        cmd = cmd.split()
        cmd[0] = cmd[0].upper()
        match cmd[0]:
            case 'POWER_OFF':
                ret += POWER_OFF
            case 'POWER_ON':
                ret += POWER_ON
            case 'START_CHARGING':
                ret += START_CHARGING
            case 'PE_ON':
                ret += PE_ON
            case 'PE_OFF':
                ret += PE_OFF
            case 'B_ON':
                ret += B_ON
            case 'B_OFF':
                ret += B_OFF
            case 'C_ON':
                ret += C_ON
            case 'C_OFF':
                ret += C_OFF
            case 'WAIT':
                ret += WAIT
                ret += int(cmd[1]).to_bytes(4,byteorder='little')
            case 'WAIT_MS':
                ret += WAIT_MS
                ret += int(cmd[1]).to_bytes(4,byteorder='little')
            case 'RFID':
                ret += RFID
            case 'WLAN_UP':
                ret += WLAN_UP
            case 'WLAN_DOWN':
                ret += WLAN_DOWN
            case default:
                print("Command not found: "+ cmd[0])
                input("Transmission aborted! Press enter to quit")
                exit()
                
    return ret
        
if __name__ == "__main__":
    global arduino
    print("Available ports: ")
    comPorts = serial.tools.list_ports.comports()
    for com in comPorts:
        print(com)
    invPort = True
    while(invPort):
        comPort = input("Select port (write the name of the port): ")
        try:
            arduino = serial.Serial(port=str(comPort), baudrate=115200, timeout = 5)
            invPort = False
        except:
            print("Invalid port name\nEnter something like 'COM5'")
            invPort = True
    ready = 0
    while (not ready):
        while(not arduino.in_waiting):
            print(".",end="")
            sleep(0.05)
        ready = arduino.readline()
    print("Arduino is ready")
    filesInDir = glob("*.txt")
    print("Select one of the following files:")
    for f in filesInDir:
        print(f)

    invFile = True
    while(invFile):
        fileName = input("Enter the name of the command file:")
        fileName = fileName.strip()
        try:
            cmdFile = open(fileName+".txt","r")
            invFile = False
        except:
            try:
                cmdFile = open(fileName,"r")
                invFile = False
            except:
                print("Invalid file name!")
                invFile = True
        
    cmds = cmdFile.readlines()
    numOfBytes = byte_count(cmds)
    arduino.write(bytes(str(numOfBytes),'utf-8'))
    print(numOfBytes)
    while(not arduino.in_waiting):
        print(".",end="")
        sleep(0.05)
    cmdToSend = makeByteArr(cmds)
    print(cmdToSend)
    arduino.write(cmdToSend)
    sleep(0.1)
    while(not arduino.in_waiting):
        print(".",end="")
        sleep(0.05)
    read=arduino.read_until('?',numOfBytes)
    print(read)
    sleep(5)
    print(arduino.readline())
    sleep(5)
    print(arduino.readline())
    sleep(5)
    print(arduino.readline())
    sleep(5)
    print(arduino.readline())
    arduino.close()
    input("End of transmission. You may close the program.")
#### end of main ####          



