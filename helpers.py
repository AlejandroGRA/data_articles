import logging
import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from dotenv import load_dotenv

# Load environment variables in local
load_dotenv()                    

# Logging configuration, write the logs to console and logs file
logging.basicConfig(
        handlers=[
        logging.FileHandler("./data/logs.log"),
        logging.StreamHandler()
        ],
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

# Feedly api secrets for feedly.py
ACCESS_TOKEN_FEEDLY = os.environ.get('ACCESS_TOKEN_FEEDLY')
USER_ID = os.environ.get('USER_ID')
DATA_ARTICLES_CATEGORY = os.environ.get('DATA_ARTICLES_CATEGORY')

# Twitter api secrets for tweet.py
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# Email alerts configuration
EMAIL_ENABLED = os.environ.get('EMAIL_ENABLED')
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_SENDER_PASS = os.environ.get('EMAIL_SENDER_PASS')
EMAIL_RECEIVER = [os.environ.get('EMAIL_RECEIVER')]

def send_mail(subject, text, files=None):
    if EMAIL_ENABLED:
        assert isinstance(EMAIL_RECEIVER, list)

        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = COMMASPACE.join(EMAIL_RECEIVER)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        smtp = smtplib.SMTP(host=EMAIL_SERVER, port=EMAIL_PORT)
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_SENDER_PASS)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        smtp.close()
    else:
        logging.debug('Email alerts are not enabled')