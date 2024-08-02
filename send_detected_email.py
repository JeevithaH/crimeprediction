import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Assuming you have a function to perform object detection named `model`


def send_email(subject, message):
    # Email configuration
    sender_email = ''  # Your email address
    receiver_email = ''  # Recipient email address
    password = ""  # Your email password

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    #bczx qpgu qhza rkaq
    msg.attach(MIMEText(message, 'plain'))

    # Establish a secure session with the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Close the SMTP server session
    server.quit()


def notify_me():
    keywords = ['Gun', 'Pistol', 'Knife', 'handgun', 'Grenade', 'rifle']
    lines = ""
    with open('yolo_logs.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if any(keyword in line for keyword in keywords):
                lines += '\n' + line

    subject = "Crime Detection Report"
    message = lines
    send_email(subject, message)
