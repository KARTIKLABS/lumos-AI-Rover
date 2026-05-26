#ifndef ACTUATORS_H
#define ACTUATORS_H

#include <Arduino.h>

class Actuators {
public:
    Actuators(int lockPin, int ledPin);
    void begin();
    void setLock(bool locked);
    void setLed(bool state);

private:
    int _lockPin;
    int _ledPin;
};

#endif
