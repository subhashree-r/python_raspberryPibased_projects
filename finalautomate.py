# A code that automates the various process such as watering the plants, heating and day night cycle through RF Modules. The RF codes are identified using RF Snipper and passed
#through raspberry pi transmitter receiver port#



import os,subprocess
from datetime import datetime,date
import time
from apscheduler.scheduler import Scheduler

on1=21811
off1=21820
on2=21955
off2=21964
on3=22275
off3=22284
Aon=1361
Aoff=1364
Bon=4433
Boff=4436
Con=5201
Coff=5204

sched = Scheduler()
sched.daemonic = False

def pump():

    data=[(time.strftime("%d/%m/%Y"))]

    with open(pumplog, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(data)

    #water pump
    os.system("sudo /var/www/rfoutlet/./codesend "+ str(Con)+ " -l 198 -p 0")
    print('pump on')
    time.sleep(120)
    os.system("sudo /var/www/rfoutlet/./codesend "+ str(Coff)+ " -l 198 -p 0")
    print('pump off')

def lighton():

    data = [(time.strftime("%d/%m/%Y"))]

    os.system("sudo /var/www/rfoutlet/./codesend " + str(on2) + " -l 198 -p 0")

    with open(lightonlog, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)

def lightoff():
    data = [(time.strftime("%d/%m/%Y"))]

    os.system("sudo /var/www/rfoutlet/./codesend " + str(off2) + " -l 198 -p 0")

    with open(lightofflog, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)

if __name__ == '__main__':

    pump()
    lighton()
    lightoff()
    sched.add_cron_job(pump, hour=8)
    sched.add_cron_job(lighton, hour=10)
    sched.add_cron_job(lightoff, hour=23)
    sched.start()
