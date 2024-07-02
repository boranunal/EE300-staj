byte x;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
}

void  loop() {
  while (!Serial.available());
  x = Serial.read();
  if(x == 0x69)
    Serial.print('x');
  else
    Serial.write(x);
}
