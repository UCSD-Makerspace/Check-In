import serial
import time
import argparse


class TrafficLight:
    def __init__(self, addr, baud=115200):
        self.ser = serial.Serial(addr, baud)
        self.ser.reset_input_buffer()

    def set_off(self):
        self.ser.write(b"off\n")

    def set_red(self):
        self.ser.write(b"red\n")

    def set_yellow(self):
        self.ser.write(b"yellow\n")

    def set_green(self):
        self.ser.write(b"green\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Traffic Light Debug",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        default="0",
        choices={"0", "1"},
        help="USB id to use (0 or 1)",
    )

    args = parser.parse_args()
    config = vars(args)

    usb_id = f"/dev/ttyUSB{config['i']}"

    light = TrafficLight(usb_id)
    while True:
        light.set_off()
        time.sleep(1)
        light.set_red()
        time.sleep(1)
        light.set_green()
        time.sleep(1)
        light.set_yellow()
        time.sleep(1)
