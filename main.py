import os
import re
import sendgrid
import conf

domains = conf.domains
sendgrid_password = conf.sendgrid_password
mail = conf.mail
address = conf.address
sendgrid_username = conf.sendgrid_username

def pingstats(domain):
	
	return (os.popen('ping -c2 ' + domain))

def extract_packetloss(reply):
	match = re.search("([0-9]{1,3})(% packet loss)", reply)
	
	if match:
		return int(match.groups('0')[0])	

hosts_down = ""
hosts_up = ""

pings = dict();

for domain in domains:
	pings[domain] = pingstats(domain)
	#print ping

for domain in domains:
	output = pings[domain].read()
	packetloss = extract_packetloss(output)
	
	if packetloss > 0:
		hosts_down += domain + ", "
	else:
		hosts_up += domain + ", "

if  len(hosts_up) == 0: 
	hosts_up = "None of the  servers "
if len(hosts_down) == 0 :
	hosts_down = " None of the servers "

final_text = str(hosts_up + " seem(s) up "+ "\n" + hosts_down + " seem(s) down")

#email_module.email(final_text)


sg = sendgrid.SendGridClient(sendgrid_username, sendgrid_password)
message = sendgrid.Mail()
message.add_to(mail)
message.set_subject('Notifications on servers status')
message.set_text(final_text)
message.set_from(address)
status, msg = sg.send(message)
