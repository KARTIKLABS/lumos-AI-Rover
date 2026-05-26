import logging
from core.state_manager import StateManager, RoverState
from core.comms_esp32 import ESP32Comms

class NavigationSystem:
    def __init__(self, comms: ESP32Comms, state: StateManager, config: dict):
        self.comms = comms
        self.state = state
        self.max_speed = config.get("max_speed_pwm", 200)
        self.turn_speed = config.get("turn_speed_pwm", 150)
        self.obstacle_threshold = config.get("obstacle_distance_cm", 40)

    def process_telemetry(self):
        # Read sonar and handle emergency stop if in autonomous or semi-auto mode
        current_state = self.state.get_state()
        if current_state in [RoverState.PATROL, RoverState.DELIVERY]:
            telemetry = self.comms.get_telemetry()
            front = telemetry.get("front_cm", -1)
            
            if front != -1 and front < self.obstacle_threshold:
                logging.warning(f"Obstacle detected at {front}cm. Halting.")
                self.comms.drive(0, 0)
                # Later: Add obstacle avoidance logic (turn left/right until clear)

    def manual_drive(self, command: str):
        # command: "forward", "backward", "left", "right", "stop"
        if self.state.get_state() != RoverState.MANUAL:
            return # Ignore manual commands if not in manual mode
            
        if command == "forward":
            self.comms.drive(self.max_speed, self.max_speed)
        elif command == "backward":
            self.comms.drive(-self.max_speed, -self.max_speed)
        elif command == "left":
            self.comms.drive(-self.turn_speed, self.turn_speed)
        elif command == "right":
            self.comms.drive(self.turn_speed, -self.turn_speed)
        else:
            self.comms.drive(0, 0)
