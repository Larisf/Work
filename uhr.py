#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO
import time
import os
 
os.system("echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device")
time.sleep(2)
os.system("hwclock -s")
