#include <Servo.h>

Servo myservo_x;
Servo myservo_y;
const int pi_pin_x_pos = 2;
const int pi_pin_x_neg = 3;
int state_x = 1;
int pi_state = 0;

void setup() {
  Serial.begin(9600);
  delay(1000);
  pinMode(pi_pin, INPUT);
  myservo_x.attach(9);
  myservo_x.attach(10);
  Serial.println("Starting...\n");
}

void loop() {
  pi_state = digitalRead(pi_pin);
  Serial.println("Current Pi State is:");
  Serial.println(pi_state);
  if (pi_state_x == HIGH && state_x == 1)
  {
    myservo.write(120);
    delay(1000);
    myservo.write(90);
    state = 2;
  }
  if (pi_state == LOW && state_x == 2)
  {
    state = 1;
  }
  delay(1000);

}
