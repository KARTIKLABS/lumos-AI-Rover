#include "Actuators.h"

Actuators::Actuators(int lockPin, int ledPin) {
    _lockPin = lockPin;
    _ledPin = ledPin;
}

void Actuators::begin() {
    pinMode(_lockPin, OUTPUT);
    pinMode(_ledPin, OUTPUT);
    setLock(true); // Default to locked
    setLed(false);
}

void Actuators::setLock(bool locked) {
    // If using a servo, you'd use ESP32Servo here. 
    // Assuming simple relay/solenoid for this example:
    if (locked) {
        digitalWrite(_lockPin, LOW); // De-energize
    } else {
        digitalWrite(_lockPin, HIGH); // Energize to open
    }
}

void Actuators::setLed(bool state) {
    digitalWrite(_ledPin, state ? HIGH : LOW);
}
