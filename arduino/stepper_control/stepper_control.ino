#include <Stepper.h>

#define STEPS 32

 Stepper stepper(STEPS, 8, 10, 9, 11);
 int val = 0;
void setup() {
  stepper.setSpeed(10);
  stepper.step(2048);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0)
  {
    val = Serial.parseInt();
    stepper.step(val);
    Serial.println(val); //for debugging
  }
}
