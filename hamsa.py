import serial
import time
import configparser

class HamsaHand:
    def __init__(self, config_path="hamsa.config", port="/dev/ttyUSB0", baudrate=115200):
        self.ser = serial.Serial(port, 1000000, timeout=1)
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Build lookup tables for each motion
        self.motions = {}
        for section in self.config.sections():
            params = {k: int(v) for k, v in self.config[section].items() if k != 'id'}
            params['id'] = int(self.config[section]['id'])
            self.motions[section] = params

    def _send_servo_command(self, servo_id, position, duration):
        """Send a position command to a single servo."""
        cmd = f"#{servo_id}P{int(position)}T{int(duration)}\r\n"
	print("Sending command:", cmd)
        self.ser.write(cmd.encode())
        time.sleep(0.02)

    def _map_ratio(self, ratio, min_val, max_val):
        """Map ratio (0–1) to servo position."""
        return min_val + ratio * (max_val - min_val)

    # --- Curling ---
    def curl_thumb(self, ratio, duration): self._curl("thumb curl", ratio, duration)
    def curl_index(self, ratio, duration): self._curl("index curl", ratio, duration)
    def curl_middle(self, ratio, duration): self._curl("middle curl", ratio, duration)
    def curl_ring(self, ratio, duration): self._curl("ring curl", ratio, duration)
    def curl_pinky(self, ratio, duration): self._curl("pinky curl", ratio, duration)

    def _curl(self, finger, ratio, duration):
        data = self.motions[finger]
        servo_id, pos_in, pos_out = data["id"], data["in"], data["out"]
        position = self._map_ratio(ratio, pos_in, pos_out)
        self._send_servo_command(servo_id, position, duration)

    # --- Wiggling ---
    def wiggle_thumb(self, ratio, duration): self._wiggle("thumb wiggle", ratio, duration)
    def wiggle_index(self, ratio, duration): self._wiggle("index wiggle", ratio, duration)
    def wiggle_middle(self, ratio, duration): self._wiggle("middle wiggle", ratio, duration)
    def wiggle_ring(self, ratio, duration): self._wiggle("ring wiggle", ratio, duration)
    def wiggle_pinky(self, ratio, duration): self._wiggle("pinky wiggle", ratio, duration)

    def _wiggle(self, finger, ratio, duration):
        data = self.motions[finger]
        servo_id, pos_left, pos_right = data["id"], data["left"], data["right"]
        position = self._map_ratio(ratio, pos_left, pos_right)
        self._send_servo_command(servo_id, position, duration)

