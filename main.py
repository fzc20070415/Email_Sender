import smtplib
import ssl
import configparser
import argparse

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")
emailAddr = config['ACCOUNT']['EmailAddr']
pwd = config['ACCOUNT']['Pwd']
serverAddr = config['SERVER'][config['ACCOUNT']['Provider']]

port = config['SSL']['Port']  # For SSL

print("Configuration Loaded:\n\t\
    Email Address: {}\n\t\
    Email Provider: {}\n\t\
    Port Number: {}"\
    .format(emailAddr, config['ACCOUNT']['Provider'], port))

# Load arguments
parser = argparse.ArgumentParser(description='Email Sender')
parser.add_argument('receiver_email_address', type=str)
# parser.add_argument('email_title', type=str)
parser.add_argument('email_content', type=str)
parser.add_argument('--subject', type=str, help="Optional Email Title/Subject")
args = parser.parse_args()
receiver = args.receiver_email_address
text = args.email_content
subject = ""
if args.subject is not None:
    subject = args.subject
content = 'Subject: {}\n\n{}'.format(subject, text)

print("Arguments Loaded:\n\t\
    Receiver Email Address: {}\n\t\
    Subject: {}\n\t\
    Content: {}"
    .format(receiver, subject, text))

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(serverAddr, port, context=context) as server:
    server.login(emailAddr, pwd)
    # Send email
    server.sendmail(emailAddr, receiver, content)

print("Email successfully sent. Exiting")
