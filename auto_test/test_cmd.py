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
REP = b'\xc0'
END = b'\xff'


##########

#return the number of bytes to send.
#arduino waits for the number of bytes to read.
#all commands are 1 byte
#commands with arguments (WAIT, WAIT_MS, REPEAT) consist of
#5 bytes, 1 for the command 4 for the uint32_t number
def byte_count(cmds):
    count = 0
    for cmd in cmds:
        if cmd.strip():
            cmd = cmd.strip()
            cmd = cmd.split()
            cmd[0] = cmd[0].upper()
            
            if (cmd[0] == "WAIT" or cmd[0] == "WAIT_MS" or cmd[0]=="REPEAT"):
                count = count + 5
            else:
                count = count + 1
    return count
#returns a bytearray consisting of commands
#commands with arguments have the 4 byte argument following
#the command, argument is a uint32_t number stored in little_endian format
def makeByteArr(cmds):
    ret = bytes(0)
    for cmd in cmds:
        if cmd.strip():
            cmd = cmd.strip()
            cmd = cmd.split()
            cmd[0] = cmd[0].upper()
            print(cmd[0],end=' ')
            if cmd[0]=='WAIT' or cmd[0]=='WAIT_MS' or cmd[0]=='REPEAT':
                print(cmd[1])
            else:
                print()
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
                case 'REPEAT':
                    ret += REP
                    ret += int(cmd[1]).to_bytes(4,byteorder='little')
                case default:
                    print("Command not found: "+ cmd[0])
                    input("Transmission aborted! Press enter to quit")
                    exit()
                
    return ret
        
if __name__ == "__main__":
    global arduino
    #this part is for selecting com port#
    print("Available ports: ")
    comPorts = serial.tools.list_ports.comports()
    for com in comPorts:
        print(com)
    #input the port name until it is a valid port name
    invPort = True
    while(invPort):
        comPort = input("Select port (write the name of the port): ")
        try:
            arduino = serial.Serial(port=str(comPort), baudrate=115200, timeout = 5)
            invPort = False
        except:
            print("Invalid port name\nEnter something like 'COM5'")
            invPort = True
    #######################################

    #wait until arduino sends a byte indicating
    #it is ready for communication
    ready = 0
    while (not ready):
        while(not arduino.in_waiting):
            print(".",end="")
            sleep(0.05)
        ready = arduino.readline().strip()
    print("Arduino is ready")
    #######################################

    #this is for selecting the command file
    #which should be a .txt file
    #the command file should be in the same directory
    #as this .py file
    filesInDir = glob("*.txt")
    print("Select one of the following files:")
    for f in filesInDir:
        print(f)
    #input the file name until it is a valid file name#
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
    #######################################   
    cmds = cmdFile.readlines()
    numOfBytes = byte_count(cmds)
    #send the number of bytes to be send
    arduino.write(bytes(str(numOfBytes),'utf-8')) 
    print(numOfBytes)
    #this loop is for waiting acknowledgement
    while(not arduino.in_waiting):
        print(".",end="")
        sleep(0.05)
    cmdToSend = makeByteArr(cmds)
    print(cmdToSend)
    #send the commands
    arduino.write(cmdToSend)
    sleep(0.1)
    #wait for acknowledge from arduino
    while(not arduino.in_waiting):
        print(".",end="")
        sleep(0.05)
    ack = arduino.readline()
    print(ack)
    arduino.close()
    input("End of transmission. You may close the program.")
#### end of main ####          



