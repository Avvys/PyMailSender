#!/usr/bin/python
#-*- coding: utf-8 -*-

import smtplib
import json
import sys

from email.mime.text import MIMEText


# usage: ./sendmail.py "message to send" aat1.x atts2.y
 
def getData(file) : 
	json_data = open(file)
	data = json.load(json_data)
	json_data.close()
	return data 

def getMessage(mess, data) : # todo nicer message format
	msg = MIMEText(mess)

	msg['Subject'] = "ALARM DETECTED"
	msg['From'] = data['login']
	msg['To'] = data['tomail']
	msg['Body'] = mess

	return msg

def send(message, attachment) :	
	config = getData('config.json')
	try:
		server = smtplib.SMTP(config['smtpsrv'], config['port'])
		server.set_debuglevel(True) 


		server.ehlo()  # need to say EHLO before just running straight into STARTTLS
		server.starttls()

		# log in to the server
		server.login(config['login'], config['pass'])
		
		# message
		msg = getMessage(message, config)

		# Send the mail
		server.sendmail(config['login'], config['tomail'], msg.as_string())

		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"
	return

message = sys.argv[1]
send(message, "b")