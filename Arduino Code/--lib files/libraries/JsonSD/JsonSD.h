/*
  Json.h Library for creating Json with Arduino
*/

#ifndef JsonSD_h
#define JsonSD_h



#include "Arduino.h"
//#include "SFE_CC3000.h"
#include "SD.h"
#include "SPI.h"

class JsonSD
{
  public:
    JsonSD(int sessionID, String dataType1, String dataType2, String dataType3, String dataType4);
    void jsonWrite(String data1, String data2, String data3, String data4);
    String getStatus();
    void jsonSDInit(int pin);
    void capJson();
    String getJson();
    void closeGetJson();
  private:
    String _dataType1;
    String _dataType2;
    String _dataType3;
    String _dataType4;
    int _sessionID;
    String _runningJson;
    String _filename;
    String _status;
    boolean _firstPrint;
    File _sdFile;
};

#endif
