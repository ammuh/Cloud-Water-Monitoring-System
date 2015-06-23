/*
Code for Fluxduino
*/

/* Libraries */
//libraries for temp sensor
#include <OneWire.h>
#include <DallasTemperature.h>

/*Variables*/
//Button variables
int buttonPin = 3;   // choose the input pin (for a pushbutton)
boolean state = false;     // variable for reading the pin status

//Temp Sensor vars
#define ONE_WIRE_BUS 4
DallasTemperature sensors(&oneWire);
float temperature;

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
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  sensors.begin();
  //Temp Sensor Setup
}

void loop(){  
  //Halts till Push Button is pressed
  while (digitalRead(buttonPin) == LOW){
  }
  oldTime = 0;
  //Measurement Process
  if((millis() - oldTime) > 1000)    // Only process counters once per second
          { 
            //Flow Meter Conversions
            detachInterrupt(sensorInterrupt);           
            flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
            oldTime = millis();
            flowMilliLitres = (flowRate / 60) * 1000;
            totalMilliLitres += flowMilliLitres;
            unsigned int frac;
            frac = (flowRate - int(flowRate)) * 10;
            //Temp Sensor Conversions
            sensors.requestTemperatures();
            temperature = sensors.getTempCByIndex(0);
            //TODO Add in JSON Write
            pulseCount = 0;
            attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
          }
}

/*Extra Methods*/

//For Flow Meter
void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}
