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
Aconst = 2,136000936
Nconst = 2,441549178
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
def c(x):
    left(1/3)
    forward(x)
    right(1/3)
    forward(x)
    right(1/3)
    forward(x)
    right(1/6)
def a1(x):
    right(110/180)
    forward(Aconst * x)
    right(1)
    forward(1.25*x)
    right(70/180)
    forward(0.75 * x)
    left(110/180)
    forward((Aconst-1.25)*x)
    left(1)
    forward(Aconst * x)
    left(70/180)
def n(x):
    left(1/2)
    forward (2*x)
    right(145/180)
    forward(Nconst * x)
    left(145/180)
    forward(2*x)
    right(1/2)
def s(x):
    forward(x)
    right(1)
    forward(x)
    left(1/2)
    forward(x)
    left(1/2)
    forward(x)
    right(1/2)
    forward(x)
    right(1/2)
    forward(x)
    right(1)
    forward(x)

def a2(x):
    left(70/180)
    forward(Aconst*x)
    left(1)
    forward((Aconst-1.25)*x)
    left(110/180)
    forward(0.75 * x)
    left(110/180)
    forward((Aconst-1.25)*x)
    left(1)
    forward(Aconst*x)
    left(70/180)


def t(x):
    pass
try:
    # c -> a1 -> n -> s -> a2 -> t
    x=20
    c(x)
    forward(20)
    a1(x)
    forward(20)
    n(x)
    forward(20)
    s(x)
    forward(20)
    a2(x)
    forward(20)
    t(x)

finally:
    GPIO.cleanup()
