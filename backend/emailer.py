import smtplib
from email.message import EmailMessage

from db import *
from scrape import *
from datetime import date

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'best.scrape.app@gmail.com'
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('best.scrape.app@gmail.com', 'ehmw mftu sjqs owmu')
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        return Exception