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
        toAddress = number + carrierCodes[carrier]
        fromAddress = input('\'From\' address (gmail only): ')
        password = input('Password: ')
        messages = parseTXT(input('Message: '))
        for segment in messages:
            send(self, segment, fromAddress, password, toAddress)

def parseTXT(message):
# split the message into parts smaller than 150 characters, 
# preferably at spaces
    messages = int(len(message)/150)
    messageList = [''] * (messages + 1)
    i = 0
    while len(message) > 150:
        temp = message[:message[:150].rfind(' ')]
        messageList[i] = temp
        message = message[message[:150].rfind(' '):]
        i += 1
    messageList[messages] = message
    print(messageList)
    return messageList
    
def send(self, msg, fromAddress, password, toAddress):
    # Create a text/plain message
    message = MIMEText(msg)
    message['Subject'] = ''
    message['From'], message['To'] = fromAddress, toAddress
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    if self.settingsList['password'] is '':
     try:
        s.login(message['From'], password)
     except smtplib.SMTPAuthenticationError:
        s.login(message['From'], password)
    else:
     try:
        s.login(message['From'], self.settingsList['password'][0])
     except smtplib.SMTPAuthenticationError:
        s.login(message['From'], password)

    s.send_message(message)
    s.quit()
    
func_alias = 'txt'
func_info = (emailToSMS,
             2,
             2,
             'Sends text messages through gmail; txt <number> <carrier>',
             False,
             )
