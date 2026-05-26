# Campus Rover Wiring Guide

This guide maps the hardware connections between the main modules.
Ensure logic levels are respected (ESP32 is 3.3V logic, Raspberry Pi is 3.3V logic, Sensors might be 5V).

## Power System
- **Main Battery**: 12V LiPo/Li-Ion (3S/4S) -> BMS
- **Motors**: 12V direct from Battery (via BTS7960 Motor Drivers)
- **Raspberry Pi 5**: 5V/5A Buck Converter (from 12V) connected to USB-C or GPIO Power.
- **ESP32**: 5V from Buck Converter or Pi's USB (preferred for serial comms and power sharing).

## Raspberry Pi 5 Connections
- **USB Port 1**: Cable to ESP32 (Serial UART Communication & Power)
- **USB Port 2/3/4**: Optional peripherals (LiDAR, Keyboard, etc.)
- **CSI Port**: Raspberry Pi Camera Module 3
- **Audio Jack / I2S**: External Speaker/Amplifier for Voice/Sirens

## ESP32 DevKit V1 Pin Mappings

### Motor Drivers (BTS7960)
- **Left Motor L_PWM**: GPIO 25
- **Left Motor R_PWM**: GPIO 26
- **Left Motor L_EN & R_EN**: Tied to 3.3V or 5V (always enabled)
- **Right Motor L_PWM**: GPIO 27
- **Right Motor R_PWM**: GPIO 14
- **Right Motor L_EN & R_EN**: Tied to 3.3V or 5V

### Ultrasonic Sensors (HC-SR04) - *Use voltage dividers for Echo!*
- **Front Sonar Trig**: GPIO 32
- **Front Sonar Echo**: GPIO 33
- **Rear Sonar Trig**: GPIO 4
- **Rear Sonar Echo**: GPIO 5

### I2C Bus (IMU / Temp)
- **SDA**: GPIO 21
- **SCL**: GPIO 22
- **MPU6050** IMU (for tilt/fall detection)

### Thermal & Actuators
- **Cooling Fan PWM**: GPIO 18 (Mosfet driven)
- **Parcel Compartment Lock (Servo or Solenoid relay)**: GPIO 19
- **Pan/Tilt Camera Servos**: GPIO 12 (Pan), GPIO 13 (Tilt)

### Safety/Monitoring
- **Battery Voltage Monitor**: GPIO 34 (Analog In, through a voltage divider: e.g., 10k/1k to step 12V down to <3.3V)
- **Physical Emergency Stop Button**: Interrupts main power to motor drivers.

---

> **WARNING**: Never plug 12V or 5V directly into ESP32 or Raspberry Pi GPIO pins. Always use appropriate level shifters or voltage dividers (especially for the Battery voltage monitor and 5V ultrasonic echo pins).
