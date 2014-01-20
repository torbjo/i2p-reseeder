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


## INSTALL ##

TODO

### Permissions ###

Webserver needs access to the netDb files.

This works for me:

    cd /home/i2p/.i2p
    chgrp -R www-data netDb
    chmod -R g+rX netDb
    find netDb/ -type d | xargs chmod g+s
