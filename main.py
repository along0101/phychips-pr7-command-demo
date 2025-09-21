import serial
import time


# RCP (Reader Control Protocol)
# Command: preamble(0xCC) + header(2 Bytes) + payload length(1-2 Bytes) + payload(N Bytes) + checksum(1 Byte)
class SerialReader:
    def __init__(self, port="/dev/ttyUSB0", baudrate=460800):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)

    # 从头到尾全部相加，如果大于0xff，取头尾字节相加，直到全部处理完毕。然后取反码。最后如果遇到0xcc或者0xaa，减1.例如0xCC变成0xCB，0xAA变成0xA9
    def __checksum(self, buffer: bytearray):
        val = 0x00
        for byte in buffer:
            # val += byte
            # val += (val >> 8)
            # val &= 0xFF
            val = val + byte
            if val > 0xFF:
                val = (val >> 8 & 0xFF) + (val & 0xFF)
        # print("origin:", hex(val))
        # 取反码
        val = ~val & 0xFF
        if val in [0xCC, 0xAA]:
            val -= 1
        return val

    def test(self):
        val = self.__checksum(bytearray([0xCC, 0x11, 0x60, 0x01, 0x30]))
        print(hex(val), val == 0x90)

    def info(self):
        header = 0x101
        # product code: 0x01, serial number: 0x02, firmware version: 0x03, max power: 0x07
        command = [0xCC, header >> 8 & 0xFF, header & 0xFF, 0x01, 0x02]
        checksum = self.__checksum(bytearray(command))
        command.append(checksum)
        self.ser.write(bytearray(command))
        time.sleep(0.08)  # 延迟，准备数据
        resp = self.ser.read_all()
        # resp = self.ser.read(100)
        print(resp)
        # print("checksum:", hex(resp[-1]), hex(self.__checksum(resp[0:-1])))
        if resp and len(resp) > 5 and resp[-1] == self.__checksum(resp[0:-1]):
            print("payload length:", hex(resp[3]))
            print("error code:", resp[4])
            # print("payload:", resp[5 : (5 + 16 - 1)])
            print("payload:", resp[5:-1])
            print("id:", hex(resp[5]))
            print("data length:", hex(resp[6]))
            print("data:", resp[7:-1].decode())

    def region(self):
        header = 0x119
        command = [0xCC, header >> 8 & 0xFF, header & 0xFF, 0x00]
        checksum = self.__checksum(bytearray(command))
        command.append(checksum)
        self.ser.write(bytearray(command))
        time.sleep(0.08)  # 延迟，准备数据
        resp = self.ser.read_all()
        print(resp)
        # print("checksum:", hex(resp[-1]), hex(self.__checksum(resp[0:-1])))
        if resp and len(resp) > 5 and resp[-1] == self.__checksum(resp[0:-1]):
            print("payload length:", hex(resp[3]))
            print("error code:", resp[4])
            print("payload:", resp[5:-1])

    def set_region(self, code: int):
        header = 0x01 << 12 | 0x119
        command = [0xCC, header >> 8 & 0xFF, header & 0xFF, 0x01, code & 0xFF]
        checksum = self.__checksum(bytearray(command))
        command.append(checksum)
        self.ser.write(bytearray(command))
        time.sleep(0.08)  # 延迟，准备数据
        resp = self.ser.read_all()
        print(resp)
        # print("checksum:", hex(resp[-1]), hex(self.__checksum(resp[0:-1])))
        if resp and len(resp) > 5 and resp[-1] == self.__checksum(resp[0:-1]):
            print("payload length:", hex(resp[3]))
            print("error code:", resp[4])
            print("payload:", resp[5:-1])

    def mode(self):
        header = 0x00 << 12 | 0x155
        command = [0xCC, header >> 8 & 0xFF, header & 0xFF, 0x00]
        checksum = self.__checksum(bytearray(command))
        command.append(checksum)
        self.ser.write(bytearray(command))
        time.sleep(0.08)  # 延迟，准备数据
        resp = self.ser.read_all()
        print(resp)
        # print("checksum:", hex(resp[-1]), hex(self.__checksum(resp[0:-1])))
        if resp and len(resp) > 5 and resp[-1] == self.__checksum(resp[0:-1]):
            print("payload length:", hex(resp[3]))
            print("error code:", resp[4])
            print("payload:", resp[5:-1], hex(ord(resp[5:-1])))

    def access_mode(self):
        header = 0x00 << 12 | 0x170
        command = [0xCC, header >> 8 & 0xFF, header & 0xFF, 0x00]
        checksum = self.__checksum(bytearray(command))
        command.append(checksum)
        self.ser.write(bytearray(command))
        time.sleep(0.08)  # 延迟，准备数据
        resp = self.ser.read_all()
        print(resp)
        # print("checksum:", hex(resp[-1]), hex(self.__checksum(resp[0:-1])))
        if resp and len(resp) > 5 and resp[-1] == self.__checksum(resp[0:-1]):
            print("payload length:", hex(resp[3]))
            print("error code:", resp[4])
            print("payload:", resp[5:-1], hex(ord(resp[5:-1])))

    def read_mem(self, bank: int):
        header = 0x01 << 12 | 0x220
        command = [0xCC, header >> 8 & 0xFF, header & 0xFF, 0x01, bank & 0xFF]
        checksum = self.__checksum(bytearray(command))
        command.append(checksum)
        self.ser.write(bytearray(command))
        time.sleep(0.08)  # 延迟，准备数据
        resp = self.ser.read_all()
        print(resp)
        # print("checksum:", hex(resp[-1]), hex(self.__checksum(resp[0:-1])))
        if resp and len(resp) > 5 and resp[-1] == self.__checksum(resp[0:-1]):
            print("payload length:", hex(resp[3]))
            print("error code:", resp[4])
            print("payload:", resp[5:-1])

    def connect(self):
        if self.ser is None:
            self.ser = serial.Serial(self.port, self.baudrate)
        else:
            self.ser.open()

    def disconnect(self):
        self.ser.close()
        self.ser = None


if __name__ == "__main__":
    # 8N1
    reader = SerialReader("/dev/tty.usbserial-0001")
    # reader.test()
    # reader.info()
    # reader.set_region(0x07)
    # time.sleep(0.1)
    # reader.region()
    # reader.mode()
    # reader.access_mode()
    reader.read_mem(0x00)
    reader.disconnect()
