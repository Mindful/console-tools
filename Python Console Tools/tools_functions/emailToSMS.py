import smtplib, sys
from email.mime.text import MIMEText

def emailToSMS(self, args):
    carrierCodes = {
    'sprint': '@messaging.sprintpcs.com',
    'verizon': '@vtext.com',
    't-mobile': 'phonenumber@tmomail.net',
    'at&t': '@txt.att.net',
    'virgin mobile': '@vmobl.com',
    'us cellular': '@email.uscc.net',
    'nextel': '@messaging.nextel.com',
    'boost': '@myboostmobile.com',
    'alltel': '@message.alltel.com'}
    
    number = args[0]
    carrier = args[1]
    couldFindCarrier = True
    if carrier not in carrierCodes:
        couldFindCarrier = False
        print('Error: unrecognized carrier.')
    else:
        address = number + carrierCodes[carrier]
        messages = parseText(input('Message: '))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        for segment in messages:
            send(self, segment, address, s)
        s.quit()

def parseText(message):
# split the message into parts smaller than 150 characters, 
# preferably at spaces
    messages = int(len(message)/150)
    messageList = [''] * (messages + 1)
    i = 0
    while len(message) > 150:
        temp = message[:message.rfind(' ')]
        messageList[i] = temp
        del message[:message.rfind(' ')]
        i += 1
    messageList[messages] = message
    return messageList
    
def send(self, message, address, connection):
    # Create a text/plain message
    message = MIMEText(message)
    message['Subject'] = 'Sent from %s' % sys.argv[0]
    message['From'], message['To'] = input('\'From\' address? (gmail only): '), address
    # Send the message via gmail SMTP server
    connection.ehlo()
    connection.starttls()
    if self.settingsList['password'] is '':
        connection.login(message['From'], input('Password: '))
    else:
     try:
        connection.login(message['From'], self.settingsList['password'][0])
     except smtplib.SMTPAuthenticationError:
        connection.login(message['From'], input('Password: '))
    connection.send_message(message)
    
func_alias = 'txt'
func_info = (emailToSMS,
             2,
             2,
             'Sends text messages through gmail; txt <number> <carrier>',
             False,
             )
