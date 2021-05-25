#include <Servo.h>

Servo myservo_x;
Servo myservo_y;
const int pi_pin_x_pos = 2;
const int pi_pin_x_neg = 3;
int state_x_pos = 1;
int state_x_neg = 1;
int pi_state_x_pos = 0;
int pi_state_x_neg = 0;

void setup() {
  Serial.begin(9600);
  delay(1000);
  pinMode(pi_pin_x_pos, INPUT);
  pinMode(pi_pin_x_neg, INPUT);
  myservo_x.attach(9);
  myservo_y.attach(10);
  myservo_x.write(90);
  Serial.println("Starting...\n");
}

void loop() {
  pi_state_x_pos = digitalRead(pi_pin_x_pos);
  pi_state_x_neg = digitalRead(pi_pin_x_neg);

  if (pi_state_x_pos == HIGH && state_x_pos == 1)
  {
    myservo_x.write(120);
    state_x_pos = 2;
  }
  if (pi_state_x_pos == LOW && state_x_pos == 2)
  {
    myservo_x.write(90);
    state_x_pos = 1;
  }
  if (pi_state_x_neg == HIGH && state_x_neg == 1)
  {
    myservo_x.write(60);
    state_x_neg = 2;
  }
  if (pi_state_x_neg == LOW && state_x_neg == 2)
  {
    myservo_x.write(90);
    state_x_neg = 1;
  }
  delay(1000);
}
