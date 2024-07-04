import serial
import time

    
#COMMANDS:
START_CHARGING = b'\x22'
PE_ON = b'\x01'
PE_OFF = b'\x11'
B_ON = b'\x02'
B_OFF = b'\x12'
C_ON = b'\x03'
C_OFF = b'\x13'
RFID = b'\x33'
WAIT = b'\x0f'
WAIT_MS = b'\x1f'
END = b'\xff'

arduino = serial.Serial(port='COM5', baudrate=115200, timeout = 5)
##########

def send_byte(byt):
    arduino.write(byt)
    time.sleep(0.5)
    print(byt)

def byte_count(cmds):
    count = 0
    for cmd in cmds:
        cmd = cmd.strip()
        cmd = cmd.split()
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
        match cmd[0]:
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
                ret += int(cmd[1]).to_bytes(4,byteorder='big')
            case 'WAIT_MS':
                ret += WAIT_MS
                ret += int(cmd[1]).to_bytes(4,byteorder='big')
            case 'RFID':
                ret += RFID
            case default:
                print("Command not found")
    return ret
        
if __name__ == "__main__":
    ready = 0
    while (not ready):
        while(not arduino.in_waiting):
            print(".",end="")
            time.sleep(0.05)
        ready = arduino.readline()
    cmdFile = open('testCMD.txt','r')
    cmds = cmdFile.readlines()
    numOfBytes = byte_count(cmds)
    arduino.write(bytes(str(numOfBytes),'utf-8'))
    print(numOfBytes)
    while(not arduino.in_waiting):
        print(".",end="")
        time.sleep(0.05)
    nOBret = arduino.readline()
    print(nOBret)
    cmdToSend = makeByteArr(cmds)
    print(cmdToSend)
    print("dingdong\n")
    arduino.write(cmdToSend)
    time.sleep(0.1)
    bytsRead = arduino.read_until(expected = '?', size = 200)
    print(bytsRead)
    arduino.close()
#### end of main ####          



