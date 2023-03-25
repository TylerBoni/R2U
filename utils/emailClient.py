import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
<<<<<<< HEAD
from utils.helpers import getJsonFromFile
import json

def getSecrets():
    return getJsonFromFile('email_secrets.json')
=======
import json

def getSecrets():
    # read the contents of the JSON file
    with open('email_secrets.json', 'r') as f:
        secrets = json.load(f)
    return secrets
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

def sendEmail(to,subject,msg):
    secrets = getSecrets()

    # Email Parameters
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = secrets['email']['sender_email']
    sender_password = secrets['email']['sender_pw']
    receiver_email = to
    subject = subject
    message = msg

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.ehlo()
        smtp_connection.starttls()
        smtp_connection.login(sender_email, sender_password)

        # Send the email
        smtp_connection.sendmail(sender_email, receiver_email, msg.as_string())

        # Disconnect from the SMTP server
        smtp_connection.quit()

        print('Email sent successfully.')

    except smtplib.SMTPAuthenticationError:
        print('SMTP authentication error occurred.')
    except Exception as ex:
        print('An error occurred:', ex)
