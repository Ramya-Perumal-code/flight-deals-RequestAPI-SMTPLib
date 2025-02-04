import smtplib
import os


class NotificationManager:
    def __init__(self):
        self.email_port = int(os.getenv("Email_port"))
        self.username = os.getenv("Email")
        self.password = os.getenv("Password")

    #This class is responsible for sending notifications with the deal flight details.
    def send_mail(self, alert_msg, user):
        with smtplib.SMTP("smtp.gmail.com", port=self.email_port) as connection:
            connection.starttls()
            connection.login(user=self.username, password=self.password)
            connection.sendmail(from_addr=self.username, to_addrs=user,
                                msg=f"Subject:Low price alert!\n\n {alert_msg.encode('utf-8').strip()}")
