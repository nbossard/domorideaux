# copytight nbossard 2020
# coding=UTF-8

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
TURNS_TO_DO = 10

# ------ Configuration ------

stepPins = [IN1,IN2,IN3,IN4] # Motor GPIO pins</p><p>
stepDir = 1        # Set to 1 for clockwise
                           # Set to -1 for anti-clockwise
mode = HIGH_SPEED_MODE            # mode = 1: Low Speed ==> Higher Power
                           # mode = 0: High Speed ==> Lower Power
waitTime = 0.0040    # 2 miliseconds in whigh speed mode was the maximun speed got on my tests
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

# ----- Methods ---------

def print_and_log(message): 
    logging.info(message)
    print (message)

def init(): 
    logging.basicConfig(filename='rideaux.log', level=logging.DEBUG, format='%(asctime)s — %(name)s — %(levelname)s — %(message)s')

def open(parNbreTurns):
    print_and_log("Opening")
    print_and_log("Rotating clockwise")
    global stepdir
    do(parNbreTurns, 1)

def close(parNbreTurns):
    print_and_log("Opening")
    print_and_log("Rotating anti-clockwise")
    global stepdir
    do(parNbreTurns,-1)

def do(parNbreTurns, parStepDir): 
    stepCounter = 0
    stepTotal = 0
    quotient = 0
    while quotient < parNbreTurns :                          # Start main loop
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
        stepCounter += parStepDir
        if (stepCounter >= stepCount):
            stepCounter = 0
        if (stepCounter < 0):
            stepCounter = stepCount+parStepDir
        time.sleep(waitTime)     # Wait before moving on
