import os
import sys

sys.path.insert (0, os.path.dirname(__file__))

from reseeder import Reseeder
application = Reseeder ('/home/i2p/.i2p/netDb')
# XXX hardcoded path
#application = Reseeder (os.environ['I2P_NETDB_PATH'])
