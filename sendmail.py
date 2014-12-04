#!/usr/bin/python
#-*- coding: utf-8 -*-

import smtplib
import json
import sys
import os 

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


# usage: ./sendmail.py "message to send" aat1.x atts2.y

def getAttachmentsFromCmd(args) : 
	attachments = []
	for i in range(2, len(args)) :
		attachments.append(args[i])
	return attachments

 
def getData(file) : 
	json_data = open(file)
	data = json.load(json_data)
	json_data.close()
	return data 

def prepareMessage(mess, attachments, data) : # todo nicer message format
	msg = MIMEMultipart()
	
	msg['Subject'] = "ALARM DETECTED"
	msg['From'] = data['login']
	msg['To'] = data['tomail']
	msg.attach(MIMEText(mess))


	for a in attachments :
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(a,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(a))
		msg.attach(part)

	return msg

def send(message, attachments) :	
	config = getData('config.json')
	try:
		server = smtplib.SMTP(config['smtpsrv'], config['port'])
		server.set_debuglevel(True) 

		# need to say EHLO before just running straight into STARTTLS
		server.ehlo()  
		server.starttls()

		# log in to the server
		server.login(config['login'], config['pass'])
		
		# message
		msg = prepareMessage(message, attachments, config)

		# Send the mail
		server.sendmail(config['login'], config['tomail'], msg.as_string())

		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"
	return

assert (len(sys.argv) >= 3),"Needed 3 or more params!"

message = sys.argv[1]
attachments = getAttachmentsFromCmd(sys.argv)

send(message, attachments)