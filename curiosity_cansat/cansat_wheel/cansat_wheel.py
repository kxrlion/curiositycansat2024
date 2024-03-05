from xml.etree.ElementTree import PI
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
#left motor
motorA_in1 = 5
motorA_in2 = 6

#right motor
motorB_in1 = 23
motorB_in2 = 24

GPIO.setup(motorA_in1, GPIO.OUT)
GPIO.setup(motorA_in2, GPIO.OUT)
GPIO.setup(motorB_in1, GPIO.OUT)
GPIO.setup(motorB_in2, GPIO.OUT)
angle = 285
spin = 360/angle
r=3.25;

def backward(m):
    #m -> liczba cm do przejechania
    #n -> ile razy ma sie obrocic kolo
    n=m/2*PI*r
    GPIO.output(motorA_in1, GPIO.LOW)
    GPIO.output(motorA_in2, GPIO.HIGH)
    GPIO.output(motorB_in1, GPIO.LOW)
    GPIO.output(motorB_in2, GPIO.HIGH)
    
    time.sleep(n*spin)
def forward(m):
    #m -> liczba cm do przejechania
    #n -> ile razy ma sie obrocic kolo
    n=m/2*PI*r
    GPIO.output(motorA_in1, GPIO.HIGH)
    GPIO.output(motorA_in2, GPIO.LOW)
    GPIO.output(motorB_in1, GPIO.HIGH)
    GPIO.output(motorB_in2, GPIO.LOW)
    time.sleep(n*spin)
def right(a):
    #a -> a podane w radianach / PI
    GPIO.output(motorA_in1, GPIO.HIGH)
    GPIO.output(motorA_in2, GPIO.LOW)
    GPIO.output(motorB_in1, GPIO.LOW)
    GPIO.output(motorB_in2, GPIO.HIGH)
    time.sleep(a*spin)
def left(a):
    #a -> a podane w radianach / PI
    GPIO.output(motorA_in1, GPIO.LOW)
    GPIO.output(motorA_in2, GPIO.HIGH)
    GPIO.output(motorB_in1, GPIO.HIGH)
    GPIO.output(motorB_in2, GPIO.LOW)
    time.sleep(a*spin)
def c():
    left(1/3)
    forward(20)
    right(1/3)
    forward(20)
    right(1/3)
    forward(20)
    right(1/6)
def a1():
    pass
def n():
    pass
def s():
    pass
def a2():
    pass
def t():
    pass
try:
    # c -> a1 -> n -> s -> a2 -> t
    c()
    a1()
    n()
    s()
    a2()
    t()

finally:
    GPIO.cleanup()
