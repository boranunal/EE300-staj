bool B = HIGH;
bool C = HIGH;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(3000);
  pinMode(2,OUTPUT);
  digitalWrite(2, HIGH);
  pinMode(3,OUTPUT);
  digitalWrite(3, HIGH);
  pinMode(4,OUTPUT);
  digitalWrite(4, HIGH);
  pinMode(7,OUTPUT);
  digitalWrite(7, HIGH);
  pinMode(8,INPUT);
  pinMode(12,INPUT);
  digitalWrite(7, LOW);
  delay(1000);
  digitalWrite(2, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("pin 8: ");
  Serial.println(digitalRead(8));
  Serial.print("pin 12: ");
  Serial.println(digitalRead(12));
  if(digitalRead(8) == HIGH){
    while(digitalRead(8) == HIGH);
    Serial.print("B: ");
    Serial.println(B);
    
    B = !B;
    digitalWrite(3, B);
  }
  if(digitalRead(12) == HIGH){
    while(digitalRead(12) == HIGH);
    Serial.print("C: ");
    Serial.println(C);
    
    C = !C;
    digitalWrite(4, C);
  }
}
