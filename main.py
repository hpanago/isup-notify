import os
import re
import conf
import smtplib
from email.message import EmailMessage

DOMAINS = conf.domains
EMAIL = conf.email
USERNAME = conf.user if conf.user is not '' else conf.email
PASSWORD = conf.password
RECIEVERS = conf.recievers
SMTP_SERVER = conf.smtp_server
SMTP_PORT = conf.smtp_port

def pingstats(domain):
    return os.popen('ping -c2 %s' % domain)

def extract_packetloss(reply):
    match = re.search("([0-9]{1,3})(% packet loss)", reply)

    if match:
        return int(match.groups('0')[0])

hosts_down = ""
hosts_up = ""

pings = dict();

for domain in DOMAINS:
    pings[domain] = pingstats(domain)

for domain in DOMAINS:
    output = pings[domain].read()
    packetloss = extract_packetloss(output)

    if packetloss > 0:
        hosts_down += domain + ", "
    else:
        hosts_up += domain + ", "

if len(hosts_up) == 0:
    hosts_up = "None of the  servers "
if len(hosts_down) == 0 :
    hosts_down = " None of the servers "

final_text = str(hosts_up + " seem(s) up "+ "\n" + hosts_down + " seem(s) down")

# Create a text/plain message
msg = EmailMessage()
msg['Subject'] = 'Notifications on servers status'
msg['From'] = EMAIL
msg['To'] = RECIEVERS
msg.set_content(final_text)

# Send the message via our own SMTP server.
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
    s.starttls() # secure connection
    s.login(USERNAME, PASSWORD)
    s.send_message(msg)
