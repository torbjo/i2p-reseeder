#!/bin/sh -e

# Run this to import I2P's netDb into current directory, and fix
# permissions. Can be run from a daily crontab to keep the netDb
# up-to-date so the reseeder don't seed stale router-info.
#
# Example:
# $ (crontab -l ; echo @daily /path/to/this/file) | crontab 


GROUP=www-data
NETDB=`getent passwd i2p | cut -d: -f6`/.i2p/netDb


# Copy/import
cp -r --preserve=timestamps $NETDB netDb.new

# Fix permissions
chgrp -R $GROUP netDb.new
chmod -R g+rX netDb.new

# Remove old, then move into place.
rm -r netDb
mv netDb.new netDb

# Notify reseeder app
touch wsgi.py
