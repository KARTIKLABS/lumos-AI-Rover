#include "SerialParser.h"

SerialParser::SerialParser(MotorController* motors, ThermalController* thermal, Actuators* actuators) {
    _motors = motors;
    _thermal = thermal;
    _actuators = actuators;
    _buffer = "";
    _lastCommandTime = millis();
}

void SerialParser::update() {
    while (Serial.available() > 0) {
        char c = Serial.read();
        if (c == '\n' || c == '>') {
            if (_buffer.startsWith("<")) {
                parseCommand(_buffer.substring(1));
            }
            _buffer = "";
        } else {
            _buffer += c;
        }
    }
}

void SerialParser::parseCommand(String cmd) {
    // Expected formats:
    // DRIVE,left_pwm,right_pwm
    // TEMP,pi_temp
    // LOCK,state
    
    _lastCommandTime = millis(); // Update failsafe timer

    int firstComma = cmd.indexOf(',');
    if (firstComma == -1) return;

    String type = cmd.substring(0, firstComma);
    String data = cmd.substring(firstComma + 1);

    if (type == "DRIVE") {
        int secondComma = data.indexOf(',');
        if (secondComma != -1) {
            int left = data.substring(0, secondComma).toInt();
            int right = data.substring(secondComma + 1).toInt();
            _motors->drive(left, right);
        }
    } else if (type == "TEMP") {
        float piTemp = data.toFloat();
        _thermal->update(piTemp);
    } else if (type == "LOCK") {
        int state = data.toInt();
        _actuators->setLock(state == 1);
    }
}

unsigned long SerialParser::getLastCommandTime() {
    return _lastCommandTime;
}
