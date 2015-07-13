/*
Code for Fluxduino
*/

/* Libraries */
//libraries for temp sensor
#include <OneWire.h>
OneWire ds(6);
float temperature;

//Libs for JSON Parse
#include <JsonParse.h>
JsonParse jsonEngine(String("Time"),String("Flow_Rate"),String("ML_Used"),String("Temperature"));
boolean isFirst;

//Libs for SD
#include <SPI.h>
#include <SD.h>
File jsonStore;
File httpRequest;

//Libs for Wifi
#include <Adafruit_CC3000.h>
#define ADAFRUIT_CC3000_IRQ   2  // MUST be an interrupt pin!
// These can be any two pins
#define ADAFRUIT_CC3000_VBAT  7
#define ADAFRUIT_CC3000_CS    10
// Use hardware SPI for the remaining pins
// On an UNO, SCK = 13, MISO = 12, and MOSI = 11
Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
                                         SPI_CLOCK_DIVIDER);
#define WLAN_SSID       "Ammar's iPhone"           // cannot be longer than 32 characters!
#define WLAN_PASS       "ammar123"
#define WLAN_SECURITY   WLAN_SEC_WPA2
#define IDLE_TIMEOUT  3000
#define WEBSITE      "flux-plant.appspot.com/_ah_api/fluxplant/v1"
#define NEWSESSION      "/NewSession"
#define DATASESSION      "/DataSubmit"
uint32_t ip;
String uniqueId;
String clientToken;
//Button variables
int buttonPin = 4;   // choose the input pin (for a pushbutton)
boolean state; // variable for reading the pin status
int lastpress;

//Flow Meter Variabls
byte sensorInterrupt = 1;  // 1 = digital pin 3
byte sensorPin       = 3;
// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;
volatile byte pulseCount =0;  
float flowRate = 0;
unsigned int flowMilliLitres = 0;
unsigned long totalMilliLitres = 0;
unsigned long oldTime = 0;

void setup() {
  Serial.begin(115200);
  pnt(F("\nInitializing..."));
  if (!cc3000.begin())
  {
    pnt(F("Couldn't begin()! Check your wiring?"));
    while(1);
  }
  pnt("Passed begin if statement");
  // Optional SSID scan
  // listSSIDResults();
  
  pnt(F("\nAttempting to connect to ")); pnt(WLAN_SSID);
  if (!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) {
    pnt(F("Failed!"));
    while(1);
  }
   
  pnt(F("Connected!"));
  
  /* Wait for DHCP to complete */
  pnt(F("Request DHCP"));
  while (!cc3000.checkDHCP())
  {
    delay(100); // ToDo: Insert a DHCP timeout!
  }  

  /* Display the IP address DNS, Gateway, etc. */  
  while (! displayConnectionDetails()) {
    delay(1000);
  }

  ip = 0;
  // Try looking up the website's IP address
  pnt(WEBSITE); pnt(F(" -> "));
  while (ip == 0) {
    if (! cc3000.getHostByName(WEBSITE, &ip)) {
      pnt(F("Couldn't resolve!"));
    }
    delay(500);
  }

  cc3000.printIPdotsRev(ip);
  
  //Serial Setup
  
  //Pushbutton Setup
  pinMode(buttonPin, INPUT);    // declare pushbutton as input
  state = false;
  lastpress = millis();
  pnt("Push button initialized");
  //Flow Meter Setup
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  pnt("Flow Meter initialized");
  //Temp Sensor Setup
  //SD Initialization
  if (!SD.begin(53)) {
    pnt("Sd did not initialize");
    return;
  }
  if(SD.exists("json.txt")){
    boolean check = SD.remove("json.txt");
    if (check) {
    pnt("Existing JSON removed");
    }
  }
  pnt("Initialization complete");
}

void loop(){  
  //Halts till Push Button is pressed
  while (!state)
  {
    if (digitalRead(buttonPin) == HIGH && (millis()-lastpress)>1000) {
      pnt("Button Press");
      state = true;
      lastpress = millis();
      //TODO Request Session ID
      //TODO start SD file and write first part of JSON
      jstore(jsonEngine.jsonHead(1135));
      isFirst = true;
      oldTime = millis();
    }
  }
  while (state)
  {
    //Measurement Process
    if((millis() - oldTime) > 1000)    // Only process counters once per second
          { 
            //Flow Meter Conversions
            detachInterrupt(sensorInterrupt);           
            flowMilliLitres  = ((1000.0 / (millis() - oldTime)) * pulseCount * 1000) / (60 * calibrationFactor);
            oldTime = millis();
            totalMilliLitres += flowMilliLitres;
            //Temp Sensor Conversions
            temperature = getTemp();
            //TODO Add in JSON Write
            jstore(jsonEngine.jsonAdd(String(millis()),String(flowMilliLitres),String(totalMilliLitres),String(temperature), isFirst));
            pnt("Time: " + String(millis()));
            pnt("Flow Rate: " + String(flowMilliLitres));
            pnt("Total Used: " + String(totalMilliLitres));
            pnt("Temperature: " + String(temperature));
            pnt("");
            isFirst = false; //Sets json lib so that wont at extra spaces and commas
            oldTime = millis(); 
            pulseCount = 0;
            attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
          }
     if (digitalRead(buttonPin) == HIGH && (millis()-lastpress)>1000)
     {
      pnt("Button Press");
      state = false;
      lastpress = millis();
      jstore(jsonEngine.jsonCap());
      pnt("Final Data");
      jsonStore = SD.open("json.txt");
      int bodyLength = jsonStore.size();
        if(!jsonStore.seek(0)){
              pnt("error");
            }
          while (jsonStore.available()) {   
            int a =(byte)jsonStore.peek();
            char c = char(a);
            String str;
            int pos = jsonStore.position() + 1;
            if(!jsonStore.seek(pos)){
              pnt("error");
            }
           Serial.print(c);        
          }
       pnt("Building HTTP request");
       writeHTTP("POST", WEBSITE, WEBPAGE, bodyLength, true);
      Adafruit_CC3000_Client www = cc3000.connectTCP(ip, 80);
      if (www.connected()) {
        pnt("Connection Established");
        /*jsonStore = SD.open("json.txt");
        if(!jsonStore.seek(0)){
              pnt("error");
            }
          while (jsonStore.available()) {   
            int a =(byte)jsonStore.peek();
            char c = char(a);
            String str;
            int pos = jsonStore.position() + 1;
            if(!jsonStore.seek(pos)){
              pnt("error");
            }
           www.write(c);        
          }
         jsonStore.close();*/
         
         httpRequest = SD.open("http.txt");
        if(!httpRequest.seek(0)){
              pnt("error");
            }
          while (httpRequest.available()) {   
            int a =(byte)httpRequest.peek();
            char c = char(a);
            int pos = httpRequest.position() + 1;
            if(!httpRequest.seek(pos)){
              pnt("error");
            }
           www.write(c);        
          }
          pnt("While Loop Finished");
         httpRequest.close();
         www.println();
      }       
      unsigned long lastRead = millis();
      while (www.connected() && (millis() - lastRead < IDLE_TIMEOUT)) {
        while (www.available()) {
          char c = www.read();
          Serial.print(c);
          lastRead = millis();
        }
      }
      www.close();
      
    }
  }
}

/*Extra Methods*/

//For Flow Meter
void pulseCounter()
{
  pulseCount++;
}
//For Logging to SD log
void jstore(String msg)
{
  jsonStore = SD.open("json.txt", FILE_WRITE);
  jsonStore.println(msg);
  jsonStore.close();
}
void pnt (String msg) {
  Serial.println(msg);
}
float getTemp(){
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
  ds.write(0x44,1); // start conversion, with parasite power on at the end

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
//wifi Methods
bool displayConnectionDetails(void)
{
  uint32_t ipAddress, netmask, gateway, dhcpserv, dnsserv;
  
  if(!cc3000.getIPAddress(&ipAddress, &netmask, &gateway, &dhcpserv, &dnsserv))
  {
    Serial.println(F("Unable to retrieve the IP Address!\r\n"));
    return false;
  }
  else
  {
    Serial.print(F("\nIP Addr: ")); cc3000.printIPdotsRev(ipAddress);
    Serial.print(F("\nNetmask: ")); cc3000.printIPdotsRev(netmask);
    Serial.print(F("\nGateway: ")); cc3000.printIPdotsRev(gateway);
    Serial.print(F("\nDHCPsrv: ")); cc3000.printIPdotsRev(dhcpserv);
    Serial.print(F("\nDNSserv: ")); cc3000.printIPdotsRev(dnsserv);
    Serial.println();
    return true;
  }
}
//Create HTTP request
void writeHTTP (String method, String host, String webpage, int bodyLength, bool addJson) {
  if(SD.exists("http.txt")){
    boolean check = SD.remove("http.txt");
    if (check) {
    pnt("Existing http request file removed");
    }
  }
  httpRequest = SD.open("http.txt", FILE_WRITE);
  httpRequest.println(method + " " + webpage + " HTTP/1.1"); 
  httpRequest.println("Host: " + host);
  httpRequest.print("Content-Length: ");
  httpRequest.println(bodyLength);
  httpRequest.println("User-Agent: Arduino/1.0");
  httpRequest.println("Connection: close");
  if (addJson) {
    httpRequest.println("Content-Type: application/json");
  }
  else {
    httpRequest.println("Content-Type: application/xml");
  }
  httpRequest.println();
  httpRequest.close();
  if (addJson) {
  jsonStore = SD.open("json.txt");
  int pos = 0;
    while (jsonStore.available()) {
      if(!jsonStore.seek(pos)){
        pnt("Error");
      }   
      int a =(byte)jsonStore.peek();
      char c = char(a);
      pos++;
      jsonStore.close();
      httpRequest = SD.open("http.txt", FILE_WRITE);
      httpRequest.print(c);
      httpRequest.close();
      jsonStore = SD.open("json.txt");   
      if(!jsonStore.seek(pos - 1)){
        pnt("Error");
      } 
    }
 jsonStore.close();
  }
  else {
    httpRequest = SD.open("http.txt", FILE_WRITE);
    httpRequest.print("<MESSAGE>Hello World</MESSAGE>");
    httpRequest.close();
  }
}
