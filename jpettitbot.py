import socket
import sys
import os
import glob
import time
import datetime
import MySQLdb as mdb
import random

from creds import *

server = "irc.oftc.net"
channel = "#jpettitbot"
botnick = "jpettitBot"
password = CHANNEL_PASSWORD

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Connecting to " + server
irc.connect((server,6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
irc.send("NICK "+ botnick +"\n")                            #sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
irc.send("JOIN "+ channel + " " + password + "\n")

try:
	con = mdb.connect(HOSTNAME, DBUSER, DBPASS, DBNAME)
	print "Connected to database."
except _mysql.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)

while 1:
        text = irc.recv(2040)
        print text

        if text.find('PING') != -1:
                irc.send('PONG ' + text.split() [1] + '\r\n')
                print 'PONG sent to server'
	
	if text.find('!jpettitbot') != -1:
		irc.send('PRIVMSG '+channel+' : jpettitbot here, what can I do for you?\r\n')
	
	if text.find('!commands') != -1:
                irc.send('PRIVMSG '+channel+' :Enter !sensorname to view the current reading on that sensor, use sensors command for list\r\n')

        if text.find('!outsidetemp') != -1:
                cur = con.cursor()
                cur.execute("SELECT * FROM outside_temp ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+' F / '+str(rows[0][2])+'\r\n')
                rows = ' '

        if text.find('!pressure') != -1:
                cur = con.cursor()
                cur.execute("SELECT * FROM pressure ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+' mPa / '+str(rows[0][2])+'\r\n')

        if text.find('!outsidehumidity') != -1:
                cur = con.cursor()
                cur.execute("SELECT * FROM outside_humidity ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+'% / '+str(rows[0][2])+'\r\n')

        if text.find('!closettemp') != -1:
                cur = con.cursor()
                cur.execute("SELECT * FROM closet_temp ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+' F / '+str(rows[0][2])+'\r\n')

        if text.find('!housetemp') != -1:
                cur = con.cursor()
                cur.execute("SELECT * FROM house_temp ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+' F / '+str(rows[0][2])+'\r\n')

        if text.find('!bedroomtemp') != -1:
                cur = con.cursor()
                cur.execute("SELECT * FROM bedroom_temp ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+' F / '+str(rows[0][2])+'\r\n')

        if text.find('!bedroomhumidity') != -1:
		cur = con.cursor()
                cur.execute("SELECT * FROM bedroom_humidity ORDER BY id DESC LIMIT 1;")
                rows = cur.fetchall()

                irc.send('PRIVMSG '+channel+' :'+str(rows[0][1])+'% / '+str(rows[0][2])+'\r\n')

        if text.find('!sensors') != -1:
                irc.send('PRIVMSG '+channel+' :Sensors: bedroomtmp, bedroomhumidity, housetemp, closettemp, pressure, outsidetemp, outsidehumidity\r\n')

        if text.find('!filicputemp') != -1:
                irc.send('PRIVMSG '+channel+' :Welp, nothing here yet. But someday...someday!\r\n')

        if text.find('!filiambtemp') != -1:
                irc.send('PRIVMSG '+channel+' :Wait, what...am I in a bathroom? -Fili\r\n')

        if text.find('!ping') != -1:
                irc.send('PRIVMSG '+channel+' : Pong!\r\n')

        if text.find('!roll') != -1:
                num = random.randint(0,100)
                irc.send('PRIVMSG '+channel+' : You rolled a '+str(num)+'\r\n')

	if text.find('!pa') != -1:
		irc.send('PRIVMSG '+channel+' : jpettit: Time | jstewart: Time | buhman: Time \r\n')

