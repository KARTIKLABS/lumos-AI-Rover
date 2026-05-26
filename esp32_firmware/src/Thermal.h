#ifndef THERMAL_H
#define THERMAL_H

#include <Arduino.h>

class ThermalController {
public:
    ThermalController(int fanPin);
    void begin();
    void setFanSpeed(int speed); // 0 to 255
    void update(float piTemp);

private:
    int _fanPin;
    int _currentSpeed;
};

#endif
