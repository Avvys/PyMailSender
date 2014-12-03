#!/usr/bin/python

import smtplib
import json
import sys

# usage: ./sendmail.py "message to send" aat1.x atts2.y
 
def getData(file) : 
	json_data = open(file)
	data = json.load(json_data)
	json_data.close()
	return data 

def getMessage(mess, data) : # todo nicer message format
	msg = "\r\n".join([
	data['login'],
	data['tomail'],
	"Subject: ALARM DETECTED",
	"",
	mess
	])
	return msg

def send(message, attachment) :	
	config = getData('config.json')
	try:
		server = smtplib.SMTP(config['smtpsrv'], config['port'])
		server.set_debuglevel(True) 


		server.ehlo()  # need to say EHLO before just running straight into STARTTLS
		server.starttls()

		#Next, log in to the server
		server.login(config['login'], config['pass'])


		#Send the mail
		#msg = "\n Hello!" # The /n separates the message from the headers
		msg = getMessage(message, config)

		server.sendmail(config['login'], config['tomail'], msg)

		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"
	return

message = sys.argv[1]
send(message, "b")