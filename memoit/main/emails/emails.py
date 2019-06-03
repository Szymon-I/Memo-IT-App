from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os.path import exists
import os


# send welcome email after registration success
def welcome_email(user):
    from_addr = ""
    to_addr = user.email
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Welcome to Memo-IT"

    # send html message from "welcome_template.html"
    dir_path = os.path.dirname(__file__) 
    rel_path = "welcome_template.html"
    f_path = os.path.join(dir_path, rel_path)

    if exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace("{username}", user.username)
            msg.attach(MIMEText(content, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("your-email", "your-email-password")
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
