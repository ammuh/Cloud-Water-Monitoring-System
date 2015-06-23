/*
Code for Fluxduino
*/

//Button variables
int buttonPin = 3;   // choose the input pin (for a pushbutton)
boolean state = false;     // variable for reading the pin status

//Flow Meter Variabls
byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 2;
// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;
volatile byte pulseCount;  
float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;
unsigned long oldTime;


void setup() {
  //Pushbutton Setup
  pinMode(buttonPin, INPUT);    // declare pushbutton as input
  
  //Flow Meter Setup
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;
  

  // The Hall-effect sensor is connected to pin 2 which uses interrupt 0.
  // Configured to trigger on a FALLING state change (transition from HIGH
  // state to LOW state)
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}

void loop(){  
  //Halts till Push Button is pressed
  while (digitalRead(buttonPin) == LOW){
  }
  
}

/*Extra Methods*/

//For Flow Meter
void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}
