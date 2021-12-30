#Python progam to run a UHF RFID m5stack reader
#!/usr/bin/env python

import time
import datetime
import serial
import binascii
import sys

# Commands already implemented
CMD_GET_HARDWARE_VERSION = b'\xBB\x00\x03\x00\x01\x00\x04\x7E'
CMD_GET_SOFTWARE_VERSION = b'\xBB\x00\x03\x00\x01\x01\x05\x7E'
CMD_GET_MANUFACTURERS    = b"\xBB\x00\x03\x00\x01\x02\x06\x7E"
CMD_GET_SINGLE_POOLING   = b'\xBB\x00\x22\x00\x00\x22\x7E'
CMD_TERMINATOR           = b'\x0A\x0D' # b'\n\r'
CNT_GET_SINGLE_POOLING    = b"\xBB\x02\x22\x00\x11"

_antennaGain    =   3;
_coupling       = -20;

def readString():
  buffer = []
  while (ser.in_waiting > 0):
    read_byte = ser.read().decode("ascii", "ignore")
    buffer.append(read_byte)

  ser.flush()
  return "".join(buffer)

def readHex():
  buffer = []
  while (ser.in_waiting > 0):
    read_byte = ser.read().hex()
    buffer.append(read_byte)

  ser.flush()
  return "".join(buffer)

try:
  #ser = serial.Serial("/dev/ttyS0", 115200)
  ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None
  )

  ser.flush()
  ser.isOpen() 
  print ("port is opened!")

except IOError:
  ser.close()
  ser.open()
  print ("port was already open, was closed and opened again!")

try:
  ser.write(CMD_GET_MANUFACTURERS)
  ser.write(CMD_TERMINATOR)
  time.sleep(0.5)
  buffer = readString();
  print(buffer)

  while 1: 

    ser.write(CMD_GET_SINGLE_POOLING)
    ser.write(CMD_TERMINATOR)
    time.sleep(0.5)
    buffer = readHex();

    # verify output is valid - card found
    if buffer.startswith(CNT_GET_SINGLE_POOLING.hex()):
        rssi = int(buffer[10:12], 16)
        rssi =  -( (-rssi) & 0xFF )

        pc = buffer[12:16]
        epc = buffer[16:40]
        crc = buffer[40:44]
        print('PC: {0} EPC: {1} RSSI: {2} dBm'.format(pc, epc, rssi))

finally:
  print("closing serial port")
  ser.flush()
  ser.close()
