from threading import Thread
from ctypes.wintypes import LONG
import os
import sys
import time
import board
import busio as io
import pyrebase
import random
import serial
import math
import datetime
import uuid
import RPi.GPIO as GPIO
from bmp280 import BMP280
from smbus import SMBus
from picamera2 import Picamera2
from libcamera import controls
from LoRaRF import SX127x
#picam2=Picamera2()
ser = serial.Serial("/dev/ttyUSB2",115200)
rec_buff =''
lora = SX127x()
config={
        "apiKey": "I0953io9puBU1pfUulttRETKFNqhNKdkmz2eZCnR",
        "authDomain": "cansat-eda48.firebaseapp.com",
        "databaseURL": "https://cansat-eda48-default-rtdb.europe-west1.firebasedatabase.app/",
        "storageBucket": "cansat-eda48.appspot.com"
}

#firebase = pyrebase.initialize_app(config)
#db = firebase.database()

def initApp():
    try:
#       print("starting cam\n")
#       picam2.start()
       print("starting gps\n")
       ser.write(("AT+CGPS=1"+'\r\n').encode())
       time.sleep(10)
 if ser.inWaiting():
          time.sleep(0.01)
       lora.begin()
       lora.setFrequency(434000000)
       lora.setLoRaModulation(7,125000,5,True)
    except:
       print("ERROR:INIT")
def loraCom(counter,message):
    try:
       messageT = str(counter)+";"+message
       messageList = list(messageT)
       for i in range(len(messageList)):
           messageList[i] = ord(messageList[i])
       print (messageT)
       lora.beginPacket()
       lora.write(messageList,len(messageList))
       lora.endPacket()
       lora.wait()
    except:
       print("ERROR:LORA")
def bmpT():
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)
    temp= bmp280.get_temperature()
    txt = "\ntemperature: {t:.3f} \n"
#    print(txt.format(t=temp))
    return temp
def bmpP():
    bus = SMBus(1)
    bmp280 = BMP280(i2c_dev=bus)
    press = bmp280.get_pressure()
    txt = "pressure: {p:.3f} \n"
#    print(txt.format(p=press))
    return press


def accelX():
    bus =SMBus(1)
    bus.write_byte_data(0x19,0x20,0x27)
    bus.write_byte_data(0x19,0x23,0x00)
    time.sleep(0.5)
    data0 = bus.read_byte_data(0x19,0x28)
    data1 = bus.read_byte_data(0x19,0x29)
    xAccl = data1*256 + data0
    if xAccl > 32767:
        xAccl -=65536
    x=xAccl
    txt = "xA: {x:.6f}/n"
#    print (txt.format(x=xAccl))
    return x
def accelY():
    bus =SMBus(1)
    bus.write_byte_data(0x19,0x20,0x27)
    bus.write_byte_data(0x19,0x23,0x00)
    time.sleep(0.5)
    data0 = bus.read_byte_data(0x19,0x2A)
    data1 = bus.read_byte_data(0x19,0x2B)
    yAccl = data1*256 + data0
    if yAccl > 32767:
        yAccl -= 65536
    y=yAccl
    txt = "yA: {y:.6f}/n"
#    print (txt.format(y=yAccl))
    return y
def accelZ():
    bus =SMBus(1)
    bus.write_byte_data(0x19,0x20,0x27)
    bus.write_byte_data(0x19,0x23,0x00)
    time.sleep(0.5)
    data0 = bus.read_byte_data(0x19,0x2C)
    data1 = bus.read_byte_data(0x19,0x2D)
zAccl = data1 * 256 + data0
    if zAccl > 32767:
        zAccl -= 65536
    z=zAccl
    txt = "zA: {z:.6f}/n"
#    print (txt.format(z=zAccl))
    return z


def drive(x):
   GPIO.setmode(GPIO.BCM)
   #set up GPIO pins
   #left motor
   motorL1 = 5
   motorL2 = 6
   #right motor
   motorR1 = 23
   motorR2 = 24
   try:
      GPIO.setup(motorL1,GPIO.OUT)
      GPIO.setup(motorL2,GPIO.OUT)
      GPIO.setup(motorR1,GPIO.OUT)
      GPIO.setup(motorR2,GPIO.OUT)
      angle = 285
      spin = 360/angle
      def forward(n):
          #m -> liczba cm do przejechania
          #n -> ile razy ma sie obrocic kolo
          GPIO.output(motorA_in1, GPIO.LOW)
          GPIO.output(motorA_in2, GPIO.HIGH)
          GPIO.output(motorB_in1, GPIO.LOW)
          GPIO.output(motorB_in2, GPIO.HIGH)
          time.sleep(n)
      def backward(n):
          #m -> liczba cm do przejechania
          #n -> ile razy ma sie obrocic kolo
          GPIO.output(motorA_in1, GPIO.HIGH)
GPIO.output(motorA_in2, GPIO.LOW)
          GPIO.output(motorB_in1, GPIO.HIGH)
          GPIO.output(motorB_in2, GPIO.LOW)
          time.sleep(n)
      def right(a):
          #a -> a podane w radianach / PI
          GPIO.output(motorA_in1, GPIO.HIGH)
          GPIO.output(motorA_in2, GPIO.LOW)
          GPIO.output(motorB_in1, GPIO.LOW)
          GPIO.output(motorB_in2, GPIO.HIGH)
          time.sleep(a)
      def left(a):
          #a -> a podane w radianach / PI
          GPIO.output(motorA_in1, GPIO.LOW)
          GPIO.output(motorA_in2, GPIO.HIGH)
          GPIO.output(motorB_in1, GPIO.HIGH)
          GPIO.output(motorB_in2, GPIO.LOW)
          time.sleep(a)
   except:
       print("ERROR:MOTORFUNC")
   try:
       forward(10)
   except:
       print("ERROR:WHEEL")
   finally:
       GPIO.cleanup()


def sendGps(x):
       t = []
       ts =""
       s=""
       temper=0
       pressu=0
       iter=0
       def toFormat(n):
          out=0;
out+=math.floor(n/100)
          n=n-out*100
          out+=n/60
          return out
#try:
       ser.write(("AT+CGPSINFO"+"\r\n").encode())
       time.sleep(1)
       if ser.inWaiting():
          time.sleep(0.01)
          rec_buff = ser.read(ser.inWaiting())
       ts= rec_buff
       s=rec_buff
       while s==ts:
          ser.write(("AT+CGPSINFO"+"\r\n").encode())
          time.sleep(1)
          if(ser.inWaiting()):
            time.sleep(0.01)
            rec_buff = ser.read(ser.inWaiting())
          s=rec_buff.decode()
          s=s[2:len(s)-8]
          temper= bmpT()
          pressu= bmpP()
          message = "{temp};{press}; ; ".format(temp=temper,press=pressu)
#          print("=========================\nThread1")
#          loraCom(iter,message)
#          iter+=1
          print(message)
       while s!=ts:
          ser.write(("AT+CGPSINFO"+"\r\n").encode())
          time.sleep(1)
          if ser.inWaiting():
            time.sleep(0.01)
            rec_buff = ser.read(ser.inWaiting())
          s=rec_buff.decode()
          temper = bmpT()
          pressu = bmpP()
          gps ={
"longi":s[0:11],
          "lat":s[15:26]
          #"longi":"A",
          #"lat":"B"
          }
          message = "{temp};{press};{longi};{lati}".format(temp=temper,press=pressu,longi=gps["longi"],lati=gps["lat"])
#          loraCom(iter,message)
          #db.child("gps").child("newest").set(gps)
          #db.child("gps").child("data").push(gps)
#         print("=========================\nThread1")
          iter+=1
          print(message)
#    except:
#       print("ERROR:gps")

#def makePhoto(c):
#    #picam2=Picamera2()
#    try:
#       picam2.set_controls({"AfMode":controls.AfModeEnum.Manual,"LensPosition":1.0})
#       picam2.capture_file("{}.png".format(c))
#    except:
#       print("ERROR:PHOTOFUNC")
def canStop(p0,pr):
    p=bmpP()
    a=0
    ax=0
    ay=0
    az=0
    try:
       def accel(pr):
           #pr-precision
           while 1-pr<a<1+pr:
             ax=accelX()
             ay=accelY()
             az=accelZ()
             a=np.sqrt(ax*ax + ay*ay + az*az)
             #print(a)
 return a
       while p>p0-150:
         p=bmpP()
         #print("1 loop:p:{}".format(p))
       while abs(1-a)>p:
         a=accel()
         #print("2 loop:a:{}".format(a))
       while abs(p-p0)>10:
         p=bmpP()
         #print("3 loop:p:{}".format(p))
       print("wyladowal")
    except:
      print("ERROR:canStop")
def sendData(x):
    try:
       #firebase = pyrebase.initialize_app(config)
       #db = firebase.database()
       print("A")
       #stor = firebase.storage()
       id=0
       w=''
       while True:
            #f = open("text2.txt",'a')
            temp = bmpT()
            press = bmpP()
            data = {
             "id":id,
             "temp": temp,
             "pressure": press,
            }
            print("=========================\nThread2")
            #print("temperature:{t} ; pressure:{p}".format(t=data["temp"],p=data["pressure"]))
            #f.write(str(temp)+";"+str(press)+'\n')
            #db.child("cansat").child("newest").set(data)
            #db.child("cansat").child("data").push(data)
            #if id % 2:
            #w=uuid.uuid1()
#makePhoto(w)
            #stor.child("img/{}.png".format(w)).put("{}.png".format(w))
            #txt = stor.child("img/{}.png".format(w)).get_url("None")
            #link = {
            #"timestamp":str(datetime.datetime.now()),
            #"link":txt
            #}
            #db.child("zdjecia").push(link)
            #w+=1
            #id+=1
            time.sleep(1)
    except:
            print("ERROR:sendData")
initApp()
#Thread(target=sendData, args=[1]).start()
#Thread(target=sendGps, args=[1]).start()
Thread(target=drive ,args=[1]).start()