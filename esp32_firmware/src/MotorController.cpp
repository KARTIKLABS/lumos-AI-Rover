#include "MotorController.h"

MotorController::MotorController(int leftPwm1, int leftPwm2, int rightPwm1, int rightPwm2) {
    _lpwm1 = leftPwm1;
    _lpwm2 = leftPwm2;
    _rpwm1 = rightPwm1;
    _rpwm2 = rightPwm2;
}

void MotorController::begin() {
    pinMode(_lpwm1, OUTPUT);
    pinMode(_lpwm2, OUTPUT);
    pinMode(_rpwm1, OUTPUT);
    pinMode(_rpwm2, OUTPUT);
    stop();
}

void MotorController::setMotor(int pin1, int pin2, int speed) {
    if (speed > 0) {
        analogWrite(pin1, speed);
        analogWrite(pin2, 0);
    } else if (speed < 0) {
        analogWrite(pin1, 0);
        analogWrite(pin2, -speed);
    } else {
        analogWrite(pin1, 0);
        analogWrite(pin2, 0);
    }
}

void MotorController::drive(int leftSpeed, int rightSpeed) {
    // constrain to -255 to 255
    leftSpeed = constrain(leftSpeed, -255, 255);
    rightSpeed = constrain(rightSpeed, -255, 255);
    
    setMotor(_lpwm1, _lpwm2, leftSpeed);
    setMotor(_rpwm1, _rpwm2, rightSpeed);
}

void MotorController::stop() {
    drive(0, 0);
}
