#!/bin/bash

# Run this to import I2P's netDb into current directory, and fix
# permissions. Can be run from a daily crontab to keep the netDb
# up-to-date so the reseeder don't seed stale router-info.
#
# Example:
# $ (crontab -l ; echo @daily /path/to/this/file) | crontab 


GROUP=www-data
NETDB=`getent passwd i2p | cut -d: -f6`/.i2p/netDb

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -f $ROOT_DIR/prod.conf ]; then
  source $ROOT_DIR/prod.conf
else
  echo "Please rename prod.dist to prod.conf and set your config before continuing!"
  exit 1
fi

# Copy/import
mkdir netDb.new
find $NETDB -type f -exec cp {} netDb.new \;

# Fix permissions
chgrp -R $GROUP netDb.new
chmod -R g+rX netDb.new

# Switch files
mv netDb netDb.old # This way we don't have to wait on the deletion I/O
mv netDb.new netDb

# Make su3 files
if [ $DEBUG -eq 1 ]; then
  python make-su3files.py $ROOT_DIR/netDb $ROOT_DIR/su3netDb $I2PLIBJAR $KEYSTORE $SIGNER $PASSWORD
else
  python make-su3files.py $ROOT_DIR/netDb $ROOT_DIR/su3netDb $I2PLIBJAR $KEYSTORE $SIGNER $PASSWORD > /dev/null 2>&1
fi

# The real cleanup
rm -r netDb.old


# Notify reseeder app
touch wsgi.py
