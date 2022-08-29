#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import smbus

GPIO.setmode(GPIO.BCM) #set GPIO layout to the Broadcom GPIO numbers convention
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.out)

bus = smbus.SMBus(1)
data = bus.read_i2c_block_data(0x48, 0) #0x48 is the TMP102s default I²C address
msb = data[0] #store most and least significant bit in order
lsb = data[1]

output = (((msb << 8) | lsb) >> 4) * 0.0625 #convert to decimal

if output > 20:
  GPIO.output(26, GPIO.HIGH)

else:
  GPIO.output(26, GPIO.LOW)
