#!/usr/bin/python
#-*- coding: utf-8 -*-

import smtplib
import json
import sys
import os 
import logging
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


# usage: ./sendmail.py subject "message to send" aat1.x atts2.y


logging.basicConfig(filename='pymailsender.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %R')

def getAttachmentsFromCmd(args) : 
	attachments = []
	for i in range(3, len(args)) :
		attachments.append(args[i]) 
		if not os.path.isfile(args[i]) : 
			logging.warning(args[i] + " doesn't exist! Aborting!")
			sys.exit(args[i] + " doesn't exist! Aborting!")
	return attachments

 
def getData(file) : 
	if not os.path.isfile(file) :
		logging.warning("Can't load config: " + file)
		sys.exit("Can't load config: " + file)

	json_data = open(file)
	data = json.load(json_data)
	json_data.close()
	return data 

def prepareMessage(subject, mess, attachments, data) : # todo nicer message format
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = data['login']
	msg['To'] = ', '.join(data['to'])
	msg['Cc'] = ', '.join(data['cc'])
	msg['Bcc'] = ', '.join(data['bcc'])
	msg.attach(MIMEText(mess))

	for a in attachments :
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(a,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(a))
		msg.attach(part)

	return msg

def send(subject, message, attachments) :	
	config = getData('config.json')
	try:
		server = smtplib.SMTP(config['smtpsrv'], config['port'])
		#server.set_debuglevel(True) 

		# need to say EHLO before just running straight into STARTTLS
		server.ehlo()  
		server.starttls()

		# log in to the server
		server.login(config['login'], config['pass'])
		
		# message
		msg = prepareMessage(subject, message, attachments, config)

		# list of recipients
		toList = config['to'] + config['cc'] + config['bcc']
		print toList
		# Send the mail
		server.sendmail(config['login'], toList, msg.as_string())

		server.close()
		print 'successfully sent the mail'
		logging.info('successfully sent the mail')
	except:
		print "failed to send mail"
		logging.warning('failed to send mail')
	return




assert (len(sys.argv) >= 3),"Needed 3 or more params!"

subject = sys.argv[1]
message = sys.argv[2]

attachments = getAttachmentsFromCmd(sys.argv)

send(subject, message, attachments)