"""
uart_comm.py — WRO 2026 Future Engineers — CHUISA ARCITEP
=======================================================
Serial (UART) communication between Raspberry Pi and Arduino Nano.

Protocol (115200 baud, newline-terminated):
  Pi → Arduino:  "S<steering>,<speed>\n"
    steering: int -100 (full left) to +100 (full right)
    speed:    int -100 (full reverse) to +100 (full forward)

  Arduino → Pi:  "T<tof_l>,<tof_f>,<tof_r>,<yaw>,<enc>\n"
    tof_l/f/r: int, distance in mm (40–1300mm for short mode)
    yaw:       float, integrated heading in degrees
    enc:       int, total encoder pulses since start
  
  Arduino → Pi (events):
    "READY\n" — Arduino finished setup
    "START\n" — Start button was pressed (Rule 9.11)

Usage:
    comm = ArduinoComm(port="/dev/ttyUSB0")
    comm.wait_for_start()
    comm.set_steering(0.5)   # 50% right
    comm.set_speed(0.4)      # 40% forward
    sensors = comm.get_sensors()
    comm.stop_vehicle()
"""

import serial
import threading
import time
from typing import Optional, Dict


class ArduinoComm:
    """
    Thread-safe serial communication with Arduino Nano.
    Reads sensor data in background thread, exposes via get_sensors().
    Sends steering/speed commands on demand.
    """

    def __init__(self, port: str = "/dev/ttyUSB0", baud: int = 115200):
        self._port   = port
        self._baud   = baud
        self._ser: Optional[serial.Serial] = None
        self._sensors: Dict[str, float] = {
            "tof_left":  9999,
            "tof_front": 9999,
            "tof_right": 9999,
            "yaw":       0.0,
            "encoder":   0,
        }
        self._lock    = threading.Lock()
        self._running = False
        self._reader_thread: Optional[threading.Thread] = None

        self._connect()
        self._start_reader()

    # ── Public API ────────────────────────────────────────────────────────────

    def wait_for_start(self):
        """
        Block until Arduino sends "START" (start button pressed).
        Rule 9.11: Vehicle must wait in standby state for start button.
        Rule 9.10: Only ONE start button is permitted.
        """
        print("[COMM] Waiting for start button...")
        while self._running:
            try:
                if self._ser and self._ser.in_waiting:
                    line = self._ser.readline().decode("utf-8", errors="ignore").strip()
                    if line == "START":
                        print("[COMM] Start button pressed. GO!")
                        return
            except serial.SerialException:
                pass
            time.sleep(0.01)

    def get_sensors(self) -> Dict[str, float]:
        """Thread-safe access to latest sensor readings."""
        with self._lock:
            return self._sensors.copy()

    def set_steering(self, value: float):
        """
        Set steering. value: -1.0 (full left) to +1.0 (full right).
        Maps to -100 to +100 for the Arduino protocol.
        """
        v = max(-1.0, min(1.0, value))
        self._send(f"S{int(v * 100)},{self._last_speed}\n")

    def set_speed(self, value: float):
        """
        Set drive speed. value: -1.0 (full reverse) to +1.0 (full forward), 0=stop.
        """
        v = max(-1.0, min(1.0, value))
        self._last_speed = int(v * 100)
        self._send(f"S{self._last_steering},{self._last_speed}\n")

    def stop_vehicle(self):
        """Emergency stop: zero all outputs."""
        self._last_steering = 0
        self._last_speed    = 0
        self._send("S0,0\n")

    def close(self):
        """Cleanly close connection."""
        self.stop_vehicle()
        self._running = False
        if self._reader_thread:
            self._reader_thread.join(timeout=2.0)
        if self._ser and self._ser.is_open:
            self._ser.close()

    # ── Internal ──────────────────────────────────────────────────────────────

    _last_steering = 0
    _last_speed    = 0

    def _connect(self):
        """Open serial port. Waits 2s for Arduino to reboot after connection."""
        print(f"[COMM] Connecting to Arduino on {self._port} @ {self._baud} baud...")
        self._ser = serial.Serial(
            self._port, self._baud, timeout=0.1
        )
        time.sleep(2.0)  # Arduino resets on USB connect; wait for it to boot
        self._ser.reset_input_buffer()
        self._running = True
        print("[COMM] Serial connected.")

    def _start_reader(self):
        """Start background thread that continuously reads sensor lines."""
        self._reader_thread = threading.Thread(
            target=self._read_loop, daemon=True, name="uart-reader"
        )
        self._reader_thread.start()

    def _read_loop(self):
        """Background reader: parse 'T...' lines into sensor dict."""
        while self._running:
            try:
                if self._ser and self._ser.in_waiting:
                    raw  = self._ser.readline()
                    line = raw.decode("utf-8", errors="ignore").strip()
                    if line.startswith("T"):
                        self._parse_sensor_line(line)
            except serial.SerialException as e:
                print(f"[COMM] Serial error: {e}")
                time.sleep(0.1)
            except Exception:
                pass

    def _parse_sensor_line(self, line: str):
        """
        Parse: "T<tof_l>,<tof_f>,<tof_r>,<yaw>,<enc>"
        Updates internal sensor dict thread-safely.
        """
        try:
            parts = line[1:].split(",")
            if len(parts) != 5:
                return
            sensors = {
                "tof_left":  int(parts[0]),
                "tof_front": int(parts[1]),
                "tof_right": int(parts[2]),
                "yaw":       float(parts[3]),
                "encoder":   int(parts[4]),
            }
            with self._lock:
                self._sensors = sensors
        except (ValueError, IndexError):
            pass

    def _send(self, message: str):
        """Send a message to Arduino. No-op if connection is unavailable."""
        try:
            if self._ser and self._ser.is_open:
                self._ser.write(message.encode("utf-8"))
        except serial.SerialException:
            pass
