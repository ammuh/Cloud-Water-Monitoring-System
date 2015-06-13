#include <Json.h>

Json obj1(String(12345), String("Fruits"), String("Vegetables"), String("Desserts"), String("Meal"));

void setup()
{
  Serial.begin(38400);
  obj1.jsonAdd(String("Apple"), String("Potato"), String("Ice Cream"), String("Chicken"));
}

void loop()
{
  
  Serial.println(obj1.getJson());
  delay(2000);
}
