import RPi.GPIO
import time
import subprocess
import os
import signal
import pygame
import sys
import test1

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(5, RPi.GPIO.IN)

state = 0
pin = 5

while True:
    input_state = RPi.GPIO.input(pin)
    if input_state == False and state == 0:
        #p = subprocess.Popen("python /home/pi/workspace/backup_sensor/backup_cam.py", shell=True, preexec_fn=os.setsid)
        test1.launch_cam()
        #time.sleep(0.1)
        state = 1
        while RPi.GPIO.input(pin) == 0:
            time.sleep(0.1)
    input_state = RPi.GPIO.input(pin)
    if input_state == False and state == 1:
        state = 0
        pygame.display.quit()
        pygame.quit()
        #backup_cam.quit_prog()
        sys.exit()
        os.killpg(p.pid, signal.SIGTERM)
        #time.sleep(0.1)
        while RPi.GPIO.input(pin) == 0:
            time.sleep(0.1)
        
