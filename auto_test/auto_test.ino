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
const byte ACK = 0x1F;
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
      Serial.print('1');
      startCharging();
      break;
    case PE_ON:
      digitalWrite(PE,LOW);
      Serial.print('2');
      break;
    case PE_OFF:
      digitalWrite(PE,HIGH);
      Serial.print('3');
      break;
    case B_ON:
      digitalWrite(B,LOW);
      Serial.print('4');
      break;
    case B_OFF:
      digitalWrite(B,HIGH);
      Serial.print('5');
      break;
    case C_ON:
      digitalWrite(C,LOW);
      Serial.print('6');
      break;
    case C_OFF:
      digitalWrite(C,HIGH);
      Serial.print('7');
      break;
    case WAIT:
      sec = Serial.readString().toInt();
      Serial.print("WAIT: ");
      Serial.println(sec);
      Serial.flush();
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
  Serial.print('x');
  digitalWrite(PE,LOW);
  delay(1000);
  digitalWrite(B,LOW);
  delay(1000);
  digitalWrite(C,LOW);
}
