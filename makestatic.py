#!/usr/bin/env python

import sys
import getopt
import os.path
from desagetexparser import DeSageTex

def usage():
  print("""Usage: %s [-h|--help] [-o|--overwrite] inputfile [outputfile] 

Removes SageTeX macros from `inputfile' and replaces them with the
Sage-computed results to make a "static" file. You'll need to have run
Sage on `inputfile' already.

`inputfile' can include the .tex extension or not. If you provide
`outputfile', the results will be written to a file of that name.
Specify `-o' or `--overwrite' to overwrite the file if it exists.

See the SageTeX documentation for more details.""" % sys.argv[0])

try:
  opts, args = getopt.getopt(sys.argv[1:], 'ho', ['help', 'overwrite'])
except getopt.GetoptError, err:
  print str(err)
  usage()
  sys.exit(1)

overwrite = False
for o, a in opts:
  if o in ('-h', '--help'):
    usage()
    sys.exit()
  elif o in ('-o', '--overwrite'):
    overwrite = True

if len(args) == 0 or len(args) > 2:
  print('Error: wrong number of arguments. Make sure you specify options first.\n') 
  usage()
  sys.exit(1)

if len(args) == 2 and (os.path.exists(args[1]) and not overwrite):
  print('Error: %s exists and overwrite option not specified.' % args[1])
  sys.exit(1)

src, ext = os.path.splitext(args[0])
desagetexed = DeSageTex(src)

if len(args) == 2:
  dest = open(args[1], 'w')
  dest.write(desagetexed.result)
else:
  print(desagetexed.result)
