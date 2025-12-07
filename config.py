"""
Configuration for Smart ADR System
"""

# Demand Thresholds (kW)
DEMAND_LIMIT_HIGH = 500  # Trigger load shedding (Upper Bound)
DEMAND_LIMIT_LOW = 450   # Trigger load restoration (Lower Bound - Hysteresis)

# Control Interval (seconds)
CONTROL_LOOP_INTERVAL = 5

# Device Groups Configuration
# Priority Logic: 
# 1 = Critical (Hospital, Server Room) -> Shed Last
# 3 = Non-Critical (AC, Lighting) -> Shed First
DEVICE_GROUPS = {
    'group_a': {'priority': 3, 'description': 'AC Units - Zone A'},
    'group_b': {'priority': 2, 'description': 'Lighting - Warehouse'},
    'group_c': {'priority': 1, 'description': 'Server Room Cooling'}
}

# Modbus Connection Settings (Mock)
MODBUS_PORT = '/dev/ttyUSB0'
MODBUS_BAUDRATE = 9600
