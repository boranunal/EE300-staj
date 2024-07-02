const int PE=2;
const int B=3;
const int C=4;

//variables:
unsigned long int msec;
unsigned long int sec;
byte cmd;

//COMMANDS:
const byte START_CHARGING = 0x20;
const byte PE_ON = 0x01;
const byte PE_OFF = 0x11;
const byte B_ON = 0x02;
const byte B_OFF = 0x12;
const byte C_ON = 0x03;
const byte C_OFF = 0x13;
const byte WAIT = 0x0F;
void setup() {
  pinMode(PE, OUTPUT);
  digitalWrite(PE,HIGH);
  pinMode(B, OUTPUT);
  digitalWrite(B,HIGH);
  pinMode(C, OUTPUT);
  digitalWrite(C, HIGH);
  Serial.begin(9600);
  
}

void loop() {
  while(!Serial.available()){
    if(!Serial) {  //check if Serial is available... if not,
      Serial.end();      // close serial port
      delay(100);        //wait 100 millis
      Serial.begin(9600); // reenable serial again
    }
  }
  cmd = Serial.read();
  send_ACK(cmd);
  switch(cmd){
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
      sec = Serial.readString().toInt();
      wait(sec);
      break;
    default: 
      break;
  }
  
}
void wait(int sec){
  msec = 1000*sec;
  delay(msec);
}
void send_ACK(byte cmd){
  Serial.write(cmd);
}
void startCharging(void){
  digitalWrite(PE,LOW);
  delay(1000);
  digitalWrite(B,LOW);
  delay(1000);
  digitalWrite(C,LOW);
}
