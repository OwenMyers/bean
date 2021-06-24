#include <Stepper.h>

#define STEPS 32

 Stepper stepper(STEPS, 8, 10, 9, 11);
int val = 0;
void setup() {
  stepper.setSpeed(400);
  //This is steps per revolution
  //stepper.step(2048);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (val < 6) {
     delay(500);
     stepper.step(-10000); 
     val += 1;
  }
}
