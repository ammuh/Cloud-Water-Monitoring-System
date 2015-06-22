/*
  Json.cpp - Library for creating Json with Arduino
*/
#include "JsonSD.h"
#include "Arduino.h"
//#include "SFE_CC3000.h"
#include "SD.h"
#include "SPI.h"

JsonSD::JsonSD(int sessionID, String dataType1, String dataType2, String dataType3, String dataType4)
{
	pinMode(SD_CS, OUTPUT);
	_dataType1 = dataType1;
	_dataType2 = dataType2;
	_dataType3 = dataType3;
	_dataType4 = dataType4;
	_sessionID = sessionID;
	_firstPrint = true;
}

void JsonSD::jsonSDInit(int pin)
{
	//initialize pin
	pinMode(pin, OUTPUT);
	if ( !SD.begin(pin) ) {
	  _status = "103";
	}
	//Check for existence of file
	if ( SD.exists(_filename) ) {
		if ( !SD.remove(_filename) ) {
		  _status = "101";
		}
	}
}

void JsonSD::jsonWrite(String data1, String data2, String data3, String data4)
{
	//Writes JSON to SD Card

	String _currentWrite;
	//Check if this is first JSON print
	if (_firstPrint) {
		_currentWrite = "{\"" + _sessionID + "\":[";
	}
	//Encode JSON data
	_currentWrite = _currentWrite + "{";
	_currentWrite = _currentWrite + "\""+ _dataType1 + "\":\"" + data1 + "\", ";
	_currentWrite = _currentWrite + "\""+ _dataType2 + "\":\"" + data2 + "\", ";
	_currentWrite = _currentWrite + "\""+ _dataType3 + "\":\"" + data3 + "\", ";
	_currentWrite = _currentWrite + "\""+ _dataType4 + "\":\"" + data4 + "\"";
	_currentWrite = _currentWrite + "}, ";
	//Open SD
	_sdFile = SD.open(_filename, FILE_WRITE);
	if (_sdFile) {
		_status = "100";
	}
	else {
		_status = "102";
	}
	//Print to SD
	if (_sdFile) {
		_sdFile.print(_currentWrite);
	}
	if (_sdFile) {
		_sdFile.close();
	}
	_currentWrite = "";
}

String JsonSD::getStatus()
{
	return _status;
}
void JsonSD::capJson()
{
	_sdFile = SD.open(_filename, FILE_WRITE);
		if (_sdFile) {
			_status = "100";
		}
		else {
			_status = "102";
		}
		//Print to SD
		if (_sdFile) {
			_sdFile.print("]}");
		}
		if (_sdFile) {
			_sdFile.close();
	}
}

String JsonSD::getJson()
{
	_sd_file = SD.open(_filename, FILE_READ);
	return _sdFile.read();
}

void JsonSD::closeGetJson()
{
	sd_file.close();
}