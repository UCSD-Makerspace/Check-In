import serial
import time


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
    light = TrafficLight("/dev/tty.usbserial-1310")
    while True:
        light.set_off()
        time.sleep(1)
        light.set_red()
        time.sleep(1)
        light.set_green()
        time.sleep(1)
        light.set_yellow()
        time.sleep(1)
