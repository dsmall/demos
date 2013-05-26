"""
    Rascal SMTP Library
    ~~~~~~~~~~~~~~~~~~~
    Support for sending email messages via SMTP
    dsmall 8 Apr 2012, 24 Jun 2012, 19 Apr 2013
"""
from flask import Blueprint, render_template, request
public = Blueprint('lib_smtp', __name__, template_folder='templates')

""" SET UP SMTP SERVER """

""" Fill in details of the SMTP server you will be using """
# If your ISP doesn't provide an SMTP service, you can sign up with gmail
# These settings are correct for gmail SMTP but you will need to provide
# a LOCAL_HOST name for your Rascal and your gmail LOGIN and PASSWORD
HOST = 'smtp.gmail.com'     # Outgoing mail server
PORT = 587                  # Usually 25 or 587
LOCAL_HOST = 'rascalNN'     # Name of your Rascal
TIMEOUT = 30.0              # Seconds

""" Fill in this section if the SMTP server requires TLS (gmail does) """
USE_TLS = True              # True or False
LOGIN = 'username@gmail.com'
PASSWORD = 'YourGmailPassword'

""" Replace the section within the angle brackets with your email address """
SENDER = LOCAL_HOST + ' <username@gmail.com>'

""" END OF SET UP """

HELP = ''
""" Delete this section to remove the help message """
HELP = """Before using this page, please edit smtp_lib.py and enter details of
the SMTP server you will be using to send email. To get rid of this message and
automatically fill in the Sender email address, edit the variables HELP and
SENDER in smtp_lib.py. After making these changes, remember to click the
Reload pytronics button to ensure that the server is running the latest version
of the code."""
""" Delete up to here """


def sendmail(sender, recipients, subject, body):
    """
    Send email to one or more recipients
    sender, recipients, subject and body are strings
    Separate multiple recipients with space, comma or semicolon
    Return tuple (status, msg) where status 0 for success, 1 for error
    """
    import smtplib
    import time
    from email.mime.text import MIMEText

    # Replace comma or semicolon with a space, then split into a list
    toaddrs = recipients.replace(',', ' ').replace(';', ' ').split()
    print '## sendmail ##', sender, toaddrs, subject
    msg = MIMEText(body)
    msg['From'] = sender
    msg['To'] = ', '.join(toaddrs)
    msg['Subject'] = subject
    msg['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
    try:
        server = smtplib.SMTP(HOST, PORT, LOCAL_HOST, TIMEOUT)
        try:
            if USE_TLS:
                server.starttls()
                server.ehlo()
                server.login(LOGIN, PASSWORD)
            resdict = server.sendmail(sender, toaddrs, msg.as_string())
            if len(resdict) == 0:
                result = (0, 'Email sent')
            else:
                _sendmail_log(resdict)
                result = (1, 'Can\'t send to some recipients, see log')
        except smtplib.SMTPRecipientsRefused as resdict:
            sendmail_log (resdict)
            result = (1, 'Can\'t send to any recipients, see log')
        except smtplib.SMTPHeloError:
            result = (1, 'The server didn\'t reply properly to the HELO greeting')
        except smtplib.SMTPSenderRefused:
            result = (1, 'The server didn\'t accept the sender')
        except smtplib.SMTPAuthenticationError:
            result = (1, 'The server didn\'t accept the login/password')
        except smtplib.SMTPDataError:
            result = (1, 'The server replied with an unexpected error code')
        except:
            result = (1, 'Unexpected error')
        server.quit()
    except smtplib.SMTPConnectError:
        result = (1, 'Could not connect to server')
    except:
        result = (1, 'Unexpected error on connect')
    return result

def _sendmail_log(resdict):
    print '## sendmail ## Can\'t send to', resdict

@public.route('/email.html')
def email_form():
    return render_template('email.html', sender=SENDER, help=HELP)

@public.route('/send-email', methods=['POST'])
def send_email():
    import json
    sender = request.form['sender'].strip()
    recipients = request.form['recipients'].strip()
    subject = request.form['subject'].strip()
    body = request.form['body'].strip()
    if sender == '':
        result = (1, 'Please enter the sender')
    elif recipients == '':
        result = (1, 'Please enter at least one recipient')
    else:
        result = sendmail(sender, recipients, subject, body)
    data = {
        "status" : int(result[0]),
        "message" : result[1]
    }
    return json.dumps(data)

