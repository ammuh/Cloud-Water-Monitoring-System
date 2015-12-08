
#include <Json.h>
byte statusLed    = 13;

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
//creates json for formatting objects
Json obj1(String(12345), String("Seconds"), String("Flow_Rate"), String("Temperature"), String("Milliliters_Used"));

//Variables for starting with switch

int inPin = 4;         // the number of the input pin
int outPin = 13;       // the number of the output pin

boolean state = false;      // the current state of the output pin
int reading;           // the current reading from the input pin
boolean previous = false;    // the previous reading from the input pin

// the follow variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long time = 0;         // the last time the output pin was toggled
long debounce = 200;   // the debounce time, increase if the output flickers


void setup()
{
  
  // Initialize a serial connection for reporting values to the host
   Serial.begin(115200);
   //Switch
   
   pinMode(inPin, INPUT);
  
  
  // Set up the status LED line as an output
  pinMode(statusLed, OUTPUT);
  digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  
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

/**
 * Main program loop
 */
 
void loop()
{
   reading = digitalRead(inPin);
   
   if (reading == HIGH && previous == false && millis() - time > debounce) {
    state = true; //Change state
    oldTime = millis(); //reset oldTime to compensate for time user takes to press button
    time = millis(); //switch was toggled so need to reset time for next logic gate
    unsigned long timeStart = millis();
    Serial.println("Switch Activated, measure loop began");
    
    while (state == true) {
        
      
      if (digitalRead(inPin) == HIGH && millis() - time > debounce) {
        Serial.println("Swith Toggled");
        state = false;
        
      }
      else {
        //Continues with measurement process
        if((millis() - oldTime) > 1000)    // Only process counters once per second
          { 
            // Disable the interrupt while calculating flow rate and sending the value to
            // the host
            detachInterrupt(sensorInterrupt);
            Serial.println("In measurement");    
            // Because this loop may not complete in exactly 1 second intervals we calculate
            // the number of milliseconds that have passed since the last execution and use
            // that to scale the output. We also apply the calibrationFactor to scale the output
            // based on the number of pulses per second per units of measure (litres/minute in
            // this case) coming from the sensor.
            flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
            
            // Note the time this processing pass was executed. Note that because we've
            // disabled interrupts the millis() function won't actually be incrementing right
            // at this point, but it will still return the value it was set to just before
            // interrupts went away.
            oldTime = millis();
            
            // Divide the flow rate in litres/minute by 60 to determine how many litres have
            // passed through the sensor in this 1 second interval, then multiply by 1000 to
            // convert to millilitres.
            flowMilliLitres = (flowRate / 60) * 1000;
            
            // Add the millilitres passed in this second to the cumulative total
            totalMilliLitres += flowMilliLitres;
              
            unsigned int frac;
            // Determine the fractional part. The 10 multiplier gives us 1 decimal place.
            frac = (flowRate - int(flowRate)) * 10;
            
            obj1.jsonAdd(String(millis()-timeStart),String(flowMilliLitres),String(0),String(totalMilliLitres));
                  
            // Reset the pulse counter so we can start incrementing again
            pulseCount = 0;
            
            // Enable the interrupt again now that we've finished sending output
            attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
          }
        
      }
      
    }
    Serial.println("Exited while Loop");
    Serial.println(obj1.getJson());
    time = millis();    
  }
 
  //reset previous setting
  previous = false;   
}



void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}

/*
JSON Encoder
*/


