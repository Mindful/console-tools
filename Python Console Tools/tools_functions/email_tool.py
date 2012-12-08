import smtplib, sys
from email.mime.text import MIMEText
# email tool function
# currently takes the 'to' address as a command line argument.
# Plans:
# -add format options, like automatic vs. user-generated subject line
# -make to address argument optional
# -add more sophisticated error handling
# -put 'attempting pre-entered password...' and 'password failed, try again' messages 
#    during password authentication
# -put password and from address in a loop with an exit command, 
#    so that bad input doesn't crash the program
# -add error handling for nonexistent/poorly formatted 'to' address

max_args = 1
help_info = 'emails the address supplied as a command line argument with an email from the user\'s gmail account. The subject heading is the calling program.'
case_sensitive = False
command_name = 'email'


def email_tool(self,args):
    # this email function code is borrowed heavily from 
    #   http://www.daniweb.com/software-development/python/code/380881/python-3-and-python-2-send-email-through-gmail
    # thanks to http://segfault.in/2010/12/sending-gmail-from-python/

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
