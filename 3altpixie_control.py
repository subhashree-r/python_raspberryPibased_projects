# -*- coding: utf-8 -*-

''' 
Before running the code on the raspberry
sudo apt-get install python-serial

 the pixies are connected to a chain 
 pixie 0-2 are the far red pixies
 pixie 3-8 are the 3 LED pixies

'''


import serial
import time
import random
from datetime import datetime, time as dtime

#tmp
import os
import csv

PIXIES = 9 # number of pixies in chain

#Day night configuration
NIGHT_START = 23 # hour of the day
NIGHT_END = 6 # hour of the day

#tmp
LOG_FOLDER = '/home/pi/logs/'
logfile = os.path.join(
    LOG_FOLDER, 'log_day_night' +
    time.strftime('_%y%m%d%H%M%S', time.gmtime()) + 'UTC.csv')
    

COLORS = [] 

def dayconfig():
    #configuration for the far red pixies
    setcolor(0, 0,0,0)
    setcolor(1, 0,0,0)
    setcolor(2, 0,0,0)
    

    # configuration for all other pixies
    i = 0
    while i < PIXIES:
        setcolor(i, 85,85,85)
        i +=1


def nightconfig():
    #configuration for the far red pixies
    setcolor(0, 0,0,0)
    setcolor(1, 0,0,0)
    setcolor(2, 0,0,0)

    # configuration for all other pixies
    i = 3
    while i < PIXIES:
        setcolor(i, 0,0,0)
        i +=1

def init(): 
    i = 0
    # adding new empty color definition for each pixie
    while i < PIXIES:
        rgb = 0
        while rgb < 3:
            COLORS.append(0)
            rgb +=1
        i +=1


def setcolor(pix, red, green, blue): # set the color of an individual pixie
    COLORS[pix*3 ] = red
    COLORS[pix*3 +1 ] = green
    COLORS[pix*3 +2 ] = blue

def checkDay():
    start = dtime(NIGHT_START)
    end = dtime(NIGHT_END)
    now = datetime.now().time()
    mytime = "nothing"
    if start <= end:
        if start < now < end:
            nightconfig()
            mytime = "night"
        else:
            dayconfig()
            mytime = "day"
    else: # over midnight e.g., 23:30-04:15
        if start <= now or now < end:
            nightconfig()
            mytime = "night"
        else:
            dayconfig()
            mytime = "day"


    #tmp
    print mytime
    t = time.time()
    data = [
         mytime,
         time.strftime('_%H:%M:%S', time.gmtime())]

    with open(logfile, 'ab') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)


def main():
    port = serial.Serial("/dev/ttyAMA0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=3.0)

    init()
    checkDay()
    count = 0
    while True:
        count +=1
        port.write(bytearray(COLORS)) # write colors on outport
        time.sleep(0.5) 
        if count == 60: #check every 30 seconds 
            count = 0
            checkDay()


if __name__ == "__main__":
    main()


p = PIXIES-1 
i = 0   





'''
while True: # this test code sets each pixie to a random color one by one and switches off the previous one
    setcolor(p, 0,0,0) # set previous pixie to 0
    r = random.randrange(0, 101, 1) 
    g = random.randrange(0, 101, 1) 
    b = random.randrange(0, 101, 1) 
    setcolor(i, r, g, b) # set color of pixie i to a random color

    port.write(bytearray(colors)) # write colors on outport

    p = i;
    i+=1;
    if i > PIXIES-1:
        i = 0

    time.sleep(0.5) 


'''
