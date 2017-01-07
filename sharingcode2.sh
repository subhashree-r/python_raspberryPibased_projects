# A sheel script to mount the local drive of raspberry pi to the flash drive
#!/bin/bash
##Network path to drive
NET_DRIVE="//192.168.178.1/fritz.nas/WD-Elements10B8-01/"
LOCAL_PATH="/home/pi/net"
USER="nas"
PASSWORD="florarobotica"
store='/home/pi/store/'


#Unmount possible mounted drive on path
#sudo umount $LOCAL_PATH &

#mount drive to local path
#print"1"
sudo mount -t cifs -o user=$USER,password=$PASSWORD $NET_DRIVE $store
