# This file will mount the raspberry pi home directory
# to a local directory using SSHFS.
#
# By default, it will mount it to a directory above the current
# directory. This keeps it out of the current git repo.

# To unmount, run this command:
# umount ./remote_pi/

PI_IP=192.168.1.11
PI_HOME_DIR=/home/pi/ # mind the trailing slash
LOCAL_DIR=../remote_pi/

mkdir -p $LOCAL_DIR

sshfs \
    pi@$PI_IP:$PI_HOME_DIR \
    $LOCAL_DIR

