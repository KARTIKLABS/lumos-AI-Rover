import serial
import time
import threading
import logging

class ESP32Comms:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connected = False
        
        self.telemetry = {
            "front_cm": -1,
            "rear_cm": -1,
            "vBatt": 0.0
        }
        
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.connected = True
            logging.info(f"Connected to ESP32 on {self.port}")
            self.start_listening()
            return True
        except serial.SerialException as e:
            logging.error(f"Failed to connect to ESP32: {e}")
            self.connected = False
            return False

    def start_listening(self):
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def _listen_loop(self):
        while self._running and self.connected:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith("<") and line.endswith(">"):
                        self._parse_telemetry(line[1:-1])
            except Exception as e:
                logging.error(f"Serial read error: {e}")
                self.connected = False
            time.sleep(0.01)

    def _parse_telemetry(self, data):
        parts = data.split(",")
        if len(parts) >= 4 and parts[0] == "TELEMETRY":
            with self._lock:
                try:
                    self.telemetry["front_cm"] = float(parts[1])
                    self.telemetry["rear_cm"] = float(parts[2])
                    self.telemetry["vBatt"] = float(parts[3])
                except ValueError:
                    pass

    def send_command(self, cmd_str):
        if self.connected and self.ser:
            try:
                msg = f"<{cmd_str}>\n"
                self.ser.write(msg.encode('utf-8'))
            except Exception as e:
                logging.error(f"Serial write error: {e}")
                self.connected = False

    def drive(self, left_pwm, right_pwm):
        self.send_command(f"DRIVE,{left_pwm},{right_pwm}")

    def set_lock(self, locked: bool):
        val = 1 if locked else 0
        self.send_command(f"LOCK,{val}")

    def send_pi_temp(self, temp: float):
        self.send_command(f"TEMP,{temp:.1f}")

    def get_telemetry(self):
        with self._lock:
            return self.telemetry.copy()

    def disconnect(self):
        self._running = False
        if self.ser:
            self.ser.close()
        self.connected = False
