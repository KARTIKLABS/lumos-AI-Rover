# Setup and Installation Guide

## 1. Raspberry Pi 5 Setup

### System Requirements
- Raspberry Pi OS (64-bit, Bookworm recommended)
- Python 3.11+
- Internet connection for initial setup

### Installation
1. Clone this repository to your Pi.
2. Make the installation script executable and run it:
   ```bash
   cd rover_stack/scripts
   chmod +x install_dependencies.sh
   ./install_dependencies.sh
   ```
3. Update the `pi_core/config.yaml` file if you have different serial ports or camera indexes.

### Running the Pi Logic
To start the core stack (Dashboard + AI + Navigation):
```bash
cd rover_stack/pi_core
python3 main.py
```
*Note: We recommend setting this up as a systemd service using `start_rover.sh` for auto-boot.*

## 2. ESP32 Firmware Setup

We recommend using **PlatformIO** via VSCode to upload the firmware.

1. Install VSCode and the PlatformIO extension.
2. Open the `rover_stack/esp32_firmware` folder in VSCode.
3. Connect your ESP32 via USB.
4. Click the "Upload" arrow in the bottom PlatformIO toolbar.

Alternatively, you can copy the contents of `src/` into the Arduino IDE, rename `main.cpp` to `esp32_firmware.ino`, and install the required libraries manually (PID, ESP32Servo, etc.).

## 3. Web Dashboard
Once the Pi is running, connect to the same Wi-Fi network as the Pi.
Open a browser and navigate to:
`http://<RASPBERRY_PI_IP>:8000`

Default Port is 8000. You should see the live camera feed and telemetry data.
