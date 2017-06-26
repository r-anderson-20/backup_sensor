#!/usr/bin/env python

import RPi.GPIO
import subprocess

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(3, RPi.GPIO.IN)
RPi.GPIO.wait_for_edge(3, RPi.GPIO.FALLING)

subprocess.call(['shutdown', '-h', 'now'], shell=False)

