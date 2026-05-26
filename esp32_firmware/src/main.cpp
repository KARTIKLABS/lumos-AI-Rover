#include <Arduino.h>
#include "MotorController.h"
#include "Sensors.h"
#include "Thermal.h"
#include "Actuators.h"
#include "SerialParser.h"

// --- PIN DEFINITIONS ---
// Motors
#define L_PWM1 25
#define L_PWM2 26
#define R_PWM1 27
#define R_PWM2 14

// Sensors
#define TRIG_F 32
#define ECHO_F 33
#define TRIG_R 4
#define ECHO_R 5
#define BATT_PIN 34

// Thermal & Actuators
#define FAN_PIN 18
#define LOCK_PIN 19
#define LED_PIN 2

// --- INSTANTIATE MODULES ---
MotorController motors(L_PWM1, L_PWM2, R_PWM1, R_PWM2);
Sensors sensors(TRIG_F, ECHO_F, TRIG_R, ECHO_R, BATT_PIN);
ThermalController thermal(FAN_PIN);
Actuators actuators(LOCK_PIN, LED_PIN);
SerialParser parser(&motors, &thermal, &actuators);

unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL = 100; // 10Hz
const unsigned long FAILSAFE_TIMEOUT = 1000;  // 1s without comms = stop

void setup() {
    Serial.begin(115200);
    
    motors.begin();
    sensors.begin();
    thermal.begin();
    actuators.begin();
    
    actuators.setLed(true); // Indicate ready
}

void loop() {
    // 1. Parse incoming commands from Raspberry Pi
    parser.update();

    // 2. Failsafe check: Stop motors if we lose connection to Pi
    if (millis() - parser.getLastCommandTime() > FAILSAFE_TIMEOUT) {
        motors.stop();
        actuators.setLed(false); // Indicate comms loss
    } else {
        actuators.setLed(true);
    }

    // 3. Send Telemetry to Raspberry Pi
    if (millis() - lastTelemetryTime > TELEMETRY_INTERVAL) {
        lastTelemetryTime = millis();
        
        float frontDist = sensors.getFrontDistance();
        float rearDist = sensors.getRearDistance();
        float vBatt = sensors.getBatteryVoltage();
        
        // Format: <TELEMETRY,front_cm,rear_cm,vBatt>
        Serial.print("<TELEMETRY,");
        Serial.print(frontDist);
        Serial.print(",");
        Serial.print(rearDist);
        Serial.print(",");
        Serial.print(vBatt);
        Serial.println(">");
    }
}
