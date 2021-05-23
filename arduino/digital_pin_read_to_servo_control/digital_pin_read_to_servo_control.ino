#include <Servo.h>

Servo myservo;
const int pi_pin = 2;
int state = 1;
int pi_state = 0;

void setup() {
  Serial.begin(9600);
  delay(1000);
  pinMode(pi_pin, INPUT);
  myservo.attach(9);
  Serial.println("Starting...\n");
}

void loop() {
  pi_state = digitalRead(pi_pin);
  Serial.println("Current Pi State is:");
  Serial.println(pi_state);
  if (pi_state == HIGH && state == 1)
  {
    myservo.write(120);
    delay(1000);
    myservo.write(90);
    state = 2;
  }
  if (pi_state == LOW && state == 2)
  {
    state = 1;
  }
  delay(1000);
}
