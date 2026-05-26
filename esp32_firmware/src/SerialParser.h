#ifndef SERIAL_PARSER_H
#define SERIAL_PARSER_H

#include <Arduino.h>
#include "MotorController.h"
#include "Thermal.h"
#include "Actuators.h"

class SerialParser {
public:
    SerialParser(MotorController* motors, ThermalController* thermal, Actuators* actuators);
    void update();
    unsigned long getLastCommandTime();

private:
    MotorController* _motors;
    ThermalController* _thermal;
    Actuators* _actuators;
    String _buffer;
    unsigned long _lastCommandTime;

    void parseCommand(String cmd);
};

#endif
