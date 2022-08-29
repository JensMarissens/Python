#!/usr/bin/python3

import random
import urllib.request
import threading

def thingspeak_post():
  threading.Timer(15, thingspeak_post).start() #wait 15 seconds
  val = random.randint(15,30) #generate temperature data
  URL = 'https://api.thingspeak.com/update?api_key=R3558AT1K4BN92VC&field1=' + str(val) #add value to URL string
  data = urllib.request.urlopen(URL) #URL gets executed and the data is added
  
if __name__ == '__main__':
  thingspeak_post() #execute 
