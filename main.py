# copytight nbossard 2020

import time
import sys
import logging
from gpiozero import OutputDevice as stepper

# ----- Constansts -----

IN1 = stepper(12)
IN2 = stepper(16)
IN3 = stepper(20)
IN4 = stepper(21)
LOW_SPEED_MODE = 0
HIGH_SPEED_MODE = 1
STEPS_PER_TURN = 4000
TURNS_TO_DO = 4

# ------ Configuration ------

stepPins = [IN1,IN2,IN3,IN4] # Motor GPIO pins</p><p>
mode = HIGH_SPEED_MODE            # mode = 1: Low Speed ==> Higher Power
                           # mode = 0: High Speed ==> Lower Power
if mode:              # Low Speed ==> High Power
    seq = [[1,0,0,1], # Define step sequence as shown in manufacturers datasheet
            [1,0,0,0], 
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]]
else:                    # High Speed ==> Low Power 
    seq = [[1,0,0,0], # Define step sequence as shown in manufacturers datasheet
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]]

stepCount = len(seq)
waitTime = 0.002    # 2 miliseconds in whigh speed mode was the maximun speed got on my tests
stepDir = 1

# ----- Methods ---------

def print_and_log(message): 
    logging.info(message)
    print (message)

def init(): 
    logging.basicConfig(filename='chicken.log', level=logging.DEBUG, format='%(asctime)s — %(name)s — %(levelname)s — %(message)s')

def open():
    print_and_log("Opening")
    print_and_log("Rotating clockwise")
    stepDir = 1        # Set to 1 for clockwise,  Set to -1 for anti-clockwise
    do()

def close():
    print_and_log("Opening")
    print_and_log("Rotating anti-clockwise")
    stepDir = -1        # Set to 1 for clockwise,  Set to -1 for anti-clockwise
    do()

def do(): 
    stepCounter = 0
    stepTotal = 0
    quotient = 0
    while quotient < TURNS_TO_DO :                          # Start main loop
        stepTotal += 1
        #print_and_log("Total of stes: " + str(stepTotal))
        quotient, remainder = divmod(stepTotal,STEPS_PER_TURN) 
        if (remainder == 0):
            print_and_log("Number of turn done : " + str(quotient))
        for pin in range(0,4):
            xPin=stepPins[pin]          # Get GPIO
            if seq[stepCounter][pin]!=0:
                xPin.on()
            else:
                xPin.off()
        stepCounter += stepDir
        if (stepCounter >= stepCount):
            stepCounter = 0
        if (stepCounter < 0):
            stepCounter = stepCount+stepDir
        time.sleep(waitTime)     # Wait before moving on

init()
close()
