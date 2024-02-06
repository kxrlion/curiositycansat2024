from ctypes.wintypes import LONG
import time
import board
import busio as io
import pyrebase
import random

config = {  
  "apiKey": "I0953io9puBU1pfUulttRETKFNqhNKdkmz2eZCnR",
  "authDomain": "cansat-eda48.firebaseapp.com",
  "databaseURL": "https://cansat-eda48-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "cansat-eda48.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

longi =random.randint(100,200)
lat =random.randint(100,200)


gps={
    "longi":longi,
    "lat":lat,
    }


while True:
  temp=random.randint(1,100)
  pressure=random.randint(100,200)
  longi =random.randint(100,200)
  lat =random.randint(100,200)

  data = {
      "temp": temp,
      "pressure": pressure,
      "gps":gps
  }
   

  jeden=random.randint(1,100)
  dwa=random.randint(100,200)

  db.child("cansat").child("newest").set(data) 
  db.child("cansat").child("data").push(data)
  time.sleep(2)