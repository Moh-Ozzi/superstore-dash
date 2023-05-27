
import smtplib
from email.message import EmailMessage

def sendemail(OTP):
    EMAIL_ADDRESS = 'mohamedelauzei@gmail.com'
    EMAIL_PASSWORD = 'snbvyvvmiqxhvuty'
    msg = EmailMessage()
    msg['Subject'] = 'New user'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'mohamedelauzei@gmail.com'
    msg.set_content('The OTP IS {}'.format(OTP))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

otp = 'rret'
sendemail(otp)