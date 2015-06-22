#include <JsonSD.h>
//#include <SFE_CC3000.h>
#include <SD.h>
#include <SPI.h>

JsonSD obj1(12345, String("Fruits"), String("Vegetables"), String("Desserts"), String("Meal"));

void setup()
{
  Serial.begin(38400);
  obj1.jsonSDInit(8);
  obj1.jsonWrite(String("Apple"), String("Potato"), String("Ice Cream"), String("Chicken"));
  
}

void loop()
{
  obj1.capJson();
  Serial.println(obj1.getJson());
  obj1.closeGetJson();
  delay(2000);
}
