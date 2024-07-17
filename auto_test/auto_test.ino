#include <Servo.h>
#include <cppQueue.h>
union arrToInt {
  byte arr[4];
  uint32_t integer;
};
arrToInt convert;
const int PE=2;
const int B=3;
const int C=4;
const int WLAN_SW=7;
const int POWER=8;
const int SERVO=10;

//variables:
unsigned long msec;
unsigned long sec;
byte cmd;
byte data;
byte recvd;
//byte byteArr[700];
int i;
int temp;
char reed;
uint16_t qsize;
bool runTest = true;

//COMMANDS:
const byte POWER_OFF = 0x20;
const byte POWER_ON = 0x21;
const byte START_CHARGING = 0x22;
const byte PE_ON = 0x01;
const byte PE_OFF = 0x11;
const byte B_ON = 0x02;
const byte B_OFF = 0x12;
const byte C_ON = 0x03;
const byte C_OFF = 0x13;
const byte RFID = 0x33;
const byte WLAN_DOWN = 0x51;
const byte WLAN_UP = 0x52;
const byte WAIT = 0x0F;
const byte WAIT_MS = 0x1F;

Servo myservo;
cppQueue q(1,700,FIFO,true);

void setup() {
  Serial.begin(115200);
  myservo.attach(SERVO);
  servoSetup();
  //servoSetup();
  pinMode(POWER,OUTPUT);
  digitalWrite(POWER,LOW);
  pinMode(WLAN_SW,OUTPUT);
  digitalWrite(WLAN_SW,HIGH);
  pinMode(PE, OUTPUT);
  digitalWrite(PE,HIGH);
  pinMode(B, OUTPUT);
  digitalWrite(B,HIGH);
  pinMode(C, OUTPUT);
  digitalWrite(C, HIGH);
  Serial.println(1);
  while(!Serial.available());
  qsize = Serial.readString().toInt();
  Serial.println(qsize);
  recCmds();
}

void loop() {

  while(!q.isEmpty()){
    q.pop(&cmd);
    switch(cmd){
      case POWER_OFF:
        digitalWrite(POWER,HIGH);
        break;
      case POWER_ON:
        digitalWrite(POWER,LOW);
        break;
      case START_CHARGING:
        startCharging();
        break;
      case PE_ON:
        digitalWrite(PE,LOW);
        break;
      case PE_OFF:
        digitalWrite(PE,HIGH);
        break;
      case B_ON:
        digitalWrite(B,LOW);
        break;
      case B_OFF:
        digitalWrite(B,HIGH);
        break;
      case C_ON:
        digitalWrite(C,LOW);
        break;
      case C_OFF:
        digitalWrite(C,HIGH);
        break;
      case WAIT:
        i = 0;
        while(i<4){
          q.pop(&convert.arr[i++]);
        }
        Serial.println(convert.integer);
        msec = convert.integer;
        delay(1000*msec);
        break;
      case WAIT_MS:
        i = 0;
        while(i<4){
          q.pop(&convert.arr[i++]);
        }
        msec = convert.integer;
        Serial.println(msec);
        delay(msec);
        break;
      case RFID:
        rfidScan();
        break;
      case WLAN_DOWN:
        digitalWrite(WLAN_SW,LOW);
        break;
      case WLAN_UP:
        digitalWrite(WLAN_SW,HIGH);
        break;
      default:
        break;
    }
  }
}

void recCmds(void){
  int count = 0;
  while(count<qsize){
    if(Serial.available()>0){
      if(Serial.readBytes(&data,1)){
        q.push(&data);
        Serial.print(recvd);
        count++;
      }
    }
  }
}

void startCharging(void){
  digitalWrite(PE,LOW);
  delay(1000);
  digitalWrite(B,LOW);
  delay(1000);
  digitalWrite(C,LOW);
}
void rfidScan(void){
  myservo.write(180);
  delay(1500);
  myservo.write(90);
  delay(500);
}
void servoSetup(void){
  myservo.write(0);
  delay(500);
  myservo.write(90);
  delay(500);
}

void hi(void){
  myservo.write(0);
  delay(1000);
  myservo.write(90);
  delay(1000);
}
