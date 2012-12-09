import smtplib, sys
from email.mime.text import MIMEText
# email tool function

max_args = 1
help_info = 'emails the address supplied as a command line argument with an email from the user\'s gmail account. The subject heading is the calling program.'
case_sensitive = False
command_name = 'email'
settings = {'subject': 'T', 'anonymous': 'F','password':'','toAddress':'arg'}


def email_tool(self,args):
    message = input('Enter message body: ')
    # Create a text/plain message
    msg = MIMEText(message)
    msg['Subject'] = 'Sent from %s' % sys.argv[0]
    msg['From'], msg['To'] = input('\'From\' address? (gmail only): '), args[0]
    # Send the message via gmail SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    if self.settingsList['password'] is '':
        s.login(msg['From'], input('Password: '))
    else:
     try:
        s.login(msg['From'], self.settingsList['password'])
     except smtplib.SMTPAuthenticationError:
        s.login(msg['From'], input('Password: '))
    
    s.send_message(msg)
    s.quit()
