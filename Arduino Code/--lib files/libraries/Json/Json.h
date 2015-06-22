/*
  Json.h Library for creating Json with Arduino
*/
#ifndef Json_h
#define Json_h

#include "Arduino.h"

class Json
{
  public:
    Json(String sessionID, String dataType1, String dataType2, String dataType3, String dataType4);
    void jsonAdd(String data1, String data2, String data3, String data4);
    String getJson();
  private:
    String _dataType1;
    String _dataType2;
    String _dataType3;
    String _dataType4;
    String _runningJson;
};

#endif
