#!/usr/bin/python

from os import listdir
from os.path import isfile, join
from zipfile import ZipFile as zip
from subprocess import Popen, PIPE, check_call
import random,sys,os

numSu3Files = 50
numRoutersPerFile = 60

curDir = os.getcwd()

if len(sys.argv) < 5:
  sys.stderr.write('Usage: '+str(sys.argv[0])+' sourcedir targetdir /path/to/i2p.jar keystore signer password\n')
  sys.exit(1)

sourceDir = sys.argv[1]
targetDir = sys.argv[2]
i2pDir    = sys.argv[3]
keystore  = sys.argv[4]
signer    = sys.argv[5]
password  = sys.argv[6]

files = [ f for f in listdir(sourceDir) if isfile(join(sourceDir,f)) and f.endswith('.dat') ]
i=0
zlist=[]
os.chdir(sourceDir)
while (i<=numSu3Files):
  print "Creating file #"+str(i)
  randomFiles = random.sample(files,numRoutersPerFile)
  # Remove RIs from the list if the netDb is big, so they don't get reused
  if len(files) > 500:
    files = [f for f in files if f not in randomFiles]
  zipFile = os.path.join(targetDir,str(i)+'.zip')
  z = zip(zipFile, 'w')
  for f in randomFiles:
   z.write(f)
  z.close()
  zlist.append(zipFile)
  i=i+1

error=False
try:
  proc=Popen(['java','-cp',i2pDir,'net.i2p.crypto.SU3File','bulksign',
    '-c3','-t6',targetDir,keystore,'3',signer],stdin=PIPE,stdout=PIPE,stderr=PIPE)
  proc.stdin.write(str(password)+'\n')
  proc.stdin.flush()  
  stdout,stderr = proc.communicate()
  print stdout,stderr
except CalledProcessError:
  print "Error! Can't sign files!!!"
  error=True

# Cleanup
os.chdir(targetDir)
for f in zlist:
 os.remove(f)

os.chdir(curDir)

if error:
  sys,exit(1)
sys.exit(0)

