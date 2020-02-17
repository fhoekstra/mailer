import email, smtplib, ssl
from collections import Iterable
import getpass

from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#### PARAMETERS FOR TESTS ######
my_name = 'my'
my_domain = '@gmail.com'
my_mail = my_name + my_domain

class Mailer(object):
    def __init__(self, domain, port, username, password=None):
        # Create a secure SSL context
        self.context = ssl.create_default_context()
        self.password = password
        self.domain = domain
        self.port = port
        self.username = username

    def send_mail(self, sender, receiver, message):
        """ log in and send a single mail """
        with smtplib.SMTP_SSL(self.domain, self.port, context=self.context) as server:
            if self.password is not None:
                server.login(self.username, self.password)
            server.sendmail(sender, receiver, message)

    def batch_mail(self, sender, receivers, subject, messages, attachments=None, attachdifpermail=False):
        """
        log in and send iterable (or one) message(s)
        to iterable (or one) receiver(s)
        attachments must be iterable of length N if attachment set is different per mail
        """
        multirec = False
        multimess = False
        multiattach = attachdifpermail
        if type(receivers) is not str:
            multirec = True
            N = len(receivers)
        if type(messages) is not str:
            multimess = True
            N = len(messages)
        if multirec and type(messages) is not str:
            assert len(receivers) == len(messages)
        if multiattach:
            assert len(attachments) == N
            assert type(attachments) is list
        with smtplib.SMTP_SSL(self.domain, self.port, context=self.context) as server:
            if self.password is not None:
                server.login(self.username, self.password)
            for i in range(N):
                if multirec:
                    receiver = receivers[i]
                else:
                    receiver = receivers
                if multimess:
                    message = messages[i]
                else:
                    message = messages
                if multiattach:
                    attachment = attachments[i]
                else:
                    attachment = attachments
                mail = make_mime_mail(subject, sender, receiver, message, attachment)
                server.sendmail(sender, receiver, mail)


def make_mime_mail(subject, sender_email, receiver_email, body, attachpaths=None):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))  # Add text to mail

    if attachpaths is not None:
        for pth in attachpaths:
            pth = Path(pth)
            # Open PDF file in binary mode
            with open(pth, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {pth.name}",
            )

            # Add attachment to message
            message.attach(part)

    text = message.as_string()  # convert message to string

    return text

def setup_mailer(domain = "smtp.gmail.com", port = 465, username = my_mail):
    # domain "localhost" or "smtp.gmail.com" for gmail server
    # port 1025 for local or 465 For SSL Gmail
    if domain == "localhost":
        password = None
    elif domain == "smtp.gmail.com":
        password = getpass.getpass("Type your password and press Enter: ")
    else:
        needpass = input("Do you need a password?[Y/n]")
        if needpass in ("Y", 'y', 'yes', 'yeah', ""):
            password = getpass.getpass("Type your password and press Enter: ")
        elif needpass in ("N", "n", "no"):
            password = None
        else:
            print("Not sure about your response, continuing without.")
            password = None

    return Mailer(domain, port, username, password=password)


def test_single_mail(mailer):
    message = """Subject: Hi there

    This message is sent from Python."""

    mailer.send_mail(my_mail, my_mail, message)


def test_batch_mail(mailer):
    receivers = [f'{my_name}+rec{j}{my_domain}' for j in range(10)]
    messages = [f'Dit is testmail nummer {j}' for j in range(10)]
    attachments = [sorted(Path().cwd().glob(f'[0-9][0-9].pdf'))[j:j+4] for j in range(2,12)]

    mailer.batch_mail(my_mail, receivers, "Test-attach", messages, attachments=attachments, attachdifpermail=True)


def test_mailer():
    mailer = setup_mailer()

    # test_single_mail(mailer)

    # test_batch_mail(mailer)


if __name__ == '__main__':
    test_mailer()
