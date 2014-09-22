#!/usr/bin/python
from subprocess import Popen,PIPE,STDOUT
import sys
import os
import stat
import re

exclude = ['bash','ps','process_checker','sh','init','ata','network']

def usage():
  print "I recommend using psenum output for this script\n" +\
  "Usage:\n" +\
  "\tps -u root | ./process_checker.py\n" +\
  "\ttasklist | ./process_checker.py (not implemented yet)\n" +\
  "\t-i <file>\tcheck based on input file\n" +\
  "\t-o <os>\tsearch for a specific os\n"

def piped():
  rm = False
  output = ''
  checked = []
  for line in sys.stdin:
    if rm:
      out = ''
      proc = re.sub(r'.*[0-9][0-9]\s', '', line)
      proc = proc.replace('\n','')
      if proc not in exclude and proc not in checked:
        checked.append(proc)
        results = Popen(['searchsploit', proc], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        r = results.stdout.readlines()
        r = filter(lambda a: '/dos/' not in a and 'windows' not in a, r)
        if len(r) != 2:
          out = 'Results for ' + proc + '\n'
          out += '####################################################################\n'
          out += ''.join(r)
          out += '####################################################################\n\n'
        else:
          empty.append(proc) 
        output += out  
    else:
      rm = True
  print output

def norm():
  f = open(sys.argv[1])
  output = ''
  checked = []
  empty = []
  for proc in f.readlines():
    out = ''
    proc = proc.replace('\n','')
    if proc not in exclude and proc not in checked:
      checked.append(proc)
      results = Popen(['searchsploit', proc], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
      r = results.stdout.readlines()
      r = filter(lambda a: '/dos/' not in a and 'windows' not in a, r)
      if len(r) != 2:
        out = 'Results for ' + proc + '\n'
        out += '####################################################################\n'
        out += ''.join(r)
        out += '####################################################################\n\n'
      else:
        empty.append(proc) 
      output += out  
  print output
  print 'Process without exploits: \n' + '\n'.join(empty)

mode = os.fstat(0).st_mode
if stat.S_ISFIFO(mode):
  piped()
else:
  norm()


