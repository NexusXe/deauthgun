import RPi.GPIO as GPIO
import time
import subprocess
import os
import signal


FSU = 'sudo mdk3 mon0 d'

# tell the GPIO module that we want to use the chip's numbering scheme
GPIO.setmode(GPIO.BCM)

# set GPIO16 as an input with internal pull-up resistor to hold it HIGH until it is pulled down to GND by the
# connected switch
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

running = False

while True: # who needs asyncio anyway
    if GPIO.input(16) == GPIO.LOW:  # not making an event with the GPIO library because it SUCKS and doesnt work
        if not running:  # failsafe because my code sucks
            print('Button was pushed!')
            # declare the proc variabe again and also start the process
            proc = subprocess.Popen(FSU, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            running = True
            time.sleep(0.1)
        elif running:  # print when button is pushed and process is already running
            print('The process is running.')
            time.sleep(0.1)
    elif GPIO.input(16) == GPIO.HIGH and running == True:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # kill the deauth process
        print('Process killed.')
        running = False
        time.sleep(0.1)
    elif not running:
        print('The process is not running.')
        time.sleep(0.1)
time.sleep(0.1)
