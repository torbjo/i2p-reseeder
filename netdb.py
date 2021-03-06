r'''

http://docs.i2p2.de/javadoc/net/i2p/data/Base64.html
I2P uses a modified Base64 encoding:
    +   =>  -
    /   =>  ~

netDb/rx/routerInfo-xWq3~CLjsn3IAFOAxWmDsPw4j0ADZj7ohVr9YewNWbA=.dat

/some/path/to/netDb/rx
                    ^
                    |--- this is the prefix (r)

'''

import os

def on_error (ex):
    raise ex
    # @todo ingore access denied?
    # IOError: [Errno 13] Permission denied:
    # Note: new routerInfo files created by I2P has wrong permissions
    # workaround: i2p umask?, setfacl?


def load (netdb_path):
    """Load all router info from neteDb"""

    # List of all routers. Just to give each router a short integer id.
    rlist = []

    # @todo onerror
    # os.walk (path, topdown=True, onerror=None, followlinks=False)

    for dirpath, dirnames, filenames in os.walk (netdb_path, onerror=on_error):
        #if not filenames: continue
        #print 'Loading %d files from %s' % (len(filenames), dirpath)
        for filename in filenames:
            base = os.path.basename (dirpath)
            # Add prefix, then strip 'routerInfo-' and '.dat' to get
            # router hash as base64 encoded string.
            #b64str = base[0] + filename[11:-4]
            rlist.append ((base, filename))

            # ('rG', 'routerInfo-GPPJQ-5dtsa~OZUWxxN8Ln~cYULRl7t50FMX1gK37GM=.dat')
            # @todo no need to store base since it's always equal to
            #       base = 'r' + filename[11]

            #size = os.path.getsize (os.path.join (dirpath, filename))
            #rlist.append ((base, filename, size))
            #rlist.append (os.path.join(base, filename))
            #rlist.append (os.path.join(dirpath, filename))

    return rlist
