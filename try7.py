
#A code that automatically transfers the pictures from the raspberry pi to backup flash drive every 30 minutes with the help of advanced python scheduler.
# If the drive is not mounted, the pictures are transferred to a backup folder . It automatically identifies if the drive is mounted and transfers the pictures to flash drive.

#!/usr/bin/python
#!/bin/bash


#PATH = /usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#export DISPLAY=:0.0
#up=$(uptime | grep "day" > /home/dnaneet/uptime.foo && awk < /home/dnaneet/uptime.foo '{ print $3 }')

#[[ $up -gt 0 ]] && xmessage -center "Restart!"`
#flashdrivetransfer
import os,subprocess
import shutil
import sys
#from apscheduler.scheduler  import BackgroundScheduler
from apscheduler.scheduler import Scheduler
import time
import logging

from apscheduler.scheduler import Scheduler

#Scheduler.start()

# Start the scheduler
sched = Scheduler()
sched.daemonic = False


#logging.basicConfig()
logging.basicConfig(filename='Transfer_output',level=logging.INFO)
NET_DRIVE='//192.168.178.1/fritz.nas/WD-Elements10B8-01/pictures/'
LOCAL_PATH='/home/pi/net/'
BACKUPFLASHDRIVE='/home/pi/BACKUP/'
store='/home/pi/store/pictures/'

def mount():
  if not (os.path.ismount('/home/pi/store/')):
    print('mounting')
    subprocess.call(['./sharingcode2.sh'])

def foldercheck1(d):
  if os.path.exists(os.path.join(store,d)):
    return
  else:
    os.makedirs(os.path.join(store,d))

def foldercheck2(d):
  if os.path.exists(os.path.join(BACKUPFLASHDRIVE,d)):
    return
  else:
    os.makedirs(os.path.join(BACKUPFLASHDRIVE,d))
  

def net_check(d,f):
  if (os.path.ismount('/home/pi/store/')):
    print('mounted')
    foldercheck1(d)
    shutil.move(os.path.join(LOCAL_PATH, os.path.join(d,f)) , os.path.join(store, os.path.join(d,f)))
  else:
    print('NOT MOUNTED FAILED TO MOVE TO FLASH DRIVE')
    foldercheck2(d)
    shutil.move(os.path.join(LOCAL_PATH,os.path.join(d,f)) , os.path.join(BACKUPFLASHDRIVE, os.path.join(d,f)))
    print('moved to backup')


def backup_check():
  print('BACKUP TRANSFER')
  if (os.path.ismount('/home/pi/store/')):
    
    for k in os.listdir(BACKUPFLASHDRIVE):
      while(os.listdir(os.path.join(BACKUPFLASHDRIVE,k))):  
          for f in os.listdir(os.path.join(BACKUPFLASHDRIVE,k)):
            foldercheck1(k)
            foldercheck2(k)
            f1=os.path.join(k,f)
            shutil.move(os.path.join(BACKUPFLASHDRIVE,f1),os.path.join(store,f1))
            print('transferred file')
    print('BACKUP TRANSFER COMPLETE')
    logging.info('BACKUP TRANSFER COMPLETE')
  else:
    return


def transfer():
  backup_check()
  print('TRANSFER')
  logging.info('TRANSFER COMPLETE')
  #while(os.listdir(LOCAL_PATH)):
  #for dirname,subdirs,files in os.walk(LOCAL_PATH):sudo python sharingcode2.sh
  #while(os.list):


  for d in os.listdir(LOCAL_PATH):
    #for d1 in subdirs:
    while(os.listdir(os.path.join(LOCAL_PATH,d))):
      for d1 in (os.listdir(os.path.join(LOCAL_PATH,d))):
        #for f in os.listdir(os.path.join(os.path.join(LOCAL_PATH,d1),d)):
          print "In directory %s and transferring file  %s" %(d,d1)
          net_check(d,d1)
          print('transferred  file')



                  
if __name__ == '__main__':
  mount()
  transfer()
  #backup_check()
  #sched.add_interval_job(transfer, minutes=1)
  #transfer()
  print('transferred a directory')

  #scheduler = BackgroundScheduler()
  #scheduler.add_job(transfer,'interval',minutes=60)

  #scheduler.start()
  try:
    print('next schedule')
    sched.add_interval_job(mount, hours=1)
    sched.add_interval_job(transfer, minutes=2)
    sched.start()
    sys.stdout.write("Running")
    #dots = True
    #while True:
    #Console feedback on running program
      #for i in xrange(0,5):
        #if dots:
         # sys.stdout.write("..")
          #time.sleep(0.5)
        #else:
         #sys.stdout.write("  \b\b\b\b")
        # time.sleep(0.5)
         #sys.stdout.flush()
        # dots = not dots
         #time.sleep(0.5)
  except (KeyboardInterrupt, SystemExit):
   print "Terminated"
   sched.shutdown(wait=False,shutdown_threadpool=False)
