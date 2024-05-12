from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
load_dotenv() # to use the env content here


def send_mail():
    mail_confirmation = False
    # IMPORTANT
    sender_email = os.getenv('SENDER_MAIL')
    recipient_email = os.getenv('RECIPIENT_MAIL')
    subject = "ALERT !! (from motion detector)"
    message = "Motion Detected in your house !\n Image is attached below."
    image_path = "motion_detected.jpg"  # Replace with the actual path to your image
    try:
        with open(image_path, 'rb') as f:
            img_data = f.read()
    except Exception as e:
        print("File path is Not Valid !")
        return True  # because we do not want to enter the function if the path is wrong

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    text = MIMEText(message)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(image_path))
    msg.attach(image)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        try:
            server.login(sender_email, os.getenv('PASSWORD'))
            server.sendmail(sender_email, recipient_email, msg.as_string())
            mail_confirmation = True
        except Exception as e:
            print(f"Could not send the email. \n {e}")

    return mail_confirmation
