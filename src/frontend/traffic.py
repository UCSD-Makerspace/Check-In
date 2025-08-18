import serial
import serial.tools.list_ports as list_ports
import time


class TrafficLight:
    def __init__(self, addr=None, baud=115200):
        self.ser = None

        if addr:
            self.ser = serial.Serial(addr, baud)
            self.ser.reset_input_buffer()

    def set_off(self):
        if self.ser:
            self.ser.write(b"off\n")

    def set_red(self):
        if self.ser:
            self.ser.write(b"red\n")

    def set_yellow(self):
        if self.ser:
            self.ser.write(b"yellow\n")

    def set_green(self):
        if self.ser:
            self.ser.write(b"green\n")


if __name__ == "__main__":
    ports = list(serial.tools.list_ports.comports())
    traffic_light_vid = 6790

    for p in ports:
        if p.vid == traffic_light_vid:
            break

    light = TrafficLight(p.device)
    while True:
        light.set_off()
        time.sleep(1)
        light.set_red()
        time.sleep(1)
        light.set_green()
        time.sleep(1)
        light.set_yellow()
        time.sleep(1)
