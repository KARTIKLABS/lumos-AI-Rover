#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

class Sensors {
public:
    Sensors(int trigFront, int echoFront, int trigRear, int echoRear, int battPin);
    void begin();
    float getFrontDistance();
    float getRearDistance();
    float getBatteryVoltage();

private:
    int _trigFront, _echoFront, _trigRear, _echoRear, _battPin;
    float readUltrasonic(int trig, int echo);
};

#endif
