import time
import yaml
import logging
from core.state_manager import StateManager, RoverState
from core.comms_esp32 import ESP32Comms
from systems.thermal_sys import ThermalSystem
from systems.navigation import NavigationSystem
from hardware.camera import CameraManager
from hardware.audio_sys import AudioSystem
from ai_pipeline.vision import VisionPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error("config.yaml not found! Using defaults.")
        return {}

def main():
    config = load_config()
    
    state_mgr = StateManager()
    state_mgr.set_state(RoverState.IDLE)
    
    # Initialize Comms
    serial_cfg = config.get("serial", {})
    comms = ESP32Comms(
        port=serial_cfg.get("port", "/dev/ttyUSB0"),
        baudrate=serial_cfg.get("baudrate", 115200)
    )
    comms.connect()
    
    # Initialize Systems
    thermal = ThermalSystem(comms, config.get("thermal", {}))
    nav = NavigationSystem(comms, state_mgr, config.get("navigation", {}))
    cam = CameraManager(config.get("camera", {}))
    audio = AudioSystem()
    vision = VisionPipeline(config.get("ai", {}))
    
    cam.start()
    audio.speak("System initialized. Campus rover ready.")
    
    try:
        while True:
            # 1. Thermal Management Update
            thermal.update()
            
            # 2. Navigation & Telemetry Update
            nav.process_telemetry()
            
            # 3. Vision Processing (if in an autonomous state)
            current_state = state_mgr.get_state()
            if current_state in [RoverState.PATROL, RoverState.DELIVERY]:
                frame = cam.get_frame()
                if frame is not None:
                    proc_frame, detections = vision.process_frame(frame)
                    # Look for humans
                    for det in detections:
                        if det["class"] == "person":
                            audio.speak("Hello there.")
                            state_mgr.set_state(RoverState.IDLE) # Pause to greet
                            break
            
            time.sleep(0.1) # 10Hz Main Loop
            
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        cam.stop()
        comms.disconnect()

if __name__ == "__main__":
    main()
