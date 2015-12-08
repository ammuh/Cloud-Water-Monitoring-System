/*
* Fluxduino Code for sending CSV data over bluetooth.
*/

#include <OneWire.h>
OneWire ds(6);
float temperature;
bool isFirst;
//Button variables
int buttonPin = 4;   // choose the input pin (for a pushbutton)
bool state; // variable for reading the pin status
int lastpress;

//Flow Meter Variabls
byte sensorInterrupt = 1;  // 1 = digital pin 3
byte sensorPin       = 3;
// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;
volatile byte pulseCount = 0;
float flowRate = 0;
unsigned int flowMilliLitres = 0;
unsigned long totalMilliLitres = 0;
unsigned long oldTime = 0;

char blueToothVal;


void setup() {
	Serial.begin(9600);
}

void loop() {
	if(Serial.available()>0)
  {//if there is data being recieved
    blueToothVal=Serial.read(); //read it
  }
  oldTime = millis();
  if (blueToothVal=='b')
  {//if value from bluetooth serial is n
  	state = true;
  	isFirst = true;
    Serial.print("time,flowRate,mlUsed,temperature\n");
  	while(state){
	    if ((millis() - oldTime) > 1000)   // Only process counters once per second
	    {
	      //Flow Meter Conversions
	      detachInterrupt(sensorInterrupt);
	      flowMilliLitres  = ((1000.0 / (millis() - oldTime)) * pulseCount * 1000) / (60 * calibrationFactor);
	      oldTime = millis();
	      totalMilliLitres += flowMilliLitres;
	      //Temp Sensor Conversions
	      temperature = getTemp();
	      //TODO Add in JSON Write
	 
	      	if (!isFirst){
	      		Serial.print('\n');
	      	}
	      
	
	      Serial.print(String(millis()) + ',' + String(flowMilliLitres) + ',' + String(totalMilliLitres) + ',' + String(temperature));

	      isFirst = false; //Sets json lib so that wont at extra spaces and commas
	      oldTime = millis();
	      pulseCount = 0;
	      attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
	    }
	    if(Serial.available()>0)
		  {//if there is data being recieved
		    blueToothVal=Serial.read(); //read it
		  }
		  if (blueToothVal=='s')
		  {//if value from bluetooth serial is n
		    state = false;            //turn off LED
		  }
  	}
  }
  delay(1000);
}
//Flowrate
void pulseCounter()
{
  pulseCount++;
}
//Temperature
float getTemp(void)
{
  //returns the temperature from one DS18S20 in DEG Celsius

  byte data[12];
  byte addr[8];

  if ( !ds.search(addr)) {
    //no more sensors on chain, reset search
    ds.reset_search();
    return -1000;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1); // start conversion, with parasite power on at the end

  byte present = ds.reset();
  ds.select(addr);
  ds.write(0xBE); // Read Scratchpad


  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = ds.read();
  }

  ds.reset_search();

  byte MSB = data[1];
  byte LSB = data[0];

  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16;

  return TemperatureSum;
}
