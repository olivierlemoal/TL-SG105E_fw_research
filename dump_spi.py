#! /usr/bin/env python

import binascii
from time import sleep

import serial
import io


SIZE = 0x40 * 600
OUTPUT = "SPI.dmp"

def read_serial(output=None):
    raw = b""
    sleep(.1)
    while True:
        res = sio.readline().strip()
        if not res or res == b'>' :
            break
        print(res)
        if res[0] == "[":
            raw += binascii.unhexlify(res[9:56].replace(" ", ""))
    if output:
        output.write(raw)

    ser.reset_output_buffer()


def write_serial(cmd):
    ser.write(cmd)
 #   ser.reset_input_buffer()


def dump(output):
    for i in range(0x106800, 0xffffff, SIZE):
        print("r {}".format(hex(i)))
        write_serial(b"r ")
        sleep(0.1)
        write_serial("{}".format(hex(i)).encode())
        sleep(0.1)
        write_serial(" {}\n".format(hex(SIZE)).encode())
        read_serial(output)


ser = serial.Serial('/dev/buspirate', 115200,
                   bytesize = serial.EIGHTBITS,
                   parity = serial.PARITY_NONE,
                   stopbits = serial.STOPBITS_ONE, timeout=.5)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
while ser.inWaiting():
    print(ser.read(ser.inWaiting()))
with open(OUTPUT, "wb+") as output:
    dump(output)
ser.close()


