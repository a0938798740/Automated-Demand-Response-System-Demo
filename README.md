# Automated Demand Response System (Demo)

## Overview
This repository demonstrates the core logic of an **Automated Demand Response (ADR)** controller. The system monitors real-time power consumption from a main meter and automatically sheds peripheral loads (e.g., HVAC, Lighting) when demand exceeds a pre-set threshold to prevent penalties.

> **Note:** This is a logic demonstration. The underlying Modbus communication layer (`mbfType` and `drivers`) has been replaced with a mock implementation to protect proprietary hardware interface code.

## 🏗️ Architecture

The system is designed with a closed-loop control strategy:

1.  **Monitor**: Reads current kW demand via Modbus (Mocked).
2.  **Evaluate**: Compares current load against `DEMAND_LIMIT_HIGH` and `DEMAND_LIMIT_LOW`.
3.  **Act**:
    *   **Load Shedding**: If demand > limit, turns off device groups based on **Priority Level** (Lower priority shed first).
    *   **Restoration**: If demand < safe buffer, restores device groups (Higher priority restored first).

## 📂 Key Files

*   **`smart_adr.py`**:
    *   Contains the `SmartADR` class which implements the shedding/restoration algorithm.
    *   Includes a `ModbusManagerMock` class to simulate hardware responses for testing logic without physical devices.
*   **`config.py`**:
    *   Defines threshold values and device grouping configurations (Priority 1-3).

## 🚀 Technical Highlights

*   **Priority-Based Control**: Demonstrates a sophisticated algorithm that manages devices based on business importance rather than simple random switching.
*   **Hysteresis Loop**: Implements distinct High/Low thresholds to prevent "flapping" (rapid on/off switching) of equipment.
*   **Hardware Abstraction**: The control logic is decoupled from the specific communication protocol (Modbus RTU/TCP).

## Usage

1.  Configure thresholds in `config.py`.
2.  Run the simulation loop:
    ```
    python smart_adr.py
    ```
