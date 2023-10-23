import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email():
    def __init__(self):
        self.recipient_to = []
        self.recipient_cc = []
        self.recipient_bcc = []

        self.subject = ""
        self.content = ""

    def add_recipient(self, recipients, type):
        if type == "to":
            self.recipient_to.extend(recipients)
        elif type == "cc":
            self.recipient_cc.extend(recipients)
        elif type == "bcc":
            self.recipient_bcc.extend(recipients)

    def add_subject(self, subject):
        self.subject = subject

    def add_content(self, content):
        self.content = content

class EmailSender():
    def __init__(self, user):
        self.email = user['email']
        self.password = user['password']
        self.smtp_server = "smtp.gmail.com"
        self.port = 587

        self.session = smtplib.SMTP(self.smtp_server, self.port) 
        self.session.starttls()
        self.session.login(self.email, self.password)

    def create_email(self):
        return Email()
    
    def send_email(self, email_data):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = ', '.join(email_data.recipient_to)
        msg['Subject'] = email_data.subject

        body_content = email_data.content
        msg.attach(MIMEText(body_content, 'plain'))

        text = msg.as_string()

        self.session.sendmail(self.email, email_data.recipient_to, text)