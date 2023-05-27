import random
import string
import hashlib
import smtplib
from email.mime.text import MIMEText

# Generate a random string of 6 characters
random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
print("Random string:", random_string)

# Hash the random string using SHA-256
hashed_string = hashlib.sha256(random_string.encode()).hexdigest()
print("Hashed string:", hashed_string)

# Set up email parameters
sender_email = "mohamedelauzei@gmail.com"
receiver_email = "mohamedelauzei@gmail.com"
password = "263369ggMM"
message = MIMEText(hashed_string)
message['Subject'] = 'Randomly generated string'
message['From'] = sender_email
message['To'] = receiver_email

# Send the email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent!")
