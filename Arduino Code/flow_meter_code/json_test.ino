#include <Morse.h>

Json obj1(12345, "Fruits", "Vegetables", "Desserts", "Meal");

void setup()
{
}

void loop()
{
  morse.dot(); morse.dot(); morse.dot();
  morse.dash(); morse.dash(); morse.dash();
  morse.dot(); morse.dot(); morse.dot();
  delay(3000);
}
