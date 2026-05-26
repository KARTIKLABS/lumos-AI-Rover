from enum import Enum
import threading

class RoverState(Enum):
    IDLE = "IDLE"
    MANUAL = "MANUAL"
    PATROL = "PATROL"
    EMERGENCY = "EMERGENCY"
    DELIVERY = "DELIVERY"

class StateManager:
    def __init__(self):
        self._state = RoverState.IDLE
        self._lock = threading.Lock()

    def set_state(self, new_state: RoverState):
        with self._lock:
            self._state = new_state
            
    def get_state(self) -> RoverState:
        with self._lock:
            return self._state

    def is_emergency(self):
        return self.get_state() == RoverState.EMERGENCY
