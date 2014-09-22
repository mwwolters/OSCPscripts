#!/usr/bin/python
from subprocess import Popen,PIPE,STDOUT,call
import re
import os
import sys
import stat
#mysql -h localhost -V
#kernel version: uname -a
#rsync --version

proc_list = []
proc_ver = {"mysql":["mysql","-h","localhost","-V"],
	"kernel":["uname", "-a"],
	"rsync":["rsync","--version"],
	"vim":["vim","-v"],
	"sudo":["sudo","--version"],
	"apache":["apachectl","-V"],
	"nginx":["nginx","-V"],
	"sshd":["ssh","-V"],
	"openvasad":["openvasad","-V"]}
ver_list = {}
exclude = ['bash','ps','process_checker','sh','init','ata','network','procenum.py']

def usage():
  print "Usage:\n" +\
  "ps -u root | ./psenum.py\n" +\
  "tasklist | ./psenum.py\n (not implemented yet)"

def get_ps():
  out = open("ps_res.txt","w")
  checked = []
  rm = False
  for line in sys.stdin:
    if rm:
      proc = re.sub(r'.*[0-9][0-9]\s', '', line)
      proc = proc.replace('\n','')
      if proc not in checked and proc not in exclude:
        checked.append(proc)
        ver = check_ver(proc)
        if ver is not None:
          ver = ver.replace("\n","")
          out.write(proc+":"+ver+"\n")
        else:
          out.write(proc+"\n")
    else:
      rm = True
  out.close()

def check_ver(proc):
  if proc in proc_ver:
    #change
    ver_list[proc] = Popen(proc_ver[proc], stdout=PIPE, stdin=PIPE, stderr=STDOUT).stdout.readlines()[0]
    return ver_list[proc]
  return None

mode = os.fstat(0).st_mode
if stat.S_ISFIFO(mode):
  get_ps()
else:
  usage()
