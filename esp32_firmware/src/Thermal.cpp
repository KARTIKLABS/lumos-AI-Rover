#include "Thermal.h"

ThermalController::ThermalController(int fanPin) {
    _fanPin = fanPin;
    _currentSpeed = 0;
}

void ThermalController::begin() {
    pinMode(_fanPin, OUTPUT);
    setFanSpeed(0);
}

void ThermalController::setFanSpeed(int speed) {
    _currentSpeed = constrain(speed, 0, 255);
    analogWrite(_fanPin, _currentSpeed);
}

void ThermalController::update(float piTemp) {
    // Simple dynamic fan curve based on Pi's reported temp
    if (piTemp > 75.0) {
        setFanSpeed(255); // Max cooling
    } else if (piTemp > 65.0) {
        setFanSpeed(180); // Medium cooling
    } else if (piTemp > 50.0) {
        setFanSpeed(100); // Silent mode
    } else {
        setFanSpeed(0);   // Off
    }
}
