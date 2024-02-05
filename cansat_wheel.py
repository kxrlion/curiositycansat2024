import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
motorA_in1 = 17
motorA_in2 = 18

motorB_in1 = 22
motorB_in2 = 23

GPIO.setup(motorA_in1, GPIO.OUT)
GPIO.setup(motorA_in2, GPIO.OUT)
GPIO.setup(motorB_in1, GPIO.OUT)
GPIO.setup(motorB_in2, GPIO.OUT)

def move_forward():
    GPIO.output(motorA_in1, GPIO.HIGH)
    GPIO.output(motorA_in2, GPIO.LOW)
    GPIO.output(motorB_in1, GPIO.HIGH)
    GPIO.output(motorB_in2, GPIO.LOW)

def move_backward():
    GPIO.output(motorA_in1, GPIO.LOW)
    GPIO.output(motorA_in2, GPIO.HIGH)
    GPIO.output(motorB_in1, GPIO.LOW)
    GPIO.output(motorB_in2, GPIO.HIGH)

try:
    move_forward()
    time.sleep(2)

    move_backward()
    time.sleep(2)

finally:
    GPIO.cleanup()
