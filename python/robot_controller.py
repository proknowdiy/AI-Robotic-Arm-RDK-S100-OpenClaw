import serial
import json
import time


class RobotController:

    def __init__(
        self,
        port="/dev/ttyACM0",
        baudrate=115200
    ):

        self.ser = serial.Serial(
            port,
            baudrate,
            timeout=1
        )

        time.sleep(2)

    # ---------------------------------

    def send(self, data):

        self.ser.reset_input_buffer()

        self.ser.write(
            (json.dumps(data) + "\n").encode()
        )

        while True:

            line = (
                self.ser.readline()
                .decode(errors="ignore")
                .strip()
            )

            if not line:
                continue

            print("ESP32:", line)

            # Success

            if line == "Done":
                return True

            # Error

            if line.startswith("ERROR:"):
                return False

    # ---------------------------------

    def go_home(self):

        return self.send({
            "action": "home"
        })

    # ---------------------------------

    def pick_cube(self, slot):

        return self.send({
            "action": "pick_cube",
            "source": slot
        })

    # ---------------------------------

    def drop_cube(self, side):

        return self.send({
            "action": "drop_cube",
            "destination": side
        })

    # ---------------------------------

    def move_cube(self, slot, side):

        return self.send({
            "action": "move_cube",
            "source": slot,
            "destination": side
        })
        
    # ----------------------------------

    def get_status(self):

        self.ser.reset_input_buffer()

        self.ser.write(
            b'{"action":"status"}\n'
        )

        while True:

            line = (
                self.ser.readline()
                .decode(errors="ignore")
                .strip()
            )

            if not line:
                continue

            try:

                return json.loads(line)

            except:

                pass    
