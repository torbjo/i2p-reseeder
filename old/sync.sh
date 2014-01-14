#!/bin/sh -e

I2PHOME=`getent passwd "i2p" | cut -d: -f6`

SRC="$I2PHOME/.i2p/netDb"
DST=/srv/www/i2p-netdb.innovatio.no/htdocs/netdb

# xxx got wierd error message when using -0:
# cp: omitting directory `/home/i2p/.i2p/netDb/r4'
#find "$SRC" -print0 -name \*.dat | xargs -0 cp --link -t "$DST"

find "$SRC" -name \*.dat | xargs cp --update --link -t "$DST"

# Make world readable
chmod -R o+rX "$DST"
