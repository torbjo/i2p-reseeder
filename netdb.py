r'''

/home/torkel/tmp/netDb/rx
    routerInfo-xWq3~CLjsn3IAFOAxWmDsPw4j0ADZj7ohVr9YewNWbA=.dat

http://docs.i2p2.de/javadoc/net/i2p/data/Base64.html
I2P uses a modified Base64 encoding:
    +   =>  -
    /   =>  ~

/some/path/to/netDb/rx
                    ^
                    |--- this is the prefix (r)

'''

import os


def load (netdb_path):
    """Load all router info from neteDb"""

    # List of all routers. Just to give each router a short integer id.
    rlist = []

    # @todo onerror
    # os.walk (path, topdown=True, onerror=None, followlinks=False)

    for dirpath, dirnames, filenames in os.walk (netdb_path):
        #if not filenames: continue
        #print 'Loading %d files from %s' % (len(filenames), dirpath)
        for filename in filenames:
            base = os.path.basename (dirpath)
            b64str = base[0] + filename[11:-4]
            rlist.append ((base, filename))
            #rlist.append (os.path.join(base, filename))
            #rlist.append (os.path.join(dirpath, filename))

    return rlist