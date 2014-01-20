r'''

There are two ways to point to I2P's netDb:

  1) Copy it to this directory (same as wsgi.py is in).

  2) Set NETDB_PATH bellow correctly.

'''

import os
import sys

ROOT = os.path.dirname(__file__)
sys.path.insert (0, ROOT)

NETDB_PATH = os.path.join (ROOT, 'netDb')
#NETDB_PATH = '/path/to/netDb'

from reseeder import Reseeder
application = Reseeder (NETDB_PATH)


# did not work. permission problem
#application = Reseeder ('/home/i2p/.i2p/netDb')

# did not work to pass from apache.conf
#application = Reseeder (os.environ['I2P_NETDB_PATH'])
