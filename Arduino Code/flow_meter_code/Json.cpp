/*
  Json.cpp - Library for creating Json with Arduino
*/

#include "Arduino.h"
#include "Json.h"

Json::Json(String sessionID, String dataType1, String dataType2, String dataType3, String dataType4)
{
  dataType1 = _dataType1;
  dataType2 = _dataType2;
  dataType3 = _dataType3;
  dataType4 = _dataType4;
  _runningJson = "{\"" + sessionID + "\":[";   
}

void Json::jsonAdd(String data1, String data2, String data3, String data4)
{
  //Creates JSON by adding data to datatypes
  _runningJson = _runningJson + "{";
  _runningJson = _runningJson + "\""+ _dataType1 + "\":\"" + data1 + "\", ";
  _runningJson = _runningJson + "\""+ _dataType2 + "\":\"" + data2 + "\", ";
  _runningJson = _runningJson + "\""+ _dataType3 + "\":\"" + data3 + "\", ";
  _runningJson = _runningJson + "\""+ _dataType4 + "\":\"" + data4 + "\",";
  _runningJson = _runningJson + "}, ";
}

String Json::getJson()
{
  int cutMark = _runningJson.length() - 2;
  _runningJson.remove(cutMark);
  _runningJson = _runningJson + "]}";
  return _runningJson;
  
}
