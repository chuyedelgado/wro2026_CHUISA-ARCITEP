#!/usr/bin/env python3
"""
main.py — WRO 2026 Future Engineers — CHUISA ARCITEP
==================================================
Entry point for the Raspberry Pi autonomous driving system.

System architecture:
    main.py
    ├── ArduinoComm   → serial thread (reads sensors, writes commands)
    ├── VisionSystem  → camera thread (captures + processes frames at 30fps)
    └── StateMachine  → main control loop (runs at ~50Hz)

Competition startup sequence (Rules 9.6–9.14):
    1. Vehicle is placed in start zone, POWERED OFF (Rule 9.6)
    2. Power switch ON → this program starts automatically (via /etc/rc.local)
    3. Program initializes all subsystems
    4. Vehicle WAITS in standby for start button press (Rule 9.11)
    5. Start button pressed → StateMachine.run() begins the autonomous run
    6. Vehicle operates autonomously until STOP state (3 laps complete)

Configuration:
    All tunable parameters are in config.py.
    No runtime data input is permitted during competition (Rule 9.9).
"""

import sys
import time
import signal

from config import Config
from vision import VisionSystem
from state_machine import StateMachine
from uart_comm import ArduinoComm


def main():
    print("=" * 60)
    print(" WRO 2026 Future Engineers — [TEAM NAME]")
    print(f" Challenge: {Config.CHALLENGE}")
    print("=" * 60)

    config = Config()
    comm   = None
    vision = None

    try:
        # Initialize communication with Arduino
        comm = ArduinoComm(port=config.ARDUINO_PORT, baud=config.BAUD_RATE)

        # Initialize vision system (camera setup, does not start capture yet)
        vision = VisionSystem(config)

        # Initialize state machine
        sm = StateMachine(config, vision, comm)

        # WAIT for start button (Rule 9.11: single start button, standby state)
        # The start button is on the Arduino. ArduinoComm.wait_for_start()
        # blocks until the Arduino sends "START" over serial.
        comm.wait_for_start()

        # Run the autonomous program
        sm.run()

    except KeyboardInterrupt:
        print("\n[MAIN] Interrupted by user.")
    except Exception as e:
        print(f"\n[MAIN] FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always stop vehicle on exit
        if comm:
            comm.stop_vehicle()
            comm.close()
        if vision:
            vision.stop()
        print("[MAIN] Shutdown complete.")


def _handle_signal(sig, frame):
    """Handle SIGTERM/SIGINT gracefully."""
    print(f"\n[MAIN] Signal {sig} received. Shutting down.")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT,  _handle_signal)
    main()
