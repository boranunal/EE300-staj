#include <Servo.h>
#include <cppQueue.h>

//union struct is used to convert incoming bytes to integer
union arrToInt {
  byte arr[4];
  uint32_t integer;
};
arrToInt convert;
//pin numbers
const int PE=2;
const int B=3;
const int C=4;
//WLAN switch unoperational
const int WLAN_SW=7;
const int POWER=8;
//LED indicates the test is finished
const int LED=9;
const int SERVO=10;

//variables:
unsigned long msec;
byte cmd;
byte data;
byte recvd;
unsigned long repCount = 0;
int i;
uint16_t qsize;

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
const byte REP = 0xC0;
const byte WLAN_DOWN = 0x51;
const byte WLAN_UP = 0x52;
const byte WAIT = 0x0F;
const byte WAIT_MS = 0x1F;

Servo myservo;
//command queue
cppQueue q(1,700,FIFO,true);
//queue for repeating the test
cppQueue repQ(1,700,FIFO,true);
void setup() {
  Serial.begin(115200);
  myservo.attach(SERVO);
  servoSetup();
  pinMode(LED,OUTPUT);
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
  if(q.isEmpty())
    digitalWrite(LED,HIGH);
  else
    digitalWrite(LED,LOW);
  
  while(!q.isEmpty()){
    
    q.pop(&cmd);
    repQ.push(&cmd);//copy the commands into repeat buffer
    
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
      //convert incoming little endian bytes to integer
      //while copying the bytes into repeat buffer
      //if you want to change to big endian, uncomment 
      //below lines and comment out the current lines
      //note that I did not check if these work use with attention
      /*
        i = 3;
        while(i>=0){
          q.pop(&convert.arr[i]);
          repQ.push(&convert.arr[i--]);
        }
       */
        i = 0;
        while(i<4){
          q.pop(&convert.arr[i]);
          repQ.push(&convert.arr[i++]);
        }
        msec = convert.integer;
        delay(1000*msec);
        break;
      case WAIT_MS:
      //convert incoming little endian bytes to integer
      //while copying the bytes into repeat buffer
      //if you want to change to big endian, uncomment 
      //below lines and comment out the current lines
      //note that I did not check if these work use with attention
      /*
        i = 3;
        while(i>=0){
          q.pop(&convert.arr[i]);
          repQ.push(&convert.arr[i--]);
        }
       */
        i = 0;
        while(i<4){
          q.pop(&convert.arr[i]);
          repQ.push(&convert.arr[i++]);
        }
        msec = convert.integer;
        delay(msec);
        break;
      case RFID:
        rfidScan();
        break;
      //WLAN commands currently unoperational
      case WLAN_DOWN:
        digitalWrite(WLAN_SW,LOW);
        break;
      case WLAN_UP:
        digitalWrite(WLAN_SW,HIGH);
        break;
      /////////////////////////////
      case REP:
      //convert incoming little endian bytes to integer
      //while decrementing and restoring into the repeat buffer
      //uncomment the lines below for big endian format
      //note that I did not check if these work use with attention
      /*
        i = 3;
        while(i>=0){
          q.pop(&convert.arr[i--]);
        }
        repCount=convert.integer;
        if(repCount>0){
          convert.integer = --repCount;
          i=3;
          while(i>=0)
            repQ.push(&convert.arr[i--]);
          copyQ();
        }
        break;        
       
       */
        i = 0;
        while(i<4){
          q.pop(&convert.arr[i++]);
        }
        repCount=convert.integer;
        if(repCount>0){
          convert.integer = --repCount;
          i=0;
          while(i<4)
            repQ.push(&convert.arr[i++]);
          copyQ();
        }
        break;
      default:
        break;
    }
  }
}
//receive commands and put them in a queue
void recCmds(void){
  int count = 0;
  while(count<qsize){
    if(Serial.available()>0){
      if(Serial.readBytes(&data,1)){
        q.push(&data);
        count++;
      }
    }
  }
  Serial.println("success");
}
//copy the queue from repQ to q
void copyQ(void){
  byte copy;
  while(!repQ.isEmpty()){
    repQ.pop(&copy);
    q.push(&copy);
  }
}
//close all the switches to start charging, pretty self explanatory
void startCharging(void){
  digitalWrite(PE,LOW);
  delay(1000);
  digitalWrite(B,LOW);
  delay(1000);
  digitalWrite(C,LOW);
}
//scans the rfid card 
//write method for the servo object takes degrees as its argument
//the values may need changing after re-installing the servo
//servo needs to be installed in the correct configuration for this to work
void rfidScan(void){
  myservo.write(180);
  delay(2000);
  myservo.write(90);
  delay(500);
}
//this works only at setup to initialize the servo
//and serves as a visual indicator for when the arduino resets
void servoSetup(void){
  myservo.write(0);
  delay(500);
  myservo.write(90);
  delay(500);
}
