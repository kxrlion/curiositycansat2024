from LoRaRF import SX127x
import os,sys,time
import random
lora = SX127x()

def ascii_interpreter(a):
    return ord(a)


lora.begin()
#lora.setTxPower(13,lora.TX_POWER_SX1278)
lora.setFrequency(434000000)
lora.setLoRaModulation(7,125000,5,True)
#lora.setLoRaPacket(lora.HEADER_EXPLICIT,12,100,True,False)

counter = 0
message=str(counter)+ord(":")
for i in range(19-int(counter/10)):
    message+=chr(random.randint(48,57))
 
messagelist = list(message)
for i in range(len(messagelist)):
   messagelist[i] = ord(messagelist[i])
counter = 0
while True:
    message=str(counter)+ord(":")
    for i in range(19-int(counter/10)):
        message+=chr(random.randint(48,57))
    
        
    messagelist = list(message)
    for i in range(len(messagelist)):
        messagelist[i] = ord(messagelist[i])
    lora.beginPacket()
    lora.write(messagelist,len(messagelist))
    lora.endPacket()
    lora.wait()
    time.sleep(2)
    counter = (counter+1)%1001
