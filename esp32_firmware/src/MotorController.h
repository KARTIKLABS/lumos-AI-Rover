#ifndef MOTOR_CONTROLLER_H
#define MOTOR_CONTROLLER_H

#include <Arduino.h>

class MotorController {
public:
    MotorController(int leftPwm1, int leftPwm2, int rightPwm1, int rightPwm2);
    void begin();
    void drive(int leftSpeed, int rightSpeed);
    void stop();

private:
    int _lpwm1, _lpwm2, _rpwm1, _rpwm2;
    // Map speed (-255 to 255) to PWM pins
    void setMotor(int pin1, int pin2, int speed);
};

#endif
