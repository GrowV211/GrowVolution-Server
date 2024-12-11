from . import NRS_PASSWORD
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from email.utils import format_datetime


def _nrs():
    return smtplib.SMTP("mail.growvolution.org", 587)


SENDER = "noreply@growvolution.org"
MAIL_SERVICE = _nrs()


def _get_code():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))


def _get_html(content):
    return f"""
    <html>
        <body>
            <p>
                {content}
            </p>
        </body>
    </html>
    """


def _connect():
    MAIL_SERVICE.starttls()
    MAIL_SERVICE.login(SENDER, NRS_PASSWORD)


def _reconnect():
    global MAIL_SERVICE

    MAIL_SERVICE.close()
    MAIL_SERVICE = _nrs()
    _connect()


def _resend(receiver, subject, body, c_type):
    _reconnect()
    send(receiver, subject, body, c_type)


def send(receiver, subject, body, c_type):
    msg = MIMEMultipart()
    msg['From'] = f"GrowV Service<{SENDER}>"
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['Date'] = format_datetime(datetime.now())
    msg.add_header('Reply-To', 'info@growvolution.org')
    msg.attach(MIMEText(body, c_type))

    try:
        MAIL_SERVICE.sendmail(SENDER, receiver, msg.as_string())
    except smtplib.SMTPSenderRefused:
        _resend(receiver, subject, body, c_type)
    except smtplib.SMTPServerDisconnected:
        _resend(receiver, subject, body, c_type)


def send_confirm_mail(receiver, user):
    code = _get_code()
    body = _get_html(f"""
        Hey {user}!<br><br>Wir freuen uns, dass du ein Teil der GrowVolution bist.<br>
        Bitte bestätige kurz <a href="https://growvolution.org/confirm/{code}">deine E-Mail Adresse</a>.<br><br>
        Diese Nachricht hier geht automatisch raus. Bitte antworte nicht darauf!
        Falls du Hilfe benötigst, kannst du uns jederzeit <a href="mailto:info@growvolution.org">kontaktieren</a>.<br><br>
        Alles Liebe<br>Dein GrowV Team!
    """)

    send(receiver, "Bestätigungslink", body, "html")
    return code


def send_reset_link(receiver, user, ):
    code = _get_code()
    body = _get_html(f"""
        Hey {user}!<br><br>Wie es scheint, hast du dein Passwort vergessen.<br>Keine Sorge, sowas passiert jedem mal!<br>
        Deshalb kannst du dein Passwort ganz einfach <a href="https://growvolution.org/reset/{code}">hier zurücksetzen</a>.<br>
        Der Link ist 10 Minuten gültig.<br><br>
        Wenn du diese Anfrage nicht von dir stammt, kannst du diese E-Mail einfach ignorieren.<br>Für weitere Hilfe
        kannst du uns <a href="mailto:info@growvolution.org">gern kontaktieren</a>.<br><br>Alles Liebe<br>Dein GrowV Team!
    """)

    send(receiver, "Passwort zurücksetzen", body, "html")

    return code


def start():
    _connect()
