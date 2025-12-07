import time
import logging
import config

# Mocking the external dependency to avoid including proprietary code
class ModbusManagerMock:
    """
    Mock class representing the external Modbus communication layer.
    In the production environment, this handles RS485 read/write operations.
    """
    def read_power_meter(self):
        # Simulation: Return a mock value oscillating around the limit
        import random
        base_load = 480
        noise = random.randint(-40, 40)
        return base_load + noise

    def switch_device(self, group_name, status):
        action = "ON" if status else "OFF"
        # Simulate hardware latency
        time.sleep(0.5)
        logging.info(f"[HARDWARE CTRL] Group {group_name} switched {action}")

class SmartADR:
    """
    Core Logic for Automated Demand Response (ADR).
    Monitors power usage and sheds load based on configured thresholds.
    """

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('SmartADR')
        self.driver = ModbusManagerMock()
        self.current_load = 0
        # Initialize status: True = ON, False = OFF
        self.shed_status = {group: True for group in config.DEVICE_GROUPS}

    def run(self):
        self.logger.info("Smart ADR System Started.")
        try:
            while True:
                self._control_loop()
                time.sleep(config.CONTROL_LOOP_INTERVAL)
        except KeyboardInterrupt:
            self.logger.info("System stopping...")

    def _control_loop(self):
        """Main decision-making loop."""
        # 1. Acquire Data
        self.current_load = self.driver.read_power_meter()
        self.logger.info(f"Current Load: {self.current_load} kW")

        # 2. Evaluate Logic
        if self.current_load >= config.DEMAND_LIMIT_HIGH:
            self.logger.warning("Demand Limit Exceeded! Initiating Load Shedding...")
            self._shed_load()
        elif self.current_load <= config.DEMAND_LIMIT_LOW:
            self.logger.info("Load is stable. Attempting Restoration...")
            self._restore_load()
        else:
            self.logger.info("Load within normal range. No action needed.")

    def _shed_load(self):
        """
        Iterates through device groups by priority (low to high) and turns them OFF
        until load is expected to drop.
        """
        # Sort groups by priority: 1 (High Priority) should be shed LAST.
        # So we sort descending? No, usually Priority 1 is most important.
        # Let's assume Priority 1 = Critical (Don't shed), Priority 3 = Non-critical (Shed first).
        # We shed from High Priority Number (3) down to Low Priority Number (1).
        
        sorted_groups = sorted(config.DEVICE_GROUPS.items(), key=lambda x: x[1]['priority'], reverse=True)
        
        for group_name, _ in sorted_groups:
            if self.shed_status[group_name]: # If device is currently ON
                self.logger.info(f"Shedding Group: {group_name} (Priority {config.DEVICE_GROUPS[group_name]['priority']})")
                self.driver.switch_device(group_name, False) # Turn OFF
                self.shed_status[group_name] = False
                break # Shed one group at a time to prevent over-correction

    def _restore_load(self):
        """
        Restores power to devices in priority order (Critical first).
        Priority 1 (Critical) -> Priority 3 (Non-critical).
        """
        sorted_groups = sorted(config.DEVICE_GROUPS.items(), key=lambda x: x[1]['priority'])
        
        for group_name, _ in sorted_groups:
            if not self.shed_status[group_name]: # If device is currently OFF
                self.logger.info(f"Restoring Group: {group_name} (Priority {config.DEVICE_GROUPS[group_name]['priority']})")
                self.driver.switch_device(group_name, True) # Turn ON
                self.shed_status[group_name] = True
                break

if __name__ == "__main__":
    app = SmartADR()
    app.run()
