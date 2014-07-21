i2p-reseeder
============

[I2P](https://geti2p.net) Reseeder written in Python (WSGI).

It can run under all webservers supporting WSGI.

It also contains a built in webserver used for testing.


## Dependencies ##

It depends on [Werkzeug](https://pypi.python.org/pypi/Werkzeug)
(The Python WSGI Utility Library).

Run `apt-get install python-werkzeug` or `pip install werkzeug`.

This is tested with Python 2.7 and Werkzeug 0.9.4.

The master/default branch is currently maintained by https://github.com/mikalv / https://github.com/meeh420.


## INSTALL ##

* Install all dependencies `apt-get install python-werkzeug libapache2-mod-wsgi apache2`
* Create a SSL certificate (If you use openssl you can do; `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650`)
* Edit apache or nginx to use wsgi.py
* Copy the prod.dist file to prod.conf and edit it so it matches your environment
* Download the code

Example
```
cd /var/www/
git clone https://github.com/mikalv/i2p-reseeder.git us.reseed.i2p2.no
```

* Make sure required apache modules is enabled `a2enmod wsgi ssl`
* Restart apache `service apache2 restart`
* Test your reseed server with a I2P router, check for errors in the log

### Permissions ###

Webserver needs access to the netDb files.

This works for me:

    cd /home/i2p/.i2p
    chgrp -R www-data netDb
    chmod -R g+rX netDb
    find netDb/ -type d | xargs chmod g+s


## Creation of SU3 keys ##

The tool help menu looks like this:
```
$ java -cp /Applications/i2p/lib/i2p.jar net.i2p.crypto.SU3File
Usage: SU3File keygen       [-t type|code] publicKeyFile keystore.ks you@mail.i2p
       SU3File sign         [-c type|code] [-t type|code] inputFile.zip signedFile.su3 keystore.ks version you@mail.i2p
       SU3File bulksign     [-c type|code] [-t type|code] directory keystore.ks version you@mail.i2p
       SU3File showversion  signedFile.su3
       SU3File verifysig    signedFile.su3
       SU3File extract      signedFile.su3 outFile.zip
Available signature types (-t):
      DSA_SHA1  (code: 0) DEFAULT
      ECDSA_SHA256_P256 (code: 1)
      ECDSA_SHA384_P384 (code: 2)
      ECDSA_SHA512_P521 (code: 3)
      RSA_SHA256_2048   (code: 4)
      RSA_SHA384_3072   (code: 5)
      RSA_SHA512_4096   (code: 6)
Available content types (-c):
      UNKNOWN   (code: 0) DEFAULT
      ROUTER    (code: 1)
      PLUGIN    (code: 2)
      RESEED    (code: 3)
```

Example for creating a key:

$ java -cp /Applications/i2p/lib/i2p.jar net.i2p.crypto.SU3File keygen -t 6 reseed.pub-key.pem sindu.reseed-keystore.ks your-email-address@whatever.i2porg

