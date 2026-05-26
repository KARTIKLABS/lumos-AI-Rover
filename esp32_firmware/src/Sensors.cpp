#include "Sensors.h"

Sensors::Sensors(int trigFront, int echoFront, int trigRear, int echoRear, int battPin) {
    _trigFront = trigFront;
    _echoFront = echoFront;
    _trigRear = trigRear;
    _echoRear = echoRear;
    _battPin = battPin;
}

void Sensors::begin() {
    pinMode(_trigFront, OUTPUT);
    pinMode(_echoFront, INPUT);
    pinMode(_trigRear, OUTPUT);
    pinMode(_echoRear, INPUT);
    // Battery analog read doesn't need pinMode explicitly on ESP32, but good practice
    pinMode(_battPin, INPUT);
}

float Sensors::readUltrasonic(int trig, int echo) {
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    
    long duration = pulseIn(echo, HIGH, 30000); // 30ms timeout ~ 5 meters
    if (duration == 0) return -1;
    
    // speed of sound = 343 m/s
    return duration * 0.034 / 2;
}

float Sensors::getFrontDistance() {
    return readUltrasonic(_trigFront, _echoFront);
}

float Sensors::getRearDistance() {
    return readUltrasonic(_trigRear, _echoRear);
}

float Sensors::getBatteryVoltage() {
    int raw = analogRead(_battPin);
    // Assuming a voltage divider (e.g., 10k and 1k) to map 12.6V down to <3.3V
    // Adjust this multiplier based on your specific resistor values.
    float voltage = (raw / 4095.0) * 3.3 * 11.0; 
    return voltage;
}
