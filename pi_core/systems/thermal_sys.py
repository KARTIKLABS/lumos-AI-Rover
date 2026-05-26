import subprocess
import time
import logging
from core.comms_esp32 import ESP32Comms

class ThermalSystem:
    def __init__(self, comms: ESP32Comms, config: dict):
        self.comms = comms
        self.limit = config.get("cpu_temp_limit", 75.0)
        self.current_temp = 0.0

    def get_cpu_temp(self) -> float:
        try:
            # Requires vcgencmd on Raspberry Pi
            result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            # Output format: temp=45.0'C
            output = result.stdout
            if "temp=" in output:
                temp_str = output.replace("temp=", "").replace("'C", "").strip()
                return float(temp_str)
        except Exception as e:
            logging.debug(f"Could not read Pi temp (are you running on a Pi?): {e}")
        return 40.0 # Mock temperature

    def update(self):
        self.current_temp = self.get_cpu_temp()
        self.comms.send_pi_temp(self.current_temp)
        
        if self.current_temp >= self.limit:
            logging.warning(f"THERMAL THROTTLING/WARNING! CPU Temp: {self.current_temp}C")
            # You could hook into state_manager here to stop driving if it gets too hot
