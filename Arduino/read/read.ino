unsigned long myTime;

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
}

void loop() {
  myTime = millis();
  Serial.print(myTime);
  Serial.print(" ");
  Serial.println(analogRead(A0));
  delay(3.9);
}
